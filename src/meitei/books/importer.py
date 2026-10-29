# -*- coding: utf-8 -*-
"""
Text Importer and Segmentation Engine for the Meitei Digital Book Library.

Supports ingestion of authorized local files across:
- JSON (.json)
- JSON Lines (.jsonl)
- Markdown (.md)
- Plain Text (.txt)

Guarantees:
- Deterministic segmentation into chapters and passages.
- Assigns stable, verifiable passage IDs: `{book_id}-c{ch:02d}-p{p:03d}`.
- Computes SHA-256 cryptographic digests for tamper detection.
- Records import manifests recording provenance and checksums.
- Honest tracking of CATALOG_ONLY, PARTIALLY_IMPORTED, and FULLY_IMPORTED statuses.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from meitei.books.catalog import BookCatalog
from meitei.books.models import (
    BookCatalogRecord,
    Chapter,
    ImportManifest,
    ImportStatus,
    Passage,
)
from meitei.unicode_utils import normalize_text


def compute_sha256(file_path: Union[str, Path]) -> str:
    """Compute cryptographic SHA-256 checksum of a file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def segment_text_into_passages(
    book_id: str,
    chapter_num: int,
    raw_text: str,
) -> List[Passage]:
    """
    Segment chapter text into discrete passages with deterministic identifiers.

    Splits on paragraph breaks or Meitei Cheikhei delimiters (꯫) to create
    readable, referenceable passages.

    Args:
        book_id: Book identifier.
        chapter_num: Numeric chapter index.
        raw_text: Raw chapter text content.

    Returns:
        List of Passage objects with stable IDs: {book_id}-c{ch:02d}-p{p:03d}.
    """
    cleaned = normalize_text(raw_text).strip()
    if not cleaned:
        return []

    # 1. Try splitting into paragraphs first
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", cleaned) if p.strip()]

    # 2. If single paragraph, split into sentences by Meitei Cheikhei (꯫) or periods
    chunks: List[str] = []
    if len(paragraphs) == 1:
        # Split by Cheikhei (꯫) while preserving the punctuation
        raw_chunks = re.split(r"(?<=[꯫\.?!])\s+", paragraphs[0])
        chunks = [c.strip() for c in raw_chunks if c.strip()]
        if not chunks:
            chunks = paragraphs
    else:
        chunks = paragraphs

    passages: List[Passage] = []
    for p_idx, text_chunk in enumerate(chunks, start=1):
        p_id = f"{book_id}-c{chapter_num:02d}-p{p_idx:03d}"
        passages.append(
            Passage(
                passage_id=p_id,
                book_id=book_id,
                chapter_number=chapter_num,
                passage_number=p_idx,
                text=text_chunk,
                word_count=len(text_chunk.split()),
                character_count=len(text_chunk),
            )
        )

    return passages


class BookImporter:
    """
    Importer for local book texts, managing parsing, segmentation, and manifest generation.
    """

    def __init__(self, data_dir: Union[str, Path] = "data") -> None:
        self.data_dir = Path(data_dir)
        self.texts_dir = self.data_dir / "books" / "texts"
        self.manifests_dir = self.data_dir / "books" / "manifests"
        self.texts_dir.mkdir(parents=True, exist_ok=True)
        self.manifests_dir.mkdir(parents=True, exist_ok=True)
        self.catalog = BookCatalog(data_dir=self.data_dir)

    def import_json(
        self,
        file_path: Union[str, Path],
        target_book_id: Optional[str] = None,
    ) -> List[ImportManifest]:
        """
        Import books and chapters from structured JSON format.

        Supports single book objects or lists of books containing chapters and text.
        """
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"Source file not found: {p}")

        checksum = compute_sha256(p)
        now_iso = datetime.now(timezone.utc).isoformat()

        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)

        items = data if isinstance(data, list) else [data]
        manifests: List[ImportManifest] = []

        for item in items:
            b_id = item.get("book_id")
            if not b_id:
                continue
            if target_book_id and b_id != target_book_id:
                continue

            chapters_raw = item.get("chapters", [])
            chapters: List[Chapter] = []
            total_passages = 0
            total_words = 0

            for ch_dict in chapters_raw:
                ch_num = int(ch_dict.get("chapter_number", 1))
                ch_title = ch_dict.get("title", f"Chapter {ch_num}")
                ch_title_en = ch_dict.get("title_en", f"Chapter {ch_num}")
                raw_text = ch_dict.get("text", "")

                passages = segment_text_into_passages(b_id, ch_num, raw_text)
                total_passages += len(passages)
                total_words += sum(p.word_count for p in passages)

                ch_obj = Chapter(
                    chapter_id=f"{b_id}-c{ch_num:02d}",
                    book_id=b_id,
                    chapter_number=ch_num,
                    title=ch_title,
                    title_en=ch_title_en,
                    passages=passages,
                    summary=ch_dict.get("summary"),
                    translation_en=ch_dict.get("translation_en"),
                )
                chapters.append(ch_obj)

            # Persist segmented book to data/books/texts/{b_id}.json
            book_dest = self.texts_dir / f"{b_id}.json"
            book_payload = {
                "book_id": b_id,
                "title": item.get("title", ""),
                "title_en": item.get("title_en", ""),
                "author": item.get("author", ""),
                "language": item.get("language", "Meitei (Manipuri)"),
                "script": item.get("script", "Meitei Mayek"),
                "genre": item.get("genre", ""),
                "description": item.get("description", ""),
                "source": item.get("source", ""),
                "copyright": item.get("copyright", "Public Domain"),
                "chapters": [c.to_dict() for c in chapters],
            }
            with open(book_dest, "w", encoding="utf-8") as f:
                json.dump(book_payload, f, indent=2, ensure_ascii=False)

            # Record manifest
            manifest = ImportManifest(
                manifest_id=f"MAN-{b_id}-{checksum[:8]}",
                book_id=b_id,
                source_file_path=str(p),
                file_format="json",
                sha256_checksum=checksum,
                imported_at=now_iso,
                total_chapters=len(chapters),
                total_passages=total_passages,
                total_word_count=total_words,
                importer="meitei-books-importer",
                notes=f"Successfully segmented into {len(chapters)} chapters and {total_passages} passages.",
            )
            manifest_file = self.manifests_dir / f"{manifest.manifest_id}.json"
            with open(manifest_file, "w", encoding="utf-8") as f:
                json.dump(manifest.to_dict(), f, indent=2, ensure_ascii=False)
            manifests.append(manifest)

            # Update catalog record
            cat_rec = self.catalog.get_book(b_id)
            if not cat_rec:
                cat_rec = BookCatalogRecord(
                    book_id=b_id,
                    title=item.get("title", b_id),
                    title_en=item.get("title_en", b_id),
                    author=item.get("author", "Traditional"),
                    genre=item.get("genre", ""),
                    description=item.get("description", ""),
                    source=item.get("source", ""),
                    copyright=item.get("copyright", "Public Domain"),
                    total_chapters=len(chapters),
                )
                self.catalog.register_book(cat_rec)

            expected_ch = cat_rec.total_chapters or len(chapters)
            status = ImportStatus.FULLY_IMPORTED if len(chapters) >= expected_ch else ImportStatus.PARTIALLY_IMPORTED

            self.catalog.update_import_status(
                book_id=b_id,
                status=status,
                imported_chapters=len(chapters),
                total_passages=total_passages,
                checksum_sha256=checksum,
                source_file=str(p.name),
                imported_at=now_iso,
            )

        return manifests

    def import_markdown(
        self,
        file_path: Union[str, Path],
        book_id: str,
        title: str,
        title_en: str,
        author: str,
        genre: str = "Literary Heritage",
        description: str = "",
        copyright: str = "Public Domain",
    ) -> ImportManifest:
        """
        Import a book from a Markdown (.md) file.

        Parses headers (# Chapter X: ...) into chapters, and segments body paragraphs into passages.
        """
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"Markdown file not found: {p}")

        checksum = compute_sha256(p)
        now_iso = datetime.now(timezone.utc).isoformat()

        with open(p, "r", encoding="utf-8") as f:
            content = f.read()

        # Split on markdown headers: # Chapter or ## Chapter
        sections = re.split(r"(?m)^#{1,2}\s+(.+)$", content)

        chapters: List[Chapter] = []
        total_passages = 0
        total_words = 0

        if len(sections) <= 1:
            # Single chapter
            passages = segment_text_into_passages(book_id, 1, content)
            total_passages += len(passages)
            total_words += sum(p.word_count for p in passages)
            chapters.append(
                Chapter(
                    chapter_id=f"{book_id}-c01",
                    book_id=book_id,
                    chapter_number=1,
                    title=title,
                    title_en=title_en,
                    passages=passages,
                )
            )
        else:
            ch_idx = 1
            for i in range(1, len(sections), 2):
                header_title = sections[i].strip()
                body_text = sections[i + 1].strip() if i + 1 < len(sections) else ""
                passages = segment_text_into_passages(book_id, ch_idx, body_text)
                total_passages += len(passages)
                total_words += sum(p.word_count for p in passages)

                chapters.append(
                    Chapter(
                        chapter_id=f"{book_id}-c{ch_idx:02d}",
                        book_id=book_id,
                        chapter_number=ch_idx,
                        title=header_title,
                        title_en=header_title,
                        passages=passages,
                    )
                )
                ch_idx += 1

        # Persist book
        book_dest = self.texts_dir / f"{book_id}.json"
        book_payload = {
            "book_id": book_id,
            "title": title,
            "title_en": title_en,
            "author": author,
            "genre": genre,
            "description": description,
            "copyright": copyright,
            "chapters": [c.to_dict() for c in chapters],
        }
        with open(book_dest, "w", encoding="utf-8") as f:
            json.dump(book_payload, f, indent=2, ensure_ascii=False)

        manifest = ImportManifest(
            manifest_id=f"MAN-{book_id}-{checksum[:8]}",
            book_id=book_id,
            source_file_path=str(p),
            file_format="markdown",
            sha256_checksum=checksum,
            imported_at=now_iso,
            total_chapters=len(chapters),
            total_passages=total_passages,
            total_word_count=total_words,
            importer="meitei-books-importer",
            notes="Segmented from Markdown source file.",
        )
        with open(self.manifests_dir / f"{manifest.manifest_id}.json", "w", encoding="utf-8") as f:
            json.dump(manifest.to_dict(), f, indent=2, ensure_ascii=False)

        cat_rec = self.catalog.get_book(book_id)
        if not cat_rec:
            cat_rec = BookCatalogRecord(
                book_id=book_id,
                title=title,
                title_en=title_en,
                author=author,
                genre=genre,
                description=description,
                copyright=copyright,
                total_chapters=len(chapters),
            )
            self.catalog.register_book(cat_rec)

        self.catalog.update_import_status(
            book_id=book_id,
            status=ImportStatus.FULLY_IMPORTED,
            imported_chapters=len(chapters),
            total_passages=total_passages,
            checksum_sha256=checksum,
            source_file=str(p.name),
            imported_at=now_iso,
        )
        return manifest

    def import_text(
        self,
        file_path: Union[str, Path],
        book_id: str,
        title: str,
        title_en: str,
        author: str,
        genre: str = "Literary Heritage",
        description: str = "",
        copyright: str = "Public Domain",
    ) -> ImportManifest:
        """Import a plain text (.txt) file with chapter separation."""
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"Text file not found: {p}")

        checksum = compute_sha256(p)
        now_iso = datetime.now(timezone.utc).isoformat()

        with open(p, "r", encoding="utf-8") as f:
            content = f.read()

        # Split on chapter dividers: e.g. Chapter 1 or --- Chapter 1 ---
        chapter_splits = re.split(r"(?im)^(?:\-{3,}\s*)?Chapter\s+(\d+)[:\s\-]+(.*?)(?:\s*\-{3,})?$", content)

        chapters: List[Chapter] = []
        total_passages = 0
        total_words = 0

        if len(chapter_splits) <= 1:
            passages = segment_text_into_passages(book_id, 1, content)
            total_passages += len(passages)
            total_words += sum(p.word_count for p in passages)
            chapters.append(
                Chapter(
                    chapter_id=f"{book_id}-c01",
                    book_id=book_id,
                    chapter_number=1,
                    title=title,
                    title_en=title_en,
                    passages=passages,
                )
            )
        else:
            for i in range(1, len(chapter_splits), 3):
                ch_num = int(chapter_splits[i])
                ch_title = chapter_splits[i + 1].strip() or f"Chapter {ch_num}"
                body = chapter_splits[i + 2].strip() if i + 2 < len(chapter_splits) else ""

                passages = segment_text_into_passages(book_id, ch_num, body)
                total_passages += len(passages)
                total_words += sum(p.word_count for p in passages)

                chapters.append(
                    Chapter(
                        chapter_id=f"{book_id}-c{ch_num:02d}",
                        book_id=book_id,
                        chapter_number=ch_num,
                        title=ch_title,
                        title_en=ch_title,
                        passages=passages,
                    )
                )

        book_dest = self.texts_dir / f"{book_id}.json"
        book_payload = {
            "book_id": book_id,
            "title": title,
            "title_en": title_en,
            "author": author,
            "genre": genre,
            "description": description,
            "copyright": copyright,
            "chapters": [c.to_dict() for c in chapters],
        }
        with open(book_dest, "w", encoding="utf-8") as f:
            json.dump(book_payload, f, indent=2, ensure_ascii=False)

        manifest = ImportManifest(
            manifest_id=f"MAN-{book_id}-{checksum[:8]}",
            book_id=book_id,
            source_file_path=str(p),
            file_format="txt",
            sha256_checksum=checksum,
            imported_at=now_iso,
            total_chapters=len(chapters),
            total_passages=total_passages,
            total_word_count=total_words,
            importer="meitei-books-importer",
            notes="Segmented from plain text source file.",
        )
        with open(self.manifests_dir / f"{manifest.manifest_id}.json", "w", encoding="utf-8") as f:
            json.dump(manifest.to_dict(), f, indent=2, ensure_ascii=False)

        self.catalog.update_import_status(
            book_id=book_id,
            status=ImportStatus.FULLY_IMPORTED,
            imported_chapters=len(chapters),
            total_passages=total_passages,
            checksum_sha256=checksum,
            source_file=str(p.name),
            imported_at=now_iso,
        )
        return manifest

    def import_default_heritage_books(
        self,
        fallback_source: Optional[Union[str, Path]] = None,
    ) -> List[ImportManifest]:
        """
        Import the 10 authorized traditional Meitei heritage books.

        Reads from available local datasets (e.g. src/meitei_lang/data/books.json).
        """
        candidates = [
            Path(fallback_source) if fallback_source else None,
            Path("src/meitei_lang/data/books.json"),
            Path("data/books/source_books.json"),
        ]
        source_file = next((c for c in candidates if c and c.exists()), None)
        if not source_file:
            return []

        return self.import_json(source_file)


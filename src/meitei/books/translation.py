# -*- coding: utf-8 -*-
"""
Translation Alignment and Provenance Engine for Book Texts.

Aligns source Meitei Mayek passages with verified cross-lingual translations,
preserving full translator attributions, notes, and citations.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from meitei.books.reader import BookReader


@dataclass
class AlignedPassage:
    """
    Bilingual passage alignment with citation provenance.

    Attributes:
        passage_id: Passage identifier.
        book_id: Book identifier.
        chapter_number: Chapter index.
        passage_number: Passage index.
        source_text: Original text in Meitei Mayek.
        source_roman: Roman transliteration.
        translation_text: English translation text.
        translation_language: Target language (default: 'en').
        translator: Translator name or scholar attribution.
        citation_reference: Physical volume, page, or publication citation.
        alignment_confidence: Alignment confidence score (0.0 to 1.0).
        notes: Editorial or linguistic annotations.
    """
    passage_id: str
    book_id: str
    chapter_number: int
    passage_number: int
    source_text: str
    source_roman: Optional[str] = None
    translation_text: str = ""
    translation_language: str = "en"
    translator: Optional[str] = None
    citation_reference: Optional[str] = None
    alignment_confidence: float = 1.0
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert alignment to dictionary."""
        return asdict(self)


class BookTranslationAligner:
    """
    Manages translation alignment mappings and bilingual chapter rendering.
    """

    def __init__(self, data_dir: Union[str, Path] = "data") -> None:
        self.data_dir = Path(data_dir)
        self.reader = BookReader(data_dir=self.data_dir)
        self.alignments_dir = self.data_dir / "books" / "translations"
        self.alignments_dir.mkdir(parents=True, exist_ok=True)

    def align_passage(
        self,
        passage_id: str,
        translation_text: str,
        translator: Optional[str] = None,
        citation_reference: Optional[str] = None,
        translation_language: str = "en",
        notes: Optional[str] = None,
    ) -> AlignedPassage:
        """
        Record a verified translation alignment for a specific passage.
        """
        passage = self.reader.get_passage_by_id(passage_id)
        if not passage:
            raise ValueError(f"Passage '{passage_id}' does not exist in reader.")

        aligned = AlignedPassage(
            passage_id=passage_id,
            book_id=passage.book_id,
            chapter_number=passage.chapter_number,
            passage_number=passage.passage_number,
            source_text=passage.text,
            source_roman=passage.text_roman,
            translation_text=translation_text,
            translation_language=translation_language,
            translator=translator,
            citation_reference=citation_reference,
            notes=notes,
        )

        # Save to disk
        dest = self.alignments_dir / f"{passage.book_id}_alignments.jsonl"
        with open(dest, "a", encoding="utf-8") as f:
            f.write(json.dumps(aligned.to_dict(), ensure_ascii=False) + "\n")

        return aligned

    def get_chapter_bilingual(
        self,
        book_id: str,
        chapter_number: int,
    ) -> List[AlignedPassage]:
        """
        Retrieve bilingual parallel text view of a chapter.
        """
        chapter = self.reader.get_chapter(book_id, chapter_number)

        # Load any dedicated alignment records
        custom_alignments: Dict[str, Dict[str, Any]] = {}
        dest = self.alignments_dir / f"{book_id}_alignments.jsonl"
        if dest.exists():
            with open(dest, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        record = json.loads(line)
                        custom_alignments[record["passage_id"]] = record
                    except Exception:
                        continue

        results: List[AlignedPassage] = []
        for p in chapter.passages:
            custom = custom_alignments.get(p.passage_id, {})
            trans_text = custom.get("translation_text") or p.translation_en or ""
            translator = custom.get("translator") or p.translation_provenance

            results.append(
                AlignedPassage(
                    passage_id=p.passage_id,
                    book_id=p.book_id,
                    chapter_number=p.chapter_number,
                    passage_number=p.passage_number,
                    source_text=p.text,
                    source_roman=p.text_roman,
                    translation_text=trans_text,
                    translation_language="en",
                    translator=translator,
                    citation_reference=custom.get("citation_reference"),
                    notes=custom.get("notes"),
                )
            )

        return results


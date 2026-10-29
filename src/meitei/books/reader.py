# -*- coding: utf-8 -*-
"""
Book Reader and Pagination Engine for the Meitei Digital Book Library.

Supports:
- Structured reading of chapters and passages with pagination.
- Passage lookups by deterministic identifier (e.g. `khamba_thoibi-c01-p001`).
- Graceful handling of CATALOG_ONLY books where full text has not been imported.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from meitei.books.catalog import BookCatalog
from meitei.books.models import Chapter, ImportStatus, Passage
from meitei.loader import get_default_data_dir


class BookNotImportedError(Exception):
    """Raised when attempting to read text from a book that is CATALOG_ONLY."""
    pass


class BookNotFoundError(Exception):
    """Raised when a requested book_id is not found in the catalog."""
    pass


class ChapterNotFoundError(Exception):
    """Raised when a requested chapter_number does not exist in the book."""
    pass


class BookReader:
    """
    Offline reader providing paginated passage access and chapter navigation.
    """

    def __init__(self, data_dir: Union[str, Path] = "data") -> None:
        self.data_dir = get_default_data_dir(data_dir)
        self.texts_dir = self.data_dir / "books" / "texts"
        self.catalog = BookCatalog(data_dir=self.data_dir)

    def _load_book_data(self, book_id: str) -> Dict[str, Any]:
        """Load parsed book JSON structure from texts storage."""
        book_file = self.texts_dir / f"{book_id}.json"
        if not book_file.exists():
            cat_rec = self.catalog.get_book(book_id)
            if not cat_rec:
                raise BookNotFoundError(f"Book '{book_id}' is not registered in the catalog.")
            raise BookNotImportedError(
                f"Book '{book_id}' has status '{cat_rec.import_status.value}'; "
                f"full text has not been imported into local storage."
            )

        with open(book_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_chapters(self, book_id: str) -> List[Chapter]:
        """Retrieve all chapters for an imported book."""
        data = self._load_book_data(book_id)
        chapters_raw = data.get("chapters", [])
        return [Chapter.from_dict(c) for c in chapters_raw]

    def get_chapter(self, book_id: str, chapter_number: int) -> Chapter:
        """
        Retrieve a specific chapter by its 1-based index.

        Raises:
            ChapterNotFoundError: If the chapter number does not exist.
        """
        chapters = self.get_chapters(book_id)
        for ch in chapters:
            if ch.chapter_number == chapter_number:
                return ch
        raise ChapterNotFoundError(
            f"Chapter {chapter_number} not found in book '{book_id}'. "
            f"Available chapters: 1 to {len(chapters)}."
        )

    def read_passages(
        self,
        book_id: str,
        chapter_number: int = 1,
        page: int = 1,
        page_size: int = 5,
    ) -> Tuple[List[Passage], Dict[str, Any]]:
        """
        Read passages from a chapter with pagination metadata.

        Args:
            book_id: Book identifier.
            chapter_number: 1-based chapter index.
            page: 1-based page number.
            page_size: Number of passages per page.

        Returns:
            Tuple of (passages_on_page, pagination_metadata_dict).
        """
        chapter = self.get_chapter(book_id, chapter_number)
        passages = chapter.passages
        total_passages = len(passages)
        total_pages = max(1, math.ceil(total_passages / page_size)) if total_passages > 0 else 1

        # Bound page number
        safe_page = max(1, min(page, total_pages))
        start_idx = (safe_page - 1) * page_size
        end_idx = start_idx + page_size

        page_passages = passages[start_idx:end_idx]

        pagination = {
            "book_id": book_id,
            "chapter_number": chapter_number,
            "chapter_title": chapter.title,
            "chapter_title_en": chapter.title_en,
            "page": safe_page,
            "page_size": page_size,
            "total_passages": total_passages,
            "total_pages": total_pages,
            "has_next": safe_page < total_pages,
            "has_prev": safe_page > 1,
        }

        return page_passages, pagination

    def get_passage_by_id(self, passage_id: str) -> Optional[Passage]:
        """
        Locate and return a passage by its stable passage ID (e.g. khamba_thoibi-c01-p001).
        """
        # Parse book_id and chapter_number from passage ID format: {book_id}-c{ch}-p{p}
        parts = passage_id.split("-c")
        if len(parts) != 2:
            return None
        book_id = parts[0]
        subparts = parts[1].split("-p")
        if len(subparts) != 2:
            return None

        try:
            ch_num = int(subparts[0])
            chapter = self.get_chapter(book_id, ch_num)
            for p in chapter.passages:
                if p.passage_id == passage_id:
                    return p
        except Exception:
            return None
        return None


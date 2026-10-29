# -*- coding: utf-8 -*-
"""
Meitei Digital Book Library Subsystem (`meitei.books`).

Provides offline-first cataloging, ingestion, pagination, multi-script full-text
search, citation validation, translation alignment, and quarantined vocabulary
extraction for traditional and historical Meitei texts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from meitei.books.catalog import BookCatalog
from meitei.books.importer import (
    BookImporter,
    compute_sha256,
    segment_text_into_passages,
)
from meitei.books.models import (
    BookCatalogRecord,
    Chapter,
    ImportManifest,
    ImportStatus,
    Passage,
    RightsStatus,
    VocabularyCandidate,
    is_valid_passage_id,
)
from meitei.books.reader import (
    BookNotFoundError,
    BookNotImportedError,
    BookReader,
    ChapterNotFoundError,
)
from meitei.books.search import (
    BookSearchEngine,
    BookSearchResult,
    search_passages,
)
from meitei.books.translation import (
    AlignedPassage,
    BookTranslationAligner,
)
from meitei.books.validation import (
    BookAuditResult,
    BookValidator,
)
from meitei.books.vocabulary import (
    VocabularyExtractor,
    tokenize_meitei_words,
)


def list_books(
    status: Optional[Union[str, ImportStatus]] = None,
    data_dir: Union[str, Path] = "data",
) -> List[BookCatalogRecord]:
    """List all registered books in the catalog."""
    catalog = BookCatalog(data_dir=data_dir)
    return catalog.list_books(status=status)


def get_book_info(
    book_id: str,
    data_dir: Union[str, Path] = "data",
) -> Optional[BookCatalogRecord]:
    """Retrieve catalog record and metadata for a specific book."""
    catalog = BookCatalog(data_dir=data_dir)
    return catalog.get_book(book_id)


def read_passages(
    book_id: str,
    chapter_number: int = 1,
    page: int = 1,
    page_size: int = 5,
    data_dir: Union[str, Path] = "data",
) -> Tuple[List[Passage], Dict[str, Any]]:
    """Read paginated passages from a book chapter."""
    reader = BookReader(data_dir=data_dir)
    return reader.read_passages(
        book_id=book_id,
        chapter_number=chapter_number,
        page=page,
        page_size=page_size,
    )


def get_book_stats(data_dir: Union[str, Path] = "data") -> Dict[str, Any]:
    """Compute catalog statistics and import completeness."""
    catalog = BookCatalog(data_dir=data_dir)
    return catalog.get_catalog_stats()


def audit_books(data_dir: Union[str, Path] = "data") -> Dict[str, Any]:
    """Perform a comprehensive structural and cryptographic audit of all books."""
    validator = BookValidator(data_dir=data_dir)
    return validator.audit_all_books()


__all__ = [
    # Models & Enums
    "BookCatalogRecord",
    "Chapter",
    "Passage",
    "ImportManifest",
    "VocabularyCandidate",
    "ImportStatus",
    "RightsStatus",
    "is_valid_passage_id",
    # Subsystem Classes
    "BookCatalog",
    "BookImporter",
    "BookReader",
    "BookSearchEngine",
    "BookSearchResult",
    "BookValidator",
    "BookAuditResult",
    "BookTranslationAligner",
    "AlignedPassage",
    "VocabularyExtractor",
    # Exceptions
    "BookNotFoundError",
    "BookNotImportedError",
    "ChapterNotFoundError",
    # High-Level APIs
    "list_books",
    "get_book_info",
    "read_passages",
    "search_passages",
    "get_book_stats",
    "audit_books",
    "compute_sha256",
    "segment_text_into_passages",
    "tokenize_meitei_words",
]


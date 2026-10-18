# -*- coding: utf-8 -*-
"""
Meitei Language Books and Reading Texts Module.

Provides access, reading, and exploration of packaged classical and folk literature
in Meitei Mayek (Manipuri) with chapter subdivisions and English annotations.
"""

from dataclasses import dataclass, asdict
import json
import os
from typing import List, Dict, Any, Optional

from .exceptions import BookNotFoundError, ChapterNotFoundError, DataLoadError


@dataclass
class Chapter:
    """Represents a single chapter within a Meitei literary work."""
    chapter_number: int
    title: str
    title_en: str
    text: str

    def word_count(self) -> int:
        """Return the number of words in this chapter text."""
        return len(self.text.split())

    def character_count(self) -> int:
        """Return the character count of this chapter text."""
        return len(self.text)

    def to_dict(self) -> Dict[str, Any]:
        """Convert chapter to a standard dictionary."""
        return asdict(self)

    def __str__(self) -> str:
        return f"Chapter {self.chapter_number}: {self.title} ({self.title_en})"


@dataclass
class Book:
    """Represents a complete Meitei reading text or literary work."""
    book_id: str
    title: str
    title_en: str
    author: str
    language: str
    script: str
    genre: str
    description: str
    source: str
    copyright: str
    chapters: List[Chapter]

    def get_chapter(self, chapter_number: int) -> Chapter:
        """
        Retrieve a specific chapter by its 1-indexed number.

        Raises ChapterNotFoundError if the chapter number does not exist.
        """
        for ch in self.chapters:
            if ch.chapter_number == chapter_number:
                return ch
        raise ChapterNotFoundError(
            f"Chapter {chapter_number} not found in book '{self.book_id}'. "
            f"Available chapters: 1 to {len(self.chapters)}."
        )

    def total_chapters(self) -> int:
        """Return the total number of chapters."""
        return len(self.chapters)

    def full_text(self, separator: str = "\n\n") -> str:
        """Return the combined text of all chapters."""
        return separator.join(ch.text for ch in self.chapters)

    def total_word_count(self) -> int:
        """Return the total word count across all chapters."""
        return sum(ch.word_count() for ch in self.chapters)

    def to_dict(self) -> Dict[str, Any]:
        """Convert book to a standard dictionary."""
        d = asdict(self)
        d["chapters"] = [ch.to_dict() for ch in self.chapters]
        return d

    def __str__(self) -> str:
        return f"Book '{self.title}' ({self.title_en}) by {self.author} [{len(self.chapters)} chapters]"


_BOOKS_CACHE: Optional[List[Book]] = None
_BOOK_MAP: Optional[Dict[str, Book]] = None


def _get_data_path() -> str:
    """Resolve path to books.json."""
    return os.path.join(os.path.dirname(__file__), "data", "books.json")


def load_books(reload: bool = False) -> List[Book]:
    """
    Load packaged Meitei reading texts.

    Returns a list of Book objects with populated chapters.
    """
    global _BOOKS_CACHE, _BOOK_MAP
    if _BOOKS_CACHE is not None and not reload:
        return _BOOKS_CACHE

    path = _get_data_path()
    if not os.path.exists(path):
        raise DataLoadError(f"Books dataset file not found at: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_books = json.load(f)
    except Exception as e:
        raise DataLoadError(f"Failed to load books data from {path}: {e}") from e

    books: List[Book] = []
    book_map: Dict[str, Book] = {}

    for b in raw_books:
        chapters = [
            Chapter(
                chapter_number=ch["chapter_number"],
                title=ch["title"],
                title_en=ch.get("title_en", ""),
                text=ch["text"],
            )
            for ch in b.get("chapters", [])
        ]
        book = Book(
            book_id=b["book_id"],
            title=b["title"],
            title_en=b.get("title_en", ""),
            author=b.get("author", "Unknown"),
            language=b.get("language", "Meitei (Manipuri)"),
            script=b.get("script", "Meitei Mayek"),
            genre=b.get("genre", ""),
            description=b.get("description", ""),
            source=b.get("source", ""),
            copyright=b.get("copyright", "Public Domain"),
            chapters=chapters,
        )
        books.append(book)
        book_map[book.book_id] = book

    _BOOKS_CACHE = books
    _BOOK_MAP = book_map
    return _BOOKS_CACHE


def _ensure_loaded():
    if _BOOKS_CACHE is None or _BOOK_MAP is None:
        load_books()


def count_books() -> int:
    """Return the total number of books in the collection."""
    _ensure_loaded()
    assert _BOOKS_CACHE is not None
    return len(_BOOKS_CACHE)


def list_books() -> List[Book]:
    """Return all available books in the collection."""
    _ensure_loaded()
    assert _BOOKS_CACHE is not None
    return list(_BOOKS_CACHE)


def get_book(book_id: str) -> Book:
    """
    Retrieve a book by its unique book_id (e.g. 'khamba_thoibi', 'phunga_wari').

    Raises BookNotFoundError if the book_id is not recognized.
    """
    _ensure_loaded()
    assert _BOOK_MAP is not None

    clean_id = book_id.strip().lower()
    if clean_id in _BOOK_MAP:
        return _BOOK_MAP[clean_id]

    # Try matching title or title_en
    for b in _BOOK_MAP.values():
        if clean_id in (b.title_en.lower(), b.title.lower()):
            return b

    available = list(_BOOK_MAP.keys())
    raise BookNotFoundError(
        f"Book '{book_id}' not found. Available book IDs: {available}"
    )


def get_chapter(book_id: str, chapter_number: int) -> Chapter:
    """Convenience function to retrieve a specific chapter directly."""
    book = get_book(book_id)
    return book.get_chapter(chapter_number)


def search_books(query: str) -> List[Dict[str, Any]]:
    """
    Search for occurrences of a string or word across all books and chapters.

    Returns a list of matching records with book metadata, chapter number,
    and matching text excerpt.
    """
    _ensure_loaded()
    assert _BOOKS_CACHE is not None

    q = query.strip()
    if not q:
        return []
    q_lower = q.lower()

    matches = []
    for b in _BOOKS_CACHE:
        for ch in b.chapters:
            if q_lower in ch.text.lower() or q_lower in ch.title.lower() or q_lower in ch.title_en.lower():
                matches.append({
                    "book_id": b.book_id,
                    "book_title": b.title,
                    "book_title_en": b.title_en,
                    "chapter_number": ch.chapter_number,
                    "chapter_title": ch.title,
                    "chapter_title_en": ch.title_en,
                    "matched_text": ch.text,
                })
    return matches

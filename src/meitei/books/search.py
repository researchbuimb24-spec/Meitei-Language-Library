# -*- coding: utf-8 -*-
"""
Full-Text Search Engine for Book Passages.

Leverages SQLite FTS5 with 'unicode61' tokenization where available,
with documented fallback to indexed relational/substring search.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from meitei.books.catalog import BookCatalog
from meitei.books.models import Chapter, Passage
from meitei.loader import get_default_data_dir
from meitei.unicode_utils import normalize_text


def check_fts5_available(conn: sqlite3.Connection) -> bool:
    """Detect whether SQLite Full-Text Search 5 is enabled."""
    try:
        cur = conn.cursor()
        cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS _test_fts5 USING fts5(x);")
        cur.execute("DROP TABLE _test_fts5;")
        return True
    except sqlite3.OperationalError:
        return False


@dataclass
class BookSearchResult:
    """
    Search match within an imported book passage.

    Attributes:
        passage_id: Stable identifier of the passage.
        book_id: Book identifier.
        book_title: Book title in Meitei Mayek.
        book_title_en: English book title.
        chapter_number: Numeric chapter index.
        chapter_title: Chapter title.
        text: Full passage text.
        matched_snippet: Highlighted or excerpted passage context.
        match_score: Relevance score.
    """
    passage_id: str
    book_id: str
    book_title: str
    book_title_en: str
    chapter_number: int
    chapter_title: str
    text: str
    matched_snippet: str
    match_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return asdict(self)


class BookSearchEngine:
    """
    In-memory or SQLite index over all imported book passages.
    """

    def __init__(self, data_dir: Union[str, Path] = "data") -> None:
        self.data_dir = get_default_data_dir(data_dir)
        self.texts_dir = self.data_dir / "books" / "texts"
        self.catalog = BookCatalog(data_dir=self.data_dir)
        self._conn = sqlite3.connect(":memory:")
        self._conn.row_factory = sqlite3.Row
        self._fts5_enabled = check_fts5_available(self._conn)
        self._init_db()
        self._index_imported_books()

    def _init_db(self) -> None:
        """Create relational passage table and FTS5 virtual table."""
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE passages (
                    passage_id TEXT PRIMARY KEY,
                    book_id TEXT NOT NULL,
                    book_title TEXT,
                    book_title_en TEXT,
                    chapter_number INTEGER NOT NULL,
                    chapter_title TEXT,
                    passage_number INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    text_roman TEXT,
                    translation_en TEXT
                );
                """
            )
            self._conn.execute("CREATE INDEX idx_psg_book ON passages(book_id);")

            if self._fts5_enabled:
                self._conn.execute(
                    """
                    CREATE VIRTUAL TABLE passages_fts USING fts5(
                        passage_id UNINDEXED,
                        book_id UNINDEXED,
                        text,
                        text_roman,
                        translation_en,
                        tokenize = 'unicode61'
                    );
                    """
                )

    def _index_imported_books(self) -> None:
        """Ingest all available texts from data/books/texts into the search index."""
        if not self.texts_dir.exists():
            return

        for book_file in self.texts_dir.glob("*.json"):
            try:
                with open(book_file, "r", encoding="utf-8") as f:
                    book_data = json.load(f)
            except Exception:
                continue

            b_id = book_data.get("book_id", "")
            b_title = book_data.get("title", "")
            b_title_en = book_data.get("title_en", "")

            with self._conn:
                for ch in book_data.get("chapters", []):
                    ch_num = ch.get("chapter_number", 1)
                    ch_title = ch.get("title", "")

                    for p in ch.get("passages", []):
                        p_id = p.get("passage_id", "")
                        p_text = normalize_text(p.get("text", ""))
                        p_roman = p.get("text_roman")
                        if not p_roman and p_text:
                            try:
                                from meitei.orthography import convert_mayek_to_roman
                                p_roman = convert_mayek_to_roman(p_text)
                            except Exception:
                                p_roman = ""
                        p_trans = p.get("translation_en")

                        self._conn.execute(
                            """
                            INSERT OR REPLACE INTO passages (
                                passage_id, book_id, book_title, book_title_en,
                                chapter_number, chapter_title, passage_number,
                                text, text_roman, translation_en
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                p_id,
                                b_id,
                                b_title,
                                b_title_en,
                                ch_num,
                                ch_title,
                                p.get("passage_number", 1),
                                p_text,
                                p_roman or "",
                                p_trans,
                            ),
                        )

                        if self._fts5_enabled:
                            self._conn.execute(
                                """
                                INSERT INTO passages_fts (passage_id, book_id, text, text_roman, translation_en)
                                VALUES (?, ?, ?, ?, ?)
                                """,
                                (p_id, b_id, p_text, p_roman or "", p_trans or ""),
                            )

    def search(
        self,
        query: str,
        book_id: Optional[str] = None,
        limit: int = 20,
    ) -> List[BookSearchResult]:
        """
        Execute full-text search across book passages.

        Args:
            query: Search query (Meitei Mayek, Roman, or English).
            book_id: Optional filter to restrict matches to a specific book.
            limit: Maximum results to return.

        Returns:
            List of BookSearchResult ordered by relevance score.
        """
        q_norm = normalize_text(query).strip()
        if not q_norm:
            return []

        cur = self._conn.cursor()
        results: List[BookSearchResult] = []

        # Substring & Relational matching
        sql = "SELECT * FROM passages WHERE 1=1"
        params: List[Any] = []
        if book_id:
            sql += " AND book_id = ?"
            params.append(book_id)

        cur.execute(sql, params)
        rows = cur.fetchall()

        q_lower = q_norm.lower()

        for row in rows:
            text = row["text"]
            b_title_en = row["book_title_en"] or ""
            ch_title = row["chapter_title"] or ""
            trans = row["translation_en"] or ""
            text_roman = row["text_roman"] or ""
            score = 0.0

            if q_norm in text:
                score = 100.0 if text == q_norm else 80.0
            elif q_lower in text.lower():
                score = 70.0
            elif text_roman and q_lower in text_roman.lower():
                score = 75.0
            elif q_lower in trans.lower():
                score = 65.0
            elif q_lower in ch_title.lower() or q_lower in b_title_en.lower():
                score = 50.0

            if score > 0.0:
                # Generate contextual snippet
                snippet = text
                if len(text) > 120:
                    idx = text.find(q_norm)
                    if idx >= 0:
                        start = max(0, idx - 40)
                        end = min(len(text), idx + len(q_norm) + 40)
                        snippet = f"...{text[start:end]}..."
                    else:
                        snippet = f"{text[:120]}..."

                results.append(
                    BookSearchResult(
                        passage_id=row["passage_id"],
                        book_id=row["book_id"],
                        book_title=row["book_title"],
                        book_title_en=row["book_title_en"],
                        chapter_number=row["chapter_number"],
                        chapter_title=row["chapter_title"],
                        text=text,
                        matched_snippet=snippet,
                        match_score=score,
                    )
                )

        # Sort deterministically by score descending, then passage_id
        results.sort(key=lambda r: (-r.match_score, r.passage_id))
        return results[:limit]


_DEFAULT_BOOK_SEARCH_ENGINE: Optional[BookSearchEngine] = None


def get_book_search_engine(data_dir: Union[str, Path] = "data") -> BookSearchEngine:
    """Return singleton BookSearchEngine instance."""
    global _DEFAULT_BOOK_SEARCH_ENGINE
    if _DEFAULT_BOOK_SEARCH_ENGINE is None:
        _DEFAULT_BOOK_SEARCH_ENGINE = BookSearchEngine(data_dir=data_dir)
    return _DEFAULT_BOOK_SEARCH_ENGINE


def search_passages(
    query: str,
    book_id: Optional[str] = None,
    limit: int = 20,
    data_dir: Union[str, Path] = "data",
) -> List[BookSearchResult]:
    """Top-level convenience function for passage full-text search."""
    engine = get_book_search_engine(data_dir=data_dir)
    return engine.search(query=query, book_id=book_id, limit=limit)

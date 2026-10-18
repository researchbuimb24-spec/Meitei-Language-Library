# -*- coding: utf-8 -*-
"""Unit tests for meitei_lang books and reading texts module."""

import pytest
from meitei_lang.books import (
    load_books,
    count_books,
    list_books,
    get_book,
    get_chapter,
    search_books,
    Book,
    Chapter,
)
from meitei_lang.exceptions import BookNotFoundError, ChapterNotFoundError


def test_books_count():
    assert count_books() >= 3


def test_list_books():
    books = list_books()
    assert len(books) >= 3
    for b in books:
        assert isinstance(b, Book)
        assert b.book_id
        assert b.title
        assert b.title_en
        assert len(b.chapters) >= 1


def test_get_book():
    book = get_book("khamba_thoibi")
    assert book.book_id == "khamba_thoibi"
    assert "Khamba Thoibi" in book.title_en
    assert book.language == "Meitei (Manipuri)"
    assert book.script == "Meitei Mayek"
    assert book.total_chapters() >= 3
    assert book.total_word_count() > 100


def test_get_book_not_found():
    with pytest.raises(BookNotFoundError):
        get_book("nonexistent_book_id")


def test_chapter_retrieval_and_counts():
    book = get_book("khamba_thoibi")
    ch1 = book.get_chapter(1)
    assert isinstance(ch1, Chapter)
    assert ch1.chapter_number == 1
    assert ch1.word_count() > 0
    assert ch1.character_count() > 0

    # Top-level helper
    ch1_direct = get_chapter("khamba_thoibi", 1)
    assert ch1_direct.title == ch1.title

    # Chapter out of bounds
    with pytest.raises(ChapterNotFoundError):
        book.get_chapter(999)


def test_full_text():
    book = get_book("phunga_wari")
    full = book.full_text()
    assert len(full) > 500
    assert any(0xABC0 <= ord(c) <= 0xABFF for c in full)


def test_search_books():
    results = search_books("Pebet")
    assert len(results) > 0
    assert any("Pebet" in r["chapter_title_en"] or "Pebet" in r["matched_text"] for r in results)

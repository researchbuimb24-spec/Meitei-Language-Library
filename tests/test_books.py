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


def test_book_and_chapter_dict_access():
    book = get_book("khamba_thoibi")
    assert book["book_id"] == "khamba_thoibi"
    assert "author" in book
    assert book.get("genre") == book.genre
    assert book.get("nonexistent", "default") == "default"
    with pytest.raises(KeyError):
        _ = book["invalid_key"]

    ch = book.get_chapter(1)
    assert ch["chapter_number"] == 1
    assert "title" in ch
    assert ch.get("title_en") == ch.title_en
    assert ch.get("missing", 42) == 42
    with pytest.raises(KeyError):
        _ = ch["missing"]


def test_ramayana_book():
    book = get_book("ramayana")
    assert book.book_id == "ramayana"
    assert book.title == "ꯔꯥꯃꯥꯌꯟ"
    assert "Ramayana" in book.title_en
    assert book.total_chapters() == 4
    assert "Angom Gopi" in book.author
    assert book.language == "Meitei (Manipuri)"
    assert book.script == "Meitei Mayek"

    # Chapter 1
    ch1 = book.get_chapter(1)
    assert "ꯑꯌꯣꯙ꯭ꯌꯥ" in ch1.title
    assert "Ayodhya" in ch1.title_en
    assert ch1.word_count() > 30

    # Chapter 3
    ch3 = book.get_chapter(3)
    assert "ꯍꯅꯨꯃꯥꯟ" in ch3.title
    assert "Hanuman" in ch3.title_en

    # Full text contains Meitei Mayek characters
    text = book.full_text()
    assert len(text) > 500
    assert any(0xABC0 <= ord(c) <= 0xABFF for c in text)


def test_mahabharata_book():
    book = get_book("mahabharata")
    assert book.book_id == "mahabharata"
    assert book.title == "ꯃꯍꯥꯚꯥꯔꯠ"
    assert "Mahabharata" in book.title_en
    assert book.total_chapters() == 4
    assert "Manipur" in book.description

    # Chapter 2 (Chitrangada)
    ch2 = book.get_chapter(2)
    assert "ꯆꯤꯇ꯭ꯔꯥꯡꯒꯗꯥ" in ch2.title
    assert "Chitrangada" in ch2.title_en

    # Chapter 3 (Babruvahana)
    ch3 = book.get_chapter(3)
    assert "ꯕꯕ꯭ꯔꯨꯕꯥꯍꯟ" in ch3.title
    assert "Babruvahana" in ch3.title_en

    # Full text
    text = book.full_text()
    assert len(text) > 500
    assert any(0xABC0 <= ord(c) <= 0xABFF for c in text)


def test_search_epics():
    # Search for Chitrangada
    chitrangada_res = search_books("Chitrangada")
    assert len(chitrangada_res) > 0
    assert any(r["book_id"] == "mahabharata" for r in chitrangada_res)

    # Search for Hanuman
    hanuman_res = search_books("Hanuman")
    assert len(hanuman_res) > 0
    assert any(r["book_id"] == "ramayana" for r in hanuman_res)

    # Search for Babruvahana
    babru_res = search_books("Babruvahana")
    assert len(babru_res) > 0
    assert any(r["book_id"] == "mahabharata" for r in babru_res)


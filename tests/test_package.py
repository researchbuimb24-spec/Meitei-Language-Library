# -*- coding: utf-8 -*-
"""Unit tests for meitei_lang package exports, versioning, and script metadata."""

import meitei_lang as mt
from meitei_lang import language_info


def test_package_metadata():
    assert hasattr(mt, "__version__")
    assert mt.__version__ == "0.2.0"
    assert hasattr(mt, "__author__")


def test_top_level_api():
    # Vocabulary
    assert callable(mt.get_word)
    assert callable(mt.count_words)
    assert mt.count_words() >= 3000

    # Transliteration
    assert callable(mt.transliterate)
    assert callable(mt.meitei_to_roman)
    assert callable(mt.roman_to_meitei)
    assert callable(mt.meitei_to_bengali)
    assert callable(mt.bengali_to_meitei)

    # Books
    assert callable(mt.list_books)
    assert callable(mt.get_book)
    assert callable(mt.get_chapter)

    # Songs
    assert callable(mt.list_songs)
    assert callable(mt.get_song)
    assert callable(mt.get_lyrics)

    # Search
    assert callable(mt.search)


def test_language_info_constants():
    # 18 Primary base letters (Iyek Ipi)
    assert len(language_info.IYEK_IPI) == 18

    # 9 Cheising Iyek (extended letters)
    assert len(language_info.CHEISING_IYEK) == 9

    # 8 Lonsum Iyek (coda consonants)
    assert len(language_info.LONSUM_IYEK) == 8

    # 8 Cheitap Iyek (vowel signs)
    assert len(language_info.CHEITAP_IYEK) == 8

    # 10 Digits
    assert len(language_info.DIGITS_MAP) == 10

    # Summary function
    summary = language_info.get_script_summary()
    assert "meitei_mayek" in summary
    assert "bengali" in summary
    assert "roman" in summary

    # Alphabet list
    alphabet = language_info.get_alphabet(include_extended=False)
    assert len(alphabet) == 18

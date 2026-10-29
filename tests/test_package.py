# -*- coding: utf-8 -*-
"""Unit tests for meitei_lang package exports, versioning, and script metadata."""

import meitei_lang as mt
from meitei_lang import language_info


def test_package_metadata():
    assert hasattr(mt, "__version__")
    assert mt.__version__ == "0.5.0"
    assert hasattr(mt, "__author__")


def test_top_level_api():
    # Vocabulary
    assert callable(mt.get_word)
    assert callable(mt.count_words)
    assert mt.count_words() >= 150000

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

    # Sentences
    assert callable(mt.list_sentences)
    assert callable(mt.get_sentence)
    assert callable(mt.count_sentences)
    assert callable(mt.search_sentences)
    assert callable(mt.get_random_sentence)
    assert mt.count_sentences() == 120

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


def test_meitei_package_metadata_and_exports():
    import meitei

    assert hasattr(meitei, "__version__")
    assert meitei.__version__ == "0.1.0"
    assert "MIT" in meitei.__license__
    assert "CC BY-SA 4.0" in meitei.__license__

    # Check that core models, functions, and enums are exported
    assert hasattr(meitei, "search")
    assert hasattr(meitei, "translate")
    assert hasattr(meitei, "list_grammar_topics")
    assert hasattr(meitei, "list_books")
    assert hasattr(meitei, "read_passages")
    assert hasattr(meitei, "audit_repository")
    assert hasattr(meitei, "normalize_text")
    assert hasattr(meitei, "detect_script")
    assert hasattr(meitei, "convert_script")


def test_meitei_offline_independent_path_resolution(tmp_path, monkeypatch):
    import meitei

    # Switch working directory to an isolated temp directory without any 'data' directory
    monkeypatch.chdir(tmp_path)
    assert not (tmp_path / "data").exists()

    # Search should still resolve data and return results
    results = meitei.search("mi")
    assert len(results) >= 1
    assert results[0].canonical_lemma == "ꯃꯤ"

    # Grammar retrieval should still resolve
    topics = meitei.list_grammar_topics()
    assert len(topics) >= 8

    # Books catalog should still resolve
    books = meitei.list_books()
    assert len(books) >= 10


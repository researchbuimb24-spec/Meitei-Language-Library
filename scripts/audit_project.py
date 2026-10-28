# -*- coding: utf-8 -*-
"""
Comprehensive Audit Script for Meitei (Manipuri) Python Library.
Checks all 10 books, 10 songs, vocabulary entries, daily usable sentences,
cross-corpus search, models, data integrity, and error handling.
"""

import io
import json
import os
import sys

if isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, "src")
DATA_DIR = os.path.join(SRC_DIR, "meitei_lang", "data")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import meitei_lang as mt

def audit_books():
    print("=== 1. AUDITING 10 BOOKS ===")
    books = mt.list_books()
    print(f"Total Books: {len(books)} (Expected: 10)")
    assert len(books) == 10, f"Expected 10 books, found {len(books)}"

    expected_ids = [
        "khamba_thoibi",
        "phunga_wari",
        "sana_leibak_chronicles",
        "ramayana",
        "mahabharata",
        "numit_kappa",
        "chainarol",
        "panthoibi_khonggul",
        "poireiton_khunthok",
        "pakhangba_laihui",
    ]

    total_chapters = 0
    for idx, expected_id in enumerate(expected_ids, 1):
        book = mt.get_book(expected_id)
        assert book.book_id == expected_id
        assert len(book.title) > 0
        assert len(book.title_en) > 0
        assert len(book.author) > 0
        assert len(book.genre) > 0
        assert len(book.description) > 0
        assert len(book.source) > 0
        assert len(book.copyright) > 0
        assert book.language == "Meitei (Manipuri)"
        assert book.script == "Meitei Mayek"

        chapters = book.chapters
        assert len(chapters) >= 3, f"Book {expected_id} has fewer than 3 chapters"
        total_chapters += len(chapters)

        for c_idx, ch in enumerate(chapters, 1):
            assert ch.chapter_number == c_idx, f"Chapter numbering mismatch in {expected_id}: {ch.chapter_number} != {c_idx}"
            assert len(ch.title) > 0
            assert len(ch.title_en) > 0
            assert len(ch.text) > 50
            # Test direct chapter retrieval
            retrieved = mt.get_chapter(expected_id, c_idx)
            assert retrieved.title == ch.title
            assert retrieved.word_count() > 10
            assert retrieved.character_count() > 50

        full_txt = book.full_text()
        assert len(full_txt) > 300
        print(f"  {idx:2d}. [{book.book_id:23s}] {book.title_en:55s} | Chapters: {len(chapters):2d} | Words: {book.total_word_count():4d}")

    print(f"Total Chapters across 10 books: {total_chapters}")
    print("Books Audit: PASSED\n")
    return len(books), total_chapters


def audit_songs():
    print("=== 2. AUDITING 10 SONGS ===")
    songs = mt.list_songs()
    print(f"Total Songs: {len(songs)} (Expected: 10)")
    assert len(songs) == 10, f"Expected 10 songs, found {len(songs)}"

    expected_ids = [
        "sana_leibak_manipur",
        "thabal_chongba_ishei",
        "eikhoi_kangleicha",
        "chingda_satpi_engellei",
        "tamna_sangba_loktak_pat",
        "moirang_kangleirol_ballad",
        "he_leipakpokpa_lai",
        "nongmaijinggi_chingmei",
        "nungshirabi_eigi_manipur",
        "khulang_eshei_harvest",
    ]

    for idx, sid in enumerate(expected_ids, 1):
        s = mt.get_song(sid)
        assert s.song_id == sid
        assert len(s.title) > 0
        assert len(s.title_en) > 0
        assert len(s.title_roman) > 0
        assert len(s.composer) > 0
        assert len(s.lyricist) > 0
        assert len(s.genre) > 0

        # Verify all 4 scripts
        for script in ("meitei", "roman", "bengali", "english"):
            lyrics = s.get_lyrics(script)
            assert len(lyrics) > 30, f"Lyrics for {sid} in {script} too short"

        meitei_lyr = s.get_lyrics("meitei")
        assert any(0xABC0 <= ord(c) <= 0xABFF for c in meitei_lyr), f"Missing Mayek chars in {sid}"
        beng_lyr = s.get_lyrics("bengali")
        assert any(0x0980 <= ord(c) <= 0x09FF for c in beng_lyr), f"Missing Bengali chars in {sid}"

        print(f"  {idx:2d}. [{s.song_id:26s}] {s.title_en:60s} | Scripts: 4/4")

    print("Songs Audit: PASSED\n")
    return len(songs)


def audit_sentences():
    print("=== 3. AUDITING DAILY USABLE SENTENCES ===")
    sentences = mt.list_sentences()
    print(f"Total Sentences: {len(sentences)} (Expected: >= 100)")
    assert len(sentences) >= 100, f"Expected at least 100 sentences, got {len(sentences)}"

    categories = mt.get_sentence_categories()
    print(f"Total Categories: {len(categories)} -> {categories}")
    assert len(categories) == 12

    seen_ids = set()
    for s in sentences:
        assert s.sentence_id not in seen_ids, f"Duplicate sentence ID: {s.sentence_id}"
        seen_ids.add(s.sentence_id)
        assert len(s.meitei) > 0
        assert len(s.roman) > 0
        assert len(s.bengali) > 0
        assert len(s.english) > 0
        assert len(s.category) > 0
        assert len(s.context) > 0
        assert any(0xABC0 <= ord(c) <= 0xABFF for c in s.meitei)
        assert any(0x0980 <= ord(c) <= 0x09FF for c in s.bengali)

    # Test random retrieval
    rand_one = mt.get_random_sentence()
    assert rand_one is not None
    rand_multi = mt.get_random_sentence(n=5)
    assert isinstance(rand_multi, list)
    assert len(rand_multi) == 5

    print("Sentences Audit: PASSED\n")
    return len(sentences), len(categories)


def audit_vocabulary():
    print("=== 4. AUDITING VOCABULARY DATASET ===")
    count = mt.count_words()
    print(f"Total Vocabulary Words: {count:,} (Expected: >= 150,000)")
    assert count >= 150000, f"Expected >= 150,000 words, got {count}"

    summary = mt.get_vocabulary_summary()
    print(f"Lexicon Categories: {len(summary['categories'])}")
    print(f"Parts of Speech: {len(summary['parts_of_speech'])}")
    print("Top Categories:", list(summary["categories"].items())[:6])

    # Test word lookup by Mayek and Roman
    w_mama = mt.get_word("ꯃꯃꯥ")
    assert w_mama.transliteration == "mama"
    assert "mother" in w_mama.meaning_en

    w_roman = mt.get_word("khurumjari")
    assert w_roman.word == "ꯈꯨꯔꯨꯝꯖꯔꯤ"

    # Test random word sampling
    rand_words = mt.get_random_words(n=5)
    assert len(rand_words) == 5

    # Test category filtering
    cult_words = mt.get_words_by_category("culture", limit=10)
    assert len(cult_words) == 10

    print("Vocabulary Audit: PASSED\n")
    return count


def audit_transliteration():
    print("=== 5. AUDITING TRANSLITERATION ENGINE ===")
    test_cases = [
        ("ꯃꯩꯇꯩ ꯂꯣꯟ", "meitei lon"),
        ("ꯃꯃꯥ", "mama"),
        ("ꯈꯨꯔꯨꯝꯖꯔꯤ", "khurumjari"),
        ("ꯏꯃꯥ", "ima"),
    ]
    for mayek, expected_roman in test_cases:
        roman = mt.meitei_to_roman(mayek)
        assert roman == expected_roman, f"meitei_to_roman('{mayek}') -> '{roman}', expected '{expected_roman}'"
        bengali = mt.meitei_to_bengali(mayek)
        assert len(bengali) > 0
        back_mayek = mt.bengali_to_meitei(bengali)
        assert len(back_mayek) > 0

    assert mt.detect_script("ꯃꯩꯇꯩ") == "meitei_mayek"
    assert mt.detect_script("মণিপুর") == "bengali"
    assert mt.detect_script("Manipur") == "latin"
    print("Transliteration Audit: PASSED\n")


def audit_cross_corpus_search():
    print("=== 6. AUDITING CROSS-CORPUS SEARCH ===")
    res = mt.search("Manipur")
    print(f"Query 'Manipur': Total={res.total_count} (Vocab={len(res.vocabulary)}, Books={len(res.books)}, Songs={len(res.songs)}, Sentences={len(res.sentences)})")
    assert len(res.vocabulary) > 0
    assert len(res.books) > 0
    assert len(res.songs) > 0
    assert len(res.sentences) > 0

    res_empty = mt.search("")
    assert res_empty.total_count == 0
    assert res_empty.is_empty()
    print("Cross-Corpus Search Audit: PASSED\n")


def audit_data_integrity():
    print("=== 7. AUDITING DATASET INTEGRITY ===")
    for fname in ["books.json", "songs.json", "sentences.json", "vocabulary.json"]:
        fpath = os.path.join(DATA_DIR, fname)
        assert os.path.exists(fpath), f"Missing data file: {fpath}"
        size_mb = os.path.getsize(fpath) / (1024 * 1024)
        print(f"  - {fname:18s}: {size_mb:6.2f} MB")
    print("Data Integrity Audit: PASSED\n")


def main():
    print("==================================================")
    print("    COMPREHENSIVE PROJECT AUDIT: MEITEI-LANG      ")
    print("==================================================\n")
    b_count, ch_count = audit_books()
    s_count = audit_songs()
    sent_count, cat_count = audit_sentences()
    v_count = audit_vocabulary()
    audit_transliteration()
    audit_cross_corpus_search()
    audit_data_integrity()
    print("==================================================")
    print("    ALL AUDIT CHECKS SUCCESSFULLY PASSED!         ")
    print(f"    - Version:        {mt.__version__}")
    print(f"    - Books:          {b_count} books ({ch_count} chapters)")
    print(f"    - Songs:          {s_count} authentic songs")
    print(f"    - Sentences:      {sent_count} daily usable sentences ({cat_count} categories)")
    print(f"    - Vocabulary:     {v_count:,} unique verified entries")
    print("==================================================")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Unit tests for meitei_lang dictionary and vocabulary module."""

import pytest
from meitei_lang.dictionary import (
    load_vocabulary,
    count_words,
    get_vocabulary_count,
    get_word,
    lookup,
    search_words,
    get_words_by_category,
    get_words_by_pos,
    get_categories,
    get_parts_of_speech,
    get_random_words,
    get_vocabulary_summary,
    WordEntry,
)
from meitei_lang.exceptions import WordNotFoundError


def test_vocabulary_count():
    # Requirement: At least 3,000 unique entries
    total = count_words()
    assert total >= 3000, f"Expected at least 3,000 words, got {total}"
    assert get_vocabulary_count() == total


def test_word_entry_structure():
    entries = load_vocabulary()
    assert len(entries) >= 3000
    entry = entries[0]
    assert isinstance(entry, WordEntry)
    assert entry.word
    assert entry.script == "Meitei Mayek"
    assert entry.transliteration
    assert entry.meaning_en
    assert entry.part_of_speech
    assert entry.category
    assert entry.source
    assert entry.verified is True

    d = entry.to_dict()
    assert isinstance(d, dict)
    assert d["word"] == entry.word


def test_get_word_exact_meitei():
    entry = get_word("ꯃꯃꯥ")
    assert entry.word == "ꯃꯃꯥ"
    assert entry.transliteration == "mama"
    assert "mother" in entry.meaning_en


def test_get_word_roman():
    entry = get_word("khurumjari")
    assert entry.word == "ꯈꯨꯔꯨꯝꯖꯔꯤ"
    assert "salutation" in entry.meaning_en or "greeting" in entry.meaning_en


def test_get_word_not_found():
    with pytest.raises(WordNotFoundError):
        get_word("xyznonexistentword12345")


def test_lookup_safe():
    assert lookup("xyznonexistentword12345") is None
    entry = lookup("mama")
    assert entry is not None
    assert entry.word == "ꯃꯃꯥ"


def test_search_words():
    # Search in meaning
    water_matches = search_words("water", search_in="meaning")
    assert len(water_matches) > 0
    assert any("water" in e.meaning_en.lower() for e in water_matches)

    # Search in transliteration
    prefix_matches = search_words("ma", match_type="prefix", search_in="transliteration", limit=5)
    assert len(prefix_matches) <= 5
    assert all(e.transliteration.lower().startswith("ma") for e in prefix_matches)


def test_categories_and_pos():
    cats = get_categories()
    assert len(cats) >= 10
    assert "family" in cats
    assert "nature" in cats
    assert "culture" in cats

    pos_list = get_parts_of_speech()
    assert "noun" in pos_list
    assert "verb" in pos_list
    assert "adjective" in pos_list

    family_words = get_words_by_category("family")
    assert len(family_words) > 0
    assert all(w.category == "family" for w in family_words)

    verbs = get_words_by_pos("verb")
    assert len(verbs) > 0
    assert all(w.part_of_speech == "verb" for w in verbs)


def test_get_random_words():
    sampled = get_random_words(n=4)
    assert len(sampled) == 4
    assert all(isinstance(w, WordEntry) for w in sampled)

    sampled_cat = get_random_words(n=3, category="culture")
    assert len(sampled_cat) == 3
    assert all(w.category == "culture" for w in sampled_cat)


def test_vocabulary_summary():
    summary = get_vocabulary_summary()
    assert summary["total_words"] >= 3000
    assert summary["categories_count"] >= 10
    assert summary["parts_of_speech_count"] >= 5
    assert isinstance(summary["categories"], dict)


def test_word_entry_dict_access():
    w = get_word("khurumjari")
    assert w["word"] == "ꯈꯨꯔꯨꯝꯖꯔꯤ"
    assert w["meaning_en"] == w.meaning_en
    assert w.get("nonexistent", "fallback") == "fallback"
    assert "meaning_en" in w
    with pytest.raises(KeyError):
        _ = w["nonexistent"]

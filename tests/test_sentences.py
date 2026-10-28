# -*- coding: utf-8 -*-
"""Unit tests for meitei_lang daily usable sentences module."""

import pytest
from meitei_lang.sentences import (
    load_sentences,
    count_sentences,
    list_sentences,
    get_sentence,
    get_sentences_by_category,
    get_sentence_categories,
    search_sentences,
    get_random_sentence,
    Sentence,
)
from meitei_lang.exceptions import SentenceNotFoundError


def test_sentences_count():
    assert count_sentences() == 120


def test_list_sentences():
    sentences = list_sentences()
    assert len(sentences) == 120
    for s in sentences:
        assert isinstance(s, Sentence)
        assert s.sentence_id
        assert s.meitei
        assert s.roman
        assert s.bengali
        assert s.english
        assert s.category
        assert s.context


def test_get_sentence():
    s = get_sentence("greet_001")
    assert isinstance(s, Sentence)
    assert s.sentence_id == "greet_001"
    assert s.meitei == "ꯈꯨꯔꯨꯝꯖꯔꯤ꯫"
    assert "Khurumjari" in s.roman
    assert "Greetings" in s.english
    assert s.category == "greetings"


def test_get_sentence_not_found():
    with pytest.raises(SentenceNotFoundError):
        get_sentence("nonexistent_sentence_id")


def test_sentence_categories():
    categories = get_sentence_categories()
    assert len(categories) == 12
    expected = {
        "greetings",
        "introductions",
        "politeness_gratitude",
        "market_shopping",
        "food_dining",
        "travel_directions",
        "time_weather",
        "family_home",
        "health_emergency",
        "work_study",
        "culture_festivals",
        "feelings_emotions",
    }
    assert expected.issubset(set(categories))

    # Test filtering by category
    greetings = get_sentences_by_category("greetings")
    assert len(greetings) == 10
    for g in greetings:
        assert g.category == "greetings"


def test_search_sentences():
    # Search Meitei Mayek
    matches_mayek = search_sentences("ꯈꯨꯔꯨꯝꯖꯔꯤ")
    assert len(matches_mayek) >= 1

    # Search Roman
    matches_roman = search_sentences("Khurumjari")
    assert len(matches_roman) >= 1

    # Search English
    matches_en = search_sentences("Kangla")
    assert len(matches_en) >= 1

    # Search market
    matches_market = search_sentences("market")
    assert len(matches_market) >= 1


def test_get_random_sentence():
    single = get_random_sentence()
    assert isinstance(single, Sentence)

    multiple = get_random_sentence(n=3)
    assert isinstance(multiple, list)
    assert len(multiple) == 3

    cat_single = get_random_sentence(category="food_dining", n=1)
    assert isinstance(cat_single, Sentence)
    assert cat_single.category == "food_dining"


def test_sentence_dict_access():
    s = get_sentence("greet_001")
    assert s["sentence_id"] == "greet_001"
    assert s["meitei"] == "ꯈꯨꯔꯨꯝꯖꯔꯤ꯫"
    assert s.get("category") == "greetings"
    assert s.get("nonexistent", "default_val") == "default_val"
    assert "meitei" in s
    with pytest.raises(KeyError):
        _ = s["invalid_key"]


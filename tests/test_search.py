# -*- coding: utf-8 -*-
"""Unit tests for meitei_lang unified cross-corpus search."""

from meitei_lang.search import search, SearchResults


def test_unified_search():
    res = search("Manipur")
    assert isinstance(res, SearchResults)
    assert res.total_count > 0
    assert res.total_results == res.total_count
    assert not res.is_empty()
    assert len(res.vocabulary) > 0
    assert len(res.books) > 0
    assert len(res.songs) > 0

    d = res.to_dict()
    assert d["total_count"] == res.total_count
    assert d["query"] == "Manipur"


def test_search_filters():
    # Only vocabulary
    res_vocab_only = search("Manipur", in_books=False, in_songs=False)
    assert len(res_vocab_only.vocabulary) > 0
    assert len(res_vocab_only.books) == 0
    assert len(res_vocab_only.songs) == 0

    # Only songs
    res_songs_only = search("Manipur", in_vocabulary=False, in_books=False)
    assert len(res_songs_only.vocabulary) == 0
    assert len(res_songs_only.books) == 0
    assert len(res_songs_only.songs) > 0


def test_empty_search():
    res = search("")
    assert res.total_count == 0
    assert res.is_empty()

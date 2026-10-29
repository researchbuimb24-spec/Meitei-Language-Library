# -*- coding: utf-8 -*-
"""
Unit tests for the unified dictionary search engine in meitei.search.
"""

from pathlib import Path
import pytest

from meitei.search import (
    SearchEngine,
    SearchResult,
    batch_search,
    check_fts5_available,
    search,
)


def test_fts5_capability():
    import sqlite3
    con = sqlite3.connect(":memory:")
    # Must report boolean without crashing
    avail = check_fts5_available(con)
    assert isinstance(avail, bool)


def test_empty_database_returns_empty_results(tmp_path):
    """Ensure search does not pretend that an empty database contains words."""
    (tmp_path / "lexicon").mkdir()
    (tmp_path / "lexicon" / "core_lexicon.jsonl").write_text("", encoding="utf-8")
    (tmp_path / "lexicon" / "candidate_lexicon.jsonl").write_text("", encoding="utf-8")
    (tmp_path / "lexicon" / "variants.jsonl").write_text("", encoding="utf-8")
    (tmp_path / "translations").mkdir()
    (tmp_path / "translations" / "glosses.jsonl").write_text("", encoding="utf-8")
    (tmp_path / "sources").mkdir()
    (tmp_path / "sources" / "sources.jsonl").write_text("", encoding="utf-8")

    engine = SearchEngine(data_dir=tmp_path)
    res = engine.search("mi")
    assert res == []

    res_empty_query = engine.search("")
    assert res_empty_query == []


def test_unicode_search_exact_matches():
    # 1. Search in Meitei Mayek
    results_mayek = search("ꯃꯤ")
    assert len(results_mayek) >= 1
    top = results_mayek[0]
    assert top.entry_id == "MEI-LEX-0000001"
    assert top.canonical_lemma == "ꯃꯤ"
    assert top.matched_field == "headword_meitei"
    assert top.match_score == 100.0

    # 2. Search in Roman transliteration
    results_roman = search("thabak")
    assert len(results_roman) >= 1
    top_thabak = results_roman[0]
    assert top_thabak.entry_id == "MEI-LEX-0000007"
    assert top_thabak.canonical_lemma == "ꯊꯕꯛ"
    assert top_thabak.matched_field == "headword_roman"
    assert top_thabak.match_score == 100.0

    # 3. Search in Bengali script
    results_bengali = search("মী")
    assert len(results_bengali) >= 1
    top_bn = results_bengali[0]
    assert top_bn.entry_id == "MEI-LEX-0000001"


def test_spelling_variants_search():
    # 'mee' is the 1859 McCulloch historical romanization for 'mi'
    res_mee = search("mee")
    assert len(res_mee) >= 1
    match = res_mee[0]
    assert match.entry_id == "MEI-LEX-0000001"
    assert match.is_variant_match is True
    assert match.matched_field == "spelling_variant"
    assert match.matched_text == "mee"
    assert match.variant_details is not None
    assert match.variant_details["source_id"] == "MEI-SRC-000002"

    # 'ai' is Pettigrew 1912 variant for 'ei' (I)
    res_ai = search("ai")
    assert len(res_ai) >= 1
    assert any(r.entry_id == "MEI-LEX-0000008" and r.is_variant_match for r in res_ai)


def test_multilingual_glosses_search():
    # Search English gloss 'person'
    res_person = search("person")
    assert len(res_person) >= 1
    assert any(r.entry_id == "MEI-LEX-0000001" for r in res_person)

    # Search English gloss 'work'
    res_work = search("work")
    assert len(res_work) >= 1
    assert any(r.entry_id == "MEI-LEX-0000007" for r in res_work)


def test_provenance_and_verified_only_filtering():
    # 'korou' is in candidate_lexicon.jsonl with status UNVERIFIED
    # 1. verified_only=False -> finds korou
    res_unverified = search("korou", verified_only=False)
    assert len(res_unverified) >= 1
    assert res_unverified[0].entry_id == "MEI-LEX-0000011"
    assert res_unverified[0].status == "UNVERIFIED"

    # 2. verified_only=True -> strictly excludes korou
    res_verified_only = search("korou", verified_only=True)
    assert len(res_verified_only) == 0


def test_citations_included_in_results():
    results = search("thabak")
    assert len(results) >= 1
    top = results[0]
    assert len(top.citations) >= 1
    cit = top.citations[0]
    assert cit["source_id"] == "MEI-SRC-000004"
    assert "Page 253" in cit["citation_locator"]


def test_homonyms_deterministic_ranking(tmp_path):
    """Test that multiple entries with identical or overlapping headwords rank deterministically."""
    (tmp_path / "sources").mkdir()
    (tmp_path / "sources" / "sources.jsonl").write_text(
        '{"id": "MEI-SRC-000001", "title": "Source", "source_type": "puya"}\n',
        encoding="utf-8"
    )
    (tmp_path / "lexicon").mkdir()
    # Two distinct homonyms for 'pa': 'pa' (eyelash) vs 'pa' (read)
    (tmp_path / "lexicon" / "core_lexicon.jsonl").write_text(
        '{"id": "MEI-LEX-0000020", "headword_meitei": "ꯄ", "headword_roman": "pa", "status": "SOURCE_ATTESTED", "source_id": "MEI-SRC-000001", "citation_locator": "Page 1", "senses": [{"id": "MEI-SNS-0000020", "definition_en": "Eyelash", "part_of_speech": "noun"}]}\n'
        '{"id": "MEI-LEX-0000021", "headword_meitei": "ꯄ", "headword_roman": "pa", "status": "SOURCE_ATTESTED", "source_id": "MEI-SRC-000001", "citation_locator": "Page 2", "senses": [{"id": "MEI-SNS-0000021", "definition_en": "To read (root)", "part_of_speech": "verb"}]}\n',
        encoding="utf-8"
    )
    (tmp_path / "lexicon" / "candidate_lexicon.jsonl").write_text("", encoding="utf-8")
    (tmp_path / "lexicon" / "variants.jsonl").write_text("", encoding="utf-8")
    (tmp_path / "translations").mkdir()
    (tmp_path / "translations" / "glosses.jsonl").write_text("", encoding="utf-8")

    engine = SearchEngine(data_dir=tmp_path)
    res = engine.search("pa")
    assert len(res) == 2
    # Both matches have equal 100.0 score, so order must follow entry_id deterministically
    assert res[0].entry_id == "MEI-LEX-0000020"
    assert res[1].entry_id == "MEI-LEX-0000021"


def test_batch_search():
    queries = ["mi", "thabak", "nonexistent_term"]
    batch_res = batch_search(queries)
    assert isinstance(batch_res, dict)
    assert len(batch_res) == 3
    assert len(batch_res["mi"]) >= 1
    assert len(batch_res["thabak"]) >= 1
    assert len(batch_res["nonexistent_term"]) == 0


def test_language_filtering():
    # Query 'thabak' with lang='latin'
    res_latin = search("thabak", lang="latin")
    assert len(res_latin) >= 1

    # Query 'thabak' with lang='mni' (Meitei Mayek only)
    res_mni = search("thabak", lang="mni")
    # 'thabak' is Latin, so lang='mni' should filter it out
    assert len(res_mni) == 0

    # Query Mayek 'ꯊꯕꯛ' with lang='mni'
    res_mayek = search("ꯊꯕꯛ", lang="mni")
    assert len(res_mayek) >= 1


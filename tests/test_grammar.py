# -*- coding: utf-8 -*-
"""
Unit and Integration Tests for the Meitei Grammar Reference Subsystem.

Verifies:
1. Retrieval of grammar records by research topic.
2. Accurate accounting of populated vs unpopulated research categories.
3. Provenance and citation completeness (source IDs, locators, reviewer history).
4. Example sentence authenticity, morpheme glosses, and translation provenance.
5. Provenance filtering with `verified_only=True`.
6. Error handling for missing references, unknown sources, and malformed schemas.
7. Bibliographic source lookup for individual topics and the subsystem as a whole.
8. CLI command execution for `meitei grammar` across plain text and JSON.
"""

import io
import json
from contextlib import redirect_stdout
from pathlib import Path
import pytest

from meitei import cli
from meitei.grammar import (
    GrammarExample,
    GrammarRecord,
    GrammarValidationError,
    get_grammar_record_by_id,
    get_grammar_records,
    get_populated_topics,
    get_topic_sources,
    get_unpopulated_topics,
    list_grammar_sources,
    list_grammar_topics,
    load_grammar_records,
    validate_grammar_record,
)
from meitei.loader import DataLoader, MissingSourceError
from meitei.schema import is_valid_gex_id, is_valid_grm_id


# =============================================================================
# Topic Accounting & Catalog Tests
# =============================================================================

def test_list_grammar_topics_catalog():
    """Verify that all 8 research categories are registered with accurate status."""
    topics = list_grammar_topics("data")
    assert len(topics) >= 8

    topic_map = {t["id"]: t for t in topics}

    # Populated categories
    expected_populated = ["pronouns", "numerals", "negation", "verb_morphology", "sentence_structure"]
    for t_id in expected_populated:
        assert t_id in topic_map, f"Missing expected topic: {t_id}"
        t = topic_map[t_id]
        assert t["status"] == "POPULATED", f"Topic '{t_id}' should be POPULATED"
        assert t["record_count"] >= 1, f"Topic '{t_id}' should have active records"
        assert "documentation" in t, f"Topic '{t_id}' should document attestation sources"

    # Unpopulated categories (research categories pending verification)
    expected_unpopulated = ["classifiers", "noun_morphology", "particles"]
    for t_id in expected_unpopulated:
        assert t_id in topic_map, f"Missing expected topic: {t_id}"
        t = topic_map[t_id]
        assert t["status"] == "UNPOPULATED", f"Topic '{t_id}' should be UNPOPULATED"
        assert t["record_count"] == 0, f"Topic '{t_id}' should have 0 records"
        assert "unpopulated_reason" in t, f"Topic '{t_id}' must document reason for pending status"


def test_get_populated_and_unpopulated_helpers():
    """Verify helper functions distinguishing populated from unpopulated topics."""
    pop = get_populated_topics("data")
    unpop = get_unpopulated_topics("data")

    assert len(pop) >= 5
    assert len(unpop) >= 3

    pop_ids = {t["id"] for t in pop}
    unpop_ids = {t["id"] for t in unpop}

    assert "pronouns" in pop_ids
    assert "negation" in pop_ids
    assert "classifiers" in unpop_ids
    assert "particles" in unpop_ids
    assert pop_ids.isdisjoint(unpop_ids)


# =============================================================================
# Record Retrieval & Topic Filtering Tests
# =============================================================================

def test_get_grammar_records_by_topic():
    """Verify retrieval of records by topic."""
    # Topic: pronouns
    pronoun_recs = get_grammar_records(topic="pronouns", data_dir="data")
    assert len(pronoun_recs) == 2
    assert all(r.topic == "pronouns" for r in pronoun_recs)

    # Check first record contents
    p1 = pronoun_recs[0]
    assert p1.id == "MEI-GRM-0000001"
    assert "Personal Pronoun Paradigm" in p1.title
    assert p1.source_id == "MEI-SRC-000003"
    assert "Page 14" in p1.citation_locator
    assert p1.morphological_rule is not None
    assert len(p1.examples) >= 1

    # Topic: negation
    neg_recs = get_grammar_records(topic="negation", data_dir="data")
    assert len(neg_recs) >= 1
    neg = neg_recs[0]
    assert neg.id == "MEI-GRM-0000004"
    assert "-te / -de" in neg.title
    assert neg.source_id == "MEI-SRC-000004"
    assert "Page 261" in neg.citation_locator


def test_get_grammar_records_nonexistent_topic():
    """Non-existent topic returns empty list cleanly without error."""
    recs = get_grammar_records(topic="nonexistent_syntax_domain", data_dir="data")
    assert recs == []


def test_get_grammar_record_by_id():
    """Retrieve individual records by stable identifier."""
    rec = get_grammar_record_by_id("MEI-GRM-0000003", data_dir="data")
    assert rec is not None
    assert rec.id == "MEI-GRM-0000003"
    assert rec.topic == "numerals"
    assert rec.source_id == "MEI-SRC-000001"

    # Nonexistent ID
    none_rec = get_grammar_record_by_id("MEI-GRM-9999999", data_dir="data")
    assert none_rec is None


# =============================================================================
# Provenance & Citation Integrity Tests
# =============================================================================

def test_grammar_records_citation_integrity():
    """Ensure all grammar records in dataset link to authentic cataloged sources."""
    loader = DataLoader("data")
    sources = loader.load_sources()
    records = load_grammar_records(data_dir="data", known_sources=set(sources.keys()))

    assert len(records) >= 6

    for r in records:
        assert is_valid_grm_id(r.id), f"Invalid grammar ID: {r.id}"
        assert r.verification_status in ["SOURCE_ATTESTED", "VERIFIED"]

        if r.verification_status == "SOURCE_ATTESTED":
            assert r.source_id in sources, f"Record {r.id} references unknown source: {r.source_id}"
            assert r.citation_locator is not None and len(r.citation_locator.strip()) > 0
            assert any(k in r.citation_locator.lower() for k in ["page", "chapter", "section", "table", "specimen"]), (
                f"Record {r.id} locator '{r.citation_locator}' lacks exact page/chapter specification"
            )

        # Reviewer attribution check
        rev = r.reviewer_attribution
        assert rev is not None, f"Record {r.id} missing reviewer_attribution"
        assert len(rev.get("reviewer_id", "").strip()) > 0
        assert len(rev.get("review_date", "").strip()) > 0

        # Review history check
        assert isinstance(r.review_history, list)
        assert len(r.review_history) >= 1
        assert r.review_history[0].get("action") == "INITIAL_VERIFICATION"


def test_grammar_examples_authenticity():
    """Verify that example sentences are source-backed with translation provenance."""
    records = load_grammar_records(data_dir="data")

    for r in records:
        assert len(r.examples) >= 1, f"Record {r.id} must contain at least one verified example"
        for ex in r.examples:
            assert is_valid_gex_id(ex.example_id), f"Invalid example ID: {ex.example_id}"
            assert len(ex.meitei.strip()) > 0
            assert len(ex.roman.strip()) > 0
            assert len(ex.english.strip()) > 0
            assert ex.source_ref is not None and len(ex.source_ref.strip()) > 0
            # Explicit translation provenance required: cannot be unstated
            assert ex.translation_provenance is not None and len(ex.translation_provenance.strip()) > 0


# =============================================================================
# Provenance Filtering (verified_only) Tests
# =============================================================================

def test_grammar_records_verified_only():
    """Verify that verified_only filter functions accurately."""
    verified_recs = get_grammar_records(verified_only=True, data_dir="data")
    assert len(verified_recs) >= 6
    for r in verified_recs:
        assert r.verification_status in ["SOURCE_ATTESTED", "VERIFIED"]


# =============================================================================
# Source Reference Lookup Tests
# =============================================================================

def test_get_topic_sources():
    """Verify listing of bibliographic sources providing evidence for a topic."""
    sources = get_topic_sources("pronouns", data_dir="data")
    assert len(sources) >= 1
    source_ids = {s["id"] for s in sources}
    assert "MEI-SRC-000003" in source_ids

    # Unpopulated topic declared source
    class_sources = get_topic_sources("classifiers", data_dir="data")
    assert len(class_sources) >= 1
    assert any(s["id"] == "MEI-SRC-000004" for s in class_sources)

    # Unknown topic returns empty list
    assert get_topic_sources("unknown_domain_xyz", data_dir="data") == []


def test_list_grammar_sources():
    """Verify listing of all sources referenced in grammar records."""
    sources = list_grammar_sources(data_dir="data")
    assert len(sources) >= 3
    source_ids = {s["id"] for s in sources}
    assert {"MEI-SRC-000001", "MEI-SRC-000003", "MEI-SRC-000004"}.issubset(source_ids)


# =============================================================================
# Missing References & Validation Error Tests
# =============================================================================

def test_validation_error_missing_source():
    """MissingSourceError raised when an attested record points to an unknown source."""
    bad_record = {
        "id": "MEI-GRM-0000999",
        "topic": "pronouns",
        "title": "Invalid Source Test",
        "description": "Test description",
        "verification_status": "SOURCE_ATTESTED",
        "source_id": "MEI-SRC-999999",  # Non-existent source
        "citation_locator": "Page 999",
        "examples": [
            {
                "example_id": "MEI-GEX-0000999",
                "meitei": "ꯃꯤ",
                "roman": "mi",
                "english": "person",
                "source_ref": "None",
                "translation_provenance": "Test",
            }
        ],
    }

    known_sources = {"MEI-SRC-000001", "MEI-SRC-000002"}
    with pytest.raises(MissingSourceError):
        validate_grammar_record(bad_record, known_sources=known_sources)


def test_validation_error_invalid_id():
    """GrammarValidationError raised on invalid ID format."""
    bad_record = {
        "id": "BAD-ID-FORMAT",
        "topic": "pronouns",
        "title": "Title",
        "description": "Desc",
        "verification_status": "SOURCE_ATTESTED",
        "source_id": "MEI-SRC-000001",
        "citation_locator": "Page 1",
    }
    with pytest.raises(GrammarValidationError) as exc:
        validate_grammar_record(bad_record)
    assert "invalid 'id'" in str(exc.value)


def test_validation_error_missing_translation_provenance():
    """GrammarValidationError raised if example lacks translation provenance."""
    bad_record = {
        "id": "MEI-GRM-0000998",
        "topic": "pronouns",
        "title": "Missing Provenance Test",
        "description": "Desc",
        "verification_status": "SOURCE_ATTESTED",
        "source_id": "MEI-SRC-000001",
        "citation_locator": "Page 1",
        "examples": [
            {
                "example_id": "MEI-GEX-0000998",
                "meitei": "ꯃꯤ",
                "roman": "mi",
                "english": "person",
                "source_ref": "Page 1",
                "translation_provenance": "",  # Missing!
            }
        ],
    }
    with pytest.raises(GrammarValidationError) as exc:
        validate_grammar_record(bad_record, known_sources={"MEI-SRC-000001"})
    assert "translation_provenance" in str(exc.value)


# =============================================================================
# CLI Subcommand Tests: meitei grammar
# =============================================================================

def test_cli_grammar_overview():
    """Test `meitei grammar` listing all topics."""
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["grammar"])
    assert exit_code == 0
    out = f.getvalue()
    assert "Grammar Subsystem" in out
    assert "pronouns" in out
    assert "[POPULATED]" in out
    assert "classifiers" in out
    assert "[UNPOPULATED]" in out


def test_cli_grammar_topic_populated():
    """Test `meitei grammar --topic pronouns`."""
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["grammar", "--topic", "pronouns"])
    assert exit_code == 0
    out = f.getvalue()
    assert "Topic 'pronouns'" in out
    assert "MEI-GRM-0000001" in out
    assert "Ei chatli." in out
    assert "SOURCE_ATTESTED" in out


def test_cli_grammar_topic_unpopulated():
    """Test `meitei grammar --topic classifiers` reports unpopulated research status."""
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["grammar", "--topic", "classifiers"])
    assert exit_code == 0
    out = f.getvalue()
    assert "unpopulated research category" in out
    assert "Numeral Classifiers" in out


def test_cli_grammar_sources():
    """Test `meitei grammar --sources`."""
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["grammar", "--sources"])
    assert exit_code == 0
    out = f.getvalue()
    assert "Bibliographic Sources" in out
    assert "MEI-SRC-000001" in out
    assert "Pettigrew" in out


def test_cli_grammar_json():
    """Test `meitei grammar --topic pronouns --json`."""
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["grammar", "--topic", "pronouns", "--json"])
    assert exit_code == 0
    data = json.loads(f.getvalue())
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == "MEI-GRM-0000001"
    assert data[0]["examples"][0]["roman"] == "Ei chatli."


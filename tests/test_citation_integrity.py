# -*- coding: utf-8 -*-
"""
Tests for bibliographic citation integrity and provenance verification.

Verifies:
1. All cataloged sources in data/sources/sources.jsonl have authentic metadata,
   valid ID formats (MEI-SRC-xxxxxx), and legal access status.
2. Every SOURCE_ATTESTED record in data/lexicon/core_lexicon.jsonl links to a
   real cataloged source with a non-empty, exact citation locator.
3. Every citation locator provides a verifiable page, folio, or example.
4. Variants and glosses referencing sources maintain referential integrity.
5. Quarantine separation: unverified claims are isolated in candidate_lexicon.jsonl.
"""

from pathlib import Path
import pytest

from meitei.loader import DataLoader
from meitei.schema import (
    RecordStatus,
    is_valid_gls_id,
    is_valid_lex_id,
    is_valid_src_id,
    is_valid_var_id,
)


@pytest.fixture(scope="module")
def data_registry():
    """Load all datasets via DataLoader."""
    loader = DataLoader("data")
    sources = loader.load_sources()
    known_sources = set(sources.keys())
    core_lexicon = loader.load_lexicon(partition="core", known_sources=known_sources)
    candidate_lexicon = loader.load_lexicon(partition="candidate", known_sources=known_sources)
    all_entries = set(core_lexicon.keys()) | set(candidate_lexicon.keys())
    variants = loader.load_variants(known_entries=all_entries, known_sources=known_sources)
    glosses = loader.load_glosses(known_entries=all_entries, known_sources=known_sources)

    return {
        "loader": loader,
        "sources": sources,
        "core_lexicon": core_lexicon,
        "candidate_lexicon": candidate_lexicon,
        "variants": variants,
        "glosses": glosses,
    }


def test_sources_catalog_validity(data_registry):
    sources = data_registry["sources"]
    assert len(sources) >= 7, "Expected at least 7 verified bibliographic sources"

    for sid, s in sources.items():
        assert is_valid_src_id(sid), f"Invalid source ID format: {sid}"
        assert len(s["title"].strip()) > 0, f"Source {sid} missing title"
        assert s["source_type"] in [
            "puya", "chronicle", "dictionary", "fieldwork", "corpus", "academic_paper", "other"
        ]
        meta = s.get("metadata", {})
        assert "legal_status" in meta, f"Source {sid} must record legal/access rights status"


def test_core_lexicon_citation_integrity(data_registry):
    core = data_registry["core_lexicon"]
    sources = data_registry["sources"]

    assert len(core) >= 10, "Expected at least 10 source-attested core entries"

    for eid, entry in core.items():
        assert is_valid_lex_id(eid), f"Invalid entry ID: {eid}"
        assert entry["status"] in ["SOURCE_ATTESTED", "VERIFIED"]

        if entry["status"] == "SOURCE_ATTESTED":
            # 1. Real source ID check
            src_id = entry.get("source_id")
            assert src_id is not None, f"SOURCE_ATTESTED entry {eid} missing source_id"
            assert src_id in sources, f"Entry {eid} references unknown source: {src_id}"

            # 2. Exact citation locator check
            locator = entry.get("citation_locator")
            assert locator is not None and len(locator.strip()) > 0, (
                f"Entry {eid} missing exact citation locator"
            )
            # Must mention page, folio, or example
            assert any(term in locator.lower() for term in ["page", "folio", "example", "no.", "chapter"]), (
                f"Entry {eid} locator '{locator}' does not contain an exact page, folio, or example citation"
            )

            # 3. Reviewer attribution check
            rev = entry.get("reviewer_attribution")
            assert rev is not None, f"Entry {eid} missing reviewer_attribution"
            assert len(rev.get("reviewer_id", "").strip()) > 0
            assert len(rev.get("review_date", "").strip()) > 0


def test_variants_citation_integrity(data_registry):
    variants = data_registry["variants"]
    sources = data_registry["sources"]
    core = data_registry["core_lexicon"]

    assert len(variants) >= 4, "Expected at least 4 verified historical variants"

    for var in variants:
        vid = var["id"]
        assert is_valid_var_id(vid)
        eid = var["entry_id"]
        assert eid in core, f"Variant {vid} references non-existent entry {eid}"

        src_id = var.get("source_id")
        if src_id:
            assert src_id in sources, f"Variant {vid} references unknown source {src_id}"
            locator = var.get("citation_locator")
            assert locator and len(locator.strip()) > 0


def test_glosses_citation_integrity(data_registry):
    glosses = data_registry["glosses"]
    sources = data_registry["sources"]
    core = data_registry["core_lexicon"]

    assert len(glosses) >= 7, "Expected at least 7 verified translation glosses"

    for gls in glosses:
        gid = gls["id"]
        assert is_valid_gls_id(gid)
        eid = gls["entry_id"]
        assert eid in core, f"Gloss {gid} references non-existent entry {eid}"

        src_id = gls.get("source_id")
        if src_id:
            assert src_id in sources, f"Gloss {gid} references unknown source {src_id}"
            locator = gls.get("citation_locator")
            assert locator and len(locator.strip()) > 0


def test_candidate_lexicon_isolation(data_registry):
    candidate = data_registry["candidate_lexicon"]
    core = data_registry["core_lexicon"]

    # No ID overlap
    overlap = set(candidate.keys()) & set(core.keys())
    assert len(overlap) == 0, f"ID collision between core and candidate: {overlap}"

    for cid, centry in candidate.items():
        assert centry["status"] != "SOURCE_ATTESTED", (
            f"Candidate entry {cid} cannot have SOURCE_ATTESTED status in candidate partition"
        )
        if centry["status"] == "UNVERIFIED":
            rev = centry.get("reviewer_attribution")
            assert rev is not None
            assert "LIMITATION" in rev.get("notes", ""), (
                f"Unverified candidate entry {cid} must document its research limitation in reviewer notes"
            )


# -*- coding: utf-8 -*-
"""Unit tests for meitei.database."""

import tempfile
from pathlib import Path
import pytest

from meitei.database import MeiteiDatabase
from meitei.models import (
    BibliographicSource,
    Entry,
    ExampleSentence,
    PartOfSpeech,
    ProvenanceRecord,
    Sense,
    VerificationStatus,
)


@pytest.fixture
def memory_db():
    """Create a fresh in-memory Meitei database."""
    db = MeiteiDatabase(":memory:")
    yield db
    db.close()


@pytest.fixture
def sample_source():
    return BibliographicSource(
        source_id="src_cheitharol",
        title="Cheitharol Kumbaba",
        author="Court Chroniclers of Kangleipak",
        year=1891,
        source_type="chronicle",
        description="The royal chronicle of the kings of Manipur.",
    )


@pytest.fixture
def sample_entry():
    sense1 = Sense(
        sense_id="sense_leibak_01",
        definition_en="Country, motherland, realm, kingdom",
        definition_mni="ꯂꯩꯕꯥꯛ",
        part_of_speech=PartOfSpeech.NOUN,
        domain="governance",
        examples=[
            ExampleSentence(
                meitei="ꯁꯅꯥ ꯂꯩꯕꯥꯛ ꯃꯅꯤꯄꯨꯔ꯫",
                roman="Sana Leibak Manipur.",
                english="Golden Land Manipur.",
            )
        ],
    )
    prov1 = ProvenanceRecord(
        provenance_id="prov_leibak_01",
        source_id="src_cheitharol",
        attestation_type="historical_attestation",
        attestation_reference="Chapter 1, Folio 2",
        verification_status=VerificationStatus.BOTH,
        verified_by="Linguist-Reviewer-01",
    )
    return Entry(
        entry_id="entry_leibak_001",
        headword_meitei="ꯂꯩꯕꯥꯛ",
        headword_roman="leibak",
        headword_bengali="লৈবাক",
        phonetic_ipa="ləibak",
        senses=[sense1],
        provenance=[prov1],
        variants=["leipāk"],
    )


def test_schema_and_empty_stats(memory_db):
    stats = memory_db.get_stats()
    assert stats["entries_count"] == 0
    assert stats["senses_count"] == 0
    assert stats["sources_count"] == 0
    assert stats["provenance_count"] == 0
    assert stats["verification_breakdown"] == {}


def test_sources_crud(memory_db, sample_source):
    # Upsert
    memory_db.upsert_source(sample_source)
    assert memory_db.count_sources() == 1

    # Get
    src = memory_db.get_source("src_cheitharol")
    assert src is not None
    assert src.title == "Cheitharol Kumbaba"
    assert src.year == 1891

    # List
    all_sources = memory_db.list_sources()
    assert len(all_sources) == 1
    assert all_sources[0].source_id == "src_cheitharol"

    # Get non-existent
    assert memory_db.get_source("non_existent") is None


def test_entries_crud_and_lookup(memory_db, sample_source, sample_entry):
    memory_db.upsert_source(sample_source)
    memory_db.upsert_entry(sample_entry)

    assert memory_db.count_entries() == 1
    assert memory_db.count_senses() == 1
    assert memory_db.count_provenance() == 1

    # Exact ID retrieval
    e = memory_db.get_entry("entry_leibak_001")
    assert e is not None
    assert e.headword_meitei == "ꯂꯩꯕꯥꯛ"
    assert e.headword_roman == "leibak"
    assert len(e.senses) == 1
    assert len(e.provenance) == 1
    assert e.get_verification_status() == VerificationStatus.BOTH

    # Lookup by Meitei Mayek
    by_mayek = memory_db.lookup_headword("ꯂꯩꯕꯥꯛ")
    assert len(by_mayek) == 1
    assert by_mayek[0].entry_id == "entry_leibak_001"

    # Lookup by Roman
    by_roman = memory_db.lookup_headword("leibak")
    assert len(by_roman) == 1

    # Lookup by Bengali
    by_bengali = memory_db.lookup_headword("লৈবাক")
    assert len(by_bengali) == 1

    # Search across definitions
    results = memory_db.search_entries("motherland")
    assert len(results) == 1
    assert results[0].entry_id == "entry_leibak_001"

    # Search across Mayek
    results_m = memory_db.search_entries("ꯂꯩꯕꯥꯛ")
    assert len(results_m) == 1

    # Verification breakdown
    stats = memory_db.get_stats()
    assert stats["verification_breakdown"]["both"] == 1


def test_delete_entry_cascading(memory_db, sample_source, sample_entry):
    memory_db.upsert_source(sample_source)
    memory_db.upsert_entry(sample_entry)

    assert memory_db.count_entries() == 1
    assert memory_db.count_senses() == 1
    assert memory_db.count_provenance() == 1

    # Delete
    deleted = memory_db.delete_entry("entry_leibak_001")
    assert deleted is True

    # Check cascading delete
    assert memory_db.count_entries() == 0
    assert memory_db.count_senses() == 0
    assert memory_db.count_provenance() == 0


def test_jsonl_export_and_import_roundtrip(memory_db, sample_source, sample_entry, tmp_path):
    memory_db.upsert_source(sample_source)
    memory_db.upsert_entry(sample_entry)

    entries_jsonl = tmp_path / "test_entries.jsonl"
    sources_jsonl = tmp_path / "test_sources.jsonl"

    # Export
    exported_entries_cnt = memory_db.export_entries_to_jsonl(entries_jsonl)
    assert exported_entries_cnt == 1
    assert entries_jsonl.exists()

    exported_sources_cnt = memory_db.export_sources_to_jsonl(sources_jsonl)
    assert exported_sources_cnt == 1
    assert sources_jsonl.exists()

    # Re-import into a separate brand new database
    db2_file = tmp_path / "reimported.sqlite3"
    with MeiteiDatabase(db2_file) as db2:
        # Import sources first (foreign key integrity)
        s_cnt = db2.import_sources_from_jsonl(sources_jsonl)
        assert s_cnt == 1

        # Import entries
        e_cnt = db2.import_entries_from_jsonl(entries_jsonl)
        assert e_cnt == 1

        re_entry = db2.get_entry("entry_leibak_001")
        assert re_entry is not None
        assert re_entry.headword_meitei == "ꯂꯩꯕꯥꯛ"
        assert re_entry.senses[0].definition_en == "Country, motherland, realm, kingdom"
        assert re_entry.provenance[0].verification_status == VerificationStatus.BOTH
        assert re_entry.senses[0].examples[0].meitei == "ꯁꯅꯥ ꯂꯩꯕꯥꯛ ꯃꯅꯤꯄꯨꯔ꯫"


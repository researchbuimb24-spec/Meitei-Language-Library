# -*- coding: utf-8 -*-
"""
Unit tests for the structured data layer, JSONL loaders, and schema validation.
"""

from pathlib import Path
import pytest

from meitei.loader import (
    CitationLocatorMissingError,
    DataLoader,
    DatasetPartitionError,
    DuplicateIDError,
    InvalidStatusError,
    MalformedJSONLError,
    MissingSourceError,
    ValidationError,
)
from meitei.schema import (
    ALL_ALLOWED_STATUSES,
    CANDIDATE_ALLOWED_STATUSES,
    CORE_ALLOWED_STATUSES,
    RecordStatus,
    is_valid_gls_id,
    is_valid_lex_id,
    is_valid_sns_id,
    is_valid_src_id,
    is_valid_var_id,
)


def test_stable_id_validators():
    assert is_valid_src_id("MEI-SRC-000001") is True
    assert is_valid_src_id("MEI-SRC-123456") is True
    assert is_valid_src_id("MEI-SRC-123") is False
    assert is_valid_src_id("SRC-000001") is False

    assert is_valid_lex_id("MEI-LEX-0000001") is True
    assert is_valid_lex_id("MEI-LEX-1234567") is True
    assert is_valid_lex_id("MEI-LEX-0001") is False

    assert is_valid_sns_id("MEI-SNS-0000001") is True
    assert is_valid_sns_id("MEI-LEX-0000001-S01") is True
    assert is_valid_sns_id("INVALID-SNS") is False

    assert is_valid_var_id("MEI-VAR-0000001") is True
    assert is_valid_var_id("MEI-VAR-123") is False

    assert is_valid_gls_id("MEI-GLS-0000001") is True
    assert is_valid_gls_id("MEI-GLS-123") is False


def test_status_sets_and_enums():
    assert RecordStatus.SOURCE_ATTESTED.value == "SOURCE_ATTESTED"
    assert RecordStatus.VERIFIED.value == "VERIFIED"
    assert RecordStatus.COMMUNITY_SUBMITTED.value == "COMMUNITY_SUBMITTED"
    assert RecordStatus.UNVERIFIED.value == "UNVERIFIED"
    assert RecordStatus.AI_CANDIDATE.value == "AI_CANDIDATE"
    assert RecordStatus.CITATION_MISMATCH.value == "CITATION_MISMATCH"
    assert RecordStatus.REJECTED.value == "REJECTED"

    assert len(ALL_ALLOWED_STATUSES) == 7
    assert CORE_ALLOWED_STATUSES == {"SOURCE_ATTESTED", "VERIFIED"}
    assert "AI_CANDIDATE" in CANDIDATE_ALLOWED_STATUSES


def test_repository_datasets_validate_cleanly():
    """Verify that the authentic verified datasets in data/ validate with 0 errors."""
    loader = DataLoader("data")
    report = loader.validate_all()
    assert report["status"] == "VALID"
    assert report["sources_count"] == 7
    assert report["core_entries_count"] == 10
    assert report["candidate_entries_count"] == 1
    assert report["variants_count"] == 4
    assert report["glosses_count"] == 7


def test_empty_datasets_validate_cleanly(tmp_path):
    """Verify that an empty repository structure validates with 0 errors."""
    (tmp_path / "sources").mkdir()
    (tmp_path / "lexicon").mkdir()
    (tmp_path / "translations").mkdir()
    (tmp_path / "sources" / "sources.jsonl").write_text("", encoding="utf-8")
    (tmp_path / "lexicon" / "core_lexicon.jsonl").write_text("", encoding="utf-8")
    (tmp_path / "lexicon" / "candidate_lexicon.jsonl").write_text("", encoding="utf-8")
    (tmp_path / "lexicon" / "variants.jsonl").write_text("", encoding="utf-8")
    (tmp_path / "translations" / "glosses.jsonl").write_text("", encoding="utf-8")

    loader = DataLoader(tmp_path)
    report = loader.validate_all()
    assert report["status"] == "VALID"
    assert report["sources_count"] == 0
    assert report["core_entries_count"] == 0


def test_valid_datasets_roundtrip(tmp_path):
    """Test full dataset loading with valid sources, entries, variants, and glosses."""
    sources_p = tmp_path / "sources.jsonl"
    core_p = tmp_path / "core.jsonl"
    candidate_p = tmp_path / "candidate.jsonl"
    variants_p = tmp_path / "variants.jsonl"
    glosses_p = tmp_path / "glosses.jsonl"

    # 1. Valid source
    sources_p.write_text(
        '{"id": "MEI-SRC-000001", "title": "Cheitharol Kumbaba", "source_type": "chronicle", "year": 1891}\n',
        encoding="utf-8"
    )

    # 2. Valid core entry (SOURCE_ATTESTED with source_id and citation locator)
    core_p.write_text(
        '{"id": "MEI-LEX-0000001", "headword_meitei": "ꯃꯤ", "headword_roman": "mi", '
        '"status": "SOURCE_ATTESTED", "source_id": "MEI-SRC-000001", "citation_locator": "Folio 2a", '
        '"reviewer_attribution": {"reviewer_id": "REV-01", "review_date": "2026-10-29"}, '
        '"senses": [{"id": "MEI-SNS-0000001", "definition_en": "Person, human", "part_of_speech": "noun"}]}\n',
        encoding="utf-8"
    )

    # 3. Valid candidate entry (AI_CANDIDATE)
    candidate_p.write_text(
        '{"id": "MEI-LEX-0000002", "headword_meitei": "ꯅꯣꯡ", "headword_roman": "nong", '
        '"status": "AI_CANDIDATE", '
        '"senses": [{"id": "MEI-SNS-0000002", "definition_en": "Rain", "part_of_speech": "noun"}]}\n',
        encoding="utf-8"
    )

    # 4. Valid variant
    variants_p.write_text(
        '{"id": "MEI-VAR-0000001", "entry_id": "MEI-LEX-0000001", "variant_form": "মী", '
        '"script": "bengali", "variant_type": "historical_spelling", "status": "VERIFIED"}\n',
        encoding="utf-8"
    )

    # 5. Valid gloss
    glosses_p.write_text(
        '{"id": "MEI-GLS-0000001", "entry_id": "MEI-LEX-0000001", "target_language": "en", '
        '"gloss": "human being", "status": "VERIFIED"}\n',
        encoding="utf-8"
    )

    loader = DataLoader(tmp_path)
    sources = loader.load_sources(sources_p)
    assert len(sources) == 1
    assert "MEI-SRC-000001" in sources

    core = loader.load_lexicon(core_p, partition="core", known_sources=set(sources.keys()))
    assert len(core) == 1

    candidate = loader.load_lexicon(candidate_p, partition="candidate", known_sources=set(sources.keys()))
    assert len(candidate) == 1

    all_entries = set(core.keys()) | set(candidate.keys())
    variants = loader.load_variants(variants_p, known_entries=all_entries, known_sources=set(sources.keys()))
    assert len(variants) == 1

    glosses = loader.load_glosses(glosses_p, known_entries=all_entries, known_sources=set(sources.keys()))
    assert len(glosses) == 1


def test_malformed_jsonl_raises_error(tmp_path):
    bad_file = tmp_path / "bad.jsonl"
    bad_file.write_text(
        '{"id": "MEI-SRC-000001", "title": "Good", "source_type": "puya"}\n'
        '{"id": "MEI-SRC-000002", "title": BROKEN JSON\n',
        encoding="utf-8"
    )
    loader = DataLoader(tmp_path)
    with pytest.raises(MalformedJSONLError) as exc_info:
        loader.load_sources(bad_file)
    assert "bad.jsonl:2" in str(exc_info.value)


def test_duplicate_source_id_raises_error(tmp_path):
    dup_file = tmp_path / "sources.jsonl"
    dup_file.write_text(
        '{"id": "MEI-SRC-000001", "title": "Source 1", "source_type": "puya"}\n'
        '{"id": "MEI-SRC-000001", "title": "Source Duplicate", "source_type": "puya"}\n',
        encoding="utf-8"
    )
    loader = DataLoader(tmp_path)
    with pytest.raises(DuplicateIDError) as exc_info:
        loader.load_sources(dup_file)
    assert "MEI-SRC-000001" in str(exc_info.value)


def test_duplicate_lexical_entry_id_raises_error(tmp_path):
    dup_file = tmp_path / "core.jsonl"
    dup_file.write_text(
        '{"id": "MEI-LEX-0000001", "headword_meitei": "ꯃꯤ", "headword_roman": "mi", "status": "VERIFIED", "senses": [{"id": "MEI-SNS-0000001", "definition_en": "person", "part_of_speech": "noun"}]}\n'
        '{"id": "MEI-LEX-0000001", "headword_meitei": "ꯃꯤ", "headword_roman": "mi", "status": "VERIFIED", "senses": [{"id": "MEI-SNS-0000002", "definition_en": "human", "part_of_speech": "noun"}]}\n',
        encoding="utf-8"
    )
    loader = DataLoader(tmp_path)
    with pytest.raises(DuplicateIDError) as exc_info:
        loader.load_lexicon(dup_file, partition="core")
    assert "MEI-LEX-0000001" in str(exc_info.value)


def test_missing_source_reference_raises_error(tmp_path):
    entry_file = tmp_path / "core.jsonl"
    entry_file.write_text(
        '{"id": "MEI-LEX-0000001", "headword_meitei": "ꯃꯤ", "headword_roman": "mi", '
        '"status": "SOURCE_ATTESTED", "source_id": "MEI-SRC-999999", "citation_locator": "Page 10", '
        '"senses": [{"id": "MEI-SNS-0000001", "definition_en": "person", "part_of_speech": "noun"}]}\n',
        encoding="utf-8"
    )
    loader = DataLoader(tmp_path)
    # known_sources only has MEI-SRC-000001
    with pytest.raises(MissingSourceError) as exc_info:
        loader.load_lexicon(entry_file, partition="core", known_sources={"MEI-SRC-000001"})
    assert "MEI-SRC-999999" in str(exc_info.value)


def test_source_attested_missing_citation_locator_raises_error(tmp_path):
    entry_file = tmp_path / "core.jsonl"
    entry_file.write_text(
        '{"id": "MEI-LEX-0000001", "headword_meitei": "ꯃꯤ", "headword_roman": "mi", '
        '"status": "SOURCE_ATTESTED", "source_id": "MEI-SRC-000001", '
        '"senses": [{"id": "MEI-SNS-0000001", "definition_en": "person", "part_of_speech": "noun"}]}\n',
        encoding="utf-8"
    )
    loader = DataLoader(tmp_path)
    with pytest.raises(CitationLocatorMissingError) as exc_info:
        loader.load_lexicon(entry_file, partition="core", known_sources={"MEI-SRC-000001"})
    assert "citation_locator" in str(exc_info.value)


def test_invalid_status_raises_error(tmp_path):
    entry_file = tmp_path / "core.jsonl"
    entry_file.write_text(
        '{"id": "MEI-LEX-0000001", "headword_meitei": "ꯃꯤ", "headword_roman": "mi", '
        '"status": "FABRICATED_STATUS", '
        '"senses": [{"id": "MEI-SNS-0000001", "definition_en": "person", "part_of_speech": "noun"}]}\n',
        encoding="utf-8"
    )
    loader = DataLoader(tmp_path)
    with pytest.raises(InvalidStatusError) as exc_info:
        loader.load_lexicon(entry_file, partition="core")
    assert "FABRICATED_STATUS" in str(exc_info.value)


def test_dataset_partition_enforcement(tmp_path):
    # 1. AI_CANDIDATE placed inside core_lexicon -> Partition Error
    core_bad = tmp_path / "core_bad.jsonl"
    core_bad.write_text(
        '{"id": "MEI-LEX-0000001", "headword_meitei": "ꯃꯤ", "headword_roman": "mi", '
        '"status": "AI_CANDIDATE", '
        '"senses": [{"id": "MEI-SNS-0000001", "definition_en": "person", "part_of_speech": "noun"}]}\n',
        encoding="utf-8"
    )
    loader = DataLoader(tmp_path)
    with pytest.raises(DatasetPartitionError) as exc_info:
        loader.load_lexicon(core_bad, partition="core")
    assert "core_lexicon" in str(exc_info.value)

    # 2. SOURCE_ATTESTED placed inside candidate_lexicon -> Partition Error
    cand_bad = tmp_path / "cand_bad.jsonl"
    cand_bad.write_text(
        '{"id": "MEI-LEX-0000002", "headword_meitei": "ꯅꯣꯡ", "headword_roman": "nong", '
        '"status": "SOURCE_ATTESTED", "source_id": "MEI-SRC-000001", "citation_locator": "Page 5", '
        '"senses": [{"id": "MEI-SNS-0000002", "definition_en": "rain", "part_of_speech": "noun"}]}\n',
        encoding="utf-8"
    )
    with pytest.raises(DatasetPartitionError) as exc_info:
        loader.load_lexicon(cand_bad, partition="candidate", known_sources={"MEI-SRC-000001"})
    assert "candidate_lexicon" in str(exc_info.value)


def test_variant_referencing_unknown_entry_raises_error(tmp_path):
    var_file = tmp_path / "variants.jsonl"
    var_file.write_text(
        '{"id": "MEI-VAR-0000001", "entry_id": "MEI-LEX-9999999", "variant_form": "মী", '
        '"script": "bengali", "status": "VERIFIED"}\n',
        encoding="utf-8"
    )
    loader = DataLoader(tmp_path)
    with pytest.raises(ValidationError) as exc_info:
        loader.load_variants(var_file, known_entries={"MEI-LEX-0000001"})
    assert "MEI-LEX-9999999" in str(exc_info.value)


def test_cli_validate_data_command():
    from meitei import cli
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["validate-data", "--data-dir", "data"])
    assert exit_code == 0
    out = f.getvalue()
    assert "DATASET SCHEMA & INTEGRITY VALIDATION: PASSED" in out

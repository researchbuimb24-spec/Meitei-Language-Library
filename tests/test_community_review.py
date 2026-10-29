# -*- coding: utf-8 -*-
"""
Unit and integration tests for Community Review, Provenance Audit,
and Dataset Validation in the Meitei Language Library (meitei).
"""

import io
import json
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import pytest

import meitei
from meitei import (
    AuditReport,
    ProvenanceAuditor,
    ReviewDecision,
    ReviewLedger,
    ReviewRecord,
    ReviewValidationError,
    ReviewerRole,
    audit_repository,
    get_review_statistics,
    get_reviews_for_target,
    load_reviews,
    validate_review_record,
)
from meitei import cli
from meitei.loader import DuplicateIDError


# =============================================================================
# 1. Review Data Models and Enum Tests
# =============================================================================

def test_review_decision_enums():
    assert ReviewDecision.ACCEPTED == "ACCEPTED"
    assert ReviewDecision.CORRECTED == "CORRECTED"
    assert ReviewDecision.REJECTED == "REJECTED"
    assert ReviewDecision.AWAITING_REVIEW == "AWAITING_REVIEW"


def test_reviewer_role_enums():
    assert ReviewerRole.NATIVE_SPEAKER == "NATIVE_SPEAKER"
    assert ReviewerRole.LINGUIST == "LINGUIST"
    assert ReviewerRole.CULTURAL_AUTHORITY == "CULTURAL_AUTHORITY"
    assert ReviewerRole.COMMUNITY_ELDER == "COMMUNITY_ELDER"
    assert ReviewerRole.ACADEMIC_EDITOR == "ACADEMIC_EDITOR"
    assert ReviewerRole.CONTRIBUTOR == "CONTRIBUTOR"


def test_review_record_construction_and_serialization():
    rec = ReviewRecord(
        id="MEI-REV-0000099",
        target_id="MEI-LEX-0000001",
        target_type="lexical_entry",
        decision=ReviewDecision.ACCEPTED,
        reviewer_role=ReviewerRole.NATIVE_SPEAKER,
        reviewer_id="REV-TEST-01",
        review_date="2026-10-29",
        source_id="MEI-SRC-000004",
        source_locator="Page 253",
        previous_value=None,
        corrected_value=None,
        revision_history=[{"date": "2026-10-29", "reviewer_id": "REV-TEST-01", "comment": "Verified"}],
        rationale="Standard vernacular word.",
        cultural_sensitivity_checked=True,
        consent_confirmed=True,
        license="CC BY-SA 4.0",
    )
    assert rec.decision == "ACCEPTED"
    assert rec.reviewer_role == "NATIVE_SPEAKER"

    d = rec.to_dict()
    assert d["id"] == "MEI-REV-0000099"
    assert d["decision"] == "ACCEPTED"

    rebuilt = ReviewRecord.from_dict(d)
    assert rebuilt.id == rec.id
    assert rebuilt.target_id == rec.target_id


# =============================================================================
# 2. Review Record Validation Rules
# =============================================================================

def test_validate_review_record_success():
    valid_data = {
        "id": "MEI-REV-0000001",
        "target_id": "MEI-LEX-0000001",
        "target_type": "lexical_entry",
        "decision": "ACCEPTED",
        "reviewer_role": "NATIVE_SPEAKER",
        "reviewer_id": "REV-01",
        "review_date": "2026-10-29",
        "cultural_sensitivity_checked": True,
        "consent_confirmed": True,
    }
    seen = set()
    validate_review_record(valid_data, seen_ids=seen)
    assert "MEI-REV-0000001" in seen


def test_validate_review_record_duplicate_id():
    valid_data = {
        "id": "MEI-REV-0000001",
        "target_id": "MEI-LEX-0000001",
        "target_type": "lexical_entry",
        "decision": "ACCEPTED",
        "reviewer_role": "NATIVE_SPEAKER",
        "reviewer_id": "REV-01",
        "review_date": "2026-10-29",
        "cultural_sensitivity_checked": True,
        "consent_confirmed": True,
    }
    seen = {"MEI-REV-0000001"}
    with pytest.raises(DuplicateIDError):
        validate_review_record(valid_data, seen_ids=seen)


def test_validate_review_record_invalid_id():
    bad_id = {
        "id": "BAD-ID-123",
        "target_id": "MEI-LEX-0000001",
        "target_type": "lexical_entry",
        "decision": "ACCEPTED",
        "reviewer_role": "NATIVE_SPEAKER",
        "reviewer_id": "REV-01",
        "review_date": "2026-10-29",
    }
    with pytest.raises(ReviewValidationError, match="Must match MEI-REV-xxxxxxx"):
        validate_review_record(bad_id)


def test_validate_review_record_invalid_decision():
    bad_dec = {
        "id": "MEI-REV-0000001",
        "target_id": "MEI-LEX-0000001",
        "target_type": "lexical_entry",
        "decision": "UNRECOGNIZED_STATUS",
        "reviewer_role": "NATIVE_SPEAKER",
        "reviewer_id": "REV-01",
        "review_date": "2026-10-29",
    }
    with pytest.raises(ReviewValidationError, match="invalid 'decision'"):
        validate_review_record(bad_dec)


def test_validate_review_record_invalid_role():
    bad_role = {
        "id": "MEI-REV-0000001",
        "target_id": "MEI-LEX-0000001",
        "target_type": "lexical_entry",
        "decision": "ACCEPTED",
        "reviewer_role": "NOT_A_ROLE",
        "reviewer_id": "REV-01",
        "review_date": "2026-10-29",
    }
    with pytest.raises(ReviewValidationError, match="invalid 'reviewer_role'"):
        validate_review_record(bad_role)


def test_validate_review_record_corrected_requires_value():
    rec = {
        "id": "MEI-REV-0000001",
        "target_id": "MEI-LEX-0000001",
        "target_type": "lexical_entry",
        "decision": "CORRECTED",
        "reviewer_role": "LINGUIST",
        "reviewer_id": "REV-01",
        "review_date": "2026-10-29",
        "corrected_value": None,
        "cultural_sensitivity_checked": True,
        "consent_confirmed": True,
    }
    with pytest.raises(ReviewValidationError, match="decision 'CORRECTED' but lacks 'corrected_value'"):
        validate_review_record(rec)


def test_validate_review_record_ethical_consent_check():
    rec = {
        "id": "MEI-REV-0000001",
        "target_id": "MEI-LEX-0000001",
        "target_type": "lexical_entry",
        "decision": "ACCEPTED",
        "reviewer_role": "NATIVE_SPEAKER",
        "reviewer_id": "REV-01",
        "review_date": "2026-10-29",
        "consent_confirmed": False,
    }
    with pytest.raises(ReviewValidationError, match="consent_confirmed must be True"):
        validate_review_record(rec)


def test_validate_review_record_cultural_sensitivity_check():
    rec = {
        "id": "MEI-REV-0000001",
        "target_id": "MEI-LEX-0000001",
        "target_type": "lexical_entry",
        "decision": "ACCEPTED",
        "reviewer_role": "NATIVE_SPEAKER",
        "reviewer_id": "REV-01",
        "review_date": "2026-10-29",
        "cultural_sensitivity_checked": False,
    }
    with pytest.raises(ReviewValidationError, match="cultural_sensitivity_checked must be True"):
        validate_review_record(rec)


# =============================================================================
# 3. Review Ledger Operations & Repo Data Integrity
# =============================================================================

def test_load_repository_reviews():
    reviews = load_reviews()
    assert len(reviews) >= 6

    # Verify presence of all core decisions
    decisions = {r.decision for r in reviews}
    assert "ACCEPTED" in decisions
    assert "CORRECTED" in decisions
    assert "REJECTED" in decisions
    assert "AWAITING_REVIEW" in decisions

    # Check target retrieval
    lex1_reviews = get_reviews_for_target("MEI-LEX-0000001")
    assert len(lex1_reviews) >= 1
    assert lex1_reviews[0].decision == "ACCEPTED"


def test_review_statistics_calculation():
    stats = get_review_statistics()
    assert stats["total_reviews"] >= 6
    assert stats["awaiting_review_count"] >= 1
    assert "ACCEPTED" in stats["decisions"]
    assert "NATIVE_SPEAKER" in stats["roles"]


def test_review_save_and_reload(tmp_path):
    ledger = ReviewLedger(data_dir=tmp_path)
    rec = ReviewRecord(
        id="MEI-REV-0000001",
        target_id="MEI-LEX-0000001",
        target_type="lexical_entry",
        decision=ReviewDecision.ACCEPTED,
        reviewer_role=ReviewerRole.NATIVE_SPEAKER,
        reviewer_id="REV-TEST",
        review_date="2026-10-29",
        cultural_sensitivity_checked=True,
        consent_confirmed=True,
    )
    ledger.save_review_record(rec)

    reloaded = ledger.load_reviews()
    assert len(reloaded) == 1
    assert reloaded[0].id == "MEI-REV-0000001"


# =============================================================================
# 4. Provenance Auditor & Dataset Validation Tests
# =============================================================================

def test_audit_repository_passes_on_clean_data():
    report = audit_repository()
    assert report.is_valid is True
    assert report.status == "PASSED"
    assert report.core_entries_count >= 10
    assert report.sources_count >= 7
    assert report.reviews_count >= 6
    assert report.errors == []


def test_audit_repository_strict_passes_on_clean_data():
    report = audit_repository(strict=True)
    assert report.is_valid is True
    assert report.strict is True
    assert report.status == "PASSED"


def test_audit_repository_fails_unreviewed_triggers_error():
    # Since candidate MEI-LEX-0000011 is UNVERIFIED and review MEI-REV-0000004 is AWAITING_REVIEW,
    # fail_unreviewed must report validation failure and non-zero exit condition.
    report = audit_repository(fail_unreviewed=True)
    assert report.is_valid is False
    assert report.status == "FAILED"
    assert any("AWAITING_REVIEW" in e or "UNVERIFIED" in e for e in report.errors)


def test_audit_detects_unauthorized_promotion_to_core(tmp_path):
    # Set up mock data directory with an unauthorized AI candidate in core
    data_dir = tmp_path / "data"
    (data_dir / "sources").mkdir(parents=True)
    (data_dir / "lexicon").mkdir(parents=True)

    sources_file = data_dir / "sources" / "sources.jsonl"
    sources_file.write_text(
        json.dumps({"id": "MEI-SRC-000001", "title": "Test Source", "source_type": "dictionary"}) + "\n",
        encoding="utf-8"
    )

    core_file = data_dir / "lexicon" / "core_lexicon.jsonl"
    bad_entry = {
        "id": "MEI-LEX-0000001",
        "headword_meitei": "ꯃꯤ",
        "headword_roman": "mi",
        "status": "AI_CANDIDATE",  # NOT PERMITTED IN CORE!
        "source_id": "MEI-SRC-000001",
        "citation_locator": "Page 10",
        "senses": [{"id": "MEI-SNS-0000001", "definition_en": "person", "part_of_speech": "noun"}],
    }
    core_file.write_text(json.dumps(bad_entry) + "\n", encoding="utf-8")

    auditor = ProvenanceAuditor(data_dir=data_dir)
    report = auditor.audit()
    assert report.is_valid is False
    assert any("AI_CANDIDATE" in e and "core_lexicon" in e for e in report.errors)


def test_audit_detects_missing_source_reference(tmp_path):
    data_dir = tmp_path / "data"
    (data_dir / "sources").mkdir(parents=True)
    (data_dir / "lexicon").mkdir(parents=True)

    # Empty sources
    (data_dir / "sources" / "sources.jsonl").write_text("", encoding="utf-8")

    core_file = data_dir / "lexicon" / "core_lexicon.jsonl"
    entry = {
        "id": "MEI-LEX-0000001",
        "headword_meitei": "ꯃꯤ",
        "headword_roman": "mi",
        "status": "SOURCE_ATTESTED",
        "source_id": "MEI-SRC-999999",  # Dangling source reference!
        "citation_locator": "Page 10",
        "senses": [{"id": "MEI-SNS-0000001", "definition_en": "person", "part_of_speech": "noun"}],
    }
    core_file.write_text(json.dumps(entry) + "\n", encoding="utf-8")

    auditor = ProvenanceAuditor(data_dir=data_dir)
    report = auditor.audit()
    assert report.is_valid is False
    assert any("MEI-SRC-999999" in e for e in report.errors)


# =============================================================================
# 5. CLI Execution & Status Tests
# =============================================================================

def test_cli_review_list():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["review", "list"])
    assert exit_code == 0
    out = f.getvalue()
    assert "Community Review Ledger" in out
    assert "MEI-REV-0000001" in out
    assert "ACCEPTED" in out


def test_cli_review_list_with_filter():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["review", "list", "--decision", "accepted"])
    assert exit_code == 0
    out = f.getvalue()
    assert "MEI-REV-0000001" in out


def test_cli_review_info():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["review", "info", "MEI-REV-0000001"])
    assert exit_code == 0
    out = f.getvalue()
    assert "Review Details: MEI-REV-0000001" in out
    assert "Target ID:            MEI-LEX-0000001" in out
    assert "Decision:             ACCEPTED" in out
    assert "Ethical Consent:      Confirmed" in out


def test_cli_review_stats():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["review", "stats", "--json"])
    assert exit_code == 0
    stats = json.loads(f.getvalue())
    assert stats["total_reviews"] >= 6
    assert stats["awaiting_review_count"] >= 1


def test_cli_review_audit():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["review", "audit"])
    assert exit_code == 0
    out = f.getvalue()
    assert "Meitei Review & Provenance Audit: PASSED" in out


def test_cli_review_audit_fail_unreviewed():
    # Calling with --fail-unreviewed triggers a non-zero exit code because of awaiting candidate
    f_err = io.StringIO()
    f_out = io.StringIO()
    with redirect_stdout(f_out), redirect_stderr(f_err):
        exit_code = cli.main(["review", "audit", "--fail-unreviewed"])
    assert exit_code == 1
    err_out = f_err.getvalue()
    assert "AWAITING_REVIEW" in err_out or "UNVERIFIED" in err_out


def test_cli_validate_fail_unreviewed():
    # Calling validate with --fail-unreviewed triggers exit code 1
    f_err = io.StringIO()
    f_out = io.StringIO()
    with redirect_stdout(f_out), redirect_stderr(f_err):
        exit_code = cli.main(["validate", "--fail-unreviewed"])
    assert exit_code == 1
    err_out = f_err.getvalue()
    assert "MEI-LEX-0000011" in err_out

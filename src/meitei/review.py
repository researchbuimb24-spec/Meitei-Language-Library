# -*- coding: utf-8 -*-
"""
Community Review, Verification Pedigree, and Review Ledger Subsystem (`meitei.review`).

Provides data models, ledger storage, and validation for editorial review decisions:
- Review decisions: ACCEPTED, CORRECTED, REJECTED, AWAITING_REVIEW
- Reviewer roles: NATIVE_SPEAKER, LINGUIST, CULTURAL_AUTHORITY, COMMUNITY_ELDER,
  ACADEMIC_EDITOR, CONTRIBUTOR
- Detailed provenance recording: source locators, previous values, corrected values,
  revision history, ethical consent, cultural sensitivity, and data reuse licensing.
- Strict separation between historical source attestation and living native-speaker verification.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from meitei.loader import (
    DuplicateIDError,
    MalformedJSONLError,
    ValidationError,
    get_default_data_dir,
    read_jsonl_lines,
)
from meitei.schema import (
    ReviewDecision,
    ReviewerRole,
    is_valid_rev_id,
    is_valid_src_id,
)


class ReviewValidationError(ValidationError):
    """Raised when a review record violates schema, decision, or citation rules."""
    pass


@dataclass
class ReviewRecord:
    """
    Formal editorial or community review record.

    Attributes:
        id: Stable unique review identifier (e.g. MEI-REV-0000001).
        target_id: Identifier of target entity (e.g. MEI-LEX-0000001, MEI-LEX-0000011).
        target_type: Typology of target ('lexical_entry', 'candidate_entry', 'variant',
            'gloss', 'grammar_record', 'book_passage').
        decision: Review decision (ACCEPTED, CORRECTED, REJECTED, AWAITING_REVIEW).
        reviewer_role: Qualification role of reviewer (NATIVE_SPEAKER, LINGUIST, etc.).
        reviewer_id: Reviewer identifier or pseudonym.
        review_date: ISO 8601 date string.
        source_id: Optional referenced bibliographic source (MEI-SRC-xxxxxx).
        source_locator: Precise citation locator (page, folio, line).
        previous_value: Previous data value or dictionary state prior to review.
        corrected_value: Corrected data value or dictionary state if corrected.
        revision_history: Chronological list of revision entries.
        rationale: Philological or linguistic reasoning for the decision.
        cultural_sensitivity_checked: Confirmation that cultural protocols were met.
        consent_confirmed: Confirmation that speaker/informant consent was granted.
        license: Open data license (e.g. CC BY-SA 4.0).
    """
    id: str
    target_id: str
    target_type: str
    decision: Union[str, ReviewDecision]
    reviewer_role: Union[str, ReviewerRole]
    reviewer_id: str
    review_date: str
    source_id: Optional[str] = None
    source_locator: Optional[str] = None
    previous_value: Optional[Union[Dict[str, Any], str]] = None
    corrected_value: Optional[Union[Dict[str, Any], str]] = None
    revision_history: List[Dict[str, str]] = field(default_factory=list)
    rationale: Optional[str] = None
    cultural_sensitivity_checked: bool = True
    consent_confirmed: bool = True
    license: str = "CC BY-SA 4.0"

    def __post_init__(self) -> None:
        if isinstance(self.decision, ReviewDecision):
            self.decision = self.decision.value
        else:
            self.decision = self.decision.upper()

        if isinstance(self.reviewer_role, ReviewerRole):
            self.reviewer_role = self.reviewer_role.value
        else:
            self.reviewer_role = self.reviewer_role.upper()

    def to_dict(self) -> Dict[str, Any]:
        """Convert record to JSON-serializable dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ReviewRecord:
        """Construct ReviewRecord from dictionary."""
        return cls(
            id=data["id"],
            target_id=data["target_id"],
            target_type=data["target_type"],
            decision=data["decision"],
            reviewer_role=data["reviewer_role"],
            reviewer_id=data["reviewer_id"],
            review_date=data["review_date"],
            source_id=data.get("source_id"),
            source_locator=data.get("source_locator"),
            previous_value=data.get("previous_value"),
            corrected_value=data.get("corrected_value"),
            revision_history=data.get("revision_history") or [],
            rationale=data.get("rationale"),
            cultural_sensitivity_checked=data.get("cultural_sensitivity_checked", True),
            consent_confirmed=data.get("consent_confirmed", True),
            license=data.get("license", "CC BY-SA 4.0"),
        )


ALLOWED_DECISIONS: Set[str] = {
    ReviewDecision.ACCEPTED.value,
    ReviewDecision.CORRECTED.value,
    ReviewDecision.REJECTED.value,
    ReviewDecision.AWAITING_REVIEW.value,
}

ALLOWED_ROLES: Set[str] = {
    ReviewerRole.NATIVE_SPEAKER.value,
    ReviewerRole.LINGUIST.value,
    ReviewerRole.CULTURAL_AUTHORITY.value,
    ReviewerRole.COMMUNITY_ELDER.value,
    ReviewerRole.ACADEMIC_EDITOR.value,
    ReviewerRole.CONTRIBUTOR.value,
}

ALLOWED_TARGET_TYPES: Set[str] = {
    "lexical_entry",
    "candidate_entry",
    "variant",
    "gloss",
    "grammar_record",
    "book_passage",
}


def validate_review_record(
    rec: Dict[str, Any],
    file_path: str = "reviews.jsonl",
    line_no: int = 1,
    seen_ids: Optional[Set[str]] = None,
    known_sources: Optional[Set[str]] = None,
) -> None:
    """
    Validate a single review record against schema and review rules.

    Raises ReviewValidationError on any schema, decision, or citation violation.
    """
    if not isinstance(rec, dict):
        raise ReviewValidationError(f"Review at {file_path}:{line_no} must be a JSON object.")

    # 1. Review ID validation
    rev_id = rec.get("id")
    if not rev_id or not isinstance(rev_id, str) or not is_valid_rev_id(rev_id):
        raise ReviewValidationError(
            f"Review record at {file_path}:{line_no} has invalid 'id': '{rev_id}'. "
            f"Must match MEI-REV-xxxxxxx (7 digits)."
        )

    if seen_ids is not None:
        if rev_id in seen_ids:
            raise DuplicateIDError(rev_id, file_path, line_no)
        seen_ids.add(rev_id)

    # 2. Target validation
    target_id = rec.get("target_id")
    if not target_id or not isinstance(target_id, str) or not target_id.strip():
        raise ReviewValidationError(
            f"Review record '{rev_id}' at {file_path}:{line_no} missing non-empty 'target_id'."
        )

    target_type = rec.get("target_type")
    if not target_type or target_type not in ALLOWED_TARGET_TYPES:
        raise ReviewValidationError(
            f"Review record '{rev_id}' at {file_path}:{line_no} invalid 'target_type': '{target_type}'. "
            f"Must be one of {sorted(ALLOWED_TARGET_TYPES)}."
        )

    # 3. Decision validation
    decision_raw = rec.get("decision")
    if not decision_raw or not isinstance(decision_raw, str):
        raise ReviewValidationError(
            f"Review record '{rev_id}' at {file_path}:{line_no} missing 'decision'."
        )
    decision = decision_raw.upper()
    if decision not in ALLOWED_DECISIONS:
        raise ReviewValidationError(
            f"Review record '{rev_id}' at {file_path}:{line_no} invalid 'decision': '{decision_raw}'. "
            f"Must be one of {sorted(ALLOWED_DECISIONS)}."
        )

    # 4. Reviewer role validation
    role_raw = rec.get("reviewer_role")
    if not role_raw or not isinstance(role_raw, str):
        raise ReviewValidationError(
            f"Review record '{rev_id}' at {file_path}:{line_no} missing 'reviewer_role'."
        )
    role = role_raw.upper()
    if role not in ALLOWED_ROLES:
        raise ReviewValidationError(
            f"Review record '{rev_id}' at {file_path}:{line_no} invalid 'reviewer_role': '{role_raw}'. "
            f"Must be one of {sorted(ALLOWED_ROLES)}."
        )

    # 5. Reviewer ID & Date validation
    reviewer_id = rec.get("reviewer_id")
    if not reviewer_id or not isinstance(reviewer_id, str) or not reviewer_id.strip():
        raise ReviewValidationError(
            f"Review record '{rev_id}' at {file_path}:{line_no} missing non-empty 'reviewer_id'."
        )

    review_date = rec.get("review_date")
    if not review_date or not isinstance(review_date, str) or not review_date.strip():
        raise ReviewValidationError(
            f"Review record '{rev_id}' at {file_path}:{line_no} missing non-empty 'review_date'."
        )

    # 6. Source ID validation if provided
    source_id = rec.get("source_id")
    if source_id:
        if not is_valid_src_id(source_id):
            raise ReviewValidationError(
                f"Review record '{rev_id}' at {file_path}:{line_no} references invalid source_id format: '{source_id}'."
            )
        if known_sources is not None and source_id not in known_sources:
            raise ReviewValidationError(
                f"Review record '{rev_id}' references unknown source_id: '{source_id}'."
            )

    # 7. Correction rule: if CORRECTED, must supply corrected_value
    if decision == ReviewDecision.CORRECTED.value:
        corrected_val = rec.get("corrected_value")
        if corrected_val is None:
            raise ReviewValidationError(
                f"Review record '{rev_id}' has decision 'CORRECTED' but lacks 'corrected_value'."
            )

    # 8. Consent & Cultural Sensitivity
    if rec.get("consent_confirmed") is False:
        raise ReviewValidationError(
            f"Review record '{rev_id}' fails validation: consent_confirmed must be True."
        )
    if rec.get("cultural_sensitivity_checked") is False:
        raise ReviewValidationError(
            f"Review record '{rev_id}' fails validation: cultural_sensitivity_checked must be True."
        )


class ReviewLedger:
    """
    Manages loading, filtering, querying, and updating review records.
    """

    def __init__(self, data_dir: Union[str, Path] = "data") -> None:
        self.data_dir = get_default_data_dir(data_dir)
        self.reviews_file = self.data_dir / "reviews" / "reviews.jsonl"

    def load_reviews(self) -> List[ReviewRecord]:
        """Load and validate all review records from the ledger."""
        if not self.reviews_file.exists():
            return []

        records: List[ReviewRecord] = []
        seen_ids: Set[str] = set()

        for line_no, raw_data in read_jsonl_lines(self.reviews_file):
            validate_review_record(raw_data, str(self.reviews_file), line_no, seen_ids)
            records.append(ReviewRecord.from_dict(raw_data))

        return records

    def get_reviews_for_target(self, target_id: str) -> List[ReviewRecord]:
        """Retrieve all review records for a specific target identifier."""
        return [r for r in self.load_reviews() if r.target_id == target_id]

    def get_review_by_id(self, review_id: str) -> Optional[ReviewRecord]:
        """Retrieve a specific review record by its ID."""
        for r in self.load_reviews():
            if r.id == review_id:
                return r
        return None

    def save_review_record(self, record: ReviewRecord) -> None:
        """Append or upsert a review record into the reviews ledger."""
        self.reviews_file.parent.mkdir(parents=True, exist_ok=True)
        existing = self.load_reviews()
        updated = False
        new_list: List[ReviewRecord] = []

        for r in existing:
            if r.id == record.id:
                new_list.append(record)
                updated = True
            else:
                new_list.append(r)

        if not updated:
            new_list.append(record)

        # Write atomically
        tmp_file = self.reviews_file.with_suffix(".tmp")
        with open(tmp_file, "w", encoding="utf-8") as f:
            for r in new_list:
                f.write(json.dumps(r.to_dict(), ensure_ascii=False) + "\n")
        tmp_file.replace(self.reviews_file)

    def get_statistics(self) -> Dict[str, Any]:
        """Compute review decisions breakdown and statistics."""
        reviews = self.load_reviews()
        decisions: Dict[str, int] = {
            ReviewDecision.ACCEPTED.value: 0,
            ReviewDecision.CORRECTED.value: 0,
            ReviewDecision.REJECTED.value: 0,
            ReviewDecision.AWAITING_REVIEW.value: 0,
        }
        roles: Dict[str, int] = {}
        target_types: Dict[str, int] = {}

        for r in reviews:
            dec = r.decision.value if isinstance(r.decision, ReviewDecision) else r.decision.upper()
            decisions[dec] = decisions.get(dec, 0) + 1

            role = r.reviewer_role.value if isinstance(r.reviewer_role, ReviewerRole) else r.reviewer_role.upper()
            roles[role] = roles.get(role, 0) + 1

            tt = r.target_type.lower()
            target_types[tt] = target_types.get(tt, 0) + 1

        return {
            "total_reviews": len(reviews),
            "decisions": decisions,
            "roles": roles,
            "target_types": target_types,
            "awaiting_review_count": decisions.get(ReviewDecision.AWAITING_REVIEW.value, 0),
        }


def load_reviews(data_dir: Union[str, Path] = "data") -> List[ReviewRecord]:
    """Helper to load all review records."""
    return ReviewLedger(data_dir=data_dir).load_reviews()


def get_reviews_for_target(target_id: str, data_dir: Union[str, Path] = "data") -> List[ReviewRecord]:
    """Helper to query reviews for a specific target ID."""
    return ReviewLedger(data_dir=data_dir).get_reviews_for_target(target_id)


def get_review_statistics(data_dir: Union[str, Path] = "data") -> Dict[str, Any]:
    """Helper to get review ledger statistics."""
    return ReviewLedger(data_dir=data_dir).get_statistics()


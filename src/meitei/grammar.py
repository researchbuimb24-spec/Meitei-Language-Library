# -*- coding: utf-8 -*-
"""
Evidence-Backed Grammar Reference Subsystem for the Meitei Language Library (meitei).

Maintains cataloged grammatical research topics, morphological rules,
citation-backed syntactic patterns, and attested example sentences
from peer-reviewed reference grammars (e.g., Chelliah 1997, Pettigrew 1912, Grierson 1904).

Principles:
- Strict evidence-backed basis: no fabricated rules or synthetic native-speaker examples.
- Clear distinction between populated topics with verified primary-source evidence
  and unpopulated research categories.
- Stable identifiers: MEI-GRM-xxxxxxx for grammar records, MEI-GEX-xxxxxxx for examples.
- Comprehensive provenance tracking: exact source locators, translation provenance,
  and reviewer attributions.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from meitei.loader import DataLoader, MissingSourceError, ValidationError, get_default_data_dir
from meitei.schema import (
    ALL_ALLOWED_STATUSES,
    CORE_ALLOWED_STATUSES,
    RecordStatus,
    is_valid_gex_id,
    is_valid_grm_id,
    is_valid_src_id,
)


class GrammarValidationError(ValidationError):
    """Raised when a grammar record violates schema or citation constraints."""
    pass


@dataclass
class GrammarExample:
    """
    Evidence-backed illustrative sentence or syntactic construction.

    Attributes:
        example_id: Stable identifier (e.g. MEI-GEX-0000001).
        meitei: Meitei Mayek text representation.
        roman: Standard Latin Romanization.
        english: English translation.
        bengali: Historical Bengali-script transcription if attested in source.
        morpheme_gloss: Interlinear morpheme-by-morpheme glossing.
        source_ref: Specific example number or page reference in source.
        translation_provenance: Attribution and authority for the translation.
    """
    example_id: str
    meitei: str
    roman: str
    english: str
    bengali: Optional[str] = None
    morpheme_gloss: Optional[str] = None
    source_ref: Optional[str] = None
    translation_provenance: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert example to serializable dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> GrammarExample:
        """Construct GrammarExample from dictionary."""
        return cls(
            example_id=data.get("example_id", ""),
            meitei=data.get("meitei", ""),
            roman=data.get("roman", ""),
            english=data.get("english", ""),
            bengali=data.get("bengali"),
            morpheme_gloss=data.get("morpheme_gloss"),
            source_ref=data.get("source_ref"),
            translation_provenance=data.get("translation_provenance"),
        )


@dataclass
class GrammarRecord:
    """
    Linguistic grammar reference record backed by primary scholarly sources.

    Attributes:
        id: Stable identifier (e.g. MEI-GRM-0000001).
        topic: Research category (e.g. pronouns, numerals, negation, verb_morphology).
        title: Descriptive title of grammatical rule or paradigm.
        description: Scholarly linguistic explanation.
        verification_status: Verification status (e.g. SOURCE_ATTESTED, VERIFIED).
        source_id: Cataloged bibliographic source ID (e.g. MEI-SRC-000003).
        citation_locator: Specific page, folio, or section in source.
        morphological_rule: Structural or morphological pattern schema.
        examples: List of verified illustrative sentences.
        reviewer_attribution: Scholar review attribution.
        review_history: Historical audit and verification milestones.
        notes: Comparative or philological notes.
    """
    id: str
    topic: str
    title: str
    description: str
    verification_status: str
    source_id: Optional[str] = None
    citation_locator: Optional[str] = None
    morphological_rule: Optional[str] = None
    examples: List[GrammarExample] = field(default_factory=list)
    reviewer_attribution: Optional[Dict[str, Any]] = None
    review_history: List[Dict[str, Any]] = field(default_factory=list)
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert grammar record to serializable dictionary."""
        data = asdict(self)
        data["examples"] = [ex.to_dict() if isinstance(ex, GrammarExample) else ex for ex in self.examples]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> GrammarRecord:
        """Construct GrammarRecord from dictionary."""
        examples_raw = data.get("examples", [])
        examples = [
            GrammarExample.from_dict(e) if isinstance(e, dict) else e
            for e in examples_raw
        ]
        return cls(
            id=data.get("id", ""),
            topic=data.get("topic", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            verification_status=data.get("verification_status", RecordStatus.UNVERIFIED.value),
            source_id=data.get("source_id"),
            citation_locator=data.get("citation_locator"),
            morphological_rule=data.get("morphological_rule"),
            examples=examples,
            reviewer_attribution=data.get("reviewer_attribution"),
            review_history=data.get("review_history", []),
            notes=data.get("notes"),
        )


@dataclass
class GrammarTopic:
    """
    Grammatical research category metadata and population status.

    Attributes:
        id: Unique topic key (e.g. pronouns, negation).
        name: Human-readable topic designation.
        status: Population status ('POPULATED' vs 'UNPOPULATED').
        description: Overview of the linguistic domain.
        primary_sources: Cataloged sources referencing this topic.
        documentation: Citation summary if populated.
        unpopulated_reason: Philological explanation if unpopulated.
        record_count: Number of active grammar records for this topic.
    """
    id: str
    name: str
    status: str
    description: str
    primary_sources: List[str] = field(default_factory=list)
    documentation: Optional[str] = None
    unpopulated_reason: Optional[str] = None
    record_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert topic metadata to dictionary."""
        return asdict(self)


# =============================================================================
# Validation Functions
# =============================================================================

def validate_grammar_record(
    rec: Dict[str, Any],
    file_path: str = "grammar_records.jsonl",
    line_no: int = 1,
    seen_ids: Optional[Set[str]] = None,
    known_sources: Optional[Set[str]] = None,
) -> None:
    """
    Validate a single grammar record for schema correctness and citation integrity.

    Args:
        rec: Raw dictionary record.
        file_path: Source file path for error context.
        line_no: Line number in file.
        seen_ids: Set of previously observed record IDs.
        known_sources: Set of verified source IDs.

    Raises:
        GrammarValidationError: When any schema, ID, or citation rule is violated.
        MissingSourceError: When an attested record references an unknown source ID.
    """
    if not isinstance(rec, dict):
        raise GrammarValidationError(f"Grammar record at {file_path}:{line_no} must be a JSON object.")

    rec_id = rec.get("id")
    if not rec_id or not is_valid_grm_id(str(rec_id)):
        raise GrammarValidationError(
            f"Record at {file_path}:{line_no} has invalid 'id': '{rec_id}'. "
            f"Must match format MEI-GRM-xxxxxxx (e.g. MEI-GRM-0000001)."
        )

    if seen_ids is not None:
        if rec_id in seen_ids:
            raise GrammarValidationError(f"Duplicate grammar record ID '{rec_id}' at {file_path}:{line_no}.")
        seen_ids.add(rec_id)

    topic = rec.get("topic")
    if not topic or not isinstance(topic, str) or not topic.strip():
        raise GrammarValidationError(f"Record '{rec_id}' at {file_path}:{line_no} missing 'topic'.")

    title = rec.get("title")
    if not title or not isinstance(title, str) or not title.strip():
        raise GrammarValidationError(f"Record '{rec_id}' at {file_path}:{line_no} missing 'title'.")

    description = rec.get("description")
    if not description or not isinstance(description, str) or not description.strip():
        raise GrammarValidationError(f"Record '{rec_id}' at {file_path}:{line_no} missing 'description'.")

    status = rec.get("verification_status")
    if not status or status not in ALL_ALLOWED_STATUSES:
        raise GrammarValidationError(
            f"Record '{rec_id}' at {file_path}:{line_no} has invalid status '{status}'. "
            f"Must be one of: {sorted(ALL_ALLOWED_STATUSES)}."
        )

    # Citation completeness for source-attested records
    if status == RecordStatus.SOURCE_ATTESTED.value:
        src_id = rec.get("source_id")
        if not src_id or not is_valid_src_id(str(src_id)):
            raise GrammarValidationError(
                f"SOURCE_ATTESTED grammar record '{rec_id}' at {file_path}:{line_no} "
                f"missing valid 'source_id' (e.g. MEI-SRC-000001)."
            )
        if known_sources is not None and src_id not in known_sources:
            raise MissingSourceError(rec_id, src_id, file_path, line_no)

        locator = rec.get("citation_locator")
        if not locator or not isinstance(locator, str) or not locator.strip():
            raise GrammarValidationError(
                f"SOURCE_ATTESTED grammar record '{rec_id}' at {file_path}:{line_no} "
                f"must provide an exact 'citation_locator' (e.g. 'Page 14, Chapter 3')."
            )

    # Validate illustrative examples
    examples = rec.get("examples", [])
    if not isinstance(examples, list):
        raise GrammarValidationError(f"Record '{rec_id}' at {file_path}:{line_no}: 'examples' must be an array.")

    seen_ex_ids: Set[str] = set()
    for ex_idx, ex in enumerate(examples, start=1):
        if not isinstance(ex, dict):
            raise GrammarValidationError(f"Record '{rec_id}' example #{ex_idx} must be an object.")
        ex_id = ex.get("example_id")
        if not ex_id or not is_valid_gex_id(str(ex_id)):
            raise GrammarValidationError(
                f"Record '{rec_id}' example #{ex_idx} has invalid 'example_id': '{ex_id}'. "
                f"Must match format MEI-GEX-xxxxxxx."
            )
        if ex_id in seen_ex_ids:
            raise GrammarValidationError(f"Record '{rec_id}' contains duplicate example ID '{ex_id}'.")
        seen_ex_ids.add(ex_id)

        for req_field in ["meitei", "roman", "english"]:
            val = ex.get(req_field)
            if not val or not isinstance(val, str) or not val.strip():
                raise GrammarValidationError(
                    f"Record '{rec_id}' example '{ex_id}' missing required field '{req_field}'."
                )

        prov = ex.get("translation_provenance")
        if not prov or not isinstance(prov, str) or not prov.strip():
            raise GrammarValidationError(
                f"Record '{rec_id}' example '{ex_id}' missing 'translation_provenance' "
                f"(must document authority or citation origin of translation)."
            )

    # Validate reviewer attribution
    rev = rec.get("reviewer_attribution")
    if rev is not None:
        if not isinstance(rev, dict):
            raise GrammarValidationError(f"Record '{rec_id}': 'reviewer_attribution' must be an object.")
        if not rev.get("reviewer_id") or not str(rev.get("reviewer_id")).strip():
            raise GrammarValidationError(f"Record '{rec_id}': 'reviewer_attribution' missing 'reviewer_id'.")
        if not rev.get("review_date") or not str(rev.get("review_date")).strip():
            raise GrammarValidationError(f"Record '{rec_id}': 'reviewer_attribution' missing 'review_date'.")


# =============================================================================
# Query and Access Functions
# =============================================================================

def load_grammar_records(
    path: Optional[Union[str, Path]] = None,
    data_dir: Union[str, Path] = "data",
    known_sources: Optional[Set[str]] = None,
) -> List[GrammarRecord]:
    """
    Load and validate all grammar records from JSONL storage.

    Args:
        path: Optional explicit file path to grammar_records.jsonl.
        data_dir: Root data directory (default: data).
        known_sources: Optional set of known source IDs to validate referential integrity.

    Returns:
        List of validated GrammarRecord objects.
    """
    data_dir = get_default_data_dir(data_dir)
    p = Path(path) if path else Path(data_dir) / "grammar" / "grammar_records.jsonl"
    if not p.exists():
        return []

    if known_sources is None:
        loader = DataLoader(data_dir)
        try:
            sources = loader.load_sources()
            known_sources = set(sources.keys())
        except Exception:
            known_sources = set()

    records: List[GrammarRecord] = []
    seen_ids: Set[str] = set()

    with open(p, "r", encoding="utf-8") as f:
        for line_no, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                rec_dict = json.loads(line)
            except json.JSONDecodeError as e:
                raise GrammarValidationError(f"Malformed JSON at {p}:{line_no}: {e}")

            validate_grammar_record(rec_dict, str(p), line_no, seen_ids, known_sources)
            records.append(GrammarRecord.from_dict(rec_dict))

    return records


def list_grammar_topics(data_dir: Union[str, Path] = "data") -> List[Dict[str, Any]]:
    """
    List all cataloged grammatical research topics and their current evidence status.

    Documents which topics have actual source-attested records and which remain
    unpopulated research categories pending philological ingestion.

    Returns:
        List of topic dictionaries with status, description, and record count.
    """
    data_dir = get_default_data_dir(data_dir)
    topics_file = Path(data_dir) / "grammar" / "topics.json"
    records = load_grammar_records(data_dir=data_dir)

    # Count records per topic
    topic_counts: Dict[str, int] = {}
    for r in records:
        topic_counts[r.topic.lower()] = topic_counts.get(r.topic.lower(), 0) + 1

    topics_raw: List[Dict[str, Any]] = []
    if topics_file.exists():
        with open(topics_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            topics_raw = data.get("topics", [])
    else:
        # Default topic definitions if topics.json missing
        topics_raw = [
            {"id": "pronouns", "name": "Personal Pronouns & Deixis", "status": "POPULATED", "description": "Pronominal paradigm."},
            {"id": "numerals", "name": "Numerals & Counting", "status": "POPULATED", "description": "Morphology of decimal roots."},
            {"id": "negation", "name": "Verbal Negation", "status": "POPULATED", "description": "Negative suffixation -te/-de."},
            {"id": "verb_morphology", "name": "Verb Morphology", "status": "POPULATED", "description": "Aspect and modal formatives."},
            {"id": "sentence_structure", "name": "Sentence Structure", "status": "POPULATED", "description": "Canonical SOV word order."},
            {"id": "classifiers", "name": "Numeral Classifiers", "status": "UNPOPULATED", "description": "Sortal and mensural numeral classifiers."},
            {"id": "noun_morphology", "name": "Noun Morphology", "status": "UNPOPULATED", "description": "Case marking postpositions."},
            {"id": "particles", "name": "Discourse Particles", "status": "UNPOPULATED", "description": "Information-packaging enclitics."},
        ]

    result: List[Dict[str, Any]] = []
    for t in topics_raw:
        tid = t["id"].lower()
        cnt = topic_counts.get(tid, 0)
        t_copy: Dict[str, Any] = dict(t)
        t_copy["record_count"] = cnt
        # Ensure status accurately reflects presence of verified records
        if cnt > 0 and t_copy["status"] != "POPULATED":
            t_copy["status"] = "POPULATED"
        result.append(t_copy)

    return result


def get_grammar_records(
    topic: Optional[str] = None,
    status: Optional[str] = None,
    verified_only: bool = False,
    data_dir: Union[str, Path] = "data",
) -> List[GrammarRecord]:
    """
    Retrieve grammar records filtered by topic, status, or verification guarantee.

    Args:
        topic: Optional topic filter (e.g. 'pronouns', 'negation', 'numerals').
        status: Optional status filter (e.g. 'SOURCE_ATTESTED', 'VERIFIED').
        verified_only: When True, strictly excludes unverified research notes.
        data_dir: Data directory root path.

    Returns:
        List of matching GrammarRecord objects.
    """
    records = load_grammar_records(data_dir=data_dir)
    filtered: List[GrammarRecord] = []

    topic_clean = topic.strip().lower() if topic else None
    status_clean = status.strip().upper() if status else None

    for r in records:
        if topic_clean and r.topic.lower() != topic_clean:
            continue
        if status_clean and r.verification_status != status_clean:
            continue
        if verified_only and r.verification_status not in CORE_ALLOWED_STATUSES:
            continue
        filtered.append(r)

    return filtered


def get_grammar_record_by_id(
    record_id: str,
    data_dir: Union[str, Path] = "data",
) -> Optional[GrammarRecord]:
    """Retrieve a single grammar record by its stable identifier (e.g. MEI-GRM-0000001)."""
    records = load_grammar_records(data_dir=data_dir)
    for r in records:
        if r.id == record_id:
            return r
    return None


def get_topic_sources(
    topic: str,
    data_dir: Union[str, Path] = "data",
) -> List[Dict[str, Any]]:
    """
    Retrieve all bibliographic sources providing evidence for a specified grammar topic.

    Args:
        topic: Grammatical research topic (e.g. 'pronouns', 'negation').
        data_dir: Data directory root.

    Returns:
        List of bibliographic source metadata dictionaries.
    """
    records = get_grammar_records(topic=topic, data_dir=data_dir)
    source_ids = {r.source_id for r in records if r.source_id}

    if not source_ids:
        # Check topic metadata for declared primary sources
        topics = list_grammar_topics(data_dir=data_dir)
        for t in topics:
            if t["id"].lower() == topic.strip().lower():
                source_ids.update(t.get("primary_sources", []))
                break

    loader = DataLoader(data_dir)
    try:
        all_sources = loader.load_sources()
    except Exception:
        all_sources = {}

    return [all_sources[sid] for sid in sorted(source_ids) if sid in all_sources]


def list_grammar_sources(data_dir: Union[str, Path] = "data") -> List[Dict[str, Any]]:
    """
    List all bibliographic sources providing evidence across the entire grammar subsystem.

    Returns:
        List of bibliographic source metadata dictionaries.
    """
    records = load_grammar_records(data_dir=data_dir)
    source_ids = {r.source_id for r in records if r.source_id}

    loader = DataLoader(data_dir)
    try:
        all_sources = loader.load_sources()
    except Exception:
        all_sources = {}

    return [all_sources[sid] for sid in sorted(source_ids) if sid in all_sources]


def get_populated_topics(data_dir: Union[str, Path] = "data") -> List[Dict[str, Any]]:
    """Return all grammar topics that have verified textual evidence."""
    return [t for t in list_grammar_topics(data_dir=data_dir) if t["status"] == "POPULATED"]


def get_unpopulated_topics(data_dir: Union[str, Path] = "data") -> List[Dict[str, Any]]:
    """Return all registered grammar categories currently awaiting primary evidence ingestion."""
    return [t for t in list_grammar_topics(data_dir=data_dir) if t["status"] == "UNPOPULATED"]


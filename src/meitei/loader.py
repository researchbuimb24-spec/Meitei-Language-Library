# -*- coding: utf-8 -*-
"""
JSONL Loader and Schema Validation Engine for the Meitei Language Library (meitei).

Implements strict validation and cross-referential integrity checks:
1. Malformed JSONL detection.
2. Stable ID pattern enforcement (MEI-LEX-xxxxxxx, MEI-SRC-xxxxxx, etc.).
3. Duplicate ID rejection.
4. Source referential integrity (cited sources must exist in sources.jsonl).
5. Exact citation locator requirement for SOURCE_ATTESTED records.
6. Dataset partition enforcement:
   - core_lexicon.jsonl is restricted to SOURCE_ATTESTED and VERIFIED.
   - candidate_lexicon.jsonl is restricted to candidate/quarantine statuses.
7. Reviewer attribution and metadata validation.

Built entirely using the Python standard library.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union

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


# =============================================================================
# Validation Exceptions
# =============================================================================

class ValidationError(Exception):
    """Base exception for all schema and data validation errors."""
    pass


class MalformedJSONLError(ValidationError):
    """Raised when a JSONL line is not valid JSON."""
    def __init__(self, file_path: str, line_no: int, message: str) -> None:
        super().__init__(f"Malformed JSONL at {file_path}:{line_no} -> {message}")
        self.file_path = file_path
        self.line_no = line_no


class DuplicateIDError(ValidationError):
    """Raised when an identifier is defined more than once."""
    def __init__(self, record_id: str, file_path: str, line_no: int) -> None:
        super().__init__(f"Duplicate identifier '{record_id}' found at {file_path}:{line_no}")
        self.record_id = record_id
        self.file_path = file_path
        self.line_no = line_no


class MissingSourceError(ValidationError):
    """Raised when a record references a non-existent source_id."""
    def __init__(self, source_id: str, record_id: str, file_path: str, line_no: int) -> None:
        super().__init__(
            f"Record '{record_id}' at {file_path}:{line_no} references unknown source_id: '{source_id}'"
        )
        self.source_id = source_id
        self.record_id = record_id


class InvalidStatusError(ValidationError):
    """Raised when a record has an unapproved status."""
    def __init__(self, status: str, record_id: str, file_path: str, line_no: int) -> None:
        super().__init__(
            f"Invalid status '{status}' for record '{record_id}' at {file_path}:{line_no}. "
            f"Must be one of {sorted(ALL_ALLOWED_STATUSES)}"
        )
        self.status = status


class CitationLocatorMissingError(ValidationError):
    """Raised when a SOURCE_ATTESTED entry lacks an exact citation locator."""
    def __init__(self, record_id: str, file_path: str, line_no: int) -> None:
        super().__init__(
            f"SOURCE_ATTESTED record '{record_id}' at {file_path}:{line_no} "
            f"must provide an exact non-empty 'citation_locator' (e.g. folio, page, verse)."
        )
        self.record_id = record_id


class DatasetPartitionError(ValidationError):
    """Raised when a record is placed in the wrong dataset partition."""
    def __init__(self, record_id: str, status: str, partition: str, file_path: str, line_no: int) -> None:
        super().__init__(
            f"Dataset partition violation at {file_path}:{line_no}: "
            f"Record '{record_id}' with status '{status}' is not permitted in the '{partition}' partition."
        )
        self.record_id = record_id
        self.status = status
        self.partition = partition


# =============================================================================
# Record-Level Validators
# =============================================================================

def validate_source_record(
    rec: Dict[str, Any],
    file_path: str,
    line_no: int,
    seen_ids: Set[str],
) -> None:
    """Validate a single bibliographic source record."""
    if not isinstance(rec, dict):
        raise ValidationError(f"Source at {file_path}:{line_no} must be a JSON object.")

    source_id = rec.get("id")
    if not source_id or not is_valid_src_id(str(source_id)):
        raise ValidationError(
            f"Source at {file_path}:{line_no} has invalid 'id': '{source_id}'. "
            f"Must match format MEI-SRC-xxxxxx (e.g. MEI-SRC-000001)."
        )

    if source_id in seen_ids:
        raise DuplicateIDError(source_id, file_path, line_no)
    seen_ids.add(source_id)

    title = rec.get("title")
    if not title or not isinstance(title, str) or not title.strip():
        raise ValidationError(f"Source '{source_id}' at {file_path}:{line_no} missing non-empty 'title'.")

    source_type = rec.get("source_type")
    if not source_type or not isinstance(source_type, str):
        raise ValidationError(f"Source '{source_id}' at {file_path}:{line_no} missing 'source_type'.")


def validate_reviewer_attribution(
    attrib: Any,
    parent_id: str,
    file_path: str,
    line_no: int,
) -> None:
    """Validate reviewer attribution object if provided."""
    if attrib is None:
        return
    if not isinstance(attrib, dict):
        raise ValidationError(
            f"Record '{parent_id}' at {file_path}:{line_no}: 'reviewer_attribution' must be an object."
        )
    reviewer_id = attrib.get("reviewer_id")
    if not reviewer_id or not isinstance(reviewer_id, str) or not reviewer_id.strip():
        raise ValidationError(
            f"Record '{parent_id}' at {file_path}:{line_no}: 'reviewer_attribution' missing 'reviewer_id'."
        )
    review_date = attrib.get("review_date")
    if not review_date or not isinstance(review_date, str) or not review_date.strip():
        raise ValidationError(
            f"Record '{parent_id}' at {file_path}:{line_no}: 'reviewer_attribution' missing 'review_date'."
        )


def validate_lexical_entry(
    rec: Dict[str, Any],
    file_path: str,
    line_no: int,
    seen_ids: Set[str],
    known_sources: Optional[Set[str]] = None,
    partition: str = "core",
) -> None:
    """
    Validate a lexical entry record, including senses, citations, and partition rules.
    """
    if not isinstance(rec, dict):
        raise ValidationError(f"Lexical entry at {file_path}:{line_no} must be a JSON object.")

    entry_id = rec.get("id")
    if not entry_id or not is_valid_lex_id(str(entry_id)):
        raise ValidationError(
            f"Entry at {file_path}:{line_no} has invalid 'id': '{entry_id}'. "
            f"Must match format MEI-LEX-xxxxxxx (e.g. MEI-LEX-0000001)."
        )

    if entry_id in seen_ids:
        raise DuplicateIDError(entry_id, file_path, line_no)
    seen_ids.add(entry_id)

    # Headwords
    headword_meitei = rec.get("headword_meitei")
    if not headword_meitei or not isinstance(headword_meitei, str) or not headword_meitei.strip():
        raise ValidationError(f"Entry '{entry_id}' at {file_path}:{line_no} missing non-empty 'headword_meitei'.")

    headword_roman = rec.get("headword_roman")
    if not headword_roman or not isinstance(headword_roman, str) or not headword_roman.strip():
        raise ValidationError(f"Entry '{entry_id}' at {file_path}:{line_no} missing non-empty 'headword_roman'.")

    # Status & Partition Verification
    status = rec.get("status")
    if not status or not isinstance(status, str) or status not in ALL_ALLOWED_STATUSES:
        raise InvalidStatusError(str(status), entry_id, file_path, line_no)

    if partition == "core" and status not in CORE_ALLOWED_STATUSES:
        raise DatasetPartitionError(entry_id, status, "core_lexicon", file_path, line_no)
    if partition == "candidate" and status not in CANDIDATE_ALLOWED_STATUSES:
        raise DatasetPartitionError(entry_id, status, "candidate_lexicon", file_path, line_no)

    # Source & Citation Locator Verification
    source_id = rec.get("source_id")
    citation_locator = rec.get("citation_locator")

    if status == RecordStatus.SOURCE_ATTESTED.value:
        if not source_id or not isinstance(source_id, str) or not source_id.strip():
            raise ValidationError(
                f"SOURCE_ATTESTED entry '{entry_id}' at {file_path}:{line_no} requires a non-empty 'source_id'."
            )
        if not citation_locator or not isinstance(citation_locator, str) or not citation_locator.strip():
            raise CitationLocatorMissingError(entry_id, file_path, line_no)

    if source_id:
        if not is_valid_src_id(source_id):
            raise ValidationError(
                f"Entry '{entry_id}' at {file_path}:{line_no} references invalid source_id format: '{source_id}'"
            )
        if known_sources is not None and source_id not in known_sources:
            raise MissingSourceError(source_id, entry_id, file_path, line_no)

    # Reviewer attribution
    validate_reviewer_attribution(rec.get("reviewer_attribution"), entry_id, file_path, line_no)

    # Senses Verification
    senses = rec.get("senses")
    if not isinstance(senses, list) or len(senses) == 0:
        raise ValidationError(f"Entry '{entry_id}' at {file_path}:{line_no} must contain at least one sense.")

    seen_sense_ids: Set[str] = set()
    for s_idx, sense in enumerate(senses, start=1):
        if not isinstance(sense, dict):
            raise ValidationError(f"Sense #{s_idx} in entry '{entry_id}' must be a JSON object.")
        sid = sense.get("id")
        if not sid or not is_valid_sns_id(str(sid)):
            raise ValidationError(
                f"Sense #{s_idx} in entry '{entry_id}' has invalid 'id': '{sid}'. "
                f"Must match MEI-SNS-xxxxxxx or MEI-LEX-xxxxxxx-Sxx."
            )
        if sid in seen_sense_ids:
            raise DuplicateIDError(sid, file_path, line_no)
        seen_sense_ids.add(sid)

        defn = sense.get("definition_en")
        if not defn or not isinstance(defn, str) or not defn.strip():
            raise ValidationError(f"Sense '{sid}' in entry '{entry_id}' missing 'definition_en'.")
        pos = sense.get("part_of_speech")
        if not pos or not isinstance(pos, str) or not pos.strip():
            raise ValidationError(f"Sense '{sid}' in entry '{entry_id}' missing 'part_of_speech'.")


def validate_variant_record(
    rec: Dict[str, Any],
    file_path: str,
    line_no: int,
    seen_ids: Set[str],
    known_entries: Optional[Set[str]] = None,
    known_sources: Optional[Set[str]] = None,
) -> None:
    """Validate a spelling/orthographic variant record."""
    if not isinstance(rec, dict):
        raise ValidationError(f"Variant at {file_path}:{line_no} must be a JSON object.")

    var_id = rec.get("id")
    if not var_id or not is_valid_var_id(str(var_id)):
        raise ValidationError(
            f"Variant at {file_path}:{line_no} has invalid 'id': '{var_id}'. Must match MEI-VAR-xxxxxxx."
        )

    if var_id in seen_ids:
        raise DuplicateIDError(var_id, file_path, line_no)
    seen_ids.add(var_id)

    entry_id = rec.get("entry_id")
    if not entry_id or not is_valid_lex_id(str(entry_id)):
        raise ValidationError(
            f"Variant '{var_id}' at {file_path}:{line_no} has invalid 'entry_id': '{entry_id}'."
        )
    if known_entries is not None and entry_id not in known_entries:
        raise ValidationError(
            f"Variant '{var_id}' references unknown lexical entry_id: '{entry_id}'."
        )

    variant_form = rec.get("variant_form")
    if not variant_form or not isinstance(variant_form, str) or not variant_form.strip():
        raise ValidationError(f"Variant '{var_id}' missing non-empty 'variant_form'.")

    status = rec.get("status")
    if not status or status not in ALL_ALLOWED_STATUSES:
        raise InvalidStatusError(str(status), var_id, file_path, line_no)

    source_id = rec.get("source_id")
    if source_id:
        if not is_valid_src_id(source_id):
            raise ValidationError(f"Variant '{var_id}' references invalid source_id format: '{source_id}'")
        if known_sources is not None and source_id not in known_sources:
            raise MissingSourceError(source_id, var_id, file_path, line_no)


def validate_gloss_record(
    rec: Dict[str, Any],
    file_path: str,
    line_no: int,
    seen_ids: Set[str],
    known_entries: Optional[Set[str]] = None,
    known_sources: Optional[Set[str]] = None,
) -> None:
    """Validate a translation gloss record."""
    if not isinstance(rec, dict):
        raise ValidationError(f"Gloss at {file_path}:{line_no} must be a JSON object.")

    gls_id = rec.get("id")
    if not gls_id or not is_valid_gls_id(str(gls_id)):
        raise ValidationError(
            f"Gloss at {file_path}:{line_no} has invalid 'id': '{gls_id}'. Must match MEI-GLS-xxxxxxx."
        )

    if gls_id in seen_ids:
        raise DuplicateIDError(gls_id, file_path, line_no)
    seen_ids.add(gls_id)

    entry_id = rec.get("entry_id")
    if not entry_id or not is_valid_lex_id(str(entry_id)):
        raise ValidationError(
            f"Gloss '{gls_id}' at {file_path}:{line_no} has invalid 'entry_id': '{entry_id}'."
        )
    if known_entries is not None and entry_id not in known_entries:
        raise ValidationError(
            f"Gloss '{gls_id}' references unknown lexical entry_id: '{entry_id}'."
        )

    target_lang = rec.get("target_language")
    if not target_lang or not isinstance(target_lang, str) or not target_lang.strip():
        raise ValidationError(f"Gloss '{gls_id}' missing non-empty 'target_language'.")

    gloss_text = rec.get("gloss")
    if not gloss_text or not isinstance(gloss_text, str) or not gloss_text.strip():
        raise ValidationError(f"Gloss '{gls_id}' missing non-empty 'gloss'.")

    status = rec.get("status")
    if not status or status not in ALL_ALLOWED_STATUSES:
        raise InvalidStatusError(str(status), gls_id, file_path, line_no)

    source_id = rec.get("source_id")
    if source_id:
        if not is_valid_src_id(source_id):
            raise ValidationError(f"Gloss '{gls_id}' references invalid source_id format: '{source_id}'")
        if known_sources is not None and source_id not in known_sources:
            raise MissingSourceError(source_id, gls_id, file_path, line_no)


# =============================================================================
# JSONL Streaming File Reader & DataLoader
# =============================================================================

def get_default_data_dir(data_dir: Optional[Union[str, Path]] = None) -> Path:
    """
    Resolve data directory using hierarchical fallback:
    1. If explicit non-default data_dir is provided and exists, use Path(data_dir).
    2. Environment variable MEITEI_DATA_DIR if set and exists.
    3. If local 'data' directory in cwd exists and has datasets, use it.
    4. Packaged data in src/meitei/data if exists.
    5. Repo root relative to this file: ../../../data.
    6. Fall back to Path(data_dir or "data").
    """
    if data_dir is not None and str(data_dir) != "data":
        p = Path(data_dir)
        if p.exists():
            return p

    import os
    env_dir = os.environ.get("MEITEI_DATA_DIR")
    if env_dir:
        p = Path(env_dir)
        if p.exists():
            return p

    local_p = Path(data_dir or "data")
    if (local_p / "sources" / "sources.jsonl").exists() or (local_p / "lexicon" / "core_lexicon.jsonl").exists():
        return local_p

    pkg_data = Path(__file__).resolve().parent / "data"
    if (pkg_data / "sources" / "sources.jsonl").exists():
        return pkg_data

    repo_data = Path(__file__).resolve().parent.parent.parent / "data"
    if (repo_data / "sources" / "sources.jsonl").exists():
        return repo_data

    return local_p


def read_jsonl_lines(path: Union[str, Path]) -> Iterator[Tuple[int, Dict[str, Any]]]:
    """
    Streamingly yield (line_number, parsed_json_dict) from a JSONL file.

    Raises MalformedJSONLError if any non-empty line fails to parse.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")

    with open(p, "r", encoding="utf-8") as f:
        for line_no, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                raise MalformedJSONLError(str(p), line_no, str(e)) from e
            yield line_no, data


class DataLoader:
    """
    Structured dataset loader and integrity verifier for Meitei Language Library.
    """

    def __init__(self, data_root: Optional[Union[str, Path]] = "data") -> None:
        self.data_root = get_default_data_dir(data_root)

    def load_sources(self, path: Optional[Union[str, Path]] = None) -> Dict[str, Dict[str, Any]]:
        """
        Load and validate sources from data/sources/sources.jsonl.

        Returns dictionary mapping source_id -> source dict.
        """
        p = Path(path) if path else self.data_root / "sources" / "sources.jsonl"
        sources: Dict[str, Dict[str, Any]] = {}
        seen_ids: Set[str] = set()

        for line_no, rec in read_jsonl_lines(p):
            validate_source_record(rec, str(p), line_no, seen_ids)
            sources[rec["id"]] = rec

        return sources

    def load_lexicon(
        self,
        path: Optional[Union[str, Path]] = None,
        partition: str = "core",
        known_sources: Optional[Set[str]] = None,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Load and validate a lexicon dataset partition (core or candidate).

        Returns dictionary mapping entry_id -> entry dict.
        """
        if path:
            p = Path(path)
        else:
            filename = "core_lexicon.jsonl" if partition == "core" else "candidate_lexicon.jsonl"
            p = self.data_root / "lexicon" / filename

        entries: Dict[str, Dict[str, Any]] = {}
        seen_ids: Set[str] = set()

        for line_no, rec in read_jsonl_lines(p):
            validate_lexical_entry(rec, str(p), line_no, seen_ids, known_sources, partition=partition)
            entries[rec["id"]] = rec

        return entries

    def load_variants(
        self,
        path: Optional[Union[str, Path]] = None,
        known_entries: Optional[Set[str]] = None,
        known_sources: Optional[Set[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Load and validate spelling/orthographic variants."""
        p = Path(path) if path else self.data_root / "lexicon" / "variants.jsonl"
        variants: List[Dict[str, Any]] = []
        seen_ids: Set[str] = set()

        for line_no, rec in read_jsonl_lines(p):
            validate_variant_record(rec, str(p), line_no, seen_ids, known_entries, known_sources)
            variants.append(rec)

        return variants

    def load_glosses(
        self,
        path: Optional[Union[str, Path]] = None,
        known_entries: Optional[Set[str]] = None,
        known_sources: Optional[Set[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Load and validate cross-lingual translation glosses."""
        p = Path(path) if path else self.data_root / "translations" / "glosses.jsonl"
        glosses: List[Dict[str, Any]] = []
        seen_ids: Set[str] = set()

        for line_no, rec in read_jsonl_lines(p):
            validate_gloss_record(rec, str(p), line_no, seen_ids, known_entries, known_sources)
            glosses.append(rec)

        return glosses

    def validate_all(self) -> Dict[str, Any]:
        """
        Perform a full cross-referential integrity validation across all datasets.

        Validates sources first, then core and candidate lexicons, and finally
        variants and translation glosses.
        """
        sources = self.load_sources()
        known_sources = set(sources.keys())

        core_lex = self.load_lexicon(partition="core", known_sources=known_sources)
        candidate_lex = self.load_lexicon(partition="candidate", known_sources=known_sources)

        # Ensure no ID collision across core and candidate lexicons
        lexicon_collision = set(core_lex.keys()) & set(candidate_lex.keys())
        if lexicon_collision:
            raise DuplicateIDError(
                next(iter(lexicon_collision)),
                str(self.data_root / "lexicon"),
                0
            )

        all_known_entries = set(core_lex.keys()) | set(candidate_lex.keys())

        variants = self.load_variants(known_entries=all_known_entries, known_sources=known_sources)
        glosses = self.load_glosses(known_entries=all_known_entries, known_sources=known_sources)

        return {
            "status": "VALID",
            "sources_count": len(sources),
            "core_entries_count": len(core_lex),
            "candidate_entries_count": len(candidate_lex),
            "variants_count": len(variants),
            "glosses_count": len(glosses),
        }


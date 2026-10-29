# -*- coding: utf-8 -*-
"""
Data Schemas and Validation Constants for the Meitei Language Library (meitei).

Defines JSON Schemas, stable ID specifications, and status enumerations for:
1. Lexical Entries (MEI-LEX-0000001)
2. Lexical Senses (MEI-SNS-0000001 or MEI-LEX-0000001-S01)
3. Bibliographic Sources (MEI-SRC-000001)
4. Spelling & Orthographic Variants (MEI-VAR-0000001)
5. Cross-Lingual Translation Glosses (MEI-GLS-0000001)
6. Community & Provenance Review Records (MEI-REV-0000001)

All validation utilizes the Python standard library exclusively.
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Any, Dict, Set


class RecordStatus(str, Enum):
    """
    Controlled vocabulary of verification and attestation statuses.

    - SOURCE_ATTESTED: Directly attested in a cataloged bibliographic source
      (Puya, chronicle, dictionary, or critical edition) with an exact citation locator.
    - VERIFIED: Attested and independently confirmed by qualified native speakers
      or professional linguists adhering to modern standardized orthography.
    - COMMUNITY_SUBMITTED: Contributed by community speakers or field informants;
      pending formal editorial review.
    - UNVERIFIED: Ingested from raw field notes or provisional text; unvetted.
    - AI_CANDIDATE: Generated or proposed by computational language models;
      quarantined in candidate_lexicon until corroborated against primary sources.
    - CITATION_MISMATCH: Flagged during audit because cited source text, folio,
      or page does not corroborate the recorded meaning or spelling.
    - REJECTED: Reviewed and formally rejected due to factual error or spurious attribution.
    """
    SOURCE_ATTESTED = "SOURCE_ATTESTED"
    VERIFIED = "VERIFIED"
    COMMUNITY_SUBMITTED = "COMMUNITY_SUBMITTED"
    UNVERIFIED = "UNVERIFIED"
    AI_CANDIDATE = "AI_CANDIDATE"
    CITATION_MISMATCH = "CITATION_MISMATCH"
    REJECTED = "REJECTED"


class ReviewDecision(str, Enum):
    """
    Decisions recorded during community, peer, and provenance review.

    - ACCEPTED: Verified as authentic and corroborated by native speaker or primary evidence.
    - CORRECTED: Field or orthographic values corrected during review with documented diff.
    - REJECTED: Formally rejected due to lack of attestation, error, or ungrounded generation.
    - AWAITING_REVIEW: Submitted to ledger awaiting formal inspection by qualified reviewer.
    """
    ACCEPTED = "ACCEPTED"
    CORRECTED = "CORRECTED"
    REJECTED = "REJECTED"
    AWAITING_REVIEW = "AWAITING_REVIEW"


class ReviewerRole(str, Enum):
    """
    Recognized reviewer roles for attribution and verification pedigree.
    """
    NATIVE_SPEAKER = "NATIVE_SPEAKER"
    LINGUIST = "LINGUIST"
    CULTURAL_AUTHORITY = "CULTURAL_AUTHORITY"
    COMMUNITY_ELDER = "COMMUNITY_ELDER"
    ACADEMIC_EDITOR = "ACADEMIC_EDITOR"
    CONTRIBUTOR = "CONTRIBUTOR"


# Dataset Partitioning Rules:
# Core lexicon MUST only contain SOURCE_ATTESTED or VERIFIED records.
# Candidate lexicon MUST contain unverified, community-submitted, or AI records.
CORE_ALLOWED_STATUSES: Set[str] = {
    RecordStatus.SOURCE_ATTESTED.value,
    RecordStatus.VERIFIED.value,
}

CANDIDATE_ALLOWED_STATUSES: Set[str] = {
    RecordStatus.COMMUNITY_SUBMITTED.value,
    RecordStatus.UNVERIFIED.value,
    RecordStatus.AI_CANDIDATE.value,
    RecordStatus.CITATION_MISMATCH.value,
    RecordStatus.REJECTED.value,
}

ALL_ALLOWED_STATUSES: Set[str] = {s.value for s in RecordStatus}


# Stable ID Regular Expressions
REGEX_LEX_ID = re.compile(r"^MEI-LEX-\d{7}$")
REGEX_SRC_ID = re.compile(r"^MEI-SRC-\d{6}$")
REGEX_SNS_ID = re.compile(r"^(MEI-SNS-\d{7}|MEI-LEX-\d{7}-S\d{2})$")
REGEX_VAR_ID = re.compile(r"^MEI-VAR-\d{7}$")
REGEX_GLS_ID = re.compile(r"^MEI-GLS-\d{7}$")
REGEX_GRM_ID = re.compile(r"^MEI-GRM-\d{7}$")
REGEX_GEX_ID = re.compile(r"^MEI-GEX-\d{7}$")
REGEX_REV_ID = re.compile(r"^MEI-REV-\d{7}$")


def is_valid_lex_id(val: str) -> bool:
    """Return True if val matches MEI-LEX-xxxxxxx (7 digits)."""
    return bool(REGEX_LEX_ID.match(val)) if isinstance(val, str) else False


def is_valid_src_id(val: str) -> bool:
    """Return True if val matches MEI-SRC-xxxxxx (6 digits)."""
    return bool(REGEX_SRC_ID.match(val)) if isinstance(val, str) else False


def is_valid_sns_id(val: str) -> bool:
    """Return True if val matches MEI-SNS-xxxxxxx or MEI-LEX-xxxxxxx-Sxx."""
    return bool(REGEX_SNS_ID.match(val)) if isinstance(val, str) else False


def is_valid_var_id(val: str) -> bool:
    """Return True if val matches MEI-VAR-xxxxxxx (7 digits)."""
    return bool(REGEX_VAR_ID.match(val)) if isinstance(val, str) else False


def is_valid_gls_id(val: str) -> bool:
    """Return True if val matches MEI-GLS-xxxxxxx (7 digits)."""
    return bool(REGEX_GLS_ID.match(val)) if isinstance(val, str) else False


def is_valid_grm_id(val: str) -> bool:
    """Return True if val matches MEI-GRM-xxxxxxx (7 digits)."""
    return bool(REGEX_GRM_ID.match(val)) if isinstance(val, str) else False


def is_valid_gex_id(val: str) -> bool:
    """Return True if val matches MEI-GEX-xxxxxxx (7 digits)."""
    return bool(REGEX_GEX_ID.match(val)) if isinstance(val, str) else False


def is_valid_rev_id(val: str) -> bool:
    """Return True if val matches MEI-REV-xxxxxxx (7 digits)."""
    return bool(REGEX_REV_ID.match(val)) if isinstance(val, str) else False


# =============================================================================
# JSON Schema Definitions (Draft 2020-12 compatible dictionaries)
# =============================================================================

SOURCE_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "BibliographicSourceRecord",
    "type": "object",
    "required": ["id", "title", "source_type"],
    "properties": {
        "id": {
            "type": "string",
            "pattern": r"^MEI-SRC-\d{6}$",
            "description": "Unique stable identifier for the source (e.g. MEI-SRC-000001)."
        },
        "title": {
            "type": "string",
            "minLength": 1,
            "description": "Full formal title of the puya, manuscript, dictionary, or fieldwork collection."
        },
        "author": {
            "type": ["string", "null"],
            "description": "Author or compiler if historically attested or known."
        },
        "editor_or_translator": {
            "type": ["string", "null"],
            "description": "Editor, translator, or critical commentator."
        },
        "year": {
            "type": ["integer", "null"],
            "description": "Gregorian year or approximate historical epoch."
        },
        "source_type": {
            "type": "string",
            "enum": ["puya", "chronicle", "dictionary", "fieldwork", "corpus", "academic_paper", "other"],
            "description": "Typology of the bibliographic source."
        },
        "publisher": {
            "type": ["string", "null"]
        },
        "archive_or_repository": {
            "type": ["string", "null"],
            "description": "Archival institution, palace library, or physical location."
        },
        "url_or_doi": {
            "type": ["string", "null"]
        },
        "description": {
            "type": ["string", "null"]
        },
        "metadata": {
            "type": "object"
        }
    },
    "additionalProperties": False
}

SENSE_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "LexicalSense",
    "type": "object",
    "required": ["id", "definition_en", "part_of_speech"],
    "properties": {
        "id": {
            "type": "string",
            "pattern": r"^(MEI-SNS-\d{7}|MEI-LEX-\d{7}-S\d{2})$",
            "description": "Unique stable identifier for the sense."
        },
        "definition_en": {
            "type": "string",
            "minLength": 1,
            "description": "Primary English definition."
        },
        "definition_mni": {
            "type": ["string", "null"],
            "description": "Meitei Mayek definition."
        },
        "part_of_speech": {
            "type": "string",
            "minLength": 1,
            "description": "Grammatical category (e.g. noun, verb, adjective, classifier)."
        },
        "domain": {
            "type": ["string", "null"],
            "description": "Semantic domain (e.g. flora, fauna, agriculture, ritual, daily)."
        },
        "examples": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["meitei", "roman", "english"],
                "properties": {
                    "meitei": {"type": "string"},
                    "roman": {"type": "string"},
                    "english": {"type": "string"},
                    "source_ref": {"type": ["string", "null"]}
                }
            }
        },
        "notes": {
            "type": ["string", "null"]
        }
    },
    "additionalProperties": False
}

REVIEWER_ATTRIBUTION_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ReviewerAttribution",
    "type": "object",
    "required": ["reviewer_id", "review_date"],
    "properties": {
        "reviewer_id": {
            "type": "string",
            "minLength": 1,
            "description": "Unique identifier of the reviewer or native speaker validator."
        },
        "review_date": {
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}(T.*)?$",
            "description": "Date of verification in ISO 8601 format."
        },
        "notes": {
            "type": ["string", "null"]
        }
    },
    "additionalProperties": False
}

LEXICAL_ENTRY_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "LexicalEntryRecord",
    "type": "object",
    "required": [
        "id",
        "headword_meitei",
        "headword_roman",
        "status",
        "senses"
    ],
    "properties": {
        "id": {
            "type": "string",
            "pattern": r"^MEI-LEX-\d{7}$",
            "description": "Unique stable identifier for the entry (e.g. MEI-LEX-0000001)."
        },
        "headword_meitei": {
            "type": "string",
            "minLength": 1,
            "description": "Canonical lemma in Meitei Mayek."
        },
        "headword_roman": {
            "type": "string",
            "minLength": 1,
            "description": "Standardized Latin transliteration of the headword."
        },
        "headword_bengali": {
            "type": ["string", "null"],
            "description": "Traditional/historical representation in Eastern Nagari / Bengali script."
        },
        "phonetic_ipa": {
            "type": ["string", "null"],
            "description": "International Phonetic Alphabet transcription."
        },
        "status": {
            "type": "string",
            "enum": list(ALL_ALLOWED_STATUSES),
            "description": "Controlled status value."
        },
        "source_id": {
            "type": ["string", "null"],
            "description": "References MEI-SRC-xxxxxx."
        },
        "citation_locator": {
            "type": ["string", "null"],
            "description": "Exact folio, page, or line reference in source."
        },
        "reviewer_attribution": {
            "type": ["object", "null"]
        },
        "senses": {
            "type": "array",
            "minItems": 1,
            "items": SENSE_SCHEMA
        },
        "etymology": {
            "type": ["string", "null"]
        },
        "created_at": {
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}(T.*)?$"
        },
        "updated_at": {
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}(T.*)?$"
        }
    },
    "additionalProperties": False
}

VARIANT_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "SpellingVariantRecord",
    "type": "object",
    "required": [
        "id",
        "entry_id",
        "variant_form",
        "script",
        "status"
    ],
    "properties": {
        "id": {
            "type": "string",
            "pattern": r"^MEI-VAR-\d{7}$",
            "description": "Unique stable identifier for variant (e.g. MEI-VAR-0000001)."
        },
        "entry_id": {
            "type": "string",
            "pattern": r"^MEI-LEX-\d{7}$",
            "description": "Identifier of the primary lexical entry this variant maps to."
        },
        "variant_form": {
            "type": "string",
            "minLength": 1,
            "description": "The spelling or orthographic variation string."
        },
        "script": {
            "type": "string",
            "enum": ["meitei_mayek", "bengali", "latin", "other"],
            "description": "Script system of the variant."
        },
        "variant_type": {
            "type": "string",
            "enum": ["historical", "dialectal", "colloquial", "archaic", "orthographic", "transcription"],
            "description": "Linguistic classification of the variation."
        },
        "status": {
            "type": "string",
            "enum": list(ALL_ALLOWED_STATUSES)
        },
        "source_id": {
            "type": ["string", "null"],
            "description": "References MEI-SRC-xxxxxx."
        },
        "citation_locator": {
            "type": ["string", "null"]
        },
        "reviewer_attribution": {
            "type": ["object", "null"]
        },
        "notes": {
            "type": ["string", "null"]
        }
    },
    "additionalProperties": False
}

GLOSS_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "TranslationGlossRecord",
    "type": "object",
    "required": [
        "id",
        "entry_id",
        "target_language",
        "gloss",
        "status"
    ],
    "properties": {
        "id": {
            "type": "string",
            "pattern": r"^MEI-GLS-\d{7}$",
            "description": "Unique stable identifier for the gloss (e.g. MEI-GLS-0000001)."
        },
        "entry_id": {
            "type": "string",
            "pattern": r"^MEI-LEX-\d{7}$",
            "description": "Identifier of the primary lexical entry."
        },
        "sense_id": {
            "type": ["string", "null"],
            "description": "Specific sense ID if the gloss maps to a particular sense."
        },
        "target_language": {
            "type": "string",
            "minLength": 2,
            "description": "ISO 639-1 / 639-3 language code (e.g. 'en', 'hi', 'bn', 'as')."
        },
        "gloss": {
            "type": "string",
            "minLength": 1,
            "description": "The translated word or phrase."
        },
        "gloss_type": {
            "type": "string",
            "enum": ["literal", "idiomatic", "cultural_equivalent", "descriptive"],
            "description": "Character of the translation equivalence."
        },
        "status": {
            "type": "string",
            "enum": list(ALL_ALLOWED_STATUSES)
        },
        "source_id": {
            "type": ["string", "null"],
            "description": "References MEI-SRC-xxxxxx."
        },
        "citation_locator": {
            "type": ["string", "null"]
        },
        "reviewer_attribution": {
            "type": ["object", "null"]
        },
        "notes": {
            "type": ["string", "null"]
        }
    },
    "additionalProperties": False
}

REVIEW_RECORD_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "CommunityReviewRecord",
    "type": "object",
    "required": [
        "id",
        "target_id",
        "target_type",
        "decision",
        "reviewer_role",
        "reviewer_id",
        "review_date"
    ],
    "properties": {
        "id": {
            "type": "string",
            "pattern": r"^MEI-REV-\d{7}$",
            "description": "Unique stable identifier for review (e.g. MEI-REV-0000001)."
        },
        "target_id": {
            "type": "string",
            "minLength": 1,
            "description": "Identifier of the reviewed record (e.g. MEI-LEX-0000001)."
        },
        "target_type": {
            "type": "string",
            "enum": [
                "lexical_entry",
                "candidate_entry",
                "variant",
                "gloss",
                "grammar_record",
                "book_passage"
            ],
            "description": "Subsystem typology of reviewed target."
        },
        "decision": {
            "type": "string",
            "enum": [
                "ACCEPTED", "CORRECTED", "REJECTED", "AWAITING_REVIEW",
                "accepted", "corrected", "rejected", "awaiting_review"
            ],
            "description": "Review decision."
        },
        "reviewer_role": {
            "type": "string",
            "enum": [
                "NATIVE_SPEAKER", "LINGUIST", "CULTURAL_AUTHORITY",
                "COMMUNITY_ELDER", "ACADEMIC_EDITOR", "CONTRIBUTOR",
                "native_speaker", "linguist", "cultural_authority",
                "community_elder", "academic_editor", "contributor"
            ],
            "description": "Role and qualification of the reviewer."
        },
        "reviewer_id": {
            "type": "string",
            "minLength": 1,
            "description": "Reviewer pseudonym or stable institutional ID."
        },
        "review_date": {
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}(T.*)?$",
            "description": "Date of review in ISO 8601 format."
        },
        "source_id": {
            "type": ["string", "null"],
            "description": "Referenced bibliographic source ID if primary citation inspected."
        },
        "source_locator": {
            "type": ["string", "null"],
            "description": "Precise citation locator (page, folio, line)."
        },
        "previous_value": {
            "type": ["object", "string", "null"],
            "description": "Value or state of target fields prior to review."
        },
        "corrected_value": {
            "type": ["object", "string", "null"],
            "description": "Corrected value or state after review (for CORRECTED decision)."
        },
        "revision_history": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["date", "reviewer_id"],
                "properties": {
                    "date": {"type": "string"},
                    "reviewer_id": {"type": "string"},
                    "comment": {"type": "string"}
                }
            },
            "description": "Chronological history of revisions."
        },
        "rationale": {
            "type": ["string", "null"],
            "description": "Philological or linguistic reasoning for the decision."
        },
        "cultural_sensitivity_checked": {
            "type": "boolean",
            "description": "Confirmation that cultural sensitivity guidelines were respected."
        },
        "consent_confirmed": {
            "type": "boolean",
            "description": "Confirmation of informant or reviewer consent."
        },
        "license": {
            "type": "string",
            "description": "License under which review contribution is published."
        }
    },
    "additionalProperties": False
}

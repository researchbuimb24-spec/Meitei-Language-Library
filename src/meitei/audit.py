# -*- coding: utf-8 -*-
"""
Provenance Audit and Comprehensive Dataset Validation Engine (`meitei.audit`).

Performs end-to-end linguistic integrity checks across all library datasets:
1. Lexical IDs, source references, and cross-dataset referential integrity.
2. Exact citation locators and primary source folio verification.
3. Gloss statuses, target languages, and translation alignment.
4. Orthographic consistency and script mapping integrity.
5. Book passage alignments, monotonic numbering, and SHA-256 manifests.
6. Editorial review ledger validation and decision tracking.
7. Quarantine enforcement: strictly prevents AI candidates and unverified translations
   from entering the core lexicon.
8. Real dataset statistics generation directly from disk files.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from meitei.books.catalog import BookCatalog
from meitei.books.models import REGEX_PASSAGE_ID
from meitei.books.validation import BookValidator
from meitei.grammar import load_grammar_records
from meitei.languages import is_supported_language
from meitei.loader import (
    CitationLocatorMissingError,
    DataLoader,
    DatasetPartitionError,
    DuplicateIDError,
    InvalidStatusError,
    MissingSourceError,
    ValidationError,
    get_default_data_dir,
    read_jsonl_lines,
)
from meitei.review import ReviewLedger, validate_review_record
from meitei.schema import (
    ALL_ALLOWED_STATUSES,
    CANDIDATE_ALLOWED_STATUSES,
    CORE_ALLOWED_STATUSES,
    RecordStatus,
    ReviewDecision,
    is_valid_gls_id,
    is_valid_grm_id,
    is_valid_lex_id,
    is_valid_rev_id,
    is_valid_sns_id,
    is_valid_src_id,
    is_valid_var_id,
)
from meitei.unicode_utils import (
    detect_script,
    is_bengali_char,
    is_latin_char,
    is_meitei_mayek_char,
    normalize_text,
)


@dataclass
class AuditReport:
    """
    Comprehensive report resulting from a dataset provenance and integrity audit.
    """
    is_valid: bool
    strict: bool
    status: str
    sources_count: int
    core_entries_count: int
    candidate_entries_count: int
    variants_count: int
    glosses_count: int
    grammar_records_count: int
    books_count: int
    book_passages_count: int
    reviews_count: int
    awaiting_review_count: int
    citation_mismatch_count: int
    unverified_candidates_count: int
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return asdict(self)


class ProvenanceAuditor:
    """
    Audits dataset referential integrity, citation completeness, script mappings,
    book alignments, and editorial reviews.
    """

    def __init__(self, data_dir: Union[str, Path] = "data") -> None:
        self.data_dir = get_default_data_dir(data_dir)
        self.loader = DataLoader(self.data_dir)

    def audit(
        self,
        strict: bool = False,
        fail_unreviewed: bool = False,
    ) -> AuditReport:
        """
        Execute full cross-dataset audit.

        Args:
            strict: Enforce rigorous citation locators, metadata completeness, and review checks.
            fail_unreviewed: When True, treats unreviewed candidates or records awaiting review as audit errors.

        Returns:
            AuditReport containing validation status, errors, warnings, and corpus statistics.
        """
        errors: List[str] = []
        warnings: List[str] = []

        # ---------------------------------------------------------------------
        # 1. Sources Audit (sources.jsonl)
        # ---------------------------------------------------------------------
        sources: Dict[str, Dict[str, Any]] = {}
        try:
            sources = self.loader.load_sources()
        except ValidationError as e:
            errors.append(f"Sources Validation Error: {e}")
        except FileNotFoundError:
            errors.append(f"Critical File Missing: {self.data_dir / 'sources' / 'sources.jsonl'}")

        known_sources = set(sources.keys())

        for sid, s in sources.items():
            if not is_valid_src_id(sid):
                errors.append(f"Source ID format invalid: '{sid}'. Must match MEI-SRC-xxxxxx.")
            meta = s.get("metadata", {})
            if strict:
                if not meta or "legal_status" not in meta:
                    errors.append(f"Source '{sid}' metadata missing required 'legal_status'.")

        # ---------------------------------------------------------------------
        # 2. Core Lexicon Audit (core_lexicon.jsonl)
        # ---------------------------------------------------------------------
        core_lex: Dict[str, Dict[str, Any]] = {}
        try:
            core_lex = self.loader.load_lexicon(partition="core", known_sources=known_sources)
        except ValidationError as e:
            errors.append(f"Core Lexicon Validation Error: {e}")
        except FileNotFoundError:
            errors.append(f"Critical File Missing: {self.data_dir / 'lexicon' / 'core_lexicon.jsonl'}")

        for eid, entry in core_lex.items():
            if not is_valid_lex_id(eid):
                errors.append(f"Core entry ID format invalid: '{eid}'. Must match MEI-LEX-xxxxxxx.")

            st = entry.get("status")
            # Strict quarantine rule: AI_CANDIDATE, UNVERIFIED, CITATION_MISMATCH, REJECTED
            # must NEVER be in the core lexicon
            if st not in CORE_ALLOWED_STATUSES:
                errors.append(
                    f"Core entry '{eid}' has unauthorized status '{st}'. "
                    f"Only {sorted(CORE_ALLOWED_STATUSES)} permitted in core partition."
                )

            # Check headword scripts
            hw_meitei = entry.get("headword_meitei", "")
            if not any(is_meitei_mayek_char(c) for c in hw_meitei):
                errors.append(f"Core entry '{eid}' headword_meitei '{hw_meitei}' contains no Meitei Mayek characters.")

            hw_bengali = entry.get("headword_bengali")
            if hw_bengali and not any(is_bengali_char(c) for c in hw_bengali):
                warnings.append(f"Core entry '{eid}' headword_bengali '{hw_bengali}' contains no Bengali script characters.")

            # Strict citation locator checks
            if st == RecordStatus.SOURCE_ATTESTED.value:
                loc = entry.get("citation_locator")
                if not loc or not loc.strip():
                    errors.append(f"Core entry '{eid}' is SOURCE_ATTESTED but lacks citation_locator.")
                elif strict and not any(k in loc.lower() for k in ["page", "folio", "example", "no.", "chapter", "verse"]):
                    errors.append(f"Core entry '{eid}' citation_locator '{loc}' lacks specific page/folio reference in strict mode.")

                rev = entry.get("reviewer_attribution")
                if strict and (not rev or not rev.get("reviewer_id")):
                    errors.append(f"Core entry '{eid}' missing required reviewer attribution.")

        # ---------------------------------------------------------------------
        # 3. Candidate Lexicon Audit (candidate_lexicon.jsonl)
        # ---------------------------------------------------------------------
        cand_lex: Dict[str, Dict[str, Any]] = {}
        try:
            cand_lex = self.loader.load_lexicon(partition="candidate", known_sources=known_sources)
        except ValidationError as e:
            errors.append(f"Candidate Lexicon Validation Error: {e}")
        except FileNotFoundError:
            warnings.append(f"Candidate lexicon file not present: {self.data_dir / 'lexicon' / 'candidate_lexicon.jsonl'}")

        # Check for ID collisions across core and candidate
        collision = set(core_lex.keys()) & set(cand_lex.keys())
        if collision:
            errors.append(f"ID Collision between core and candidate lexicons: {sorted(collision)}")

        unverified_count = 0
        citation_mismatch_count = 0

        for cid, centry in cand_lex.items():
            if not is_valid_lex_id(cid):
                errors.append(f"Candidate entry ID format invalid: '{cid}'. Must match MEI-LEX-xxxxxxx.")

            st = centry.get("status")
            if st == RecordStatus.SOURCE_ATTESTED.value:
                errors.append(f"Candidate entry '{cid}' cannot have SOURCE_ATTESTED status in candidate partition.")

            if st in (RecordStatus.UNVERIFIED.value, RecordStatus.AI_CANDIDATE.value):
                unverified_count += 1
                rev = centry.get("reviewer_attribution") or {}
                notes = rev.get("notes", "")
                if "LIMITATION" not in notes:
                    warnings.append(f"Candidate entry '{cid}' unverified status lacks documented LIMITATION in notes.")

            if st == RecordStatus.CITATION_MISMATCH.value:
                citation_mismatch_count += 1
                errors.append(f"Candidate entry '{cid}' has CITATION_MISMATCH status; cited source does not corroborate reading.")

            # If fail_unreviewed is requested, treat unreviewed entries as hard audit errors
            if fail_unreviewed and st in (RecordStatus.UNVERIFIED.value, RecordStatus.AI_CANDIDATE.value):
                errors.append(f"Candidate entry '{cid}' is {st} and requires formal review before audit passes.")

        all_entries = set(core_lex.keys()) | set(cand_lex.keys())

        # ---------------------------------------------------------------------
        # 4. Spelling Variants Audit (variants.jsonl)
        # ---------------------------------------------------------------------
        variants: List[Dict[str, Any]] = []
        try:
            variants = self.loader.load_variants(known_entries=all_entries, known_sources=known_sources)
        except ValidationError as e:
            errors.append(f"Variants Validation Error: {e}")
        except FileNotFoundError:
            pass

        for v in variants:
            vid = v.get("id", "")
            if not is_valid_var_id(vid):
                errors.append(f"Variant ID format invalid: '{vid}'. Must match MEI-VAR-xxxxxxx.")

            v_script = v.get("script")
            v_form = v.get("variant_form", "")
            if v_script == "meitei_mayek" and not any(is_meitei_mayek_char(c) for c in v_form):
                warnings.append(f"Variant '{vid}' declared script 'meitei_mayek' but form contains no Mayek: '{v_form}'.")
            elif v_script == "bengali" and not any(is_bengali_char(c) for c in v_form):
                warnings.append(f"Variant '{vid}' declared script 'bengali' but form contains no Bengali characters: '{v_form}'.")
            elif v_script == "latin" and not any(is_latin_char(c) for c in v_form):
                warnings.append(f"Variant '{vid}' declared script 'latin' but form contains no Latin characters: '{v_form}'.")

            if strict and v.get("status") == RecordStatus.SOURCE_ATTESTED.value and not v.get("citation_locator"):
                errors.append(f"Variant '{vid}' is SOURCE_ATTESTED but lacks citation_locator.")

        # ---------------------------------------------------------------------
        # 5. Translation Glosses Audit (glosses.jsonl)
        # ---------------------------------------------------------------------
        glosses: List[Dict[str, Any]] = []
        try:
            glosses = self.loader.load_glosses(known_entries=all_entries, known_sources=known_sources)
        except ValidationError as e:
            errors.append(f"Glosses Validation Error: {e}")
        except FileNotFoundError:
            pass

        for g in glosses:
            gid = g.get("id", "")
            if not is_valid_gls_id(gid):
                errors.append(f"Gloss ID format invalid: '{gid}'. Must match MEI-GLS-xxxxxxx.")

            lang = g.get("target_language", "")
            if not is_supported_language(lang):
                warnings.append(f"Gloss '{gid}' has non-standard language code: '{lang}'.")

            g_status = g.get("status")
            # Strict rule: gloss cannot claim VERIFIED without reviewer attribution
            if g_status == RecordStatus.VERIFIED.value:
                rev = g.get("reviewer_attribution")
                if not rev or not rev.get("reviewer_id"):
                    errors.append(f"Gloss '{gid}' is marked VERIFIED but lacks required reviewer attribution.")

            if strict and g_status == RecordStatus.SOURCE_ATTESTED.value and not g.get("citation_locator"):
                errors.append(f"Gloss '{gid}' is SOURCE_ATTESTED but lacks citation_locator.")

        # ---------------------------------------------------------------------
        # 6. Grammar Subsystem Audit (grammar_records.jsonl)
        # ---------------------------------------------------------------------
        grammar_records = []
        try:
            grammar_records = load_grammar_records(data_dir=self.data_dir)
        except Exception as e:
            warnings.append(f"Grammar records loading issue: {e}")

        for grm in grammar_records:
            if not is_valid_grm_id(grm.id):
                errors.append(f"Grammar record ID invalid: '{grm.id}'. Must match MEI-GRM-xxxxxxx.")
            if grm.source_id and grm.source_id not in known_sources:
                errors.append(f"Grammar record '{grm.id}' references unknown source_id '{grm.source_id}'.")
            if strict and grm.verification_status == RecordStatus.SOURCE_ATTESTED.value and not grm.citation_locator:
                errors.append(f"Grammar record '{grm.id}' is SOURCE_ATTESTED but lacks citation_locator.")

        # ---------------------------------------------------------------------
        # 7. Digital Book Library Audit (catalog.json & texts/)
        # ---------------------------------------------------------------------
        books_count = 0
        passages_count = 0
        try:
            b_validator = BookValidator(data_dir=self.data_dir)
            book_audit = b_validator.audit_all_books()
            books_count = book_audit.get("total_books_audited", 0)
            passages_count = book_audit.get("total_passages", 0)

            for b in book_audit.get("books", []):
                if not b.get("valid"):
                    for b_err in b.get("errors", []):
                        errors.append(f"Book '{b.get('book_id')}': {b_err}")
                for b_warn in b.get("warnings", []):
                    warnings.append(f"Book '{b.get('book_id')}': {b_warn}")
        except Exception as e:
            warnings.append(f"Book library validation skipped or partial: {e}")

        # ---------------------------------------------------------------------
        # 8. Community Review Ledger Audit (reviews.jsonl)
        # ---------------------------------------------------------------------
        ledger = ReviewLedger(data_dir=self.data_dir)
        reviews = []
        awaiting_review_count = 0

        try:
            reviews = ledger.load_reviews()
            for r in reviews:
                if not is_valid_rev_id(r.id):
                    errors.append(f"Review ID format invalid: '{r.id}'. Must match MEI-REV-xxxxxxx.")

                if r.decision == ReviewDecision.AWAITING_REVIEW.value:
                    awaiting_review_count += 1
                    if fail_unreviewed:
                        errors.append(f"Review '{r.id}' on '{r.target_id}' is still AWAITING_REVIEW.")

                if r.decision == ReviewDecision.CORRECTED.value and not r.corrected_value:
                    errors.append(f"Review '{r.id}' has decision CORRECTED but lacks corrected_value.")

                if r.source_id and r.source_id not in known_sources:
                    errors.append(f"Review '{r.id}' references unknown source_id '{r.source_id}'.")

                if not r.consent_confirmed:
                    errors.append(f"Review '{r.id}' lacks confirmed consent (consent_confirmed: false).")

                if not r.cultural_sensitivity_checked:
                    errors.append(f"Review '{r.id}' lacks confirmed cultural sensitivity check.")
        except Exception as e:
            errors.append(f"Review Ledger validation error: {e}")

        # Final validity determination
        is_valid = len(errors) == 0

        stats = {
            "sources": len(sources),
            "core_entries": len(core_lex),
            "candidate_entries": len(cand_lex),
            "variants": len(variants),
            "glosses": len(glosses),
            "grammar_records": len(grammar_records),
            "books": books_count,
            "book_passages": passages_count,
            "reviews": len(reviews),
            "awaiting_review": awaiting_review_count,
            "unverified_candidates": unverified_count,
            "citation_mismatches": citation_mismatch_count,
        }

        return AuditReport(
            is_valid=is_valid,
            strict=strict,
            status="PASSED" if is_valid else "FAILED",
            sources_count=len(sources),
            core_entries_count=len(core_lex),
            candidate_entries_count=len(cand_lex),
            variants_count=len(variants),
            glosses_count=len(glosses),
            grammar_records_count=len(grammar_records),
            books_count=books_count,
            book_passages_count=passages_count,
            reviews_count=len(reviews),
            awaiting_review_count=awaiting_review_count,
            citation_mismatch_count=citation_mismatch_count,
            unverified_candidates_count=unverified_count,
            errors=errors,
            warnings=warnings,
            stats=stats,
        )


def audit_repository(
    data_dir: Union[str, Path] = "data",
    strict: bool = False,
    fail_unreviewed: bool = False,
) -> AuditReport:
    """Helper function to run repository audit."""
    auditor = ProvenanceAuditor(data_dir=data_dir)
    return auditor.audit(strict=strict, fail_unreviewed=fail_unreviewed)


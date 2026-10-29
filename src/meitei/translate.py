# -*- coding: utf-8 -*-
"""
Translation and Cross-Lingual Glossing for the Meitei Language Library (meitei).

Provides deterministic, citation-backed bidirectional translation lookups
between Meitei (Meitei Mayek, Bengali script, Romanization) and target/source
languages (English, Hindi, Bengali, Assamese) based strictly on source-attested
glosses and peer-reviewed dictionary senses.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from meitei.languages import (
    canonicalize_language_code,
    get_supported_codes_summary,
    is_supported_language,
)
from meitei.loader import DataLoader
from meitei.schema import CORE_ALLOWED_STATUSES, RecordStatus
from meitei.unicode_utils import detect_script, normalize_text


@dataclass
class TranslationResult:
    """
    Structured cross-lingual translation match result.

    Attributes:
        query: Original search string.
        source_language: Canonical source language code (e.g. en, mni, hi).
        target_language: Canonical target language code (e.g. mni, en, hi).
        target_text: Translated lemma, gloss, or definition.
        target_roman: Roman transliteration of target if target is Meitei.
        target_bengali: Historical Bengali-script form if target is Meitei.
        entry_id: Stable identifier of the associated lexical entry.
        sense_id: Associated sense identifier if applicable.
        part_of_speech: Grammatical category (noun, verb, numeral, etc.).
        definition: English definition of the lexical sense.
        gloss: Exact translation gloss matched.
        gloss_type: Typology of gloss (literal, dynamic, cognate, contextual).
        status: Verification and attestation status (e.g. SOURCE_ATTESTED, UNVERIFIED).
        citations: List of source citations, folios, or locators.
        reviewer_attribution: Peer review and attribution metadata.
        match_score: Deterministic relevance score.
    """
    query: str
    source_language: str
    target_language: str
    target_text: str
    target_roman: Optional[str] = None
    target_bengali: Optional[str] = None
    entry_id: str = ""
    sense_id: Optional[str] = None
    part_of_speech: Optional[str] = None
    definition: Optional[str] = None
    gloss: Optional[str] = None
    gloss_type: Optional[str] = None
    status: str = "UNVERIFIED"
    citations: List[Dict[str, Any]] = field(default_factory=list)
    reviewer_attribution: Optional[Dict[str, Any]] = None
    match_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert translation result to JSON-serializable dictionary."""
        return asdict(self)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


def translate(
    query: str,
    from_lang: str = "en",
    to_lang: str = "mni",
    verified_only: bool = False,
    data_dir: Union[str, Path] = "data",
) -> List[TranslationResult]:
    """
    Execute translation lookup between Meitei and supported cross-lingual targets.

    Args:
        query: Search term or word to translate.
        from_lang: Source language code ('en', 'mni', 'hi', 'bn', 'as', or 'auto').
        to_lang: Target language code ('mni', 'en', 'hi', 'bn', 'as').
        verified_only: When True, excludes unverified candidates and non-attested claims.
        data_dir: Root directory of data files.

    Returns:
        List of TranslationResult objects ordered by relevance score and status.

    Raises:
        ValueError: If an unsupported or invalid language code is specified.
    """
    if not is_supported_language(from_lang, allow_auto=True):
        valid = get_supported_codes_summary()
        raise ValueError(
            f"Invalid or unsupported source language '{from_lang}'. "
            f"Supported languages: {valid} (or 'auto')."
        )

    if not is_supported_language(to_lang, allow_auto=False):
        valid = get_supported_codes_summary()
        raise ValueError(
            f"Invalid or unsupported target language '{to_lang}'. "
            f"Supported languages: {valid}."
        )

    q_norm = normalize_text(query).strip()
    if not q_norm:
        return []

    q_lower = q_norm.lower()

    # Resolve 'auto' language detection if needed
    source_code = canonicalize_language_code(from_lang)
    if source_code == "auto":
        script = detect_script(q_norm)
        if script == "MEITEI_MAYEK":
            source_code = "mni"
        elif script == "BENGALI":
            source_code = "bn"
        else:
            source_code = "en"

    target_code = canonicalize_language_code(to_lang)
    assert source_code is not None
    assert target_code is not None

    # Load authentic datasets safely without crashing on missing data
    loader = DataLoader(data_dir)
    try:
        sources = loader.load_sources()
    except Exception:
        sources = {}
    known_sources = set(sources.keys())

    try:
        core_lex = loader.load_lexicon(partition="core", known_sources=known_sources)
    except Exception:
        core_lex = {}

    cand_lex = {}
    if not verified_only:
        try:
            cand_lex = loader.load_lexicon(partition="candidate", known_sources=known_sources)
        except Exception:
            cand_lex = {}

    all_entries = {**core_lex, **cand_lex}
    if not all_entries:
        return []

    try:
        variants = loader.load_variants(known_entries=set(all_entries.keys()), known_sources=known_sources)
    except Exception:
        variants = []

    try:
        glosses = loader.load_glosses(known_entries=set(all_entries.keys()), known_sources=known_sources)
    except Exception:
        glosses = []

    results: List[TranslationResult] = []
    seen_keys: Set[Tuple[str, str, Optional[str]]] = set()

    def add_result(res: TranslationResult) -> None:
        key = (res.entry_id, res.target_text, res.sense_id)
        if key in seen_keys:
            return
        seen_keys.add(key)
        results.append(res)

    # -------------------------------------------------------------------------
    # Scenario A: Foreign Language -> Meitei (e.g. en -> mni, hi -> mni, bn -> mni)
    # -------------------------------------------------------------------------
    if source_code != "mni" and target_code == "mni":
        # 1. Check translation glosses table
        for g in glosses:
            if g.get("target_language") != source_code:
                continue
            if verified_only and g.get("status") not in CORE_ALLOWED_STATUSES:
                continue

            g_text = normalize_text(g.get("gloss", ""))
            g_lower = g_text.lower()
            score = 0.0

            if q_lower == g_lower or q_norm == g_text:
                score = 100.0
            elif re.search(r"\b" + re.escape(q_lower) + r"\b", g_lower):
                score = 85.0
            elif g_lower.startswith(q_lower) or g_text.startswith(q_norm):
                score = 70.0
            elif q_lower in g_lower:
                score = 50.0

            if score > 0.0:
                entry = all_entries.get(g["entry_id"])
                if not entry:
                    continue
                if verified_only and entry.get("status") not in CORE_ALLOWED_STATUSES:
                    continue

                # Match sense if available
                sense_match = None
                for s in entry.get("senses", []):
                    if s.get("id") == g.get("sense_id"):
                        sense_match = s
                        break
                if not sense_match and entry.get("senses"):
                    sense_match = entry["senses"][0]

                # If either entry or gloss is UNVERIFIED, overall status is UNVERIFIED
                entry_status = entry.get("status", "UNVERIFIED")
                gloss_status = g.get("status", "UNVERIFIED")
                effective_status = (
                    RecordStatus.UNVERIFIED.value
                    if (entry_status == RecordStatus.UNVERIFIED.value or gloss_status == RecordStatus.UNVERIFIED.value)
                    else entry_status
                )

                # Prepare citation
                cits: List[Dict[str, Any]] = []
                if g.get("source_id"):
                    cits.append({
                        "source_id": g["source_id"],
                        "citation_locator": g.get("citation_locator"),
                        "notes": g.get("notes"),
                    })
                elif entry.get("source_id"):
                    cits.append({
                        "source_id": entry["source_id"],
                        "citation_locator": entry.get("citation_locator"),
                        "notes": entry.get("reviewer_attribution", {}).get("notes") if isinstance(entry.get("reviewer_attribution"), dict) else None,
                    })

                add_result(
                    TranslationResult(
                        query=query,
                        source_language=source_code,
                        target_language="mni",
                        target_text=entry.get("headword_meitei", ""),
                        target_roman=entry.get("headword_roman"),
                        target_bengali=entry.get("headword_bengali"),
                        entry_id=entry.get("id", ""),
                        sense_id=sense_match.get("id") if sense_match else None,
                        part_of_speech=sense_match.get("part_of_speech") if sense_match else None,
                        definition=sense_match.get("definition_en") if sense_match else None,
                        gloss=g.get("gloss"),
                        gloss_type=g.get("gloss_type"),
                        status=effective_status,
                        citations=cits,
                        reviewer_attribution=g.get("reviewer_attribution") or entry.get("reviewer_attribution"),
                        match_score=score,
                    )
                )

        # 2. Check English definitions if source is English
        if source_code == "en":
            for eid, entry in all_entries.items():
                if verified_only and entry.get("status") not in CORE_ALLOWED_STATUSES:
                    continue

                for s in entry.get("senses", []):
                    defn = normalize_text(s.get("definition_en", ""))
                    defn_lower = defn.lower()
                    score = 0.0

                    if q_lower == defn_lower:
                        score = 80.0
                    elif re.search(r"\b" + re.escape(q_lower) + r"\b", defn_lower):
                        score = 65.0
                    elif q_lower in defn_lower:
                        score = 40.0

                    if score > 0.0:
                        cits = []
                        if entry.get("source_id"):
                            cits.append({
                                "source_id": entry["source_id"],
                                "citation_locator": entry.get("citation_locator"),
                            })

                        add_result(
                            TranslationResult(
                                query=query,
                                source_language="en",
                                target_language="mni",
                                target_text=entry.get("headword_meitei", ""),
                                target_roman=entry.get("headword_roman"),
                                target_bengali=entry.get("headword_bengali"),
                                entry_id=entry.get("id", ""),
                                sense_id=s.get("id"),
                                part_of_speech=s.get("part_of_speech"),
                                definition=s.get("definition_en"),
                                gloss=None,
                                gloss_type="definition_match",
                                status=entry.get("status", "UNVERIFIED"),
                                citations=cits,
                                reviewer_attribution=entry.get("reviewer_attribution"),
                                match_score=score,
                            )
                        )

    # -------------------------------------------------------------------------
    # Scenario B: Meitei -> Foreign Language (e.g. mni -> en, mni -> hi, mni -> bn)
    # -------------------------------------------------------------------------
    elif source_code == "mni" and target_code != "mni":
        # Group variants and glosses by entry_id
        entry_variants: Dict[str, List[Dict[str, Any]]] = {}
        for v in variants:
            entry_variants.setdefault(v["entry_id"], []).append(v)

        entry_glosses: Dict[str, List[Dict[str, Any]]] = {}
        for g in glosses:
            entry_glosses.setdefault(g["entry_id"], []).append(g)

        for eid, entry in all_entries.items():
            if verified_only and entry.get("status") not in CORE_ALLOWED_STATUSES:
                continue

            hw_meitei = entry.get("headword_meitei", "")
            hw_roman = entry.get("headword_roman", "")
            hw_bengali = entry.get("headword_bengali") or ""

            best_entry_score = 0.0

            # Exact headword match
            if q_norm == hw_meitei or q_lower == hw_roman.lower() or (hw_bengali and q_norm == hw_bengali):
                best_entry_score = 100.0
            elif hw_roman.lower().startswith(q_lower) or hw_meitei.startswith(q_norm):
                best_entry_score = 70.0
            elif q_lower in hw_roman.lower() or q_norm in hw_meitei:
                best_entry_score = 50.0

            # Variant match
            for v in entry_variants.get(eid, []):
                v_form = normalize_text(v.get("variant_form", ""))
                if q_norm == v_form or q_lower == v_form.lower():
                    best_entry_score = max(best_entry_score, 90.0)

            if best_entry_score > 0.0:
                # Find target glosses
                matched_target_glosses = [
                    g for g in entry_glosses.get(eid, [])
                    if g.get("target_language") == target_code
                ]
                if verified_only:
                    matched_target_glosses = [
                        g for g in matched_target_glosses
                        if g.get("status") in CORE_ALLOWED_STATUSES
                    ]

                if matched_target_glosses:
                    for tg in matched_target_glosses:
                        cits = []
                        if tg.get("source_id"):
                            cits.append({
                                "source_id": tg["source_id"],
                                "citation_locator": tg.get("citation_locator"),
                                "notes": tg.get("notes"),
                            })

                        add_result(
                            TranslationResult(
                                query=query,
                                source_language="mni",
                                target_language=target_code,
                                target_text=tg.get("gloss", ""),
                                target_roman=None,
                                target_bengali=None,
                                entry_id=eid,
                                sense_id=tg.get("sense_id"),
                                part_of_speech=None,
                                definition=None,
                                gloss=tg.get("gloss"),
                                gloss_type=tg.get("gloss_type"),
                                status=tg.get("status", "UNVERIFIED"),
                                citations=cits,
                                reviewer_attribution=tg.get("reviewer_attribution") or entry.get("reviewer_attribution"),
                                match_score=best_entry_score,
                            )
                        )
                elif target_code == "en":
                    # Fallback to English definitions from senses
                    for s in entry.get("senses", []):
                        defn = s.get("definition_en", "")
                        cits = []
                        if entry.get("source_id"):
                            cits.append({
                                "source_id": entry["source_id"],
                                "citation_locator": entry.get("citation_locator"),
                            })

                        add_result(
                            TranslationResult(
                                query=query,
                                source_language="mni",
                                target_language="en",
                                target_text=defn,
                                target_roman=None,
                                target_bengali=None,
                                entry_id=eid,
                                sense_id=s.get("id"),
                                part_of_speech=s.get("part_of_speech"),
                                definition=defn,
                                gloss=None,
                                gloss_type="definition",
                                status=entry.get("status", "UNVERIFIED"),
                                citations=cits,
                                reviewer_attribution=entry.get("reviewer_attribution"),
                                match_score=best_entry_score,
                            )
                        )

    # Deterministic ranking:
    # 1. Highest score first
    # 2. SOURCE_ATTESTED prioritized over UNVERIFIED
    # 3. Canonical entry_id lexicographically
    def sort_key(r: TranslationResult) -> Tuple[float, int, str]:
        prio = 0 if r.status == RecordStatus.SOURCE_ATTESTED.value else (1 if r.status == RecordStatus.VERIFIED.value else 2)
        return (-r.match_score, prio, r.entry_id)

    results.sort(key=sort_key)
    return results


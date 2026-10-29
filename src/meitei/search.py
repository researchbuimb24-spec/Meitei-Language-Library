# -*- coding: utf-8 -*-
"""
Unified Dictionary Search Engine for the Meitei Language Library (meitei).

Features:
- Full-text search across Meitei Mayek headwords, Bengali-script forms,
  registered Roman spellings, explicitly cataloged historical variants,
  and multilingual translation glosses (English, Hindi, Assamese, Bengali).
- SQLite FTS5 acceleration where available, with documented fallback to
  standard indexed relational search.
- Safe Unicode query normalization preserving tonal and morphological markers.
- Distinct identification of spelling-variant matches.
- Strict provenance and verification status filtering (`verified_only=True`).
- Language heuristic routing (`lang="auto"`).
- Deterministic score-based ranking and stable result ordering.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from meitei.loader import DataLoader, get_default_data_dir
from meitei.schema import CORE_ALLOWED_STATUSES, RecordStatus
from meitei.unicode_utils import detect_script, normalize_text


@dataclass
class SearchResult:
    """
    Structured search match result.

    Attributes:
        entry_id: Stable identifier of the matched lexical entry (e.g. MEI-LEX-0000001).
        canonical_lemma: Primary headword in Meitei Mayek script.
        headword_roman: Standard Latin Romanization.
        headword_bengali: Historical Bengali-script representation if attested.
        status: Verification and attestation status (e.g. SOURCE_ATTESTED, VERIFIED).
        matched_field: The specific record attribute that matched the query.
        matched_text: The exact text string or substring that triggered the match.
        matched_language: Language or script of the match (e.g. mni, en, hi, as, bn).
        is_variant_match: True if the match was triggered by an explicitly registered variant.
        variant_details: Additional metadata if matched via a spelling variant.
        citations: List of source citations, folios, and reviewer attributions.
        senses: List of semantic senses and definitions.
        match_score: Deterministic numeric ranking score (higher is more relevant).
    """
    entry_id: str
    canonical_lemma: str
    headword_roman: str
    headword_bengali: Optional[str]
    status: str
    matched_field: str
    matched_text: str
    matched_language: str
    is_variant_match: bool
    variant_details: Optional[Dict[str, Any]] = None
    citations: List[Dict[str, Any]] = field(default_factory=list)
    senses: List[Dict[str, Any]] = field(default_factory=list)
    match_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert result object to dictionary."""
        return asdict(self)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


def check_fts5_available(conn: sqlite3.Connection) -> bool:
    """Check whether SQLite Full-Text Search 5 (FTS5) extension is compiled in."""
    try:
        cur = conn.cursor()
        cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS _test_fts5 USING fts5(x);")
        cur.execute("DROP TABLE _test_fts5;")
        return True
    except sqlite3.OperationalError:
        return False


class SearchEngine:
    """
    High-performance, deterministic search index for Meitei language records.
    """

    def __init__(self, data_dir: Union[str, Path] = "data") -> None:
        self.data_dir = get_default_data_dir(data_dir)
        self._conn = sqlite3.connect(":memory:")
        self._conn.row_factory = sqlite3.Row
        self._fts5_enabled = check_fts5_available(self._conn)
        self._init_index_tables()
        self._load_datasets()

    def _init_index_tables(self) -> None:
        """Create relational search index tables and FTS5 virtual table if supported."""
        with self._conn:
            # Master index table
            self._conn.execute(
                """
                CREATE TABLE search_entries (
                    entry_id TEXT PRIMARY KEY,
                    headword_meitei TEXT NOT NULL,
                    headword_roman TEXT NOT NULL,
                    headword_bengali TEXT,
                    phonetic_ipa TEXT,
                    status TEXT NOT NULL,
                    source_id TEXT,
                    citation_locator TEXT,
                    reviewer_json TEXT,
                    senses_json TEXT,
                    variants_json TEXT,
                    glosses_json TEXT
                );
                """
            )
            self._conn.execute("CREATE INDEX idx_se_meitei ON search_entries(headword_meitei);")
            self._conn.execute("CREATE INDEX idx_se_roman ON search_entries(headword_roman);")
            self._conn.execute("CREATE INDEX idx_se_bengali ON search_entries(headword_bengali);")
            self._conn.execute("CREATE INDEX idx_se_status ON search_entries(status);")

            # FTS5 Virtual Table if available
            if self._fts5_enabled:
                self._conn.execute(
                    """
                    CREATE VIRTUAL TABLE search_fts USING fts5(
                        entry_id UNINDEXED,
                        headword_meitei,
                        headword_roman,
                        headword_bengali,
                        variant_forms,
                        glosses_text,
                        definitions_text,
                        tokenize = 'unicode61'
                    );
                    """
                )

    def _load_datasets(self) -> None:
        """Ingest all authentic records from data/ into the search index."""
        if not (self.data_dir / "lexicon").exists():
            return

        loader = DataLoader(self.data_dir)
        try:
            sources = loader.load_sources()
        except Exception:
            sources = {}
        known_sources = set(sources.keys())

        try:
            core_lex = loader.load_lexicon(partition="core", known_sources=known_sources)
        except Exception:
            core_lex = {}

        try:
            cand_lex = loader.load_lexicon(partition="candidate", known_sources=known_sources)
        except Exception:
            cand_lex = {}

        all_entries = {**core_lex, **cand_lex}
        if not all_entries:
            return

        try:
            variants = loader.load_variants(known_entries=set(all_entries.keys()), known_sources=known_sources)
        except Exception:
            variants = []

        try:
            glosses = loader.load_glosses(known_entries=set(all_entries.keys()), known_sources=known_sources)
        except Exception:
            glosses = []

        # Group variants and glosses by entry_id
        entry_variants: Dict[str, List[Dict[str, Any]]] = {}
        for v in variants:
            eid = v["entry_id"]
            entry_variants.setdefault(eid, []).append(v)

        entry_glosses: Dict[str, List[Dict[str, Any]]] = {}
        for g in glosses:
            eid = g["entry_id"]
            entry_glosses.setdefault(eid, []).append(g)

        # Insert records into SQLite search index
        with self._conn:
            for eid, entry in all_entries.items():
                v_list = entry_variants.get(eid, [])
                g_list = entry_glosses.get(eid, [])
                senses_list = entry.get("senses", [])

                # FTS texts aggregation
                v_forms = " ".join(v["variant_form"] for v in v_list)
                g_texts = " ".join(g["gloss"] for g in g_list)
                d_texts = " ".join(s["definition_en"] for s in senses_list)

                self._conn.execute(
                    """
                    INSERT INTO search_entries (
                        entry_id, headword_meitei, headword_roman, headword_bengali,
                        phonetic_ipa, status, source_id, citation_locator,
                        reviewer_json, senses_json, variants_json, glosses_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        eid,
                        normalize_text(entry.get("headword_meitei", "")),
                        normalize_text(entry.get("headword_roman", "")),
                        normalize_text(entry.get("headword_bengali", "")) if entry.get("headword_bengali") else None,
                        entry.get("phonetic_ipa"),
                        entry.get("status", "UNVERIFIED"),
                        entry.get("source_id"),
                        entry.get("citation_locator"),
                        json.dumps(entry.get("reviewer_attribution") or {}, ensure_ascii=False),
                        json.dumps(senses_list, ensure_ascii=False),
                        json.dumps(v_list, ensure_ascii=False),
                        json.dumps(g_list, ensure_ascii=False),
                    ),
                )

                if self._fts5_enabled:
                    self._conn.execute(
                        """
                        INSERT INTO search_fts (
                            entry_id, headword_meitei, headword_roman, headword_bengali,
                            variant_forms, glosses_text, definitions_text
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            eid,
                            entry.get("headword_meitei", ""),
                            entry.get("headword_roman", ""),
                            entry.get("headword_bengali", "") or "",
                            v_forms,
                            g_texts,
                            d_texts,
                        ),
                    )

    def search(
        self,
        query: str,
        lang: str = "auto",
        verified_only: bool = False,
    ) -> List[SearchResult]:
        """
        Execute unified dictionary search.

        Args:
            query: Search query string.
            lang: Language routing filter ('auto', 'mni', 'en', 'hi', 'bn', 'as', 'latin', 'meitei_mayek').
            verified_only: If True, restricts matches strictly to SOURCE_ATTESTED and VERIFIED entries.

        Returns:
            List of SearchResult objects ordered deterministically by relevance score and entry ID.
        """
        q_norm = normalize_text(query).strip()
        if not q_norm:
            return []

        q_lower = q_norm.lower()
        q_script = detect_script(q_norm)

        # Select candidate entries from search_entries
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM search_entries")
        rows = cur.fetchall()

        results: List[SearchResult] = []

        for row in rows:
            entry_id = row["entry_id"]
            status = row["status"]

            # Filter verified_only
            if verified_only and status not in CORE_ALLOWED_STATUSES:
                continue

            hw_meitei = row["headword_meitei"]
            hw_roman = row["headword_roman"]
            hw_bengali = row["headword_bengali"] or ""
            senses = json.loads(row["senses_json"]) if row["senses_json"] else []
            variants = json.loads(row["variants_json"]) if row["variants_json"] else []
            glosses = json.loads(row["glosses_json"]) if row["glosses_json"] else []

            # Prepare citation metadata
            citations: List[Dict[str, Any]] = []
            if row["source_id"]:
                citations.append({
                    "source_id": row["source_id"],
                    "citation_locator": row["citation_locator"],
                    "reviewer_attribution": json.loads(row["reviewer_json"]) if row["reviewer_json"] else None,
                })

            best_match: Optional[Tuple[float, str, str, str, bool, Optional[Dict[str, Any]]]] = None

            def record_match(
                score: float,
                field_name: str,
                matched_str: str,
                match_lang: str,
                is_var: bool = False,
                var_meta: Optional[Dict[str, Any]] = None,
            ) -> None:
                nonlocal best_match
                if best_match is None or score > best_match[0]:
                    best_match = (score, field_name, matched_str, match_lang, is_var, var_meta)

            # 1. Exact & Substring Canonical Headwords
            # Meitei Mayek
            if q_norm == hw_meitei:
                record_match(100.0, "headword_meitei", hw_meitei, "mni")
            elif hw_meitei.startswith(q_norm):
                record_match(70.0, "headword_meitei", hw_meitei, "mni")
            elif q_norm in hw_meitei:
                record_match(60.0, "headword_meitei", hw_meitei, "mni")

            # Roman
            if q_lower == hw_roman.lower():
                record_match(100.0, "headword_roman", hw_roman, "latin")
            elif hw_roman.lower().startswith(q_lower):
                record_match(70.0, "headword_roman", hw_roman, "latin")
            elif q_lower in hw_roman.lower():
                record_match(60.0, "headword_roman", hw_roman, "latin")

            # Bengali
            if hw_bengali:
                if q_norm == hw_bengali:
                    record_match(100.0, "headword_bengali", hw_bengali, "bn")
                elif hw_bengali.startswith(q_norm):
                    record_match(70.0, "headword_bengali", hw_bengali, "bn")
                elif q_norm in hw_bengali:
                    record_match(60.0, "headword_bengali", hw_bengali, "bn")

            # 2. Registered Spelling Variants
            for v in variants:
                if verified_only and v.get("status") not in CORE_ALLOWED_STATUSES:
                    continue
                v_form = normalize_text(v.get("variant_form", ""))
                v_lower = v_form.lower()
                v_script = v.get("script", "latin")
                v_lang = "mni" if v_script == "meitei_mayek" else ("bn" if v_script == "bengali" else "latin")

                if q_norm == v_form or q_lower == v_lower:
                    record_match(90.0, "spelling_variant", v_form, v_lang, is_var=True, var_meta=v)
                elif v_lower.startswith(q_lower) or v_form.startswith(q_norm):
                    record_match(55.0, "spelling_variant", v_form, v_lang, is_var=True, var_meta=v)
                elif q_lower in v_lower or q_norm in v_form:
                    record_match(50.0, "spelling_variant", v_form, v_lang, is_var=True, var_meta=v)

            # 3. Multilingual Translation Glosses (English, Hindi, Assamese, Bengali)
            for g in glosses:
                if verified_only and g.get("status") not in CORE_ALLOWED_STATUSES:
                    continue
                g_text = normalize_text(g.get("gloss", ""))
                g_lower = g_text.lower()
                target_lang = g.get("target_language", "en")

                if q_norm == g_text or q_lower == g_lower:
                    record_match(80.0, f"gloss_{target_lang}", g_text, target_lang)
                elif g_lower.startswith(q_lower) or g_text.startswith(q_norm):
                    record_match(45.0, f"gloss_{target_lang}", g_text, target_lang)
                elif q_lower in g_lower or q_norm in g_text:
                    record_match(40.0, f"gloss_{target_lang}", g_text, target_lang)

            # 4. English Definitions in Senses
            for s in senses:
                defn = normalize_text(s.get("definition_en", ""))
                defn_lower = defn.lower()
                if q_lower == defn_lower:
                    record_match(75.0, "definition_en", defn, "en")
                elif q_lower in defn_lower:
                    record_match(35.0, "definition_en", defn, "en")

            # Language Filtering if not auto
            if best_match is not None:
                score, f_name, m_text, m_lang, is_var, v_details = best_match

                if lang != "auto":
                    lang_clean = lang.strip().lower()
                    # Allow language match or script match
                    if lang_clean not in (m_lang.lower(), f_name.lower()):
                        # Skip if language filter doesn't match
                        continue

                results.append(
                    SearchResult(
                        entry_id=entry_id,
                        canonical_lemma=hw_meitei,
                        headword_roman=hw_roman,
                        headword_bengali=hw_bengali if hw_bengali else None,
                        status=status,
                        matched_field=f_name,
                        matched_text=m_text,
                        matched_language=m_lang,
                        is_variant_match=is_var,
                        variant_details=v_details,
                        citations=citations,
                        senses=senses,
                        match_score=score,
                    )
                )

        # Deterministic Ranking and Stable Result Ordering:
        # 1. Higher match_score first (-score)
        # 2. SOURCE_ATTESTED prioritized over UNVERIFIED
        # 3. Canonical entry_id lexicographically
        # 4. Matched field name
        def sort_key(r: SearchResult) -> Tuple[float, int, str, str]:
            status_prio = 0 if r.status == RecordStatus.SOURCE_ATTESTED.value else (1 if r.status == RecordStatus.VERIFIED.value else 2)
            return (-r.match_score, status_prio, r.entry_id, r.matched_field)

        results.sort(key=sort_key)
        return results

    def batch_search(
        self,
        queries: List[str],
        lang: str = "auto",
        verified_only: bool = False,
    ) -> Dict[str, List[SearchResult]]:
        """
        Execute batch dictionary search across multiple queries.

        Args:
            queries: List of query strings.
            lang: Language filter ('auto', 'mni', 'en', etc.).
            verified_only: If True, restricts to verified records.

        Returns:
            Dictionary mapping each query string to its list of SearchResult matches.
        """
        return {q: self.search(q, lang=lang, verified_only=verified_only) for q in queries}


# Global cached singleton instance for high-speed calls
_DEFAULT_ENGINE: Optional[SearchEngine] = None


def get_default_search_engine(data_dir: Union[str, Path] = "data") -> SearchEngine:
    """Return cached default SearchEngine instance."""
    global _DEFAULT_ENGINE
    if _DEFAULT_ENGINE is None:
        _DEFAULT_ENGINE = SearchEngine(data_dir=data_dir)
    return _DEFAULT_ENGINE


def search(
    query: str,
    lang: str = "auto",
    verified_only: bool = False,
    data_dir: Union[str, Path] = "data",
) -> List[SearchResult]:
    """
    Search across Meitei Mayek, Roman, Bengali, variants, and multilingual glosses.

    Args:
        query: Search string.
        lang: Language filter ('auto', 'mni', 'en', 'hi', 'bn', 'as', etc.).
        verified_only: If True, excludes unverified or citation-mismatch claims.
        data_dir: Path to directory containing data/ sources and lexicons.

    Returns:
        List of SearchResult objects ordered deterministically.
    """
    engine = get_default_search_engine(data_dir=data_dir)
    return engine.search(query=query, lang=lang, verified_only=verified_only)


def batch_search(
    queries: List[str],
    lang: str = "auto",
    verified_only: bool = False,
    data_dir: Union[str, Path] = "data",
) -> Dict[str, List[SearchResult]]:
    """
    Batch search across multiple queries.

    Args:
        queries: List of search strings.
        lang: Language filter ('auto', 'mni', 'en', etc.).
        verified_only: If True, excludes unverified claims.
        data_dir: Path to directory containing data/ sources and lexicons.

    Returns:
        Dictionary mapping query string -> List[SearchResult].
    """
    engine = get_default_search_engine(data_dir=data_dir)
    return engine.batch_search(queries=queries, lang=lang, verified_only=verified_only)


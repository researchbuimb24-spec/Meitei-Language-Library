# -*- coding: utf-8 -*-
"""
Command-Line Interface (CLI) for the Meitei Language Library (meitei).

Provides command-line utilities for:
- Lexical and dictionary lookup (`meitei lookup`)
- Unified multi-script full-text search (`meitei search`)
- Citation-backed bidirectional translation (`meitei translate`)
- Language catalog and ISO code inspection (`meitei languages`)
- Schema and referential dataset validation (`meitei validate`)
- SQLite database initialization and administration (`meitei init-db`, `meitei stats`)
- JSONL streaming import and export (`meitei import-jsonl`, `meitei export-jsonl`)

Designed strictly with the Python standard library `argparse`, supporting
full Unicode input and output, predictable exit codes, and machine-readable JSON.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import meitei
from meitei.audit import (
    AuditReport,
    ProvenanceAuditor,
    audit_repository,
)
from meitei.books import (
    BookAuditResult,
    BookCatalog,
    BookCatalogRecord,
    BookImporter,
    BookNotFoundError,
    BookNotImportedError,
    BookReader,
    BookSearchEngine,
    BookValidator,
    ChapterNotFoundError,
    ImportStatus,
    audit_books,
    get_book_info,
    get_book_stats,
    list_books,
    read_passages,
    search_passages,
)
from meitei.database import MeiteiDatabase
from meitei.grammar import (
    get_grammar_records,
    get_topic_sources,
    list_grammar_sources,
    list_grammar_topics,
    load_grammar_records,
)
from meitei.languages import (
    canonicalize_language_code,
    get_supported_codes_summary,
    get_supported_languages,
    is_supported_language,
)
from meitei.loader import DataLoader, ValidationError
from meitei.models import BibliographicSource
from meitei.schema import CORE_ALLOWED_STATUSES, RecordStatus
from meitei.search import check_fts5_available, search
from meitei.translate import translate


def build_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser with all supported subcommands."""
    parser = argparse.ArgumentParser(
        prog="meitei",
        description="Meitei Language Library (meitei) - Lightweight, offline-first Python library for Meiteilon.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {meitei.__version__}",
        help="Show program's version number and exit.",
    )

    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # -------------------------------------------------------------------------
    # Subcommand: lookup
    # -------------------------------------------------------------------------
    p_lookup = subparsers.add_parser(
        "lookup",
        help="Search and inspect lexical entries across headwords, variants, and glosses.",
    )
    p_lookup.add_argument("query", help="Headword, variant, or translation gloss to look up.")
    p_lookup.add_argument("--json", action="store_true", help="Output results as machine-readable JSON.")
    p_lookup.add_argument("--lang", default="auto", help="Language filter ('auto', 'mni', 'en', 'hi', 'bn', 'as').")
    p_lookup.add_argument(
        "--verified-only",
        action="store_true",
        help="Restrict results strictly to verified/source-attested records.",
    )
    p_lookup.add_argument("--data-dir", default="data", help="Directory containing data files (default: data).")
    p_lookup.add_argument("--db-path", default=None, help="Optional SQLite database path to query.")
    p_lookup.set_defaults(func=cmd_lookup)

    # -------------------------------------------------------------------------
    # Subcommand: search
    # -------------------------------------------------------------------------
    p_search = subparsers.add_parser(
        "search",
        help="Unified multi-script dictionary search across Meitei Mayek, Bengali, Roman, and glosses.",
    )
    p_search.add_argument("query", help="Search query string.")
    p_search.add_argument("--json", action="store_true", help="Output results as machine-readable JSON.")
    p_search.add_argument("--lang", default="auto", help="Language filter ('auto', 'mni', 'en', 'hi', 'bn', 'as').")
    p_search.add_argument(
        "--verified-only",
        action="store_true",
        help="Restrict results strictly to verified/source-attested records.",
    )
    p_search.add_argument("--data-dir", default="data", help="Directory containing data files (default: data).")
    p_search.set_defaults(func=cmd_search)

    # -------------------------------------------------------------------------
    # Subcommand: translate
    # -------------------------------------------------------------------------
    p_trans = subparsers.add_parser(
        "translate",
        help="Citation-backed bidirectional translation between Meitei and target languages.",
    )
    p_trans.add_argument("query", help="Word or term to translate.")
    p_trans.add_argument(
        "--from",
        dest="from_lang",
        default="auto",
        help="Source language ('en', 'mni', 'hi', 'bn', 'as', or 'auto').",
    )
    p_trans.add_argument(
        "--to",
        dest="to_lang",
        default=None,
        help="Target language (default: 'mni' when --from is non-mni, else 'en').",
    )
    p_trans.add_argument(
        "--verified-only",
        action="store_true",
        help="Exclude unverified candidates and undocumented glosses.",
    )
    p_trans.add_argument("--json", action="store_true", help="Output results as machine-readable JSON.")
    p_trans.add_argument("--data-dir", default="data", help="Directory containing data files (default: data).")
    p_trans.set_defaults(func=cmd_translate)

    # -------------------------------------------------------------------------
    # Subcommand: languages
    # -------------------------------------------------------------------------
    p_lang = subparsers.add_parser(
        "languages",
        help="Display supported language codes, script conventions, and metadata.",
    )
    p_lang.add_argument("--json", action="store_true", help="Output language catalog as machine-readable JSON.")
    p_lang.set_defaults(func=cmd_languages)

    # -------------------------------------------------------------------------
    # Subcommand: grammar
    # -------------------------------------------------------------------------
    p_grm = subparsers.add_parser(
        "grammar",
        help="Inspect evidence-backed grammatical topics, rules, and attested examples.",
    )
    p_grm.add_argument("--topic", default=None, help="Specific grammatical topic (e.g. pronouns, numerals, negation).")
    p_grm.add_argument("--sources", action="store_true", help="List bibliographic sources backing grammar records.")
    p_grm.add_argument("--verified-only", action="store_true", help="Exclude unverified grammar notes.")
    p_grm.add_argument("--json", action="store_true", help="Output grammar data as machine-readable JSON.")
    p_grm.add_argument("--data-dir", default="data", help="Path to data directory (default: data).")
    p_grm.set_defaults(func=cmd_grammar)

    # -------------------------------------------------------------------------
    # Subcommand: books
    # -------------------------------------------------------------------------
    p_books = subparsers.add_parser(
        "books",
        help="Offline digital book library operations (list, info, read, search, validate, audit, stats).",
    )
    books_sub = p_books.add_subparsers(dest="books_subcommand", help="Books subcommands")

    # books list
    p_b_list = books_sub.add_parser("list", help="List registered books and import statuses.")
    p_b_list.add_argument("--status", choices=["CATALOG_ONLY", "PARTIALLY_IMPORTED", "FULLY_IMPORTED"], default=None, help="Filter by import status.")
    p_b_list.add_argument("--json", action="store_true", help="Output as machine-readable JSON.")
    p_b_list.add_argument("--data-dir", default="data", help="Data directory (default: data).")
    p_b_list.set_defaults(func=cmd_books_list)

    # books info
    p_b_info = books_sub.add_parser("info", help="Display bibliographic and rights metadata for a book.")
    p_b_info.add_argument("book_id", help="Book identifier (e.g. khamba_thoibi).")
    p_b_info.add_argument("--json", action="store_true", help="Output metadata as JSON.")
    p_b_info.add_argument("--data-dir", default="data", help="Data directory (default: data).")
    p_b_info.set_defaults(func=cmd_books_info)

    # books read
    p_b_read = books_sub.add_parser("read", help="Read passages from a chapter with pagination.")
    p_b_read.add_argument("book_id", help="Book identifier.")
    p_b_read.add_argument("--chapter", type=int, default=1, help="Chapter number (default: 1).")
    p_b_read.add_argument("--page", type=int, default=1, help="Page number (default: 1).")
    p_b_read.add_argument("--page-size", "--size", dest="page_size", type=int, default=5, help="Passages per page (default: 5).")
    p_b_read.add_argument("--json", action="store_true", help="Output passages as JSON.")
    p_b_read.add_argument("--data-dir", default="data", help="Data directory (default: data).")
    p_b_read.set_defaults(func=cmd_books_read)

    # books search
    p_b_search = books_sub.add_parser("search", help="Full-text search across book passages.")
    p_b_search.add_argument("query", help="Search query string.")
    p_b_search.add_argument("--book-id", default=None, help="Optional book ID filter.")
    p_b_search.add_argument("--limit", type=int, default=10, help="Maximum results (default: 10).")
    p_b_search.add_argument("--json", action="store_true", help="Output results as JSON.")
    p_b_search.add_argument("--data-dir", default="data", help="Data directory (default: data).")
    p_b_search.set_defaults(func=cmd_books_search)

    # books validate
    p_b_val = books_sub.add_parser("validate", help="Validate passage sequencing, IDs, and metadata.")
    p_b_val.add_argument("book_id_arg", nargs="?", default=None, help="Specific book to validate (all if omitted).")
    p_b_val.add_argument("--book-id", default=None, help="Specific book to validate (all if omitted).")
    p_b_val.add_argument("--json", action="store_true", help="Output validation as JSON.")
    p_b_val.add_argument("--data-dir", default="data", help="Data directory (default: data).")
    p_b_val.set_defaults(func=cmd_books_validate)

    # books audit
    p_b_audit = books_sub.add_parser("audit", help="Audit catalog completeness, chapter coverage, and checksums.")
    p_b_audit.add_argument("--json", action="store_true", help="Output audit report as JSON.")
    p_b_audit.add_argument("--data-dir", default="data", help="Data directory (default: data).")
    p_b_audit.set_defaults(func=cmd_books_audit)

    # books stats
    p_b_stats = books_sub.add_parser("stats", help="Display digital book library holdings statistics.")
    p_b_stats.add_argument("--json", action="store_true", help="Output statistics as JSON.")
    p_b_stats.add_argument("--data-dir", default="data", help="Data directory (default: data).")
    p_b_stats.set_defaults(func=cmd_books_stats)

    # -------------------------------------------------------------------------
    # Subcommand: validate / validate-data
    # -------------------------------------------------------------------------
    p_val = subparsers.add_parser(
        "validate",
        help="Validate schema, cross-references, and citation integrity across datasets.",
    )
    p_val.add_argument("--strict", action="store_true", help="Enforce strict citation completeness and review checks.")
    p_val.add_argument("--fail-unreviewed", action="store_true", help="Fail with non-zero exit code if unreviewed records exist.")
    p_val.add_argument("--json", action="store_true", help="Output validation report as machine-readable JSON.")
    p_val.add_argument("--data-dir", default="data", help="Path to data directory (default: data).")
    p_val.set_defaults(func=cmd_validate)

    p_val_legacy = subparsers.add_parser(
        "validate-data",
        help="Alias for validate: Validate schema and referential integrity of data directory.",
    )
    p_val_legacy.add_argument("--strict", action="store_true", help="Enforce strict citation checks.")
    p_val_legacy.add_argument("--fail-unreviewed", action="store_true", help="Fail with non-zero exit code if unreviewed records exist.")
    p_val_legacy.add_argument("--json", action="store_true", help="Output validation report as JSON.")
    p_val_legacy.add_argument("--data-dir", default="data", help="Path to data directory (default: data).")
    p_val_legacy.set_defaults(func=cmd_validate)

    # -------------------------------------------------------------------------
    # Subcommand: info
    # -------------------------------------------------------------------------
    p_info = subparsers.add_parser("info", help="Display library metadata and architectural summary.")
    p_info.add_argument("--json", action="store_true", help="Output info as machine-readable JSON.")
    p_info.set_defaults(func=cmd_info)

    # -------------------------------------------------------------------------
    # Subcommand: init-db
    # -------------------------------------------------------------------------
    p_init = subparsers.add_parser("init-db", help="Initialize a local SQLite database schema.")
    p_init.add_argument("--db-path", default="meitei.sqlite3", help="Target SQLite file path (default: meitei.sqlite3).")
    p_init.set_defaults(func=cmd_init_db)

    # -------------------------------------------------------------------------
    # Subcommand: stats
    # -------------------------------------------------------------------------
    p_stats = subparsers.add_parser("stats", help="Display database statistics and verification status counts.")
    p_stats.add_argument("--db-path", default="meitei.sqlite3", help="SQLite database path (default: meitei.sqlite3).")
    p_stats.add_argument("--json", action="store_true", help="Output stats as JSON.")
    p_stats.set_defaults(func=cmd_stats)

    # -------------------------------------------------------------------------
    # Subcommand: import-jsonl
    # -------------------------------------------------------------------------
    p_import = subparsers.add_parser("import-jsonl", help="Import records from a JSONL file into SQLite.")
    p_import.add_argument("file_path", help="Path to input .jsonl file.")
    p_import.add_argument("--type", choices=["entries", "sources"], default="entries", help="Record type in JSONL.")
    p_import.add_argument("--db-path", default="meitei.sqlite3", help="SQLite database path.")
    p_import.set_defaults(func=cmd_import_jsonl)

    # -------------------------------------------------------------------------
    # Subcommand: export-jsonl
    # -------------------------------------------------------------------------
    p_export = subparsers.add_parser("export-jsonl", help="Export records from SQLite to a JSONL file.")
    p_export.add_argument("file_path", help="Path to destination .jsonl file.")
    p_export.add_argument("--type", choices=["entries", "sources"], default="entries", help="Record type to export.")
    p_export.add_argument("--db-path", default="meitei.sqlite3", help="SQLite database path.")
    p_export.set_defaults(func=cmd_export_jsonl)

    # -------------------------------------------------------------------------
    # Subcommand: add-source
    # -------------------------------------------------------------------------
    p_source = subparsers.add_parser("add-source", help="Register a bibliographic source in the database.")
    p_source.add_argument("source_id", help="Unique source identifier (e.g., 'MEI-SRC-000001').")
    p_source.add_argument("title", help="Full title of the manuscript, book, or fieldwork session.")
    p_source.add_argument("--author", default=None, help="Author name if known.")
    p_source.add_argument("--year", type=int, default=None, help="Year or century.")
    p_source.add_argument("--type", dest="source_type", default="puya", help="Type (puya, chronicle, dictionary, fieldwork).")
    p_source.add_argument("--db-path", default="meitei.sqlite3", help="SQLite database path.")
    p_source.set_defaults(func=cmd_add_source)

    return parser


# =============================================================================
# Subcommand Implementations
# =============================================================================

def cmd_lookup(args: argparse.Namespace) -> int:
    """Search and display matching entries across SQLite or JSONL datasets."""
    # Language code validation
    if not is_supported_language(args.lang, allow_auto=True):
        valid = get_supported_codes_summary()
        print(f"Error: Invalid or unsupported language code '{args.lang}'. Supported languages: {valid} (or 'auto').", file=sys.stderr)
        return 2

    db_path = getattr(args, "db_path", None)
    if db_path and Path(db_path).exists():
        db = MeiteiDatabase(db_path)
        try:
            results = db.lookup_headword(args.query)
            if not results:
                results = db.search_entries(args.query, limit=10)

            if args.json:
                data = [e.to_dict() for e in results]
                print(json.dumps(data, indent=2, ensure_ascii=False))
                return 0

            if not results:
                print(f"No entries found matching query: '{args.query}'")
                return 0

            print(f"Found {len(results)} matching entry/entries for '{args.query}':\n")
            for i, entry in enumerate(results, start=1):
                status = entry.get_verification_status()
                bengali_info = f" [Bengali: {entry.headword_bengali}]" if entry.headword_bengali else ""
                print(f"[{i}] {entry.headword_meitei} ({entry.headword_roman}){bengali_info} - Status: {status.value}")
                if entry.phonetic_ipa:
                    print(f"    IPA: /{entry.phonetic_ipa}/")
                for sense in entry.senses:
                    print(f"    - [{sense.part_of_speech.value}] {sense.definition_en}")
                    if sense.definition_mni:
                        print(f"      (Mayek definition: {sense.definition_mni})")
                    for ex in sense.examples:
                        print(f"      * {ex.meitei} ({ex.roman}) -> {ex.english}")
                if entry.provenance:
                    print("    Provenance:")
                    for p in entry.provenance:
                        print(f"      * Source: {p.source_id} | Type: {p.attestation_type} | Ref: {p.attestation_reference} | Status: {p.verification_status.value}")
                print()
        finally:
            db.close()
        return 0
    else:
        # Search JSONL datasets
        raw_results = search(
            args.query,
            lang=args.lang,
            verified_only=args.verified_only,
            data_dir=args.data_dir,
        )

        if args.json:
            data = [r.to_dict() for r in raw_results]
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return 0

        if not raw_results:
            print(f"No entries found matching query: '{args.query}'")
            return 0

        print(f"Found {len(raw_results)} matching entry/entries for '{args.query}':\n")
        for i, r in enumerate(raw_results, start=1):
            var_tag = " (Spelling Variant Match)" if r.is_variant_match else ""
            bengali_info = f" [Bengali: {r.headword_bengali}]" if r.headword_bengali else ""
            print(f"[{i}] {r.canonical_lemma} ({r.headword_roman}){bengali_info} - Status: {r.status}{var_tag}")
            print(f"    Matched Field: {r.matched_field} ('{r.matched_text}') [{r.matched_language}]")
            for sense in r.senses:
                pos = sense.get("part_of_speech", "noun")
                defn = sense.get("definition_en", "")
                print(f"    - [{pos}] {defn}")
                if sense.get("definition_mni"):
                    print(f"      (Mayek: {sense.get('definition_mni')})")
                for ex in sense.get("examples", []):
                    ex_mni = ex.get("meitei", "")
                    ex_rom = ex.get("roman", "")
                    ex_en = ex.get("english", "")
                    print(f"      * {ex_mni} ({ex_rom}) -> {ex_en}")
            for cit in r.citations:
                rev = cit.get("reviewer_attribution") or {}
                rev_str = f" | Reviewer: {rev.get('reviewer_id')}" if rev.get("reviewer_id") else ""
                print(f"    Citation: Source {cit.get('source_id')} | Locator: {cit.get('citation_locator')}{rev_str}")
            print()
        return 0


def cmd_search(args: argparse.Namespace) -> int:
    """Execute unified multi-script full-text dictionary search."""
    if not is_supported_language(args.lang, allow_auto=True):
        valid = get_supported_codes_summary()
        print(f"Error: Invalid or unsupported language code '{args.lang}'. Supported languages: {valid} (or 'auto').", file=sys.stderr)
        return 2

    raw_results = search(
        args.query,
        lang=args.lang,
        verified_only=args.verified_only,
        data_dir=args.data_dir,
    )

    if args.json:
        data = [r.to_dict() for r in raw_results]
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    if not raw_results:
        print(f"No entries found matching query: '{args.query}'")
        return 0

    print(f"Search results for '{args.query}' (lang: {args.lang}):\n")
    for i, r in enumerate(raw_results, start=1):
        var_tag = " [Spelling Variant]" if r.is_variant_match else ""
        bengali_info = f" [Bengali: {r.headword_bengali}]" if r.headword_bengali else ""
        print(f"[{i}] {r.canonical_lemma} ({r.headword_roman}){bengali_info} - Status: {r.status}{var_tag} (Score: {r.match_score:.1f})")
        print(f"    Matched: {r.matched_field} ('{r.matched_text}') [{r.matched_language}]")
        for sense in r.senses:
            pos = sense.get("part_of_speech", "noun")
            defn = sense.get("definition_en", "")
            print(f"    - [{pos}] {defn}")
        for cit in r.citations:
            print(f"    Citation: Source {cit.get('source_id')} | Locator: {cit.get('citation_locator')}")
        print()
    return 0


def cmd_translate(args: argparse.Namespace) -> int:
    """Execute citation-backed cross-lingual translation."""
    from_lang = args.from_lang
    if not is_supported_language(from_lang, allow_auto=True):
        valid = get_supported_codes_summary()
        print(f"Error: Invalid or unsupported source language '{from_lang}'. Supported languages: {valid} (or 'auto').", file=sys.stderr)
        return 2

    # Default target language
    to_lang = args.to_lang
    if to_lang is None:
        to_lang = "mni" if from_lang != "mni" else "en"

    if not is_supported_language(to_lang, allow_auto=False):
        valid = get_supported_codes_summary()
        print(f"Error: Invalid or unsupported target language '{to_lang}'. Supported languages: {valid}.", file=sys.stderr)
        return 2

    try:
        raw_results = translate(
            args.query,
            from_lang=from_lang,
            to_lang=to_lang,
            verified_only=args.verified_only,
            data_dir=args.data_dir,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    if args.json:
        data = [r.to_dict() for r in raw_results]
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    if not raw_results:
        print(f"No translations found for '{args.query}' (from: {from_lang}, to: {to_lang})")
        return 0

    print(f"Translations for '{args.query}' ({from_lang} -> {to_lang}):\n")
    for i, r in enumerate(raw_results, start=1):
        target_disp = r.target_text
        if r.target_roman:
            target_disp += f" ({r.target_roman})"
        if r.target_bengali:
            target_disp += f" [Bengali: {r.target_bengali}]"

        print(f"[{i}] {target_disp} - Status: {r.status}")
        if r.gloss:
            type_info = f" ({r.gloss_type})" if r.gloss_type else ""
            print(f"    Matched Gloss: {r.gloss}{type_info}")
        if r.definition:
            pos_info = f"[{r.part_of_speech}] " if r.part_of_speech else ""
            print(f"    Sense: {pos_info}{r.definition}")
        for cit in r.citations:
            print(f"    Citation: Source {cit.get('source_id')} | Locator: {cit.get('citation_locator')}")
        if r.reviewer_attribution:
            rev_id = r.reviewer_attribution.get("reviewer_id")
            rev_date = r.reviewer_attribution.get("review_date")
            rev_notes = r.reviewer_attribution.get("notes")
            print(f"    Reviewer: {rev_id} ({rev_date})")
            if rev_notes:
                print(f"    Reviewer Notes: {rev_notes}")
        print()
    return 0


def cmd_languages(args: argparse.Namespace) -> int:
    """Display supported languages and orthographic script conventions."""
    languages = get_supported_languages()
    if args.json:
        print(json.dumps(languages, indent=2, ensure_ascii=False))
        return 0

    print("================================================================")
    print("      Supported Languages in Meitei Language Library (meitei)    ")
    print("================================================================")
    for lang in languages:
        scripts = ", ".join(lang["scripts"])
        print(f"• {lang['code']:4s} - {lang['name']}")
        print(f"    Family:   {lang['family']}")
        print(f"    Scripts:  {scripts}")
        print(f"    Role:     {lang['role']}")
        print(f"    Status:   {lang['status']}")
        print()
    print("================================================================")
    return 0


def cmd_grammar(args: argparse.Namespace) -> int:
    """Inspect grammar research topics, rules, and attested examples."""
    data_dir = args.data_dir

    # 1. Sources mode: list bibliographic sources supporting grammar
    if getattr(args, "sources", False):
        if args.topic:
            sources = get_topic_sources(args.topic, data_dir=data_dir)
            title = f"Bibliographic Sources for Grammar Topic: '{args.topic}'"
        else:
            sources = list_grammar_sources(data_dir=data_dir)
            title = "Bibliographic Sources for Meitei Grammar Subsystem"

        if args.json:
            print(json.dumps(sources, indent=2, ensure_ascii=False))
            return 0

        print("================================================================")
        print(f"  {title}  ")
        print("================================================================")
        if not sources:
            print("No bibliographic sources found.")
        else:
            for s in sources:
                author_str = f" by {s.get('author')}" if s.get("author") else ""
                year_str = f" ({s.get('year')})" if s.get("year") else ""
                print(f"• [{s.get('id')}] {s.get('title')}{author_str}{year_str}")
                print(f"    Type: {s.get('source_type')} | Legal Status: {s.get('metadata', {}).get('legal_status', 'Unknown')}")
        print("================================================================")
        return 0

    # 2. Topic mode: retrieve grammar records for specific topic
    if args.topic:
        records = get_grammar_records(
            topic=args.topic,
            verified_only=args.verified_only,
            data_dir=data_dir,
        )

        if args.json:
            data = [r.to_dict() for r in records]
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return 0

        if not records:
            topics = list_grammar_topics(data_dir=data_dir)
            matching = [t for t in topics if t["id"].lower() == args.topic.strip().lower()]
            if matching and matching[0]["status"] == "UNPOPULATED":
                t = matching[0]
                print(f"Grammar Topic: '{args.topic}' is an unpopulated research category.")
                print(f"Name: {t.get('name')}")
                print(f"Description: {t.get('description')}")
                if t.get("unpopulated_reason"):
                    print(f"Status Note: {t.get('unpopulated_reason')}")
            else:
                print(f"No grammar records found for topic: '{args.topic}'")
            return 0

        print("================================================================")
        print(f"  Grammar Reference: Topic '{args.topic}' ({len(records)} record(s))")
        print("================================================================")
        for i, r in enumerate(records, start=1):
            print(f"[{i}] [{r.id}] {r.title}")
            print(f"    Status: {r.verification_status}")
            print(f"    Citation: Source {r.source_id} | Locator: {r.citation_locator}")
            if r.morphological_rule:
                print(f"    Rule / Pattern: {r.morphological_rule}")
            print(f"    Description: {r.description}")
            if r.examples:
                print("    Attested Example(s):")
                for ex in r.examples:
                    bengali_str = f" [Bengali: {ex.bengali}]" if ex.bengali else ""
                    print(f"      * {ex.meitei} ({ex.roman}){bengali_str}")
                    print(f"        English: \"{ex.english}\"")
                    if ex.morpheme_gloss:
                        print(f"        Gloss:   {ex.morpheme_gloss}")
                    if ex.translation_provenance:
                        print(f"        Provenance: {ex.translation_provenance}")
            if r.reviewer_attribution:
                rev = r.reviewer_attribution
                print(f"    Reviewer: {rev.get('reviewer_id')} ({rev.get('review_date')})")
            print()
        print("================================================================")
        return 0

    # 3. Default mode: list all research topics and population status
    topics = list_grammar_topics(data_dir=data_dir)
    if args.json:
        print(json.dumps(topics, indent=2, ensure_ascii=False))
        return 0

    print("================================================================")
    print("      Meitei Language Library (meitei) - Grammar Subsystem      ")
    print("================================================================")
    print("Research Categories & Evidence Status:\n")
    for t in topics:
        status_tag = f"[{t['status']}]"
        rec_info = f" ({t.get('record_count', 0)} verified record(s))" if t["status"] == "POPULATED" else " (Awaiting verified ingestion)"
        print(f"• {t['id']:18s} {status_tag:13s}{rec_info}")
        print(f"    Name:        {t['name']}")
        print(f"    Description: {t['description']}")
        if t.get("documentation"):
            print(f"    Attestation: {t['documentation']}")
        if t.get("unpopulated_reason"):
            print(f"    Status Note: {t.get('unpopulated_reason')}")
        print()
    print("================================================================")
    return 0


# =============================================================================
# Books Subcommand Handlers
# =============================================================================

def cmd_books_list(args: argparse.Namespace) -> int:
    """List all registered books in the catalog."""
    books = list_books(status=args.status, data_dir=args.data_dir)
    if args.json:
        print(json.dumps([b.to_dict() for b in books], indent=2, ensure_ascii=False))
        return 0

    print("================================================================")
    print("      Meitei Language Library (meitei) - Digital Books Catalog  ")
    print("================================================================")
    if not books:
        print("No books found matching criteria.")
    else:
        for b in books:
            status_tag = f"[{b.import_status.value}]"
            ch_info = f"{b.imported_chapters}/{b.total_chapters} ch ({b.total_passages} passages)"
            print(f"• {b.book_id:24s} {status_tag:20s} {ch_info}")
            print(f"    Title:  {b.title} ({b.title_en})")
            print(f"    Author: {b.author}")
            print(f"    Rights: {b.rights_status} | Copyright: {b.copyright}")
            print()
    print("================================================================")
    return 0


def cmd_books_info(args: argparse.Namespace) -> int:
    """Display detailed bibliographic, rights, and import metadata for a book."""
    book = get_book_info(args.book_id, data_dir=args.data_dir)
    if not book:
        print(f"Error: Book '{args.book_id}' not found in catalog.", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(book.to_dict(), indent=2, ensure_ascii=False))
        return 0

    print("================================================================")
    print(f"Book Information: {book.book_id}")
    print("================================================================")
    print(f"Title (Meitei Mayek): {book.title}")
    print(f"Title (English):      {book.title_en}")
    print(f"Author / Heritage:    {book.author}")
    print(f"Language / Script:    {book.language} / {book.script}")
    print(f"Genre:                {book.genre}")
    print(f"Legal Rights Status:  {book.rights_status}")
    print(f"Copyright Notice:     {book.copyright}")
    print(f"Archival Source:      {book.source}")
    print(f"Import Status:        {book.import_status.value}")
    print(f"Chapters Declared:    {book.total_chapters}")
    print(f"Chapters Imported:    {book.imported_chapters}")
    print(f"Total Passages:       {book.total_passages}")
    if book.checksum_sha256:
        print(f"SHA-256 Checksum:     {book.checksum_sha256}")
    if book.last_imported_at:
        print(f"Last Imported:        {book.last_imported_at}")
    print(f"Description:          {book.description}")
    print("================================================================")
    return 0


def cmd_books_read(args: argparse.Namespace) -> int:
    """Read paginated passages from a book chapter."""
    try:
        passages, pagination = read_passages(
            book_id=args.book_id,
            chapter_number=args.chapter,
            page=args.page,
            page_size=args.page_size,
            data_dir=args.data_dir,
        )
    except BookNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except BookNotImportedError as e:
        print(f"Status Notice: {e}", file=sys.stderr)
        return 0
    except ChapterNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        payload = {
            "pagination": pagination,
            "passages": [p.to_dict() for p in passages],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print("================================================================")
    print(f"Reading: {pagination['book_id']} - Chapter {pagination['chapter_number']}")
    print(f"Title:   {pagination['chapter_title']} ({pagination['chapter_title_en']})")
    print(f"Page:    {pagination['page']}/{pagination['total_pages']} (Passages {len(passages)} of {pagination['total_passages']})")
    print("================================================================\n")

    for p in passages:
        print(f"[{p.passage_id}] (Passage #{p.passage_number} | {p.word_count} words):")
        print(f"{p.text}")
        if p.translation_en:
            print(f"Translation: \"{p.translation_en}\"")
        print()

    if pagination["has_next"]:
        next_pg = pagination["page"] + 1
        print(f"(Use --page {next_pg} to read next page)")
    print("================================================================")
    return 0


def cmd_books_search(args: argparse.Namespace) -> int:
    """Execute full-text search across book passages."""
    results = search_passages(
        query=args.query,
        book_id=args.book_id,
        limit=args.limit,
        data_dir=args.data_dir,
    )

    if args.json:
        print(json.dumps([r.to_dict() for r in results], indent=2, ensure_ascii=False))
        return 0

    if not results:
        print(f"No book passages found matching query: '{args.query}'")
        return 0

    print(f"Found {len(results)} passage match(es) for '{args.query}':\n")
    for i, r in enumerate(results, start=1):
        print(f"[{i}] [{r.passage_id}] {r.book_title} ({r.book_title_en}) - Chapter {r.chapter_number}")
        print(f"    Snippet: {r.matched_snippet}")
        print(f"    Full Passage: {r.text}")
        print()
    return 0


def cmd_books_validate(args: argparse.Namespace) -> int:
    """Validate book passage sequencing, ID syntax, and checksums."""
    validator = BookValidator(data_dir=args.data_dir)
    target_id = args.book_id or getattr(args, "book_id_arg", None)
    if target_id:
        res = validator.validate_book(target_id)
        if args.json:
            print(json.dumps(res.to_dict(), indent=2, ensure_ascii=False))
            return 0 if res.valid else 1

        print("================================================================")
        status_str = "PASSED" if res.valid else "FAILED"
        print(f"Book Validation ({res.book_id}): {status_str}")
        print("================================================================")
        print(f"Import Status:      {res.import_status}")
        print(f"Chapters Imported:  {res.imported_chapters_count}/{res.total_chapters_declared}")
        print(f"Passages Count:     {res.passages_count}")
        if res.checksum_verified is not None:
            print(f"Checksum Verified:  {'Yes' if res.checksum_verified else 'Mismatch'}")
        if res.warnings:
            for w in res.warnings:
                print(f"  [WARN] {w}")
        if res.errors:
            for e in res.errors:
                print(f"  [ERROR] {e}", file=sys.stderr)
            return 1
        print("================================================================")
        return 0
    else:
        audit = validator.audit_all_books()
        if args.json:
            print(json.dumps(audit, indent=2, ensure_ascii=False))
            return 0 if audit["all_valid"] else 1

        print("================================================================")
        status_str = "PASSED" if audit["all_valid"] else "FAILED"
        print(f"      Digital Books Validation: {status_str}                    ")
        print("================================================================")
        print(f"Total Books Audited: {audit['total_books_audited']}")
        print(f"Fully Imported:      {audit['fully_imported']}")
        print(f"Partially Imported:  {audit['partially_imported']}")
        print(f"Catalog Only:        {audit['catalog_only']}")
        print(f"Total Passages:      {audit['total_passages']}")
        print("================================================================")
        return 0 if audit["all_valid"] else 1


def cmd_books_audit(args: argparse.Namespace) -> int:
    """Audit catalog completeness, chapter coverage, and SHA-256 checksums."""
    audit = audit_books(data_dir=args.data_dir)
    if args.json:
        print(json.dumps(audit, indent=2, ensure_ascii=False))
        return 0 if audit["all_valid"] else 1

    print("================================================================")
    print("      Meitei Digital Books Library - Cryptographic Audit        ")
    print("================================================================")
    status_str = "INTEGRITY 100% VERIFIED" if audit["all_valid"] else "AUDIT ANOMALIES DETECTED"
    print(f"Audit Status:        {status_str}")
    print(f"Total Books Audited: {audit['total_books_audited']}")
    print(f"Fully Imported:      {audit['fully_imported']}")
    print(f"Partially Imported:  {audit['partially_imported']}")
    print(f"Catalog Only:        {audit['catalog_only']}")
    print(f"Total Passages:      {audit['total_passages']}")
    print("----------------------------------------------------------------")
    for b in audit["books"]:
        icon = "✓" if b["valid"] else "✗"
        ch_str = f"{b['imported_chapters_count']}/{b['total_chapters_declared']} ch"
        print(f"[{icon}] {b['book_id']:24s} {b['import_status']:18s} {ch_str:10s} ({b['passages_count']} passages)")
        if b["errors"]:
            for err in b["errors"]:
                print(f"    [ERROR] {err}", file=sys.stderr)
        if b["warnings"]:
            for warn in b["warnings"]:
                print(f"    [WARN]  {warn}")
    print("================================================================")
    return 0 if audit["all_valid"] else 1


def cmd_books_stats(args: argparse.Namespace) -> int:
    """Display statistical summary of digital book holdings."""
    stats = get_book_stats(data_dir=args.data_dir)
    if args.json:
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        return 0

    print("================================================================")
    print("      Meitei Digital Book Library Holdings & Statistics         ")
    print("================================================================")
    print(f"Total Registered Books:       {stats['total_books']}")
    print(f"Fully Imported Books:         {stats['fully_imported']}")
    print(f"Partially Imported Books:     {stats['partially_imported']}")
    print(f"Catalog-Only Books:           {stats['catalog_only']}")
    print(f"Total Imported Chapters:      {stats['total_imported_chapters']}")
    print(f"Total Segmented Passages:     {stats['total_passages']}")
    print("================================================================")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate schema, referential integrity, and strict citation completeness."""
    data_dir = args.data_dir
    fail_unreviewed = getattr(args, "fail_unreviewed", False)
    auditor = ProvenanceAuditor(data_dir=data_dir)
    report = auditor.audit(strict=args.strict, fail_unreviewed=fail_unreviewed)

    errors = report.errors
    warnings = report.warnings
    is_valid = report.is_valid

    if args.json:
        result_payload = {
            "valid": is_valid,
            "strict": args.strict,
            "status": "PASSED" if is_valid else "FAILED",
            "sources_count": report.sources_count,
            "core_entries_count": report.core_entries_count,
            "candidate_entries_count": report.candidate_entries_count,
            "variants_count": report.variants_count,
            "glosses_count": report.glosses_count,
            "grammar_records_count": report.grammar_records_count,
            "books_count": report.books_count,
            "book_passages_count": report.book_passages_count,
            "reviews_count": report.reviews_count,
            "awaiting_review_count": report.awaiting_review_count,
            "unverified_candidates_count": report.unverified_candidates_count,
            "citation_mismatch_count": report.citation_mismatch_count,
            "errors": errors,
            "warnings": warnings,
            "stats": report.stats,
        }
        print(json.dumps(result_payload, indent=2, ensure_ascii=False))
        return 0 if is_valid else 1

    # Text report
    print("================================================================")
    status_str = "PASSED" if is_valid else "FAILED"
    print(f"          DATASET SCHEMA & INTEGRITY VALIDATION: {status_str}         ")
    print("================================================================")
    print(f"Strict Mode:                 {'Enabled' if args.strict else 'Disabled'}")
    print(f"Sources Validated:           {report.sources_count:,}")
    print(f"Core Lexicon Entries:        {report.core_entries_count:,}")
    print(f"Candidate Lexicon Entries:   {report.candidate_entries_count:,}")
    print(f"Spelling Variants:           {report.variants_count:,}")
    print(f"Translation Glosses:         {report.glosses_count:,}")
    if report.books_count > 0:
        print(f"Digital Heritage Books:      {report.books_count:,} ({report.book_passages_count:,} passages)")

    if warnings:
        print("----------------------------------------------------------------")
        print("Warnings:")
        for w in warnings:
            print(f"  [WARN] {w}")

    if errors:
        print("----------------------------------------------------------------")
        print("Validation Errors:", file=sys.stderr)
        for err in errors:
            print(f"  [ERROR] {err}", file=sys.stderr)
        print("================================================================", file=sys.stderr)
        return 1

    print("Integrity Guarantee:         100% Valid (Zero Referential Errors)")
    print("================================================================")
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    """Print project metadata and architectural principles."""
    if getattr(args, "json", False):
        info_data = {
            "package": "meitei",
            "version": meitei.__version__,
            "architecture": "Lightweight, offline-first, dual JSONL + SQLite",
            "runtime_dependencies": "None (Python standard library only)",
            "python_requires": ">=3.9",
            "scripts_supported": ["Meitei Mayek (U+ABC0-U+ABFF)", "Bengali", "Latin"],
            "license": {"code": "MIT", "data": "CC BY-SA 4.0"},
        }
        print(json.dumps(info_data, indent=2, ensure_ascii=False))
        return 0

    print("================================================================")
    print("         Meitei Language Library (meitei) - Foundation          ")
    print("================================================================")
    print(f"Version:              {meitei.__version__}")
    print("Architecture:         Lightweight, offline-first, dual JSONL + SQLite")
    print("Runtime Dependencies: ZERO (Python standard library only)")
    print("Python Requirement:   >= 3.9")
    print("Script Support:       Meitei Mayek (U+ABC0-U+ABFF), Bengali, Latin")
    print("Data Provenance:      Strict attestation vs verification tracking")
    print("Licenses:             Software: MIT | Language Data: CC BY-SA 4.0")
    print("================================================================")
    return 0


def cmd_init_db(args: argparse.Namespace) -> int:
    """Initialize SQLite database schema."""
    db_path = args.db_path
    db = MeiteiDatabase(db_path)
    db.close()
    print(f"Initialized Meitei SQLite database schema at: {db_path}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    """Display database statistics and verification status counts."""
    db_path = args.db_path
    if not Path(db_path).exists():
        print(f"Database not found at '{db_path}'. Run 'meitei init-db --db-path {db_path}' first.", file=sys.stderr)
        return 1

    db = MeiteiDatabase(db_path)
    try:
        stats = db.get_stats()
        if getattr(args, "json", False):
            print(json.dumps(stats, indent=2, ensure_ascii=False))
            return 0

        print("================================================================")
        print(f"Meitei Database Statistics: {db_path}")
        print("================================================================")
        print(f"Total Entries:     {stats['entries_count']:,}")
        print(f"Total Senses:      {stats['senses_count']:,}")
        print(f"Total Sources:     {stats['sources_count']:,}")
        print(f"Total Provenance:  {stats['provenance_count']:,}")
        print("----------------------------------------------------------------")
        print("Verification Status Breakdown:")
        breakdown = stats["verification_breakdown"]
        if not breakdown:
            print("  (No provenance records yet)")
        else:
            for status, count in sorted(breakdown.items()):
                print(f"  - {status:24s}: {count:,}")
        print("================================================================")
    finally:
        db.close()
    return 0


def cmd_import_jsonl(args: argparse.Namespace) -> int:
    """Import records from JSONL into SQLite."""
    file_path = args.file_path
    db_path = args.db_path
    rec_type = args.type

    if not Path(file_path).exists():
        print(f"Error: File '{file_path}' does not exist.", file=sys.stderr)
        return 1

    db = MeiteiDatabase(db_path)
    try:
        if rec_type == "sources":
            count = db.import_sources_from_jsonl(file_path)
            print(f"Successfully imported {count} source(s) into '{db_path}'.")
        else:
            count = db.import_entries_from_jsonl(file_path)
            print(f"Successfully imported {count} entry/entries into '{db_path}'.")
    finally:
        db.close()
    return 0


def cmd_export_jsonl(args: argparse.Namespace) -> int:
    """Export records from SQLite to JSONL."""
    file_path = args.file_path
    db_path = args.db_path
    rec_type = args.type

    if not Path(db_path).exists():
        print(f"Error: Database '{db_path}' does not exist.", file=sys.stderr)
        return 1

    db = MeiteiDatabase(db_path)
    try:
        if rec_type == "sources":
            count = db.export_sources_to_jsonl(file_path)
            print(f"Successfully exported {count} source(s) to '{file_path}'.")
        else:
            count = db.export_entries_to_jsonl(file_path)
            print(f"Successfully exported {count} entry/entries to '{file_path}'.")
    finally:
        db.close()
    return 0


def cmd_add_source(args: argparse.Namespace) -> int:
    """Register a new bibliographic source."""
    source = BibliographicSource(
        source_id=args.source_id,
        title=args.title,
        author=args.author,
        year=args.year,
        source_type=args.source_type,
    )
    db = MeiteiDatabase(args.db_path)
    try:
        db.upsert_source(source)
        print(f"Registered source '{source.source_id}' in '{args.db_path}'.")
    finally:
        db.close()
    return 0


# =============================================================================
# CLI Main Entrypoint
# =============================================================================

def main(argv: Optional[List[str]] = None) -> int:
    """
    Main CLI entrypoint for meitei command.

    Args:
        argv: Command-line argument list (defaults to sys.argv[1:] if None).

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    # Configure UTF-8 streams on Windows to prevent cp1252 charmap encoding errors
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
        except Exception:
            pass

    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""
Comprehensive Unit and Subprocess Tests for the Meitei CLI executable and subcommands.

Verifies:
- `meitei lookup` across plain text and JSON outputs
- `meitei search` with `--lang`, `--verified-only`, and `--json`
- `meitei translate` with `--from`, `--to`, `--verified-only`, and `--json`
- Provenance guarantees: unverified glosses are strictly identified and filtered
- `meitei languages` listing catalog and emitting valid JSON
- `meitei validate` standard, `--strict`, and `--json` executions
- Predictable exit codes (0 for success/empty matches, 1 for runtime errors, 2 for CLI arg/language errors)
- Graceful handling of empty or missing datasets
- Full Unicode support for Meitei Mayek and Bengali script
- Execution parity between `python -m meitei` and installed `meitei` binary
"""

import io
import json
import shutil
import subprocess
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import pytest

from meitei import cli
from meitei.database import MeiteiDatabase
from meitei.models import (
    BibliographicSource,
    Entry,
    PartOfSpeech,
    ProvenanceRecord,
    Sense,
    VerificationStatus,
)


# =============================================================================
# Subprocess Helper
# =============================================================================

def run_cli_subprocess(args, check=False):
    """Run `python -m meitei <args>` via subprocess with UTF-8 encoding."""
    cmd = [sys.executable, "-m", "meitei"] + args
    res = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed ({res.returncode}): {res.stderr}")
    return res


# =============================================================================
# Lookup Subcommand Tests
# =============================================================================

def test_cli_lookup_plain_text():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["lookup", "mi"])
    assert exit_code == 0
    out = f.getvalue()
    assert "ꯃꯤ" in out
    assert "SOURCE_ATTESTED" in out
    assert "MEI-SRC-000001" in out


def test_cli_lookup_json_output():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["lookup", "mi", "--json"])
    assert exit_code == 0
    data = json.loads(f.getvalue())
    assert isinstance(data, list)
    assert len(data) >= 1
    item = next(e for e in data if e["entry_id"] == "MEI-LEX-0000001")
    assert item["canonical_lemma"] == "ꯃꯤ"
    assert item["headword_roman"] == "mi"
    assert item["status"] == "SOURCE_ATTESTED"
    assert item["citations"][0]["source_id"] == "MEI-SRC-000001"


def test_cli_lookup_nonexistent_returns_zero_exit_code():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["lookup", "nonexistent_term_xyz_123"])
    assert exit_code == 0
    assert "No entries found" in f.getvalue()

    f_json = io.StringIO()
    with redirect_stdout(f_json):
        exit_code = cli.main(["lookup", "nonexistent_term_xyz_123", "--json"])
    assert exit_code == 0
    assert json.loads(f_json.getvalue()) == []


# =============================================================================
# Search Subcommand Tests
# =============================================================================

def test_cli_search_plain_and_lang():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["search", "person", "--lang", "en"])
    assert exit_code == 0
    out = f.getvalue()
    assert "Search results for 'person'" in out
    assert "ꯃꯤ" in out
    assert "SOURCE_ATTESTED" in out


def test_cli_search_json():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["search", "person", "--lang", "en", "--json"])
    assert exit_code == 0
    data = json.loads(f.getvalue())
    assert isinstance(data, list)
    assert any(r["canonical_lemma"] == "ꯃꯤ" for r in data)


def test_cli_search_verified_only():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["search", "korou", "--verified-only"])
    assert exit_code == 0
    assert "No entries found" in f.getvalue()


# =============================================================================
# Translate Subcommand Tests
# =============================================================================

def test_cli_translate_from_english():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["translate", "person", "--from", "en"])
    assert exit_code == 0
    out = f.getvalue()
    assert "Translations for 'person' (en -> mni):" in out
    assert "ꯃꯤ (mi)" in out
    assert "SOURCE_ATTESTED" in out
    assert "Page 54, No. 22" in out


def test_cli_translate_from_english_json():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["translate", "person", "--from", "en", "--json"])
    assert exit_code == 0
    data = json.loads(f.getvalue())
    assert isinstance(data, list)
    match = next(m for m in data if m["target_text"] == "ꯃꯤ")
    assert match["target_roman"] == "mi"
    assert match["status"] == "SOURCE_ATTESTED"
    assert match["gloss"] == "person"


def test_cli_translate_from_hi_verified_only_empty():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["translate", "person", "--from", "hi", "--verified-only"])
    assert exit_code == 0
    assert "No translations found" in f.getvalue()

    f_json = io.StringIO()
    with redirect_stdout(f_json):
        exit_code = cli.main(["translate", "person", "--from", "hi", "--verified-only", "--json"])
    assert exit_code == 0
    assert json.loads(f_json.getvalue()) == []


def test_cli_translate_unverified_provenance_isolation():
    # 1. Unverified candidate 'sun' without verified-only includes UNVERIFIED label
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["translate", "sun", "--from", "en"])
    assert exit_code == 0
    out = f.getvalue()
    assert "ꯀꯣꯔꯧ (korou)" in out
    assert "Status: UNVERIFIED" in out

    # 2. With --verified-only, unverified claims are strictly filtered out
    f2 = io.StringIO()
    with redirect_stdout(f2):
        exit_code2 = cli.main(["translate", "sun", "--from", "en", "--verified-only"])
    assert exit_code2 == 0
    assert "No translations found" in f2.getvalue()


# =============================================================================
# Languages Subcommand Tests
# =============================================================================

def test_cli_languages_plain():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["languages"])
    assert exit_code == 0
    out = f.getvalue()
    assert "mni" in out
    assert "Meitei (Manipuri / Meiteilon)" in out
    assert "English" in out
    assert "Hindi" in out
    assert "Bengali" in out
    assert "Assamese" in out


def test_cli_languages_json():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["languages", "--json"])
    assert exit_code == 0
    data = json.loads(f.getvalue())
    assert isinstance(data, list)
    codes = {l["code"] for l in data}
    assert {"mni", "en", "hi", "bn", "as"}.issubset(codes)


# =============================================================================
# Validate Subcommand Tests
# =============================================================================

def test_cli_validate_plain_and_strict():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["validate"])
    assert exit_code == 0
    assert "DATASET SCHEMA & INTEGRITY VALIDATION: PASSED" in f.getvalue()

    f_strict = io.StringIO()
    with redirect_stdout(f_strict):
        exit_strict = cli.main(["validate", "--strict"])
    assert exit_strict == 0
    out_strict = f_strict.getvalue()
    assert "Strict Mode:                 Enabled" in out_strict
    assert "DATASET SCHEMA & INTEGRITY VALIDATION: PASSED" in out_strict


def test_cli_validate_json():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["validate", "--strict", "--json"])
    assert exit_code == 0
    report = json.loads(f.getvalue())
    assert report["valid"] is True
    assert report["strict"] is True
    assert report["status"] == "PASSED"
    assert report["core_entries_count"] >= 10
    assert report["sources_count"] >= 7
    assert report["errors"] == []


# =============================================================================
# Error Handling & Exit Codes
# =============================================================================

def test_cli_invalid_language_codes():
    # Invalid search language code returns exit code 2
    err_search = io.StringIO()
    with redirect_stderr(err_search):
        exit_code = cli.main(["search", "test", "--lang", "invalid_lang"])
    assert exit_code == 2
    assert "Invalid or unsupported language code" in err_search.getvalue()

    # Invalid source language in translate returns exit code 2
    err_trans = io.StringIO()
    with redirect_stderr(err_trans):
        exit_code = cli.main(["translate", "test", "--from", "invalid_source"])
    assert exit_code == 2
    assert "Invalid or unsupported source language" in err_trans.getvalue()


def test_cli_empty_datasets_do_not_crash(tmp_path):
    empty_dir = str(tmp_path / "empty_data")
    Path(empty_dir).mkdir()

    # Lookup on empty directory
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["lookup", "test", "--data-dir", empty_dir])
    assert exit_code == 0
    assert "No entries found" in f.getvalue()

    # JSON lookup on empty directory
    f_json = io.StringIO()
    with redirect_stdout(f_json):
        exit_code = cli.main(["lookup", "test", "--data-dir", empty_dir, "--json"])
    assert exit_code == 0
    assert json.loads(f_json.getvalue()) == []

    # Translate on empty directory
    f_tr = io.StringIO()
    with redirect_stdout(f_tr):
        exit_code = cli.main(["translate", "test", "--from", "en", "--data-dir", empty_dir, "--json"])
    assert exit_code == 0
    assert json.loads(f_tr.getvalue()) == []


# =============================================================================
# Subprocess Tests: python -m meitei and installed meitei binary
# =============================================================================

def test_subprocess_python_m_meitei_lookup():
    res = run_cli_subprocess(["lookup", "mi", "--json"], check=True)
    data = json.loads(res.stdout)
    assert any(e["canonical_lemma"] == "ꯃꯤ" for e in data)


def test_subprocess_python_m_meitei_translate():
    res = run_cli_subprocess(["translate", "person", "--from", "en", "--json"], check=True)
    data = json.loads(res.stdout)
    assert any(m["target_text"] == "ꯃꯤ" for m in data)


def test_subprocess_python_m_meitei_languages():
    res = run_cli_subprocess(["languages", "--json"], check=True)
    data = json.loads(res.stdout)
    assert any(l["code"] == "mni" for l in data)


def test_subprocess_python_m_meitei_validate_strict():
    res = run_cli_subprocess(["validate", "--strict", "--json"], check=True)
    data = json.loads(res.stdout)
    assert data["valid"] is True
    assert data["strict"] is True


def test_subprocess_python_m_meitei_exit_codes():
    # Unsupported subcommand returns exit code 2
    res = run_cli_subprocess(["unsupported_subcommand_test"])
    assert res.returncode == 2

    # Invalid language code returns exit code 2
    res_lang = run_cli_subprocess(["search", "query", "--lang", "bad_code"])
    assert res_lang.returncode == 2


def test_subprocess_installed_binary_if_available():
    meitei_bin = shutil.which("meitei")
    if meitei_bin:
        res = subprocess.run(
            [meitei_bin, "languages", "--json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        assert res.returncode == 0
        data = json.loads(res.stdout)
        assert any(l["code"] == "mni" for l in data)


# =============================================================================
# Retain Original Database and Admin Subcommand Tests
# =============================================================================

def test_cli_info():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["info"])
    assert exit_code == 0
    out = f.getvalue()
    assert "Meitei Language Library (meitei)" in out
    assert "ZERO" in out
    assert "Meitei Mayek" in out


def test_cli_init_db_and_stats(tmp_path):
    db_file = str(tmp_path / "test.sqlite3")

    # 1. Initialize
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["init-db", "--db-path", db_file])
    assert exit_code == 0
    assert Path(db_file).exists()

    # 2. Stats on empty DB
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["stats", "--db-path", db_file])
    assert exit_code == 0
    out = f.getvalue()
    assert "Total Entries:     0" in out


def test_cli_add_source_and_lookup_sqlite(tmp_path):
    db_file = str(tmp_path / "test_lookup.sqlite3")
    cli.main(["init-db", "--db-path", db_file])

    cli.main([
        "add-source",
        "src_puya_sun",
        "Numit Kappa",
        "--author", "Ancient Meitei",
        "--year", "1500",
        "--type", "puya",
        "--db-path", db_file,
    ])

    with MeiteiDatabase(db_file) as db:
        entry = Entry(
            entry_id="e_numit_01",
            headword_meitei="ꯅꯨꯃꯤꯠ",
            headword_roman="numit",
            headword_bengali="নুমীৎ",
            senses=[
                Sense(
                    sense_id="s_numit_01",
                    definition_en="Sun; daytime; day",
                    definition_mni="ꯅꯨꯃꯤꯠ",
                    part_of_speech=PartOfSpeech.NOUN,
                )
            ],
            provenance=[
                ProvenanceRecord(
                    provenance_id="p_numit_01",
                    source_id="src_puya_sun",
                    attestation_type="historical_attestation",
                    verification_status=VerificationStatus.HISTORICAL_ATTESTED,
                )
            ],
        )
        db.upsert_entry(entry)

    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["lookup", "ꯅꯨꯃꯤꯠ", "--db-path", db_file])
    assert exit_code == 0
    out = f.getvalue()
    assert "ꯅꯨꯃꯤꯠ (numit)" in out
    assert "Sun; daytime; day" in out


def test_cli_import_and_export_jsonl(tmp_path):
    db_file = str(tmp_path / "test_io.sqlite3")
    jsonl_in = tmp_path / "input.jsonl"
    jsonl_out = tmp_path / "output.jsonl"

    cli.main(["init-db", "--db-path", db_file])

    with MeiteiDatabase(db_file) as db:
        db.upsert_source(
            BibliographicSource(
                source_id="src_oral_01",
                title="Oral Fieldwork",
                source_type="fieldwork",
            )
        )

    sample_entry = Entry(
        entry_id="e_sing_01",
        headword_meitei="ꯁꯤꯡ",
        headword_roman="sing",
        senses=[
            Sense(
                sense_id="s_sing_01",
                definition_en="Ginger",
                part_of_speech=PartOfSpeech.NOUN,
            )
        ],
        provenance=[
            ProvenanceRecord(
                provenance_id="p_sing_01",
                source_id="src_oral_01",
                verification_status=VerificationStatus.CONTEMPORARY_VERIFIED,
            )
        ],
    )
    with open(jsonl_in, "w", encoding="utf-8") as f:
        f.write(sample_entry.to_json() + "\n")

    cli.main(["import-jsonl", str(jsonl_in), "--db-path", db_file])
    cli.main(["export-jsonl", str(jsonl_out), "--db-path", db_file])
    assert jsonl_out.exists()


def test_cli_error_handling(tmp_path):
    f = io.StringIO()
    with redirect_stderr(f):
        code = cli.main(["stats", "--db-path", str(tmp_path / "does_not_exist.sqlite3")])
    assert code == 1

    err = io.StringIO()
    with redirect_stderr(err):
        code = cli.main(["import-jsonl", str(tmp_path / "missing.jsonl"), "--db-path", ":memory:"])
    assert code == 1

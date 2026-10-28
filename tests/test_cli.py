# -*- coding: utf-8 -*-
"""Unit tests for meitei_lang CLI commands."""

import io
import sys
from contextlib import redirect_stdout
import pytest

from meitei_lang import cli


def test_cli_info():
    f = io.StringIO()
    with redirect_stdout(f):
        cli.cmd_info()
    out = f.getvalue()
    assert "Meitei-Lang" in out
    assert "170,202" in out
    assert "10 books" in out
    assert "10 songs" in out
    assert "120 sentences" in out


def test_cli_books():
    f = io.StringIO()
    with redirect_stdout(f):
        cli.cmd_books()
    out = f.getvalue()
    assert "khamba_thoibi" in out
    assert "numit_kappa" in out
    assert "chainarol" in out
    assert "pakhangba_laihui" in out


def test_cli_book():
    f = io.StringIO()
    with redirect_stdout(f):
        cli.cmd_book("khamba_thoibi")
    out = f.getvalue()
    assert "Khamba Thoibi" in out
    assert "Chapter 1" in out


def test_cli_read():
    f = io.StringIO()
    with redirect_stdout(f):
        cli.cmd_read("numit_kappa", 1)
    out = f.getvalue()
    assert "Numit Kappa" in out
    assert "ꯅꯨꯃꯤꯠ ꯀꯥꯞꯄ" in out


def test_cli_songs():
    f = io.StringIO()
    with redirect_stdout(f):
        cli.cmd_songs()
    out = f.getvalue()
    assert "sana_leibak_manipur" in out
    assert "thabal_chongba_ishei" in out
    assert "khulang_eshei_harvest" in out


def test_cli_lyrics():
    f = io.StringIO()
    with redirect_stdout(f):
        cli.cmd_lyrics("sana_leibak_manipur", "roman")
    out = f.getvalue()
    assert "Sana leibak Manipur" in out


def test_cli_sentences():
    f = io.StringIO()
    with redirect_stdout(f):
        cli.cmd_sentences(category="greetings")
    out = f.getvalue()
    assert "greet_001" in out
    assert "Khurumjari" in out


def test_cli_word():
    f = io.StringIO()
    with redirect_stdout(f):
        cli.cmd_word("ꯃꯃꯥ")
    out = f.getvalue()
    assert "mama" in out
    assert "mother" in out


def test_cli_search():
    f = io.StringIO()
    with redirect_stdout(f):
        cli.cmd_search("Manipur")
    out = f.getvalue()
    assert "Search results for 'Manipur'" in out
    assert "Vocabulary" in out
    assert "Books" in out
    assert "Songs" in out


def test_cli_transliterate():
    f = io.StringIO()
    with redirect_stdout(f):
        cli.cmd_transliterate("ꯃꯃꯥ", target="roman")
    out = f.getvalue()
    assert "mama" in out


def test_cli_error_handling():
    f = io.StringIO()
    with redirect_stdout(f):
        cli.cmd_book("nonexistent_book")
    assert "Error:" in f.getvalue()

    f2 = io.StringIO()
    with redirect_stdout(f2):
        cli.cmd_read("khamba_thoibi", 999)
    assert "Error:" in f2.getvalue()

    f3 = io.StringIO()
    with redirect_stdout(f3):
        cli.cmd_lyrics("nonexistent_song")
    assert "Error:" in f3.getvalue()


# -*- coding: utf-8 -*-
"""Unit tests for meitei_lang transliteration and script handling."""

import pytest
from meitei_lang.transliteration import (
    normalize_text,
    detect_script,
    validate_text,
    meitei_to_roman,
    meitei_to_bengali,
    bengali_to_meitei,
    roman_to_meitei,
    transliterate,
)
from meitei_lang.exceptions import ValidationError


def test_normalize_text():
    raw = "ꯃꯩꯇꯩ    ꯂꯣꯟ  "
    norm = normalize_text(raw)
    assert norm == "ꯃꯩꯇꯩ ꯂꯣꯟ"

    with pytest.raises(TypeError):
        normalize_text(123)  # type: ignore


def test_detect_script():
    assert detect_script("ꯃꯩꯇꯩ ꯃꯌꯦꯛ") == "meitei_mayek"
    assert detect_script("মণিপুর") == "bengali"
    assert detect_script("Manipur") == "latin"
    assert detect_script("12345") == "unknown"


def test_validate_text():
    # Valid Meitei Mayek
    assert validate_text("ꯃꯩꯇꯩ", expected_script="meitei_mayek") is True

    # Valid Bengali
    assert validate_text("মণিপুর", expected_script="bengali") is True

    # Valid Latin
    assert validate_text("Manipuri", expected_script="latin") is True

    # Mismatched script
    with pytest.raises(ValidationError):
        validate_text("Hello", expected_script="meitei_mayek")


def test_meitei_to_roman():
    # Basic word
    res = meitei_to_roman("ꯈꯨꯔꯨꯝꯖꯔꯤ")
    assert isinstance(res, str)
    assert "kh" in res
    assert "j" in res

    # Mother
    assert meitei_to_roman("ꯃꯃꯥ") == "mama"

    # Empty string
    assert meitei_to_roman("") == ""


def test_meitei_to_bengali():
    # "মণিপুর" / "ꯃꯅꯤꯄꯨꯔ"
    bengali = meitei_to_bengali("ꯃꯅꯤꯄꯨꯔ")
    assert any(0x0980 <= ord(c) <= 0x09FF for c in bengali)


def test_bengali_to_meitei():
    meitei = bengali_to_meitei("মণিপুর")
    assert any(0xABC0 <= ord(c) <= 0xABFF for c in meitei)


def test_roman_to_meitei():
    mayek = roman_to_meitei("mama")
    assert "ꯃ" in mayek


def test_transliterate_wrapper():
    # Meitei to Roman
    r = transliterate("ꯃꯃꯥ", target_script="roman")
    assert r == "mama"

    # Identity
    assert transliterate("mama", source_script="roman", target_script="roman") == "mama"

    # Unsupported script
    with pytest.raises(ValueError):
        transliterate("test", target_script="hieroglyphs")

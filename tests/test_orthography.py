# -*- coding: utf-8 -*-
"""
Unit tests for Unicode normalization, script detection, and orthographic conversion.
"""

import pytest

from meitei.orthography import (
    AmbiguousConversionError,
    ConversionStatus,
    ScriptConversionResult,
    UnsupportedConversionError,
    convert_bengali_to_mayek,
    convert_mayek_to_bengali,
    convert_mayek_to_roman,
    convert_script,
    get_script_variants,
)
from meitei.unicode_utils import (
    decompose_to_codepoints,
    detect_script,
    has_combining_marks,
    is_bengali_char,
    is_combining_mark,
    is_latin_char,
    is_meitei_mayek_char,
    normalize_text,
)


# =============================================================================
# 1. Unicode Normalization Tests
# =============================================================================

def test_normalize_text_empty_and_types():
    assert normalize_text("") == ""
    with pytest.raises(TypeError):
        normalize_text(None)  # type: ignore
    with pytest.raises(TypeError):
        normalize_text(12345)  # type: ignore


def test_normalize_text_forms():
    # Combining character decomposition & composition
    # Decomposed: Latin 'e' + combining acute accent
    decomposed = "e\u0301"
    composed = "\u00e9"
    assert normalize_text(decomposed, form="NFC") == composed
    assert normalize_text(composed, form="NFD") == decomposed

    with pytest.raises(ValueError):
        normalize_text("test", form="INVALID_FORM")


def test_normalize_whitespace():
    raw = "   ꯃꯤ    \t\u00a0\u00a0  ꯑꯃꯥ   \n  ꯂꯥꯛꯏ   "
    clean = normalize_text(raw, normalize_whitespace=True)
    assert clean == "ꯃꯤ ꯑꯃꯥ\nꯂꯥꯛꯏ"


def test_normalize_punctuation():
    # Devanagari danda replaced with Meitei Mayek Cheikhei (U+ABEB)
    mayek_with_danda = "ꯃꯤ ꯑꯃꯥ ꯂꯥꯛꯏ।"
    norm = normalize_text(mayek_with_danda, normalize_punctuation=True)
    assert norm.endswith("\uabeb")

    # Quotes normalization
    curly_quotes = "\u201cꯃꯤ\u201d"
    norm_quotes = normalize_text(curly_quotes, normalize_punctuation=True)
    assert norm_quotes == '"ꯃꯤ"'


def test_combining_marks_and_codepoints():
    # Base letter Kok (U+ABC0) + Anap vowel sign (U+ABE5)
    text = "\uabc0\uabe5"
    assert has_combining_marks(text) is True
    assert is_combining_mark("\uabe5") is True
    assert is_combining_mark("\uabc0") is False

    cps = decompose_to_codepoints(text)
    assert cps == ["U+ABC0", "U+ABE5"]


# =============================================================================
# 2. Script Detection Tests
# =============================================================================

def test_detect_script_heuristics():
    # Meitei Mayek
    assert detect_script("ꯃꯤ") == "meitei_mayek"
    assert detect_script("ꯅꯨꯃꯤꯠ ꯀꯥꯞꯄ꯫") == "meitei_mayek"

    # Bengali Script
    assert detect_script("মণিপুর") == "bengali"
    assert detect_script("মীতৈলোন") == "bengali"

    # Latin / Roman
    assert detect_script("Manipur") == "latin"
    assert detect_script("thabak") == "latin"
    assert detect_script("mī") == "latin"

    # Mixed script
    assert detect_script("ꯃꯤ mi") == "mixed"
    assert detect_script("ꯃꯅꯤꯄꯨꯔ Manipur") == "mixed"

    # Unknown (digits, punctuation, or empty)
    assert detect_script("") == "unknown"
    assert detect_script("   ") == "unknown"
    assert detect_script("12345 !!! ???") == "unknown"


def test_character_classifiers():
    assert is_meitei_mayek_char("ꯃ") is True
    assert is_meitei_mayek_char("ক") is False
    assert is_meitei_mayek_char("m") is False

    assert is_bengali_char("ক") is True
    assert is_bengali_char("ম") is True
    assert is_bengali_char("ꯃ") is False

    assert is_latin_char("m") is True
    assert is_latin_char("Z") is True
    assert is_latin_char("ā") is True
    assert is_latin_char("ə") is True
    assert is_latin_char("ꯀ") is False


# =============================================================================
# 3. Rule-Governed Script Conversion Tests
# =============================================================================

def test_convert_script_empty():
    assert convert_script("", "bengali") == ""
    assert convert_script("   ", "latin") == ""


def test_convert_mayek_to_bengali():
    # ꯃꯤ (Mit + Inap) -> মি
    res_mi = convert_script("ꯃꯤ", "bengali")
    assert res_mi == "মি"

    # ꯀꯪꯂꯩꯄꯥꯛ (Kok + Nung + Lai + Cheinap + Pa + Anap + Kok Lonsum) -> কংলৈপাক্
    res_kangleipak = convert_script("ꯀꯪꯂꯩꯄꯥꯛ", "bengali")
    assert res_kangleipak == "কংলৈপাক্"

    # Digits: ꯱꯲꯳ -> ১২৩
    res_digits = convert_script("꯱꯲꯳", "bengali")
    assert res_digits == "১২৩"

    # Punctuation: Cheikhei (꯫) -> Danda (।)
    res_punct = convert_script("ꯂꯥꯛꯏ꯫", "bengali")
    assert res_punct.endswith("।")


def test_convert_mayek_to_roman():
    # ꯃꯤ -> mi
    res_mi = convert_script("ꯃꯤ", "latin")
    assert res_mi == "mi"

    # ꯑꯃ -> ama
    res_ama = convert_script("ꯑꯃ", "latin")
    assert res_ama == "ama"

    # ꯊꯕꯛ (Thou + Ba + Kok Lonsum) -> thabak
    res_thabak = convert_script("ꯊꯕꯛ", "latin")
    assert res_thabak == "thabak"


def test_convert_bengali_to_mayek_strict_and_ambiguous():
    # Clean mapped Bengali text
    clean_bengali = "অমা"  # Atiya + Mit + Anap
    res = convert_script(clean_bengali, "meitei_mayek", strict=True)
    assert "\uabd1" in res  # Atiya

    # Ambiguous Bengali sibilant 'শ' in strict mode -> raises AmbiguousConversionError
    ambig_bengali = "শ"
    with pytest.raises(AmbiguousConversionError) as exc_info:
        convert_script(ambig_bengali, "meitei_mayek", strict=True)
    assert "ambiguous" in str(exc_info.value).lower()

    # Non-strict mode converts with ambiguity reported in detailed result
    detailed = convert_bengali_to_mayek(ambig_bengali, strict=False)
    assert detailed.status == ConversionStatus.AMBIGUOUS
    assert len(detailed.ambiguities) > 0


def test_convert_latin_to_mayek_strict_non_guessing_policy():
    # Strict mode refuses to guess arbitrary Roman text without attestation
    with pytest.raises(AmbiguousConversionError) as exc_info:
        convert_script("arbitrary_word", "meitei_mayek", strict=True)
    assert "Cannot strictly convert Romanized string" in str(exc_info.value)


def test_unsupported_conversion_error():
    with pytest.raises(UnsupportedConversionError) as exc_info:
        convert_script("ꯃꯤ", "cyrillic")
    assert "Target script 'cyrillic' is not supported" in str(exc_info.value)

    with pytest.raises(UnsupportedConversionError):
        convert_script("ꯃꯤ", "devanagari")


def test_convert_script_same_source_and_target():
    mayek = "ꯃꯤ"
    assert convert_script(mayek, "meitei_mayek") == mayek
    roman = "thabak"
    assert convert_script(roman, "latin") == roman


# =============================================================================
# 4. Registered Spelling Variants Tests
# =============================================================================

def test_get_script_variants_for_verified_entry():
    # Query 'mi' which has registered variants in data/lexicon/variants.jsonl:
    # 'mee' (McCulloch 1859), 'mī' (Grierson 1904), 'মী' (Cheitharol Kumbaba 1967)
    vars_from_roman = get_script_variants("mi")
    assert "meitei_mayek" in vars_from_roman
    assert "ꯃꯤ" in vars_from_roman["meitei_mayek"]
    assert "mee" in vars_from_roman["latin"]
    assert "mī" in vars_from_roman["latin"]
    assert "মী" in vars_from_roman["bengali"]

    # Query using Meitei Mayek
    vars_from_mayek = get_script_variants("ꯃꯤ")
    assert "mee" in vars_from_mayek["latin"]
    assert "মী" in vars_from_mayek["bengali"]

    # Query using historical variant form 'mee'
    vars_from_mee = get_script_variants("mee")
    assert "ꯃꯤ" in vars_from_mee["meitei_mayek"]


def test_get_script_variants_uncataloged_word():
    # Uncataloged word returns word in its detected script without error
    vars_unknown = get_script_variants("unknown_test_token")
    assert vars_unknown["latin"] == ["unknown_test_token"]
    assert vars_unknown["meitei_mayek"] == []

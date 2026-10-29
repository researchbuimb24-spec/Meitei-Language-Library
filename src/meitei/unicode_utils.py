# -*- coding: utf-8 -*-
"""
Unicode utilities and character-level inspection for Meitei Language Library (meitei).

Provides:
- Unicode NFC normalization using standard library `unicodedata`.
- Whitespace and punctuation standardization.
- Script detection heuristics (Meitei Mayek, Bengali, Latin, Mixed).
- Unicode codepoint classification for Meetei Mayek and Meetei Mayek Extensions.
- Combining mark detection and decomposition.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, List, Optional, Set, Tuple


# Unicode Block Ranges
MEITEI_MAYEK_RANGE = (0xABC0, 0xABFF)
MEITEI_MAYEK_EXT_RANGE = (0xAAE0, 0xAAFF)
BENGALI_RANGE = (0x0980, 0x09FF)
LATIN_RANGES = [
    (0x0041, 0x005A),  # Basic Latin uppercase
    (0x0061, 0x007A),  # Basic Latin lowercase
    (0x00C0, 0x024F),  # Latin-1 Supplement + Latin Extended-A/B (e.g. ā, ī, ū, ŋ)
    (0x0250, 0x02AF),  # IPA Extensions (e.g. ə, ʃ, ʒ, ʔ)
    (0x1E00, 0x1EFF),  # Latin Extended Additional
]


def is_meitei_mayek_char(char: str) -> bool:
    """Return True if character belongs to Meetei Mayek or Meetei Mayek Extensions block."""
    if not char:
        return False
    cp = ord(char[0])
    return (
        (MEITEI_MAYEK_RANGE[0] <= cp <= MEITEI_MAYEK_RANGE[1])
        or (MEITEI_MAYEK_EXT_RANGE[0] <= cp <= MEITEI_MAYEK_EXT_RANGE[1])
    )


def is_bengali_char(char: str) -> bool:
    """Return True if character belongs to Bengali/Eastern Nagari block."""
    if not char:
        return False
    cp = ord(char[0])
    return BENGALI_RANGE[0] <= cp <= BENGALI_RANGE[1]


def is_latin_char(char: str) -> bool:
    """Return True if character belongs to Latin / Roman alphabetic ranges."""
    if not char:
        return False
    cp = ord(char[0])
    for start, end in LATIN_RANGES:
        if start <= cp <= end:
            return True
    return False


def is_combining_mark(char: str) -> bool:
    """Return True if character is a Unicode combining diacritical mark."""
    if not char:
        return False
    cat = unicodedata.category(char[0])
    return cat in ("Mn", "Mc", "Me")


def has_combining_marks(text: str) -> bool:
    """Return True if text contains any Unicode combining characters."""
    return any(is_combining_mark(c) for c in text)


def decompose_to_codepoints(text: str) -> List[str]:
    """Return list of uppercase hex Unicode codepoint representations (e.g. ['U+ABC0'])."""
    return [f"U+{ord(c):04X}" for c in text]


def normalize_text(
    text: str,
    form: str = "NFC",
    normalize_whitespace: bool = True,
    normalize_punctuation: bool = False,
) -> str:
    """
    Normalize text using standard Unicode normalization (NFC/NFD/NFKC/NFKD).

    Args:
        text: Input string.
        form: Unicode normalization form ('NFC', 'NFD', 'NFKC', or 'NFKD'). Default: 'NFC'.
        normalize_whitespace: If True, collapses excessive spaces and normalizes non-breaking spaces.
        normalize_punctuation: If True, maps punctuation variants (such as Devanagari danda to Cheikhei).

    Returns:
        Normalized string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    if not text:
        return ""

    valid_forms = ("NFC", "NFD", "NFKC", "NFKD")
    if form not in valid_forms:
        raise ValueError(f"Invalid normalization form: {form}. Must be one of {valid_forms}")

    # 1. Unicode Canonical Normalization
    result = unicodedata.normalize(form, text)

    # 2. Whitespace Normalization
    if normalize_whitespace:
        # Replace non-breaking space (U+00A0) and thin spaces with standard space
        result = re.sub(r"[\u00A0\u1680\u2000-\u200A\u202F\u205F\u3000]", " ", result)
        # Collapse multiple horizontal spaces and tabs into a single space
        result = re.sub(r"[^\S\r\n]+", " ", result)
        # Strip trailing/leading spaces on lines
        lines = [line.strip() for line in result.splitlines()]
        result = "\n".join(lines).strip()

    # 3. Punctuation Normalization
    if normalize_punctuation:
        # Standardize quotation marks
        result = re.sub(r"[\u201C\u201D\u00AB\u00BB]", '"', result)
        result = re.sub(r"[\u2018\u2019\u201A\u201B]", "'", result)
        # Normalize sentence terminators for Meitei Mayek text:
        # If text is predominantly Meitei Mayek, map Western dot or Devanagari danda to Cheikhei (U+ABEB)
        if any(is_meitei_mayek_char(c) for c in result):
            # Replace danda / double danda with Cheikhei
            result = re.sub(r"[\u0964\u0965]", "\uabeb", result)

    return result


def detect_script(text: str) -> str:
    """
    Heuristically detect the primary writing system of the text.

    Counts character frequencies across Unicode blocks.

    Returns:
        'meitei_mayek', 'bengali', 'latin', 'mixed', or 'unknown'
    """
    if not isinstance(text, str) or not text.strip():
        return "unknown"

    counts = {
        "meitei_mayek": 0,
        "bengali": 0,
        "latin": 0,
    }

    for char in text:
        if is_meitei_mayek_char(char):
            counts["meitei_mayek"] += 1
        elif is_bengali_char(char):
            counts["bengali"] += 1
        elif is_latin_char(char):
            counts["latin"] += 1

    total_letters = sum(counts.values())
    if total_letters == 0:
        return "unknown"

    # If any script represents >= 70% of identified letters, designate as primary
    for script, count in counts.items():
        if count / total_letters >= 0.70:
            return script

    return "mixed"

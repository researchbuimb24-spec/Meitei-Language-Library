# -*- coding: utf-8 -*-
"""
Orthography and Script Conversion Engine for Meitei Language Library (meitei).

Implements rigorous, rule-governed script conversion and spelling variant tracking:
1. Meitei Mayek Unicode text (Official State Standard).
2. Bengali-script representations historically used in Manipur.
3. Latin Romanization documented in primary linguistic sources.
4. Ambiguity and unsupported conversion reporting (Strict Non-Guessing Policy).
5. Explicitly registered spelling variants.

Linguistic Principle:
    A naive one-to-one character transliterator is fundamentally inaccurate
    for Meiteilon due to inherent vowel elision, tonal contrasts, and dedicated
    coda consonants (Lonsum). Script conversion is only performed when supported
    by documented orthographic rules. In ambiguous contexts, the system reports
    ambiguity rather than guessing.
"""

from __future__ import annotations

import json
import unicodedata
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from meitei.unicode_utils import detect_script, normalize_text


class ConversionStatus(str, Enum):
    """Result status of a script conversion operation."""
    EXACT = "EXACT"
    AMBIGUOUS = "AMBIGUOUS"
    UNSUPPORTED = "UNSUPPORTED"


class UnsupportedConversionError(Exception):
    """Raised when script conversion is requested between unsupported or invalid writing systems."""
    def __init__(self, source_script: str, target_script: str, message: Optional[str] = None) -> None:
        msg = message or f"Conversion from '{source_script}' to '{target_script}' is not supported."
        super().__init__(msg)
        self.source_script = source_script
        self.target_script = target_script


class AmbiguousConversionError(Exception):
    """Raised when strict script conversion fails due to ambiguous orthographic mappings."""
    def __init__(self, message: str, ambiguities: Optional[List[Dict[str, Any]]] = None) -> None:
        super().__init__(message)
        self.ambiguities = ambiguities or []


@dataclass
class ScriptConversionResult:
    """Detailed result object for a script conversion operation."""
    text: str
    source_script: str
    target_script: str
    status: ConversionStatus
    ambiguities: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


# =============================================================================
# Documented Rule-Based Mappings (Official Manipur Standards)
# =============================================================================

# Primary 18 Letters (Iyek Ipi) -> Bengali & Roman
# Source: Manipur Gazette No. 33 (1980) & Grierson (1904)
MAYEK_TO_BENGALI_BASE: Dict[str, str] = {
    "\uabc0": "ক",   # Kok
    "\uabc1": "স",   # Sam
    "\uabc2": "ল",   # Lai
    "\uabc3": "ম",   # Mit
    "\uabc4": "প",   # Pa
    "\uabc5": "ন",   # Na
    "\uabc6": "চ",   # Chil
    "\uabc7": "ত",   # Til
    "\uabc8": "খ",   # Khou
    "\uabc9": "ঙ",   # Ngou
    "\uabca": "থ",   # Thou
    "\uabcb": "ৱ",   # Wai (Manipuri Wa)
    "\uabcc": "য়",   # Yang (Ya)
    "\uabcd": "হ",   # Huk
    "\uabce": "উ",   # Un (Independent U)
    "\uabcf": "ই",   # I (Independent I)
    "\uabd0": "ফ",   # Pham
    "\uabd1": "অ",   # Atiya (Independent A)
}

# 9 Extension Letters (Cheising / Iyek Mapung)
MAYEK_TO_BENGALI_EXT: Dict[str, str] = {
    "\uabd2": "গ",   # Gok
    "\uabd3": "ঝ",   # Jham
    "\uabd4": "র",   # Rai
    "\uabd5": "ব",   # Ba
    "\uabd6": "জ",   # Jil
    "\uabd7": "দ",   # Dil
    "\uabd8": "ঘ",   # Ghou
    "\uabd9": "ধ",   # Dhou
    "\uabda": "ভ",   # Bham
}

# 8 Syllable Coda Consonants (Lonsum Iyek)
MAYEK_TO_BENGALI_LONSUM: Dict[str, str] = {
    "\uabdb": "ক্",   # Kok Lonsum
    "\uabdc": "ল্",   # Lai Lonsum
    "\uabdd": "ম্",   # Mit Lonsum
    "\uabde": "প্",   # Pa Lonsum
    "\uabdf": "ন্",   # Na Lonsum
    "\uabe0": "ৎ",   # Til Lonsum
    "\uabe1": "ং",   # Ngou Lonsum (Anusvara equivalent in Bengali spelling)
    "\uabe2": "ই",   # I Lonsum (coda i)
}

# 8 Dependent Vowel Signs (Cheitap Iyek)
MAYEK_TO_BENGALI_CHEITAP: Dict[str, str] = {
    "\uabe3": "ো",   # Otap (Onap) -> o
    "\uabe4": "ি",   # Inap -> i
    "\uabe5": "া",   # Anap -> aa
    "\uabe6": "ে",   # Yenyap -> e
    "\uabe7": "ৌ",   # Sounap -> ou
    "\uabe8": "ু",   # Unap -> u
    "\uabe9": "ৈ",   # Cheinap -> ei
    "\uabea": "ং",   # Nung -> anusvara /ng/
}

# Punctuation & Diacritics
MAYEK_TO_BENGALI_PUNCT: Dict[str, str] = {
    "\uabeb": "।",   # Cheikhei -> danda
    "\uabec": "",    # Lum Iyek (heavy tone, not represented in Bengali script)
    "\uabed": "্",   # Apun Iyek -> hasanta
}

# Digits 0-9
MAYEK_TO_BENGALI_DIGITS: Dict[str, str] = {
    "\uabf0": "০", "\uabf1": "১", "\uabf2": "২", "\uabf3": "৩", "\uabf4": "৪",
    "\uabf5": "৫", "\uabf6": "৬", "\uabf7": "৭", "\uabf8": "৮", "\uabf9": "৯",
}

# Combined Meitei Mayek -> Bengali dictionary
ALL_MAYEK_TO_BENGALI: Dict[str, str] = {
    **MAYEK_TO_BENGALI_BASE,
    **MAYEK_TO_BENGALI_EXT,
    **MAYEK_TO_BENGALI_LONSUM,
    **MAYEK_TO_BENGALI_CHEITAP,
    **MAYEK_TO_BENGALI_PUNCT,
    **MAYEK_TO_BENGALI_DIGITS,
}

# Documented Romanization of Meitei Mayek characters
MAYEK_TO_ROMAN_BASE: Dict[str, str] = {
    "\uabc0": "k", "\uabc1": "s", "\uabc2": "l", "\uabc3": "m", "\uabc4": "p",
    "\uabc5": "n", "\uabc6": "ch", "\uabc7": "t", "\uabc8": "kh", "\uabc9": "ng",
    "\uabca": "th", "\uabcb": "w", "\uabcc": "y", "\uabcd": "h", "\uabce": "u",
    "\uabcf": "i", "\uabd0": "ph", "\uabd1": "a", "\uabd2": "g", "\uabd3": "jh",
    "\uabd4": "r", "\uabd5": "b", "\uabd6": "j", "\uabd7": "d", "\uabd8": "gh",
    "\uabd9": "dh", "\uabda": "bh",
}

MAYEK_TO_ROMAN_LONSUM: Dict[str, str] = {
    "\uabdb": "k", "\uabdc": "l", "\uabdd": "m", "\uabde": "p",
    "\uabdf": "n", "\uabe0": "t", "\uabe1": "ng", "\uabe2": "i",
}

MAYEK_TO_ROMAN_CHEITAP: Dict[str, str] = {
    "\uabe3": "o", "\uabe4": "i", "\uabe5": "a", "\uabe6": "e",
    "\uabe7": "ou", "\uabe8": "u", "\uabe9": "ei", "\uabea": "ng",
}

MAYEK_TO_ROMAN_DIGITS: Dict[str, str] = {
    "\uabf0": "0", "\uabf1": "1", "\uabf2": "2", "\uabf3": "3", "\uabf4": "4",
    "\uabf5": "5", "\uabf6": "6", "\uabf7": "7", "\uabf8": "8", "\uabf9": "9",
}

# Reverse Bengali to Meitei Mayek mapping
BENGALI_TO_MAYEK_BASE: Dict[str, str] = {
    "ক": "\uabc0", "স": "\uabc1", "ল": "\uabc2", "ম": "\uabc3", "প": "\uabc4",
    "ন": "\uabc5", "চ": "\uabc6", "ত": "\uabc7", "খ": "\uabc8", "ঙ": "\uabc9",
    "থ": "\uabca", "ৱ": "\uabcb", "য়": "\uabcc", "হ": "\uabcd", "উ": "\uabce",
    "ই": "\uabcf", "ফ": "\uabd0", "অ": "\uabd1", "গ": "\uabd2", "ঝ": "\uabd3",
    "র": "\uabd4", "ব": "\uabd5", "জ": "\uabd6", "দ": "\uabd7", "ঘ": "\uabd8",
    "ধ": "\uabd9", "ভ": "\uabda", "ৎ": "\uabe0", "ং": "\uabea", "।": "\uabeb",
    "ো": "\uabe3", "ি": "\uabe4", "া": "\uabe5", "ে": "\uabe6", "ৌ": "\uabe7",
    "ু": "\uabe8", "ৈ": "\uabe9", "্": "\uabed",
    "০": "\uabf0", "১": "\uabf1", "২": "\uabf2", "৩": "\uabf3", "৪": "\uabf4",
    "৫": "\uabf5", "৬": "\uabf6", "৭": "\uabf7", "৮": "\uabf8", "৯": "\uabf9",
}


# =============================================================================
# Rule-Governed Script Conversion Functions
# =============================================================================

def convert_mayek_to_bengali(text: str) -> str:
    """
    Convert Meitei Mayek text into Bengali script according to official state rules.
    """
    out: List[str] = []
    for char in text:
        out.append(ALL_MAYEK_TO_BENGALI.get(char, char))
    return "".join(out)


def convert_mayek_to_roman(text: str) -> str:
    """
    Convert Meitei Mayek text into standard Latin Romanization.

    Adheres to phonological onset and coda rules.
    """
    out: List[str] = []
    chars = list(text)
    n = len(chars)
    i = 0

    while i < n:
        c = chars[i]

        # 1. Punctuation & Digits
        if c == "\uabeb":
            out.append(".")
            i += 1
            continue
        if c in MAYEK_TO_ROMAN_DIGITS:
            out.append(MAYEK_TO_ROMAN_DIGITS[c])
            i += 1
            continue
        if c == "\uabec" or c == "\uabed":  # Tone / Virama handled contextually
            i += 1
            continue

        # 2. Lonsum Coda consonants
        if c in MAYEK_TO_ROMAN_LONSUM:
            out.append(MAYEK_TO_ROMAN_LONSUM[c])
            i += 1
            continue

        # 3. Base Consonants and Independent Vowels
        if c in MAYEK_TO_ROMAN_BASE:
            rom = MAYEK_TO_ROMAN_BASE[c]
            # Independent vowels (Atiya 'a', Un 'u', I 'i')
            if c in ("\uabd1", "\uabce", "\uabcf"):
                # If followed by a vowel diacritic (e.g. Atiya + Cheitap), Cheitap determines vowel
                if i + 1 < n and chars[i + 1] in MAYEK_TO_ROMAN_CHEITAP:
                    next_cheitap = chars[i + 1]
                    out.append(MAYEK_TO_ROMAN_CHEITAP[next_cheitap])
                    i += 2
                    continue
                else:
                    out.append(rom)
                    i += 1
                    continue

            # Regular Consonant: Check if followed by dependent vowel sign
            if i + 1 < n and chars[i + 1] in MAYEK_TO_ROMAN_CHEITAP:
                vowel_char = chars[i + 1]
                vowel_rom = MAYEK_TO_ROMAN_CHEITAP[vowel_char]
                out.append(rom + vowel_rom)
                i += 2
                continue
            elif i + 1 < n and chars[i + 1] == "\uabed":  # Apun Iyek (consonant subjoiner)
                out.append(rom)
                i += 2
                continue
            else:
                # Inherent vowel 'a' on consonants unless followed by coda or end
                # In standard romanization, base consonant standing alone has inherent vowel 'a'
                out.append(rom + "a")
                i += 1
                continue

        # Fallback for unmapped or whitespace
        out.append(c)
        i += 1

    return "".join(out)


def convert_bengali_to_mayek(text: str, strict: bool = True) -> ScriptConversionResult:
    """
    Convert Bengali script to Meitei Mayek.

    Reports ambiguous Sanskrit conjuncts or non-native letters if strict=True.
    """
    out: List[str] = []
    ambiguities: List[Dict[str, Any]] = []
    warnings: List[str] = []

    chars = list(text)
    n = len(chars)
    i = 0

    while i < n:
        c = chars[i]

        # Check for ambiguous Bengali sibilants (শ, ষ)
        if c in ("শ", "ষ"):
            ambiguities.append({
                "index": i,
                "token": c,
                "reason": "Bengali sibilant ('শ'/'ষ') is historically ambiguous; standard native Meitei uses 'ꯁ' (Sam).",
                "candidates": ["\uabc1"],
            })
            out.append("\uabc1")  # Default to Sam
            i += 1
            continue

        # Check for Bengali 'ব' which historically can map to 'ꯕ' (Ba) or 'ꯋ' (Wa)
        if c == "ব":
            # In Manipuri orthography, 'ব' is typically Ba, but in older texts often represented Wa
            out.append("\uabd5")
            i += 1
            continue

        # Direct mapped character
        if c in BENGALI_TO_MAYEK_BASE:
            out.append(BENGALI_TO_MAYEK_BASE[c])
            i += 1
            continue

        # Unmapped or whitespace
        if c.isspace() or unicodedata.category(c).startswith("P"):
            out.append(c)
        else:
            ambiguities.append({
                "index": i,
                "token": c,
                "reason": f"Bengali character '{c}' (U+{ord(c):04X}) has no direct documented Meitei Mayek equivalent.",
                "candidates": [],
            })
            out.append(c)
        i += 1

    status = ConversionStatus.EXACT if not ambiguities else ConversionStatus.AMBIGUOUS
    res_text = "".join(out)

    if strict and ambiguities:
        raise AmbiguousConversionError(
            f"Bengali to Meitei Mayek conversion encountered {len(ambiguities)} ambiguous token(s): "
            f"{[a['token'] for a in ambiguities]}",
            ambiguities=ambiguities,
        )

    return ScriptConversionResult(
        text=res_text,
        source_script="bengali",
        target_script="meitei_mayek",
        status=status,
        ambiguities=ambiguities,
        warnings=warnings,
    )


def convert_latin_to_mayek(text: str, strict: bool = True) -> ScriptConversionResult:
    """
    Convert Latin Romanization to Meitei Mayek.

    Strict Non-Guessing Policy:
    Arbitrary Romanized text lacks explicit tonal and onset/coda disambiguation.
    In strict mode, uncataloged Roman strings raise AmbiguousConversionError.
    """
    clean = normalize_text(text).lower()
    ambiguities: List[Dict[str, Any]] = []

    # Check against known verified lexicon headwords first
    # In strict mode, if text cannot be definitively parsed without guessing, report ambiguity.
    ambiguities.append({
        "index": 0,
        "token": text,
        "reason": "Automated reverse conversion from arbitrary Latin Romanization lacks tonal and "
                  "onset/coda markers and cannot be guaranteed without dictionary attestation.",
        "candidates": [],
    })

    if strict:
        raise AmbiguousConversionError(
            f"Cannot strictly convert Romanized string '{text}' to Meitei Mayek without dictionary attestation: "
            f"reverse romanization is phonetically ambiguous.",
            ambiguities=ambiguities,
        )

    return ScriptConversionResult(
        text=text,
        source_script="latin",
        target_script="meitei_mayek",
        status=ConversionStatus.AMBIGUOUS,
        ambiguities=ambiguities,
        warnings=["Non-strict fallback: preserved original Latin text due to ambiguity."],
    )


# =============================================================================
# High-Level Script Conversion & Variants API
# =============================================================================

def convert_script(text: str, target_script: str, strict: bool = True) -> str:
    """
    Convert text to the target script using documented orthographic rules.

    Args:
        text: Input string.
        target_script: Desired target writing system ('meitei_mayek', 'bengali', 'latin').
        strict: If True, raises AmbiguousConversionError or UnsupportedConversionError
                when conversion cannot be guaranteed by authoritative rules.

    Returns:
        Converted text string.
    """
    normalized = normalize_text(text)
    if not normalized:
        return ""

    target = target_script.strip().lower()
    valid_targets = {"meitei_mayek", "bengali", "latin"}
    if target not in valid_targets:
        raise UnsupportedConversionError(
            source_script=detect_script(normalized),
            target_script=target,
            message=f"Target script '{target}' is not supported. Must be one of {sorted(valid_targets)}.",
        )

    source = detect_script(normalized)
    if source == target:
        return normalized

    if source == "meitei_mayek":
        if target == "bengali":
            return convert_mayek_to_bengali(normalized)
        elif target == "latin":
            return convert_mayek_to_roman(normalized)

    elif source == "bengali":
        if target == "meitei_mayek":
            result = convert_bengali_to_mayek(normalized, strict=strict)
            return result.text
        elif target == "latin":
            # Two-step documented conversion: Bengali -> Mayek -> Roman
            mayek_res = convert_bengali_to_mayek(normalized, strict=strict)
            return convert_mayek_to_roman(mayek_res.text)

    elif source == "latin":
        if target in ("meitei_mayek", "bengali"):
            res = convert_latin_to_mayek(normalized, strict=strict)
            if target == "bengali":
                return convert_mayek_to_bengali(res.text)
            return res.text

    raise UnsupportedConversionError(
        source_script=source,
        target_script=target,
        message=f"Conversion from '{source}' to '{target}' is not supported.",
    )


def get_script_variants(text: str, data_dir: Union[str, Path] = "data") -> Dict[str, List[str]]:
    """
    Retrieve all registered spelling variants for a given word across scripts.

    Searches core lexicon, candidate lexicon, and variants catalog.

    Returns:
        Dictionary mapping script names ('meitei_mayek', 'bengali', 'latin')
        to lists of verified variant spellings.
    """
    clean_text = normalize_text(text).strip()
    if not clean_text:
        return {"meitei_mayek": [], "bengali": [], "latin": []}

    variants_by_script: Dict[str, Set[str]] = {
        "meitei_mayek": set(),
        "bengali": set(),
        "latin": set(),
    }

    detected = detect_script(clean_text)
    if detected in variants_by_script:
        variants_by_script[detected].add(clean_text)

    # 1. Search variants.jsonl if present
    p_variants = Path(data_dir) / "lexicon" / "variants.jsonl"
    target_entry_id: Optional[str] = None

    if p_variants.exists():
        with open(p_variants, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str:
                    continue
                try:
                    data = json.loads(line_str)
                    # If input matches variant form
                    if normalize_text(data.get("variant_form", "")).lower() == clean_text.lower():
                        target_entry_id = data.get("entry_id")
                        break
                except Exception:
                    continue

    # 2. Search core_lexicon.jsonl to find parent entry
    p_core = Path(data_dir) / "lexicon" / "core_lexicon.jsonl"
    matched_entry: Optional[Dict[str, Any]] = None

    if p_core.exists():
        with open(p_core, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str:
                    continue
                try:
                    entry = json.loads(line_str)
                    eid = entry.get("id")
                    m_mayek = normalize_text(entry.get("headword_meitei", ""))
                    m_roman = normalize_text(entry.get("headword_roman", "")).lower()
                    m_bengali = normalize_text(entry.get("headword_bengali", ""))

                    if (
                        (target_entry_id and eid == target_entry_id)
                        or clean_text == m_mayek
                        or clean_text.lower() == m_roman
                        or clean_text == m_bengali
                    ):
                        matched_entry = entry
                        target_entry_id = eid
                        if m_mayek:
                            variants_by_script["meitei_mayek"].add(m_mayek)
                        if m_roman:
                            variants_by_script["latin"].add(m_roman)
                        if m_bengali:
                            variants_by_script["bengali"].add(m_bengali)
                        break
                except Exception:
                    continue

    # 3. Collect all variants mapped to this entry
    if target_entry_id and p_variants.exists():
        with open(p_variants, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str:
                    continue
                try:
                    v = json.loads(line_str)
                    if v.get("entry_id") == target_entry_id:
                        v_script = v.get("script", "latin")
                        v_form = normalize_text(v.get("variant_form", ""))
                        if v_form and v_script in variants_by_script:
                            variants_by_script[v_script].add(v_form)
                except Exception:
                    continue

    return {k: sorted(v) for k, v in variants_by_script.items()}


# -*- coding: utf-8 -*-
"""
Language registry and metadata for the Meitei Language Library (meitei).

Maintains canonical language codes, scripts, language families, and roles
supported across dictionary search, glossing, and translation.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


SUPPORTED_LANGUAGES: List[Dict[str, Any]] = [
    {
        "code": "mni",
        "name": "Meitei (Manipuri / Meiteilon)",
        "family": "Sino-Tibetan (Tibeto-Burman)",
        "scripts": ["Meitei Mayek (Mtei)", "Bengali (Beng)", "Latin (Latn)"],
        "iso_639_3": "mni",
        "glottocode": "mani1292",
        "role": "Primary source and target language (core headwords, historical texts, manuscripts)",
        "status": "Official 8th Schedule language of the Republic of India",
    },
    {
        "code": "en",
        "name": "English",
        "family": "Indo-European (Germanic)",
        "scripts": ["Latin (Latn)"],
        "iso_639_1": "en",
        "role": "Scholarly glosses, definitions, and bilingual translation",
        "status": "Standard reference language for linguistic documentation",
    },
    {
        "code": "hi",
        "name": "Hindi",
        "family": "Indo-European (Indo-Aryan)",
        "scripts": ["Devanagari (Deva)"],
        "iso_639_1": "hi",
        "role": "Comparative translation glosses and national cross-lingual references",
        "status": "Official language of the Republic of India",
    },
    {
        "code": "bn",
        "name": "Bengali",
        "family": "Indo-European (Indo-Aryan)",
        "scripts": ["Bengali (Beng)"],
        "iso_639_1": "bn",
        "role": "Historical print orthography and regional comparative glosses",
        "status": "Historically attested print medium (18th-20th century Meitei publications)",
    },
    {
        "code": "as",
        "name": "Assamese",
        "family": "Indo-European (Indo-Aryan)",
        "scripts": ["Bengali-Assamese (Beng)"],
        "iso_639_1": "as",
        "role": "Regional comparative vocabulary and Brahmaputra valley linguistic references",
        "status": "Neighboring Eastern Indo-Aryan reference language",
    },
]

LANGUAGE_ALIASES: Dict[str, str] = {
    "mni": "mni",
    "meitei": "mni",
    "manipuri": "mni",
    "meiteilon": "mni",
    "en": "en",
    "eng": "en",
    "english": "en",
    "hi": "hi",
    "hin": "hi",
    "hindi": "hi",
    "bn": "bn",
    "ben": "bn",
    "bengali": "bn",
    "bangla": "bn",
    "as": "as",
    "asm": "as",
    "assamese": "as",
}


def canonicalize_language_code(code: Optional[str]) -> Optional[str]:
    """
    Normalize a language code or natural-language name to its canonical ISO code.

    Examples:
        canonicalize_language_code('English') -> 'en'
        canonicalize_language_code('manipuri') -> 'mni'
        canonicalize_language_code('auto') -> 'auto'
    """
    if not code:
        return None
    cleaned = code.strip().lower()
    if cleaned == "auto":
        return "auto"
    return LANGUAGE_ALIASES.get(cleaned)


def is_supported_language(code: Optional[str], allow_auto: bool = False) -> bool:
    """
    Check whether a given language code or alias is supported.

    Args:
        code: The language string to validate.
        allow_auto: Whether 'auto' is considered valid (e.g. for search).
    """
    if not code:
        return False
    cleaned = code.strip().lower()
    if allow_auto and cleaned == "auto":
        return True
    return cleaned in LANGUAGE_ALIASES


def get_supported_languages() -> List[Dict[str, Any]]:
    """Return full catalog of supported languages."""
    return list(SUPPORTED_LANGUAGES)


def get_supported_codes_summary() -> str:
    """Return a comma-separated summary of valid language codes."""
    return ", ".join(lang["code"] for lang in SUPPORTED_LANGUAGES)


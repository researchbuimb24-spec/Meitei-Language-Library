"""
Language information and script metadata for Meitei (Manipuri).
"""

from typing import Dict, Any, List

# Primary 18 letters (Iyek Ipi) of Meitei Mayek with traditional body associations
IYEK_IPI: Dict[str, Dict[str, str]] = {
    "\uabc0": {"name": "Kok", "meaning": "Head", "sound": "k", "bengali": "ক", "roman": "k"},
    "\uabc1": {"name": "Sam", "meaning": "Hair", "sound": "s", "bengali": "স", "roman": "s"},
    "\uabc2": {"name": "Lai", "meaning": "Forehead", "sound": "l", "bengali": "ল", "roman": "l"},
    "\uabc3": {"name": "Mit", "meaning": "Eye", "sound": "m", "bengali": "ম", "roman": "m"},
    "\uabc4": {"name": "Pa", "meaning": "Eyelash / Forehead ridge", "sound": "p", "bengali": "প", "roman": "p"},
    "\uabc5": {"name": "Na", "meaning": "Ear", "sound": "n", "bengali": "ন", "roman": "n"},
    "\uabc6": {"name": "Chil", "meaning": "Lip", "sound": "ch", "bengali": "চ", "roman": "ch"},
    "\uabc7": {"name": "Til", "meaning": "Throat / Saliva", "sound": "t", "bengali": "ত", "roman": "t"},
    "\uabc8": {"name": "Khou", "meaning": "Throat / Clavicle", "sound": "kh", "bengali": "খ", "roman": "kh"},
    "\uabc9": {"name": "Ngou", "meaning": "Uvula / Internal throat", "sound": "ng", "bengali": "ঙ", "roman": "ng"},
    "\uabca": {"name": "Thou", "meaning": "Chest", "sound": "th", "bengali": "থ", "roman": "th"},
    "\uabcb": {"name": "Wai", "meaning": "Navel", "sound": "w", "bengali": "ৱ", "roman": "w"},
    "\uabcc": {"name": "Yang", "meaning": "Spine", "sound": "y", "bengali": "য়", "roman": "y"},
    "\uabcd": {"name": "Huk", "meaning": "Armpit / Ribs", "sound": "h", "bengali": "হ", "roman": "h"},
    "\uabce": {"name": "Un", "meaning": "Skin", "sound": "u", "bengali": "উ", "roman": "u"},
    "\uabcf": {"name": "I", "meaning": "Blood", "sound": "i", "bengali": "ই", "roman": "i"},
    "\uabd0": {"name": "Pham", "meaning": "Pelvis / Station", "sound": "ph", "bengali": "ফ", "roman": "ph"},
    "\uabd1": {"name": "Atiya", "meaning": "Sky / Crown / Emptiness", "sound": "a", "bengali": "অ", "roman": "a"},
}

# 9 Extension letters (Cheising / Iyek Mapung)
CHEISING_IYEK: Dict[str, Dict[str, str]] = {
    "\uabd2": {"name": "Gok", "meaning": "Voiced velar", "sound": "g", "bengali": "গ", "roman": "g"},
    "\uabd3": {"name": "Jham", "meaning": "Voiced aspirated affricate", "sound": "jh", "bengali": "ঝ", "roman": "jh"},
    "\uabd4": {"name": "Rai", "meaning": "Alveolar trill", "sound": "r", "bengali": "র", "roman": "r"},
    "\uabd5": {"name": "Ba", "meaning": "Voiced bilabial", "sound": "b", "bengali": "ব", "roman": "b"},
    "\uabd6": {"name": "Jil", "meaning": "Voiced palatal", "sound": "j", "bengali": "জ", "roman": "j"},
    "\uabd7": {"name": "Dil", "meaning": "Voiced dental", "sound": "d", "bengali": "দ", "roman": "d"},
    "\uabd8": {"name": "Ghou", "meaning": "Voiced aspirated velar", "sound": "gh", "bengali": "ঘ", "roman": "gh"},
    "\uabd9": {"name": "Dhou", "meaning": "Voiced aspirated dental", "sound": "dh", "bengali": "ধ", "roman": "dh"},
    "\uabda": {"name": "Bham", "meaning": "Voiced aspirated bilabial", "sound": "bh", "bengali": "ভ", "roman": "bh"},
}

# 8 Final consonants (Lonsum Iyek)
LONSUM_IYEK: Dict[str, Dict[str, str]] = {
    "\uabdb": {"name": "Kok Lonsum", "sound": "k", "bengali": "ক্", "roman": "k"},
    "\uabdc": {"name": "Lai Lonsum", "sound": "l", "bengali": "ল্", "roman": "l"},
    "\uabdd": {"name": "Mit Lonsum", "sound": "m", "bengali": "ম্", "roman": "m"},
    "\uabde": {"name": "Pa Lonsum", "sound": "p", "bengali": "প্", "roman": "p"},
    "\uabdf": {"name": "Na Lonsum", "sound": "n", "bengali": "ন্", "roman": "n"},
    "\uabe0": {"name": "Til Lonsum", "sound": "t", "bengali": "ৎ", "roman": "t"},
    "\uabe1": {"name": "Ngou Lonsum", "sound": "ng", "bengali": "ঙ্", "roman": "ng"},
    "\uabe2": {"name": "I Lonsum", "sound": "i", "bengali": "ই", "roman": "i"},
}

# 8 Vowel diacritics (Cheitap Iyek)
CHEITAP_IYEK: Dict[str, Dict[str, str]] = {
    "\uabe3": {"name": "Otap (Onap)", "sound": "o", "bengali": "ো", "roman": "o"},
    "\uabe4": {"name": "Inap", "sound": "i", "bengali": "ি", "roman": "i"},
    "\uabe5": {"name": "Anap", "sound": "a / aa", "bengali": "া", "roman": "a"},
    "\uabe6": {"name": "Yenyap", "sound": "e", "bengali": "ে", "roman": "e"},
    "\uabe7": {"name": "Sounap", "sound": "ou", "bengali": "ৌ", "roman": "ou"},
    "\uabe8": {"name": "Unap", "sound": "u", "bengali": "ু", "roman": "u"},
    "\uabe9": {"name": "Cheinap", "sound": "ei", "bengali": "ৈ", "roman": "ei"},
    "\uabea": {"name": "Nung", "sound": "ng (anusvara)", "bengali": "ং", "roman": "ng"},
}

# Punctuation & Diacritics
PUNCTUATION_IYEK: Dict[str, Dict[str, str]] = {
    "\uabeb": {"name": "Cheikhei", "symbol": "꯫", "function": "Sentence terminator (danda)"},
    "\uabec": {"name": "Lum Iyek", "symbol": "꯬", "function": "Heavy tone marker"},
    "\uabed": {"name": "Apun Iyek", "symbol": "꯭", "function": "Virama / consonant subjoiner"},
}

# Digits 0-9
DIGITS_MAP: Dict[str, Dict[str, Any]] = {
    "\uabf0": {"value": 0, "symbol": "꯰", "roman": "0", "bengali": "০", "word_m": "ꯐꯨꯟ", "word_r": "phun"},
    "\uabf1": {"value": 1, "symbol": "꯱", "roman": "1", "bengali": "১", "word_m": "ꯑꯃ", "word_r": "ama"},
    "\uabf2": {"value": 2, "symbol": "꯲", "roman": "2", "bengali": "২", "word_m": "ꯑꯅꯤ", "word_r": "ani"},
    "\uabf3": {"value": 3, "symbol": "꯳", "roman": "3", "bengali": "৩", "word_m": "ꯑꯍꯨꯝ", "word_r": "ahum"},
    "\uabf4": {"value": 4, "symbol": "꯴", "roman": "4", "bengali": "৪", "word_m": "ꯃꯔꯤ", "word_r": "mari"},
    "\uabf5": {"value": 5, "symbol": "꯵", "roman": "5", "bengali": "৫", "word_m": "ꯃꯉꯥ", "word_r": "manga"},
    "\uabf6": {"value": 6, "symbol": "꯶", "roman": "6", "bengali": "৬", "word_m": "ꯇꯔꯨꯛ", "word_r": "taruk"},
    "\uabf7": {"value": 7, "symbol": "꯷", "roman": "7", "bengali": "৭", "word_m": "ꯇꯔꯦꯠ", "word_r": "taret"},
    "\uabf8": {"value": 8, "symbol": "꯸", "roman": "8", "bengali": "৮", "word_m": "ꯅꯤꯄꯥꯜ", "word_r": "nipal"},
    "\uabf9": {"value": 9, "symbol": "꯹", "roman": "9", "bengali": "৯", "word_m": "ꯃꯥꯄꯜ", "word_r": "mapal"},
}


def get_language_info() -> Dict[str, Any]:
    """
    Return comprehensive linguistic metadata for the Meitei (Manipuri) language.
    """
    return {
        "name_english": "Manipuri",
        "name_endonym": "ꯃꯩꯇꯩꯂꯣꯟ (Meiteilon / Meiteiron)",
        "iso_639_1": "mni",
        "iso_639_2": "mni",
        "iso_639_3": "mni",
        "family": "Sino-Tibetan",
        "subfamily": "Tibeto-Burman",
        "branch": "Meitei",
        "official_status": [
            "Official language of the State of Manipur, India",
            "Recognized in the Eighth Schedule to the Constitution of India (1992)",
            "Officially used in state administration, legislature, and education"
        ],
        "native_speakers_approx": 1800000,
        "primary_script": "Meitei Mayek (ꯃꯩꯇꯩ ꯃꯌꯦꯛ)",
        "historical_scripts": ["Bengali-Eastern Nagari script (18th-20th century)"],
        "transliteration_support": ["Roman / Latin transliteration"],
        "unicode_blocks": [
            {"name": "Meetei Mayek", "range": "U+ABC0..U+ABFF", "standard": "Unicode 5.2 (2009)"},
            {"name": "Meetei Mayek Extensions", "range": "U+AAE0..U+AAFF", "standard": "Unicode 6.0 (2010)"}
        ],
        "typology": {
            "morphology": "Agglutinative with extensive suffixation and productive prefixation",
            "word_order": "SOV (Subject-Object-Verb)",
            "tones": "Two-tone register (level and falling), reflected by tone marker Lum Iyek (꯬)"
        }
    }


def get_supported_scripts() -> Dict[str, Any]:
    """
    Return details on scripts supported by meitei_lang.
    """
    return {
        "meitei_mayek": {
            "name": "Meitei Mayek (ꯃꯩꯇꯩ ꯃꯌꯦꯛ)",
            "code": "Mtei",
            "status": "Primary / Fully Supported",
            "unicode_range": "U+ABC0 to U+ABFF and U+AAE0 to U+AAFF",
            "letter_inventory": {
                "iyek_ipi_count": len(IYEK_IPI),
                "cheising_count": len(CHEISING_IYEK),
                "lonsum_count": len(LONSUM_IYEK),
                "cheitap_count": len(CHEITAP_IYEK),
                "digits_count": len(DIGITS_MAP)
            },
            "description": (
                "The indigenous Brahmic script of the Meitei people of Manipur. "
                "Historically recorded in ancient Puyas (sacred manuscripts) and royal edicts. "
                "Officially revived and reintroduced into schools and newspapers in Manipur."
            )
        },
        "bengali": {
            "name": "Bengali-Manipuri Script",
            "code": "Beng",
            "status": "Historical / Script Conversion Supported",
            "unicode_range": "U+0980 to U+09FF",
            "description": (
                "An adaptation of the Eastern Nagari / Bengali script adopted during King Pamheiba's "
                "reign in the 18th century, widely used for printing Manipuri literature throughout "
                "the 19th and 20th centuries until the modern return to Meitei Mayek."
            )
        },
        "roman": {
            "name": "Roman / Latin Transliteration",
            "code": "Latn",
            "status": "Transliteration Supported",
            "description": (
                "Standard Romanized orthography for Meiteilon used in linguistics, international "
                "scholarship, and search query input."
            )
        }
    }


def get_script_summary() -> Dict[str, Any]:
    """
    Return a summary of supported scripts (alias for get_supported_scripts).
    """
    return get_supported_scripts()


def get_alphabet(include_extended: bool = False) -> List[Dict[str, Any]]:
    """
    Return the Meitei Mayek letter inventory.

    Args:
        include_extended: If True, includes the 9 Cheising Iyek (extended letters).
                          If False, returns only the primary 18 Iyek Ipi.

    Returns:
        List of dictionaries with letter character, name, meaning, sound, bengali, and roman mappings.
    """
    letters: List[Dict[str, Any]] = []
    for char, info in IYEK_IPI.items():
        letters.append({"char": char, **info})
    if include_extended:
        for char, info in CHEISING_IYEK.items():
            letters.append({"char": char, **info})
    return letters


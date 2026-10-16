"""
Meitei Language Script Handling and Transliteration Module.

Provides:
- Script detection (Meitei Mayek, Bengali-Manipuri, Roman/Latin)
- Unicode text normalization
- Script validation
- Bi-directional transliteration between Meitei Mayek, Bengali script, and Romanization
"""

import re
import unicodedata
from typing import Optional, Dict, Any, List

from .exceptions import ValidationError
from .language_info import IYEK_IPI, CHEISING_IYEK, LONSUM_IYEK, CHEITAP_IYEK, PUNCTUATION_IYEK, DIGITS_MAP

# Consonants and independent vowels
ALL_CONSONANTS: Dict[str, str] = {}
for ch, info in {**IYEK_IPI, **CHEISING_IYEK}.items():
    if ch not in ("\uabce", "\uabcf", "\uabd1"):
        ALL_CONSONANTS[ch] = info["roman"]

INDEPENDENT_VOWELS: Dict[str, str] = {
    "\uabce": "u",   # Un
    "\uabcf": "i",   # I
    "\uabd1": "a",   # Atiya
}

MEITEE_MAYEK_RANGE = (0xABC0, 0xABFF)
MEITEE_MAYEK_EXT_RANGE = (0xAAE0, 0xAAFF)
BENGALI_RANGE = (0x0980, 0x09FF)


def normalize_text(text: str) -> str:
    """
    Normalize text using standard Unicode normalization (NFC)
    and clean up excessive extraneous whitespace.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    # Normalize Unicode canonical composition
    normalized = unicodedata.normalize("NFC", text)
    # Strip unnecessary control characters except tab and newline
    cleaned = "".join(c for c in normalized if c == "\n" or c == "\t" or not unicodedata.category(c).startswith("C"))
    return cleaned.strip()


def detect_script(text: str) -> str:
    """
    Detect whether the input text is predominantly Meitei Mayek, Bengali, Latin, or mixed.

    Returns:
        'meitei_mayek', 'bengali', 'latin', 'mixed', or 'unknown'
    """
    if not isinstance(text, str) or not text.strip():
        return "unknown"

    counts = {"meitei_mayek": 0, "bengali": 0, "latin": 0, "other": 0}

    for char in text:
        cp = ord(char)
        if (MEITEE_MAYEK_RANGE[0] <= cp <= MEITEE_MAYEK_RANGE[1]) or \
           (MEITEE_MAYEK_EXT_RANGE[0] <= cp <= MEITEE_MAYEK_EXT_RANGE[1]):
            counts["meitei_mayek"] += 1
        elif BENGALI_RANGE[0] <= cp <= BENGALI_RANGE[1]:
            counts["bengali"] += 1
        elif ("a" <= char <= "z") or ("A" <= char <= "Z"):
            counts["latin"] += 1
        elif not char.isspace() and not char.isdigit() and char not in ",.!?-—'\"()[]{}:;":
            counts["other"] += 1

    total_identified = counts["meitei_mayek"] + counts["bengali"] + counts["latin"]
    if total_identified == 0:
        return "unknown"

    for script, count in counts.items():
        if script != "other" and count / total_identified >= 0.6:
            return script

    return "mixed"


def validate_text(text: str, allowed_script: Optional[str] = None) -> bool:
    """
    Validate that text contains valid characters and matches the expected script if specified.

    Args:
        text: Input string to validate.
        allowed_script: Optional script name ('meitei_mayek', 'bengali', 'latin').

    Returns:
        True if text is valid.

    Raises:
        ValidationError: If text is empty or contains characters outside the specified script.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    if not text.strip():
        raise ValidationError("Input text cannot be empty or whitespace.")

    detected = detect_script(text)
    if allowed_script is not None:
        target = allowed_script.lower().strip()
        if target in ("meitei", "meitei_mayek", "mayek"):
            expected = "meitei_mayek"
        elif target in ("bengali", "bangla"):
            expected = "bengali"
        elif target in ("latin", "roman", "english"):
            expected = "latin"
        else:
            raise ValidationError(f"Unknown allowed_script: {allowed_script}")

        if detected != expected:
            raise ValidationError(
                f"Text script mismatch: expected '{expected}', but detected '{detected}'."
            )

    return True


def meitei_to_roman(text: str) -> str:
    """
    Transliterate Meitei Mayek text into Romanized / Latin script.
    Follows Meitei phonological transliteration conventions.
    """
    if not text:
        return ""

    out: List[str] = []
    i = 0
    n = len(text)

    while i < n:
        char = text[i]

        # Check digits
        if char in DIGITS_MAP:
            out.append(DIGITS_MAP[char]["roman"])
            i += 1
            continue

        # Check punctuation
        if char in PUNCTUATION_IYEK:
            out.append(PUNCTUATION_IYEK[char]["symbol"] if char != "\uabeb" else ".")
            i += 1
            continue

        # Check Lonsum (coda consonant)
        if char in LONSUM_IYEK:
            out.append(LONSUM_IYEK[char]["roman"])
            i += 1
            continue

        # Check independent vowels (Un, I, Atiya)
        if char in INDEPENDENT_VOWELS:
            base_vowel = INDEPENDENT_VOWELS[char]
            if i + 1 < n and text[i + 1] in CHEITAP_IYEK:
                next_v = text[i + 1]
                if char == "\uabd1":  # Atiya + vowel sign
                    out.append(CHEITAP_IYEK[next_v]["roman"])
                else:
                    out.append(base_vowel + CHEITAP_IYEK[next_v]["roman"])
                i += 2
                continue
            else:
                out.append(base_vowel)
                i += 1
                continue

        # Check consonants
        if char in ALL_CONSONANTS:
            cons_sound = ALL_CONSONANTS[char]
            # Look ahead for vowel sign or virama (Apun Iyek)
            if i + 1 < n and text[i + 1] in CHEITAP_IYEK:
                vowel_sound = CHEITAP_IYEK[text[i + 1]]["roman"]
                out.append(cons_sound + vowel_sound)
                i += 2
                continue
            elif i + 1 < n and text[i + 1] == "\uabed":  # Apun Iyek
                out.append(cons_sound)
                i += 2
                continue
            elif i + 1 < n and text[i + 1] in LONSUM_IYEK:
                out.append(cons_sound + "a")
                i += 1
                continue
            else:
                out.append(cons_sound + "a")
                i += 1
                continue

        # Standalone vowel signs
        if char in CHEITAP_IYEK:
            out.append(CHEITAP_IYEK[char]["roman"])
            i += 1
            continue

        out.append(char)
        i += 1

    result = "".join(out)
    result = re.sub(r"aa+", "a", result)
    result = re.sub(r"([bcdfghjklmnpqrstvwxyz])a([aeiou])", r"\1\2", result)
    return result


def meitei_to_bengali(text: str) -> str:
    """
    Convert Meitei Mayek text into Bengali-Manipuri script.
    """
    if not text:
        return ""

    out: List[str] = []
    i = 0
    n = len(text)

    while i < n:
        char = text[i]

        if char in DIGITS_MAP:
            out.append(DIGITS_MAP[char]["bengali"])
            i += 1
            continue

        if char == "\uabeb":
            out.append("।")
            i += 1
            continue

        if char in LONSUM_IYEK:
            out.append(LONSUM_IYEK[char]["bengali"])
            i += 1
            continue

        if char in INDEPENDENT_VOWELS:
            if char == "\uabd1":  # Atiya
                if i + 1 < n and text[i + 1] in CHEITAP_IYEK:
                    v = text[i + 1]
                    v_map = {
                        "\uabe3": "ও",
                        "\uabe4": "ই",
                        "\uabe5": "আ",
                        "\uabe6": "এ",
                        "\uabe7": "ঔ",
                        "\uabe8": "উ",
                        "\uabe9": "ঐ",
                        "\uabea": "অং",
                    }
                    out.append(v_map.get(v, "অ" + CHEITAP_IYEK[v]["bengali"]))
                    i += 2
                    continue
                else:
                    out.append("অ")
                    i += 1
                    continue
            elif char == "\uabce":
                out.append("উ")
                i += 1
                continue
            elif char == "\uabcf":
                out.append("ই")
                i += 1
                continue

        if char in ALL_CONSONANTS:
            beng_cons = {**IYEK_IPI, **CHEISING_IYEK}[char]["bengali"]
            if i + 1 < n and text[i + 1] in CHEITAP_IYEK:
                beng_vowel = CHEITAP_IYEK[text[i + 1]]["bengali"]
                out.append(beng_cons + beng_vowel)
                i += 2
                continue
            elif i + 1 < n and text[i + 1] == "\uabed":
                out.append(beng_cons + "্")
                i += 2
                continue
            else:
                out.append(beng_cons)
                i += 1
                continue

        if char in CHEITAP_IYEK:
            out.append(CHEITAP_IYEK[char]["bengali"])
            i += 1
            continue

        out.append(char)
        i += 1

    return "".join(out)


def bengali_to_meitei(text: str) -> str:
    """
    Convert Bengali-Manipuri script to Meitei Mayek.
    """
    if not text:
        return ""

    b_vowels = {
        "অ": "\uabd1", "আ": "\uabd1\uabe5", "ই": "\uabcf", "ঈ": "\uabcf",
        "উ": "\uabce", "ঊ": "\uabce", "এ": "\uabd1\uabe6", "ঐ": "\uabd1\uabe9",
        "ও": "\uabd1\uabe3", "ঔ": "\uabd1\uabe7",
    }

    b_matras = {
        "া": "\uabe5", "ꯤ": "\uabe4", "ি": "\uabe4", "ী": "\uabe4",
        "ু": "\uabe8", "ূ": "\uabe8", "ে": "\uabe6", "ৈ": "\uabe9",
        "ো": "\uabe3", "ৌ": "\uabe7", "ং": "\uabea",
    }

    b_consonants = {
        "ক": "\uabc0", "খ": "\uabc8", "গ": "\uabd2", "ঘ": "\uabd8", "ঙ": "\uabc9",
        "চ": "\uabc6", "ছ": "\uabc6", "জ": "\uabd6", "ঝ": "\uabd3", "ঞ": "\uabc5",
        "ট": "\uabc7", "ঠ": "\uabca", "ড": "\uabd7", "ঢ": "\uabd9", "ণ": "\uabc5",
        "ত": "\uabc7", "থ": "\uabca", "দ": "\uabd7", "ধ": "\uabd9", "ন": "\uabc5",
        "প": "\uabc4", "ফ": "\uabd0", "ব": "\uabd5", "ভ": "\uabda", "ম": "\uabc3",
        "য": "\uabcc", "য়": "\uabcc", "র": "\uabd4", "ল": "\uabc2", "ৱ": "\uabcb",
        "শ": "\uabc1", "ষ": "\uabc1", "স": "\uabc1", "হ": "\uabcd", "ৎ": "\uabe0",
    }

    b_lonsum = {
        "ক": "\uabdb", "ল": "\uabdc", "ম": "\uabdd", "প": "\uabde",
        "ন": "\uabdf", "ত": "\uabe0", "ঙ": "\uabe1",
    }

    b_digits = {
        "০": "\uabf0", "১": "\uabf1", "২": "\uabf2", "৩": "\uabf3", "৪": "\uabf4",
        "৫": "\uabf5", "৬": "\uabf6", "৭": "\uabf7", "৮": "\uabf8", "৯": "\uabf9",
    }

    out: List[str] = []
    i = 0
    n = len(text)

    while i < n:
        char = text[i]

        if char in b_digits:
            out.append(b_digits[char])
            i += 1
            continue

        if char == "।":
            out.append("\uabeb")
            i += 1
            continue

        if char in b_vowels:
            out.append(b_vowels[char])
            i += 1
            continue

        if char in b_consonants:
            if i + 1 < n and text[i + 1] == "্":
                if char in b_lonsum and (i + 2 >= n or text[i + 2].isspace() or text[i + 2] in "।,.-!?"):
                    out.append(b_lonsum[char])
                    i += 2
                    continue
                elif i + 2 < n and text[i + 2] in b_consonants:
                    c1 = b_consonants[char]
                    out.append(c1 + "\uabed")
                    i += 2
                    continue
                else:
                    if char in b_lonsum:
                        out.append(b_lonsum[char])
                    else:
                        out.append(b_consonants[char])
                    i += 2
                    continue
            elif i + 1 < n and text[i + 1] in b_matras:
                c = b_consonants[char]
                m = b_matras[text[i + 1]]
                out.append(c + m)
                i += 2
                continue
            else:
                out.append(b_consonants[char])
                i += 1
                continue

        if char in b_matras:
            out.append(b_matras[char])
            i += 1
            continue

        out.append(char)
        i += 1

    return "".join(out)


def roman_to_meitei(text: str) -> str:
    """
    Transliterate Roman / Latin Meitei transliteration into Meitei Mayek.
    """
    if not text:
        return ""

    multi_char_consonants = {
        "kh": "\uabc8", "th": "\uabca", "ph": "\uabd0", "ch": "\uabc6",
        "ng": "\uabc9", "jh": "\uabd3", "gh": "\uabd8", "dh": "\uabd9",
        "bh": "\uabda",
    }

    single_consonants = {
        "k": "\uabc0", "s": "\uabc1", "l": "\uabc2", "m": "\uabc3",
        "p": "\uabc4", "n": "\uabc5", "t": "\uabc7", "w": "\uabcb",
        "y": "\uabcc", "h": "\uabcd", "g": "\uabd2", "r": "\uabd4",
        "b": "\uabd5", "j": "\uabd6", "d": "\uabd7",
    }

    vowel_signs = {
        "ou": "\uabe7", "ei": "\uabe9", "ai": "\uabe9", "aa": "\uabe5",
        "a": "\uabe5", "i": "\uabe4", "u": "\uabe8", "e": "\uabe6",
        "o": "\uabe3",
    }

    indep_vowels = {
        "ou": "\uabd1\uabe7", "ei": "\uabd1\uabe9", "ai": "\uabd1\uabe9",
        "aa": "\uabd1\uabe5", "a": "\uabd1", "i": "\uabcf", "u": "\uabce",
        "e": "\uabd1\uabe6", "o": "\uabd1\uabe3",
    }

    lonsum_map = {
        "k": "\uabdb", "l": "\uabdc", "m": "\uabdd",
        "p": "\uabde", "n": "\uabdf", "t": "\uabe0",
        "ng": "\uabe1", "i": "\uabe2",
    }

    digits_roman = {str(i): chr(0xABF0 + i) for i in range(10)}

    lower = text.lower()
    i = 0
    n = len(lower)
    out: List[str] = []

    while i < n:
        if lower[i] in digits_roman:
            out.append(digits_roman[lower[i]])
            i += 1
            continue

        cons = None
        cons_len = 0
        if i + 1 < n and lower[i:i+2] in multi_char_consonants:
            cons = multi_char_consonants[lower[i:i+2]]
            cons_len = 2
        elif lower[i] in single_consonants:
            cons = single_consonants[lower[i]]
            cons_len = 1

        if cons:
            idx = i + cons_len
            is_coda = (idx >= n or lower[idx].isspace() or lower[idx] in ",.!?-—:;()[]{}")
            cluster_name = lower[i:idx]
            if is_coda and cluster_name in lonsum_map:
                out.append(lonsum_map[cluster_name])
                i = idx
                continue

            vowel = None
            vowel_len = 0
            if idx + 1 < n and lower[idx:idx+2] in vowel_signs:
                vowel = vowel_signs[lower[idx:idx+2]]
                vowel_len = 2
            elif idx < n and lower[idx] in vowel_signs:
                vowel = vowel_signs[lower[idx]]
                vowel_len = 1

            if vowel is not None:
                out.append(cons + vowel)
                i = idx + vowel_len
                continue
            else:
                out.append(cons)
                i = idx
                continue

        indep = None
        indep_len = 0
        if i + 1 < n and lower[i:i+2] in indep_vowels:
            indep = indep_vowels[lower[i:i+2]]
            indep_len = 2
        elif lower[i] in indep_vowels:
            indep = indep_vowels[lower[i]]
            indep_len = 1

        if indep:
            out.append(indep)
            i += indep_len
            continue

        out.append(text[i])
        i += 1

    return "".join(out)


def transliterate(text: str, target_script: str = "roman", source_script: Optional[str] = None) -> str:
    """
    Transliterate text between Meitei Mayek, Bengali script, and Roman transliteration.

    Args:
        text: Input text string.
        target_script: Desired output script ('roman', 'meitei_mayek', or 'bengali').
        source_script: Optional input script. If None, it will be auto-detected.

    Returns:
        Transliterated string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    if not text:
        return ""

    t_norm = target_script.lower().strip()
    if t_norm in ("meitei", "meitei_mayek", "mayek"):
        target = "meitei"
    elif t_norm in ("bengali", "bangla"):
        target = "bengali"
    elif t_norm in ("roman", "latin", "english"):
        target = "roman"
    else:
        raise ValueError(f"Unsupported target script: '{target_script}'. Choose 'meitei_mayek', 'bengali', or 'roman'.")

    if source_script is None:
        detected = detect_script(text)
        if detected == "meitei_mayek":
            src = "meitei"
        elif detected == "bengali":
            src = "bengali"
        elif detected == "latin":
            src = "roman"
        else:
            src = "meitei" if any(0xABC0 <= ord(c) <= 0xABFF for c in text) else "roman"
    else:
        s_norm = source_script.lower().strip()
        if s_norm in ("meitei", "meitei_mayek", "mayek"):
            src = "meitei"
        elif s_norm in ("bengali", "bangla"):
            src = "bengali"
        elif s_norm in ("roman", "latin", "english"):
            src = "roman"
        else:
            src = "roman"

    if src == target:
        return text

    if src == "meitei" and target == "roman":
        return meitei_to_roman(text)
    elif src == "meitei" and target == "bengali":
        return meitei_to_bengali(text)
    elif src == "bengali" and target == "meitei":
        return bengali_to_meitei(text)
    elif src == "bengali" and target == "roman":
        m = bengali_to_meitei(text)
        return meitei_to_roman(m)
    elif src == "roman" and target == "meitei":
        return roman_to_meitei(text)
    elif src == "roman" and target == "bengali":
        m = roman_to_meitei(text)
        return meitei_to_bengali(m)

    return text

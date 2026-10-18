# -*- coding: utf-8 -*-
"""
Meitei Language Dictionary and Vocabulary Module.

Provides lookup, querying, categorization, and statistical inspection
over the packaged 3,000+ authentic Meitei lexical entries.
"""

from dataclasses import dataclass, asdict
import json
import os
import random
from typing import List, Dict, Any, Optional, Union

from .exceptions import WordNotFoundError, DataLoadError


@dataclass(frozen=True)
class WordEntry:
    """Represents a single lexical entry in the Meitei language dictionary."""
    word: str
    script: str
    transliteration: str
    meaning_en: str
    part_of_speech: str
    category: str
    source: str
    verified: bool

    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to a standard Python dictionary."""
        return asdict(self)

    def __str__(self) -> str:
        return f"{self.word} ({self.transliteration}): {self.meaning_en} [{self.part_of_speech}]"


# Internal cache
_VOCABULARY_CACHE: Optional[List[WordEntry]] = None
_WORD_MAP: Optional[Dict[str, WordEntry]] = None
_ROMAN_MAP: Optional[Dict[str, WordEntry]] = None


def _get_data_path() -> str:
    """Resolve absolute path to vocabulary.json."""
    return os.path.join(os.path.dirname(__file__), "data", "vocabulary.json")


def load_vocabulary(reload: bool = False) -> List[WordEntry]:
    """
    Load the packaged vocabulary dataset.

    Returns a list of WordEntry objects. Subsequent calls use an in-memory cache
    unless reload=True.
    """
    global _VOCABULARY_CACHE, _WORD_MAP, _ROMAN_MAP
    if _VOCABULARY_CACHE is not None and not reload:
        return _VOCABULARY_CACHE

    path = _get_data_path()
    if not os.path.exists(path):
        raise DataLoadError(f"Vocabulary dataset not found at: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_entries = json.load(f)
    except Exception as e:
        raise DataLoadError(f"Failed to load vocabulary data from {path}: {e}") from e

    entries = []
    word_map = {}
    roman_map = {}

    for item in raw_entries:
        entry = WordEntry(
            word=item["word"],
            script=item.get("script", "Meitei Mayek"),
            transliteration=item.get("transliteration", ""),
            meaning_en=item.get("meaning_en", ""),
            part_of_speech=item.get("part_of_speech", ""),
            category=item.get("category", ""),
            source=item.get("source", ""),
            verified=bool(item.get("verified", True)),
        )
        entries.append(entry)
        word_map[entry.word] = entry
        # Store transliteration index in lowercase for case-insensitive lookup
        r_key = entry.transliteration.strip().lower()
        if r_key and r_key not in roman_map:
            roman_map[r_key] = entry

    _VOCABULARY_CACHE = entries
    _WORD_MAP = word_map
    _ROMAN_MAP = roman_map
    return _VOCABULARY_CACHE


def _ensure_loaded():
    if _VOCABULARY_CACHE is None or _WORD_MAP is None or _ROMAN_MAP is None:
        load_vocabulary()


def count_words() -> int:
    """Return the total number of words in the vocabulary."""
    _ensure_loaded()
    assert _VOCABULARY_CACHE is not None
    return len(_VOCABULARY_CACHE)


# Alias for convenience
get_vocabulary_count = count_words


def get_word(word_or_roman: str) -> WordEntry:
    """
    Look up a single word entry by exact Meitei Mayek word or Roman transliteration.

    Raises WordNotFoundError if the term does not exist in the vocabulary.
    """
    _ensure_loaded()
    assert _WORD_MAP is not None
    assert _ROMAN_MAP is not None

    query = word_or_roman.strip()
    if not query:
        raise WordNotFoundError("Search query cannot be empty.")

    # 1. Direct Meitei Mayek exact match
    if query in _WORD_MAP:
        return _WORD_MAP[query]

    # 2. Case-insensitive transliteration match
    q_lower = query.lower()
    if q_lower in _ROMAN_MAP:
        return _ROMAN_MAP[q_lower]

    raise WordNotFoundError(f"Word '{word_or_roman}' was not found in the Meitei dictionary.")


def lookup(word_or_roman: str) -> Optional[WordEntry]:
    """
    Safely look up a word entry by Meitei Mayek or Roman transliteration.
    Returns None if not found instead of raising an exception.
    """
    try:
        return get_word(word_or_roman)
    except WordNotFoundError:
        return None


def search_words(
    query: str,
    match_type: str = "contains",
    search_in: str = "all",
    limit: Optional[int] = None,
) -> List[WordEntry]:
    """
    Search vocabulary entries matching a given query.

    Args:
        query: Search string.
        match_type: 'exact', 'prefix', 'contains', or 'suffix'.
        search_in: 'word', 'transliteration', 'meaning', or 'all'.
        limit: Optional maximum number of results to return.

    Returns:
        List of matching WordEntry objects.
    """
    _ensure_loaded()
    assert _VOCABULARY_CACHE is not None

    q = query.strip()
    if not q:
        return []
    q_lower = q.lower()
    match_type = match_type.lower()
    search_in = search_in.lower()

    def matches(target: str) -> bool:
        t = target.lower()
        if match_type == "exact":
            return t == q_lower
        elif match_type == "prefix":
            return t.startswith(q_lower)
        elif match_type == "suffix":
            return t.endswith(q_lower)
        else:  # default: contains
            return q_lower in t

    results: List[WordEntry] = []
    for entry in _VOCABULARY_CACHE:
        hit = False
        if search_in in ("word", "all") and matches(entry.word):
            hit = True
        elif search_in in ("transliteration", "all") and matches(entry.transliteration):
            hit = True
        elif search_in in ("meaning", "meaning_en", "all") and matches(entry.meaning_en):
            hit = True

        if hit:
            results.append(entry)
            if limit is not None and len(results) >= limit:
                break

    return results


def get_words_by_category(category: str, limit: Optional[int] = None) -> List[WordEntry]:
    """Retrieve all entries belonging to a specific thematic category."""
    _ensure_loaded()
    assert _VOCABULARY_CACHE is not None

    cat = category.strip().lower()
    matches = [e for e in _VOCABULARY_CACHE if e.category.lower() == cat]
    if limit is not None:
        return matches[:limit]
    return matches


def get_words_by_pos(part_of_speech: str, limit: Optional[int] = None) -> List[WordEntry]:
    """Retrieve all entries belonging to a specific part of speech."""
    _ensure_loaded()
    assert _VOCABULARY_CACHE is not None

    pos = part_of_speech.strip().lower()
    matches = [e for e in _VOCABULARY_CACHE if e.part_of_speech.lower() == pos]
    if limit is not None:
        return matches[:limit]
    return matches


def get_categories() -> List[str]:
    """Return sorted list of all unique categories in the vocabulary."""
    _ensure_loaded()
    assert _VOCABULARY_CACHE is not None
    cats = {e.category for e in _VOCABULARY_CACHE if e.category}
    return sorted(cats)


def get_parts_of_speech() -> List[str]:
    """Return sorted list of all unique parts of speech in the vocabulary."""
    _ensure_loaded()
    assert _VOCABULARY_CACHE is not None
    pos_set = {e.part_of_speech for e in _VOCABULARY_CACHE if e.part_of_speech}
    return sorted(pos_set)


def get_random_words(
    n: int = 5,
    category: Optional[str] = None,
    part_of_speech: Optional[str] = None,
) -> List[WordEntry]:
    """Return n randomly sampled vocabulary entries, with optional category or POS filters."""
    _ensure_loaded()
    assert _VOCABULARY_CACHE is not None

    pool = _VOCABULARY_CACHE
    if category is not None:
        cat_lower = category.strip().lower()
        pool = [e for e in pool if e.category.lower() == cat_lower]
    if part_of_speech is not None:
        pos_lower = part_of_speech.strip().lower()
        pool = [e for e in pool if e.part_of_speech.lower() == pos_lower]

    if not pool:
        return []
    sample_size = min(n, len(pool))
    return random.sample(pool, sample_size)


def get_vocabulary_summary() -> Dict[str, Any]:
    """Return an analytical summary breakdown of the dictionary dataset."""
    _ensure_loaded()
    assert _VOCABULARY_CACHE is not None

    cat_counts: Dict[str, int] = {}
    pos_counts: Dict[str, int] = {}
    for e in _VOCABULARY_CACHE:
        cat_counts[e.category] = cat_counts.get(e.category, 0) + 1
        pos_counts[e.part_of_speech] = pos_counts.get(e.part_of_speech, 0) + 1

    return {
        "total_words": len(_VOCABULARY_CACHE),
        "categories_count": len(cat_counts),
        "categories": dict(sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)),
        "parts_of_speech_count": len(pos_counts),
        "parts_of_speech": dict(sorted(pos_counts.items(), key=lambda x: x[1], reverse=True)),
    }

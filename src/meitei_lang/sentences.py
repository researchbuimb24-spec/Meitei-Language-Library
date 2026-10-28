# -*- coding: utf-8 -*-
"""
Meitei Language Daily Usable Sentences Module.

Provides access to high-frequency conversational sentences in Meitei Mayek,
Roman transliteration, Bengali script, English translations, and context annotations.
"""

from dataclasses import dataclass, asdict
import json
import os
import random
from typing import List, Dict, Any, Optional, Union

from .exceptions import SentenceNotFoundError, DataLoadError


@dataclass
class Sentence:
    """Represents an everyday conversational sentence in Meitei."""
    sentence_id: str
    meitei: str
    roman: str
    bengali: str
    english: str
    category: str
    context: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert sentence object to standard Python dictionary."""
        return asdict(self)

    def __getitem__(self, key: str) -> Any:
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)

    def __str__(self) -> str:
        return f"[{self.category}] {self.meitei} ({self.roman}) -> {self.english}"


_SENTENCES_CACHE: Optional[List[Sentence]] = None
_SENTENCE_MAP: Optional[Dict[str, Sentence]] = None


def _get_data_path() -> str:
    """Resolve path to sentences.json."""
    return os.path.join(os.path.dirname(__file__), "data", "sentences.json")


def load_sentences(reload: bool = False) -> List[Sentence]:
    """
    Load packaged daily usable sentences dataset.

    Returns a list of Sentence objects.
    """
    global _SENTENCES_CACHE, _SENTENCE_MAP
    if _SENTENCES_CACHE is not None and not reload:
        return _SENTENCES_CACHE

    path = _get_data_path()
    if not os.path.exists(path):
        raise DataLoadError(f"Sentences dataset file not found at: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_sentences = json.load(f)
    except Exception as e:
        raise DataLoadError(f"Failed to load sentences data from {path}: {e}") from e

    sentences: List[Sentence] = []
    sentence_map: Dict[str, Sentence] = {}

    for s in raw_sentences:
        sent = Sentence(
            sentence_id=s["sentence_id"],
            meitei=s["meitei"],
            roman=s.get("roman", ""),
            bengali=s.get("bengali", ""),
            english=s.get("english", ""),
            category=s.get("category", "general"),
            context=s.get("context", ""),
        )
        sentences.append(sent)
        sentence_map[sent.sentence_id] = sent

    _SENTENCES_CACHE = sentences
    _SENTENCE_MAP = sentence_map
    return _SENTENCES_CACHE


def _ensure_loaded():
    if _SENTENCES_CACHE is None or _SENTENCE_MAP is None:
        load_sentences()


def count_sentences() -> int:
    """Return total number of daily usable sentences in the library."""
    _ensure_loaded()
    assert _SENTENCES_CACHE is not None
    return len(_SENTENCES_CACHE)


def list_sentences(category: Optional[str] = None) -> List[Sentence]:
    """
    Return all available sentences, optionally filtered by category.
    """
    _ensure_loaded()
    assert _SENTENCES_CACHE is not None
    if not category:
        return list(_SENTENCES_CACHE)
    cat_lower = category.strip().lower()
    return [s for s in _SENTENCES_CACHE if s.category.lower() == cat_lower]


def get_sentence(sentence_id: str) -> Sentence:
    """
    Retrieve a sentence by its unique sentence_id (e.g. 'greet_001').

    Raises SentenceNotFoundError if not found.
    """
    _ensure_loaded()
    assert _SENTENCE_MAP is not None

    clean_id = sentence_id.strip()
    if clean_id in _SENTENCE_MAP:
        return _SENTENCE_MAP[clean_id]

    # Try case-insensitive lookup
    clean_lower = clean_id.lower()
    for k, v in _SENTENCE_MAP.items():
        if k.lower() == clean_lower:
            return v

    available = list(_SENTENCE_MAP.keys())[:10]
    raise SentenceNotFoundError(
        f"Sentence '{sentence_id}' not found. Examples: {available}"
    )


def get_sentences_by_category(category: str) -> List[Sentence]:
    """Return all sentences matching a given category."""
    return list_sentences(category=category)


def get_sentence_categories() -> List[str]:
    """Return a sorted list of unique sentence categories."""
    _ensure_loaded()
    assert _SENTENCES_CACHE is not None
    return sorted({s.category for s in _SENTENCES_CACHE})


def search_sentences(query: str, search_in: str = "all") -> List[Sentence]:
    """
    Search sentences by Meitei Mayek, Roman transliteration, English, or context.

    Args:
        query: Search string.
        search_in: 'meitei', 'english', 'roman', or 'all'.

    Returns:
        List of matching Sentence objects.
    """
    _ensure_loaded()
    assert _SENTENCES_CACHE is not None

    q = query.strip()
    if not q:
        return []
    q_lower = q.lower()
    search_in = search_in.lower()

    matches = []
    for s in _SENTENCES_CACHE:
        hit = False
        if search_in in ("meitei", "all") and q in s.meitei:
            hit = True
        elif search_in in ("roman", "all") and q_lower in s.roman.lower():
            hit = True
        elif search_in in ("english", "all") and q_lower in s.english.lower():
            hit = True
        elif search_in == "all" and (q_lower in s.context.lower() or q in s.bengali):
            hit = True

        if hit:
            matches.append(s)

    return matches


def get_random_sentence(
    category: Optional[str] = None,
    n: int = 1
) -> Union[Sentence, List[Sentence]]:
    """
    Retrieve one or more randomly selected daily usable sentences.

    Args:
        category: Optional category filter.
        n: Number of sentences to retrieve.

    Returns:
        A Sentence object if n=1, or a list of Sentence objects if n > 1.
    """
    pool = list_sentences(category=category)
    if not pool:
        raise SentenceNotFoundError(f"No sentences available for category: {category}")

    sample_size = min(n, len(pool))
    sampled = random.sample(pool, sample_size)
    if n == 1:
        return sampled[0]
    return sampled


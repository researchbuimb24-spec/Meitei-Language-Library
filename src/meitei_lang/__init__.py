# -*- coding: utf-8 -*-
"""
Meitei (Manipuri) Language Library.

A complete, production-quality Python package for the Meitei language (Manipuri),
providing robust Meitei Mayek script handling, transliteration, 170,000+ authentic
lexical entries (1.5+ lakh words), daily usable sentences across 12 practical categories,
10 classical literary reading texts, and 10 cultural songs with multi-script lyrics.
"""

from .exceptions import (
    MeiteiLangError,
    WordNotFoundError,
    BookNotFoundError,
    ChapterNotFoundError,
    SongNotFoundError,
    SentenceNotFoundError,
    LyricsNotAvailableError,
    DataLoadError,
    ValidationError,
)

from .transliteration import (
    normalize_text,
    detect_script,
    validate_text,
    meitei_to_roman,
    meitei_to_bengali,
    bengali_to_meitei,
    roman_to_meitei,
    transliterate,
)

from .dictionary import (
    WordEntry,
    load_vocabulary,
    count_words,
    get_vocabulary_count,
    get_word,
    lookup,
    search_words,
    get_words_by_category,
    get_words_by_pos,
    get_categories,
    get_parts_of_speech,
    get_random_words,
    get_vocabulary_summary,
)

from .books import (
    Book,
    Chapter,
    load_books,
    count_books,
    list_books,
    get_book,
    get_chapter,
    search_books,
)

from .songs import (
    Song,
    load_songs,
    count_songs,
    list_songs,
    get_song,
    get_lyrics,
    search_songs,
)

from .sentences import (
    Sentence,
    load_sentences,
    count_sentences,
    list_sentences,
    get_sentence,
    get_sentences_by_category,
    get_sentence_categories,
    search_sentences,
    get_random_sentence,
)

from .search import (
    SearchResults,
    search,
)

from .language_info import (
    IYEK_IPI,
    CHEISING_IYEK,
    LONSUM_IYEK,
    CHEITAP_IYEK,
    PUNCTUATION_IYEK,
    DIGITS_MAP,
    get_script_summary,
    get_alphabet,
    get_language_info,
    get_supported_scripts,
)

__version__ = "0.5.0"
__author__ = "Meitei Language Project Maintainers"

__all__ = [
    # Package metadata
    "__version__",
    "__author__",
    # Exceptions
    "MeiteiLangError",
    "WordNotFoundError",
    "BookNotFoundError",
    "ChapterNotFoundError",
    "SongNotFoundError",
    "SentenceNotFoundError",
    "LyricsNotAvailableError",
    "DataLoadError",
    "ValidationError",
    # Transliteration & Script handling
    "normalize_text",
    "detect_script",
    "validate_text",
    "meitei_to_roman",
    "meitei_to_bengali",
    "bengali_to_meitei",
    "roman_to_meitei",
    "transliterate",
    # Language & Script Metadata
    "IYEK_IPI",
    "CHEISING_IYEK",
    "LONSUM_IYEK",
    "CHEITAP_IYEK",
    "PUNCTUATION_IYEK",
    "DIGITS_MAP",
    "get_script_summary",
    "get_supported_scripts",
    "get_language_info",
    "get_alphabet",
    # Dictionary & Vocabulary
    "WordEntry",
    "load_vocabulary",
    "count_words",
    "get_vocabulary_count",
    "get_word",
    "lookup",
    "search_words",
    "get_words_by_category",
    "get_words_by_pos",
    "get_categories",
    "get_parts_of_speech",
    "get_random_words",
    "get_vocabulary_summary",
    # Books & Literature
    "Book",
    "Chapter",
    "load_books",
    "count_books",
    "list_books",
    "get_book",
    "get_chapter",
    "search_books",
    # Songs & Ballads
    "Song",
    "load_songs",
    "count_songs",
    "list_songs",
    "get_song",
    "get_lyrics",
    "search_songs",
    # Daily Usable Sentences
    "Sentence",
    "load_sentences",
    "count_sentences",
    "list_sentences",
    "get_sentence",
    "get_sentences_by_category",
    "get_sentence_categories",
    "search_sentences",
    "get_random_sentence",
    # Cross-corpus Search
    "SearchResults",
    "search",
]

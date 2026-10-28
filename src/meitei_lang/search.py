# -*- coding: utf-8 -*-
"""
Meitei Language Unified Search Engine.

Enables unified cross-corpus querying across:
- Vocabulary entries (Meitei Mayek words, Roman transliterations, English definitions)
- Books and reading passages
- Traditional and cultural songs
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from .dictionary import search_words, WordEntry
from .books import search_books
from .songs import search_songs, Song
from .sentences import search_sentences, Sentence


@dataclass
class SearchResults:
    """Aggregated search results across vocabulary, books, songs, and sentences."""
    query: str
    vocabulary: List[WordEntry] = field(default_factory=list)
    books: List[Dict[str, Any]] = field(default_factory=list)
    songs: List[Song] = field(default_factory=list)
    sentences: List[Sentence] = field(default_factory=list)

    @property
    def total_count(self) -> int:
        """Return total number of matching items across all corpora."""
        return len(self.vocabulary) + len(self.books) + len(self.songs) + len(self.sentences)

    @property
    def total_results(self) -> int:
        """Alias for total_count."""
        return self.total_count

    def is_empty(self) -> bool:
        """Return True if no matches were found."""
        return self.total_count == 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert results to a standard dictionary."""
        return {
            "query": self.query,
            "total_count": self.total_count,
            "vocabulary_count": len(self.vocabulary),
            "books_count": len(self.books),
            "songs_count": len(self.songs),
            "sentences_count": len(self.sentences),
            "vocabulary": [v.to_dict() for v in self.vocabulary],
            "books": self.books,
            "songs": [s.to_dict() for s in self.songs],
            "sentences": [s.to_dict() for s in self.sentences],
        }

    def __str__(self) -> str:
        return (
            f"SearchResults(query='{self.query}', total={self.total_count}: "
            f"vocab={len(self.vocabulary)}, books={len(self.books)}, "
            f"songs={len(self.songs)}, sentences={len(self.sentences)})"
        )


def search(
    query: str,
    in_vocabulary: bool = True,
    in_books: bool = True,
    in_songs: bool = True,
    in_sentences: bool = True,
    limit: Optional[int] = 25,
) -> SearchResults:
    """
    Search across all Meitei language corpora.

    Args:
        query: Search term (in Meitei Mayek, Romanized Meitei, or English).
        in_vocabulary: Whether to search vocabulary.
        in_books: Whether to search books and chapters.
        in_songs: Whether to search song titles and lyrics.
        in_sentences: Whether to search daily usable conversational sentences.
        limit: Max entries per corpus.

    Returns:
        SearchResults containing matches grouped by corpus.
    """
    q = query.strip()
    if not q:
        return SearchResults(query=query)

    vocab_matches: List[WordEntry] = []
    book_matches: List[Dict[str, Any]] = []
    song_matches: List[Song] = []
    sentence_matches: List[Sentence] = []

    if in_vocabulary:
        vocab_matches = search_words(q, search_in="all", limit=limit)

    if in_books:
        all_book_matches = search_books(q)
        book_matches = all_book_matches[:limit] if limit else all_book_matches

    if in_songs:
        all_song_matches = search_songs(q, search_in="all")
        song_matches = all_song_matches[:limit] if limit else all_song_matches

    if in_sentences:
        all_sentence_matches = search_sentences(q, search_in="all")
        sentence_matches = all_sentence_matches[:limit] if limit else all_sentence_matches

    return SearchResults(
        query=query,
        vocabulary=vocab_matches,
        books=book_matches,
        songs=song_matches,
        sentences=sentence_matches,
    )

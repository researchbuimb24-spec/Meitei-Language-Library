# -*- coding: utf-8 -*-
"""
Meitei Language Songs and Folk Ballads Module.

Provides access to authentic Manipuri songs, state anthems, folk ballads,
and lyrics in Meitei Mayek, Roman transliteration, Bengali script, and English translation.
"""

from dataclasses import dataclass, asdict
import json
import os
from typing import List, Dict, Any, Optional, Union

from .exceptions import SongNotFoundError, LyricsNotAvailableError, DataLoadError


@dataclass
class Song:
    """Represents an authentic Manipuri song or traditional folk ballad."""
    song_id: str
    title: str
    title_en: str
    title_roman: str
    title_bengali: str
    genre: str
    composer: str
    lyricist: str
    year: Union[int, str]
    language: str
    script: str
    status: str
    description: str
    source: str
    copyright: str
    lyrics: Dict[str, str]

    def get_lyrics(self, script: str = "meitei") -> str:
        """
        Retrieve lyrics in a chosen script.

        Args:
            script: 'meitei' (or 'mayek'), 'roman' (or 'latin'),
                    'bengali' (or 'bangla'), or 'english' (or 'translation').

        Returns:
            Lyrics as a string.

        Raises:
            LyricsNotAvailableError if lyrics for the specified script cannot be provided.
        """
        s = script.lower().strip()
        alias_map = {
            "meitei": "meitei",
            "meitei_mayek": "meitei",
            "mayek": "meitei",
            "mtei": "meitei",
            "roman": "roman",
            "latin": "roman",
            "latn": "roman",
            "bengali": "bengali",
            "bangla": "bengali",
            "beng": "bengali",
            "english": "english",
            "en": "english",
            "translation": "english",
        }
        normalized_key = alias_map.get(s, s)
        if normalized_key in self.lyrics and self.lyrics[normalized_key]:
            return self.lyrics[normalized_key]

        available = list(self.lyrics.keys())
        raise LyricsNotAvailableError(
            f"Lyrics in script '{script}' not available for song '{self.song_id}'. "
            f"Available scripts: {available}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert song object to standard Python dictionary."""
        return asdict(self)

    def __str__(self) -> str:
        return f"Song '{self.title}' ({self.title_en}) [{self.genre}]"


_SONGS_CACHE: Optional[List[Song]] = None
_SONG_MAP: Optional[Dict[str, Song]] = None


def _get_data_path() -> str:
    """Resolve path to songs.json."""
    return os.path.join(os.path.dirname(__file__), "data", "songs.json")


def load_songs(reload: bool = False) -> List[Song]:
    """
    Load packaged Manipuri songs dataset.

    Returns a list of Song objects.
    """
    global _SONGS_CACHE, _SONG_MAP
    if _SONGS_CACHE is not None and not reload:
        return _SONGS_CACHE

    path = _get_data_path()
    if not os.path.exists(path):
        raise DataLoadError(f"Songs dataset file not found at: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_songs = json.load(f)
    except Exception as e:
        raise DataLoadError(f"Failed to load songs data from {path}: {e}") from e

    songs: List[Song] = []
    song_map: Dict[str, Song] = {}

    for s in raw_songs:
        song = Song(
            song_id=s["song_id"],
            title=s["title"],
            title_en=s.get("title_en", ""),
            title_roman=s.get("title_roman", ""),
            title_bengali=s.get("title_bengali", ""),
            genre=s.get("genre", ""),
            composer=s.get("composer", "Traditional"),
            lyricist=s.get("lyricist", "Traditional"),
            year=s.get("year", "Traditional"),
            language=s.get("language", "Meitei (Manipuri)"),
            script=s.get("script", "Meitei Mayek"),
            status=s.get("status", ""),
            description=s.get("description", ""),
            source=s.get("source", ""),
            copyright=s.get("copyright", "Public Domain"),
            lyrics=s.get("lyrics", {}),
        )
        songs.append(song)
        song_map[song.song_id] = song

    _SONGS_CACHE = songs
    _SONG_MAP = song_map
    return _SONGS_CACHE


def _ensure_loaded():
    if _SONGS_CACHE is None or _SONG_MAP is None:
        load_songs()


def count_songs() -> int:
    """Return total number of songs in the library."""
    _ensure_loaded()
    assert _SONGS_CACHE is not None
    return len(_SONGS_CACHE)


def list_songs() -> List[Song]:
    """Return all available songs in the collection."""
    _ensure_loaded()
    assert _SONGS_CACHE is not None
    return list(_SONGS_CACHE)


def get_song(song_id: str) -> Song:
    """
    Retrieve a song by its unique song_id (e.g. 'sana_leibak_manipur').

    Raises SongNotFoundError if the song_id is not recognized.
    """
    _ensure_loaded()
    assert _SONG_MAP is not None

    clean_id = song_id.strip().lower()
    if clean_id in _SONG_MAP:
        return _SONG_MAP[clean_id]

    # Try matching title or title_roman
    for s in _SONG_MAP.values():
        if clean_id in (s.title.lower(), s.title_roman.lower(), s.title_en.lower()):
            return s

    available = list(_SONG_MAP.keys())
    raise SongNotFoundError(
        f"Song '{song_id}' not found. Available song IDs: {available}"
    )


def get_lyrics(song_id: str, script: str = "meitei") -> str:
    """Convenience function to retrieve lyrics of a specific song in the given script."""
    song = get_song(song_id)
    return song.get_lyrics(script)


def search_songs(query: str, search_in: str = "all") -> List[Song]:
    """
    Search songs by title, genre, description, or lyrics.

    Args:
        query: Search string.
        search_in: 'title', 'genre', 'lyrics', or 'all'.

    Returns:
        List of matching Song objects.
    """
    _ensure_loaded()
    assert _SONGS_CACHE is not None

    q = query.strip()
    if not q:
        return []
    q_lower = q.lower()
    search_in = search_in.lower()

    matches = []
    for s in _SONGS_CACHE:
        hit = False
        if search_in in ("title", "all"):
            if (q_lower in s.title.lower() or
                q_lower in s.title_en.lower() or
                q_lower in s.title_roman.lower() or
                q_lower in s.title_bengali.lower()):
                hit = True

        if not hit and search_in in ("genre", "all"):
            if q_lower in s.genre.lower() or q_lower in s.description.lower():
                hit = True

        if not hit and search_in in ("lyrics", "all"):
            for text in s.lyrics.values():
                if q_lower in text.lower():
                    hit = True
                    break

        if hit:
            matches.append(s)

    return matches

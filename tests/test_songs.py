# -*- coding: utf-8 -*-
"""Unit tests for meitei_lang songs module."""

import pytest
from meitei_lang.songs import (
    load_songs,
    count_songs,
    list_songs,
    get_song,
    get_lyrics,
    search_songs,
    Song,
)
from meitei_lang.exceptions import SongNotFoundError, LyricsNotAvailableError


def test_songs_count():
    assert count_songs() >= 3


def test_list_songs():
    songs = list_songs()
    assert len(songs) >= 3
    for s in songs:
        assert isinstance(s, Song)
        assert s.song_id
        assert s.title
        assert s.title_en
        assert s.lyrics


def test_get_song():
    song = get_song("sana_leibak_manipur")
    assert song.song_id == "sana_leibak_manipur"
    assert "Sana Leibak" in song.title_en
    assert song.composer
    assert song.lyricist
    assert song.genre


def test_get_song_not_found():
    with pytest.raises(SongNotFoundError):
        get_song("nonexistent_song_id")


def test_multi_script_lyrics():
    song = get_song("sana_leibak_manipur")

    # Meitei Mayek lyrics
    meitei_lyrics = song.get_lyrics("meitei")
    assert len(meitei_lyrics) > 50
    assert any(0xABC0 <= ord(c) <= 0xABFF for c in meitei_lyrics)

    # Roman lyrics
    roman_lyrics = song.get_lyrics("roman")
    assert len(roman_lyrics) > 50
    assert "Sana leibak Manipur" in roman_lyrics

    # Bengali lyrics
    bengali_lyrics = song.get_lyrics("bengali")
    assert len(bengali_lyrics) > 50
    assert any(0x0980 <= ord(c) <= 0x09FF for c in bengali_lyrics)

    # English translation
    english_lyrics = song.get_lyrics("english")
    assert len(english_lyrics) > 50
    assert "golden land" in english_lyrics.lower()

    # Top-level helper function
    assert get_lyrics("sana_leibak_manipur", "roman") == roman_lyrics

    # Invalid script
    with pytest.raises(LyricsNotAvailableError):
        song.get_lyrics("greek")


def test_search_songs():
    matches = search_songs("Yaoshang")
    assert len(matches) > 0
    assert any(s.song_id == "thabal_chongba_ishei" for s in matches)


def test_song_dict_access():
    song = get_song("sana_leibak_manipur")
    assert song["song_id"] == "sana_leibak_manipur"
    assert "composer" in song
    assert song.get("lyricist") == song.lyricist
    assert song.get("nonexistent", "fallback") == "fallback"
    with pytest.raises(KeyError):
        _ = song["invalid_key"]

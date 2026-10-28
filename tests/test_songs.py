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

ALL_SONG_IDS = [
    "sana_leibak_manipur",
    "thabal_chongba_ishei",
    "eikhoi_kangleicha",
    "chingda_satpi_engellei",
    "tamna_sangba_loktak_pat",
    "moirang_kangleirol_ballad",
    "he_leipakpokpa_lai",
    "nongmaijinggi_chingmei",
    "nungshirabi_eigi_manipur",
    "khulang_eshei_harvest",
]


def test_songs_count():
    assert count_songs() == 10


def test_list_songs():
    songs = list_songs()
    assert len(songs) == 10
    found_ids = {s.song_id for s in songs}
    for expected_id in ALL_SONG_IDS:
        assert expected_id in found_ids
    for s in songs:
        assert isinstance(s, Song)
        assert s.song_id
        assert s.title
        assert s.title_en
        assert s.lyrics


def test_all_individual_songs_retrieval():
    for song_id in ALL_SONG_IDS:
        song = get_song(song_id)
        assert isinstance(song, Song)
        assert song.song_id == song_id
        assert len(song.title) > 0
        assert len(song.title_en) > 0
        assert len(song.title_roman) > 0
        assert len(song.genre) > 0
        assert len(song.composer) > 0
        assert len(song.lyricist) > 0

        # Verify all four script lyrics
        for script_name in ("meitei", "roman", "bengali", "english"):
            lyrics = song.get_lyrics(script_name)
            assert len(lyrics) > 20, f"Lyrics too short for {song_id} ({script_name})"

        # Verify script characters
        meitei_text = song.get_lyrics("meitei")
        assert any(0xABC0 <= ord(c) <= 0xABFF for c in meitei_text)
        bengali_text = song.get_lyrics("bengali")
        assert any(0x0980 <= ord(c) <= 0x09FF for c in bengali_text)


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


def test_multi_script_lyrics_and_aliases():
    song = get_song("sana_leibak_manipur")

    # Meitei Mayek lyrics and aliases
    meitei_lyrics = song.get_lyrics("meitei")
    assert len(meitei_lyrics) > 50
    assert any(0xABC0 <= ord(c) <= 0xABFF for c in meitei_lyrics)
    assert song.get_lyrics("mayek") == meitei_lyrics
    assert song.get_lyrics("meitei_mayek") == meitei_lyrics

    # Roman lyrics and aliases
    roman_lyrics = song.get_lyrics("roman")
    assert len(roman_lyrics) > 50
    assert "Sana leibak Manipur" in roman_lyrics
    assert song.get_lyrics("latin") == roman_lyrics

    # Bengali lyrics and aliases
    bengali_lyrics = song.get_lyrics("bengali")
    assert len(bengali_lyrics) > 50
    assert any(0x0980 <= ord(c) <= 0x09FF for c in bengali_lyrics)
    assert song.get_lyrics("bangla") == bengali_lyrics

    # English translation and aliases
    english_lyrics = song.get_lyrics("english")
    assert len(english_lyrics) > 50
    assert "golden land" in english_lyrics.lower()
    assert song.get_lyrics("translation") == english_lyrics

    # Top-level helper function
    assert get_lyrics("sana_leibak_manipur", "roman") == roman_lyrics

    # Invalid script
    with pytest.raises(LyricsNotAvailableError):
        song.get_lyrics("greek")


def test_search_songs():
    matches_yaoshang = search_songs("Yaoshang")
    assert len(matches_yaoshang) > 0
    assert any(s.song_id == "thabal_chongba_ishei" for s in matches_yaoshang)

    # Search for harvest
    matches_harvest = search_songs("harvest")
    assert len(matches_harvest) > 0
    assert any(s.song_id == "khulang_eshei_harvest" for s in matches_harvest)

    # Search for Loktak
    matches_loktak = search_songs("Loktak")
    assert len(matches_loktak) >= 2

    # Search for Nongmaijing
    matches_nongmaijing = search_songs("Nongmaijing")
    assert len(matches_nongmaijing) >= 1


def test_song_dict_access():
    song = get_song("sana_leibak_manipur")
    assert song["song_id"] == "sana_leibak_manipur"
    assert "composer" in song
    assert song.get("lyricist") == song.lyricist
    assert song.get("nonexistent", "fallback") == "fallback"
    with pytest.raises(KeyError):
        _ = song["invalid_key"]


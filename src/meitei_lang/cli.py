# -*- coding: utf-8 -*-
"""
Command Line Interface and Interactive Terminal Application for meitei_lang.

Provides command-line commands and an interactive terminal menu for exploring
Meitei Mayek literature, songs, daily conversational sentences, dictionary,
and transliteration.
"""

import argparse
import io
import sys
from typing import Optional

if isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import meitei_lang as mt
from meitei_lang import language_info
from meitei_lang.exceptions import (
    BookNotFoundError,
    ChapterNotFoundError,
    SongNotFoundError,
    SentenceNotFoundError,
    WordNotFoundError,
)


def print_banner():
    banner = f"""
========================================================================
    ꯃꯩꯇꯩ ꯂꯣꯟ (Meitei-Lang) — Manipuri Language Library v{mt.__version__}
    Meitei Mayek Script Engine • 170k+ Vocabulary • 10 Books • 10 Songs
========================================================================
"""
    print(banner.strip())


def cmd_info():
    """Display library overview, stats, and dataset sizes."""
    print_banner()
    print(f"\nPackage Version: {mt.__version__}")
    print(f"Total Verified Vocabulary: {mt.count_words():,} entries")
    print(f"Classical Books & Puyas:   {mt.count_books()} books (34 chapters)")
    print(f"Authentic Songs & Ballads: {mt.count_songs()} songs (4-script lyrics)")
    print(f"Daily Usable Sentences:    {mt.count_sentences()} sentences ({len(mt.get_sentence_categories())} categories)")
    print("\nCore Script System:")
    summary = language_info.get_script_summary()
    print(f"  - Iyek Ipi (Primary Base Letters):  18 letters (U+ABC0 to U+ABD1)")
    print(f"  - Cheising Iyek (Extended Letters): 9 letters (U+ABD2 to U+ABDA)")
    print(f"  - Lonsum Iyek (Coda Consonants):    8 letters (U+ABDB to U+ABE2)")
    print(f"  - Cheitap Iyek (Vowel Diacritics):  8 vowel signs (U+ABE3 to U+ABEA)")
    print(f"  - Indigenous Digits (0-9):          10 digits (U+ABF0 to U+ABF9)")


def cmd_books():
    """List all available books in the library."""
    print_banner()
    print("\nAvailable Classical Books and Historical Puyas:\n")
    books = mt.list_books()
    for idx, b in enumerate(books, 1):
        print(f"  {idx:2d}. [{b.book_id}]")
        print(f"      Title:   {b.title} ({b.title_en})")
        print(f"      Genre:   {b.genre} | Author: {b.author}")
        print(f"      Chapters: {b.total_chapters()} chapters | Total Words: {b.total_word_count()}")
        print()


def cmd_book(book_id: str):
    """Show details and chapter index of a specific book."""
    try:
        book = mt.get_book(book_id)
    except BookNotFoundError as e:
        print(f"Error: {e}")
        return

    print_banner()
    print(f"\nBook: {book.title} ({book.title_en})")
    print(f"ID:          {book.book_id}")
    print(f"Author:      {book.author}")
    print(f"Genre:       {book.genre}")
    print(f"Source:      {book.source}")
    print(f"Copyright:   {book.copyright}")
    print(f"\nDescription:\n  {book.description}\n")
    print(f"Chapters ({book.total_chapters()}):")
    for ch in book.chapters:
        print(f"  Chapter {ch.chapter_number}: {ch.title} ({ch.title_en}) [{ch.word_count()} words]")


def cmd_read(book_id: str, chapter_num: int):
    """Read a specific chapter of a book."""
    try:
        book = mt.get_book(book_id)
        ch = book.get_chapter(chapter_num)
    except (BookNotFoundError, ChapterNotFoundError) as e:
        print(f"Error: {e}")
        return

    print_banner()
    print(f"\n{book.title} ({book.title_en})")
    print(f"Chapter {ch.chapter_number}: {ch.title} ({ch.title_en})\n")
    print("------------------------------------------------------------------------")
    print(ch.text)
    print("------------------------------------------------------------------------")


def cmd_songs():
    """List all 10 songs in the library."""
    print_banner()
    print("\nAuthentic Manipuri Songs and Ballads Collection:\n")
    songs = mt.list_songs()
    for idx, s in enumerate(songs, 1):
        print(f"  {idx:2d}. [{s.song_id}]")
        print(f"      Title:    {s.title} ({s.title_en})")
        print(f"      Genre:    {s.genre} | Year: {s.year}")
        print(f"      Composer: {s.composer} | Lyricist: {s.lyricist}")
        print()


def cmd_lyrics(song_id: str, script: str = "meitei"):
    """Show lyrics of a specific song in the requested script."""
    try:
        song = mt.get_song(song_id)
        lyrics = song.get_lyrics(script)
    except (SongNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return

    print_banner()
    print(f"\nSong: {song.title} ({song.title_en})")
    print(f"Composer: {song.composer} | Lyricist: {song.lyricist} | Genre: {song.genre}")
    print(f"Script: {script.upper()}\n")
    print("------------------------------------------------------------------------")
    print(lyrics)
    print("------------------------------------------------------------------------")


def cmd_sentences(category: Optional[str] = None):
    """List daily usable conversational sentences."""
    print_banner()
    if category:
        sentences = mt.get_sentences_by_category(category)
        print(f"\nDaily Usable Sentences in category '{category}' ({len(sentences)}):\n")
    else:
        sentences = mt.list_sentences()
        print(f"\nAll Daily Usable Sentences ({len(sentences)}):\n")

    for idx, s in enumerate(sentences[:25], 1):
        print(f"  {idx:2d}. [{s.sentence_id}] ({s.category})")
        print(f"      Meitei Mayek: {s.meitei}")
        print(f"      Roman:        {s.roman}")
        print(f"      English:      {s.english}")
        print(f"      Context:      {s.context}\n")

    if len(sentences) > 25:
        print(f"  ... and {len(sentences) - 25} more sentences. Filter by category with --category <name>")


def cmd_word(query: str):
    """Lookup a word in the vocabulary dataset."""
    try:
        w = mt.get_word(query)
        print_banner()
        print(f"\nWord:            {w.word}")
        print(f"Transliteration: {w.transliteration}")
        print(f"Meaning (EN):    {w.meaning_en}")
        print(f"Part of Speech:  {w.part_of_speech}")
        print(f"Category:        {w.category}")
        print(f"Source:          {w.source}")
    except WordNotFoundError:
        # Fallback to substring search
        matches = mt.search_words(query, limit=10)
        print_banner()
        if matches:
            print(f"\nExact match not found. Showing {len(matches)} close results for '{query}':\n")
            for m in matches:
                print(f"  - {m.word} ({m.transliteration}) [{m.part_of_speech}]: {m.meaning_en}")
        else:
            print(f"\nNo dictionary entries found matching '{query}'.")


def cmd_search(query: str):
    """Unified cross-corpus search across vocabulary, books, songs, and sentences."""
    print_banner()
    res = mt.search(query)
    print(f"\nSearch results for '{query}' (Total: {res.total_count} matches):\n")

    if res.vocabulary:
        print(f"--- Vocabulary ({len(res.vocabulary)} matches) ---")
        for v in res.vocabulary[:5]:
            print(f"  • {v.word} ({v.transliteration}): {v.meaning_en}")
        if len(res.vocabulary) > 5:
            print(f"    ... and {len(res.vocabulary) - 5} more words.")
        print()

    if res.books:
        print(f"--- Books & Literature ({len(res.books)} matches) ---")
        for b in res.books[:5]:
            print(f"  • {b['book_title_en']} (Chapter {b['chapter_number']}): {b['matched_text']}")
        print()

    if res.songs:
        print(f"--- Songs & Ballads ({len(res.songs)} matches) ---")
        for s in res.songs:
            print(f"  • {s.title} ({s.title_en}) [{s.genre}]")
        print()

    if res.sentences:
        print(f"--- Daily Sentences ({len(res.sentences)} matches) ---")
        for st in res.sentences[:5]:
            print(f"  • [{st.category}] {st.meitei} ({st.roman}): {st.english}")
        print()

    if res.is_empty():
        print(f"No results found across any corpus for '{query}'.")


def cmd_transliterate(text: str, target: str = "roman"):
    """Transliterate text between Meitei Mayek, Roman, and Bengali."""
    out = mt.transliterate(text, target_script=target)
    print_banner()
    print(f"\nInput:  {text}")
    print(f"Target: {target.upper()}")
    print(f"Output: {out}")


def cmd_interactive():
    """Interactive text-based menu application for exploring the library."""
    print_banner()
    print("\nWelcome to the Meitei Language Interactive Explorer!")

    while True:
        print("\nMain Menu:")
        print("  1. Library Overview & Script Metadata")
        print("  2. Browse 10 Classical Books & Puyas")
        print("  3. Read a Book Chapter")
        print("  4. Browse 10 Authentic Songs & Anthems")
        print("  5. View Song Lyrics (Meitei / Roman / Bengali / English)")
        print("  6. Explore Daily Usable Conversational Sentences")
        print("  7. Dictionary Word Lookup")
        print("  8. Unified Cross-Corpus Search")
        print("  9. Transliterate Text")
        print("  0. Exit Application")

        try:
            choice = input("\nEnter choice (0-9): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Thank you! / ꯊꯥꯒꯠꯆꯔꯤ꯫")
            break

        if choice == "0":
            print("\nExiting meitei-lang. Khurumjari! / ꯈꯨꯔꯨꯝꯖꯔꯤ꯫")
            break
        elif choice == "1":
            cmd_info()
        elif choice == "2":
            cmd_books()
        elif choice == "3":
            cmd_books()
            bid = input("Enter book ID (e.g. khamba_thoibi, numit_kappa): ").strip()
            ch_str = input("Enter chapter number (1, 2, 3...): ").strip()
            if bid and ch_str.isdigit():
                cmd_read(bid, int(ch_str))
            else:
                print("Invalid input.")
        elif choice == "4":
            cmd_songs()
        elif choice == "5":
            cmd_songs()
            sid = input("Enter song ID (e.g. sana_leibak_manipur): ").strip()
            sc = input("Enter script (meitei / roman / bengali / english) [default: meitei]: ").strip() or "meitei"
            if sid:
                cmd_lyrics(sid, sc)
        elif choice == "6":
            cats = mt.get_sentence_categories()
            print("Available categories:", ", ".join(cats))
            cat = input("Enter category to filter (or press Enter for all): ").strip()
            cmd_sentences(cat if cat else None)
        elif choice == "7":
            w = input("Enter word in Meitei Mayek or Roman transliteration (e.g. ꯃꯃꯥ or khurumjari): ").strip()
            if w:
                cmd_word(w)
        elif choice == "8":
            q = input("Enter search query (e.g. Loktak, Kangla, Manipur): ").strip()
            if q:
                cmd_search(q)
        elif choice == "9":
            txt = input("Enter text to transliterate: ").strip()
            tgt = input("Enter target script (roman / meitei / bengali) [default: roman]: ").strip() or "roman"
            if txt:
                cmd_transliterate(txt, tgt)
        else:
            print("Invalid selection. Please choose an option from 0 to 9.")


def main():
    parser = argparse.ArgumentParser(
        prog="meitei",
        description="Meitei (Manipuri) Language CLI & Interactive Explorer",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # info
    subparsers.add_parser("info", help="Show library metadata, statistics, and script overview")

    # books
    subparsers.add_parser("books", help="List all 10 classical books and historical puyas")

    # book
    book_p = subparsers.add_parser("book", help="Show details and chapter index of a book")
    book_p.add_argument("book_id", help="Book identifier (e.g. khamba_thoibi, numit_kappa)")

    # read
    read_p = subparsers.add_parser("read", help="Read a chapter of a book")
    read_p.add_argument("book_id", help="Book identifier")
    read_p.add_argument("chapter", type=int, help="Chapter number (1, 2, 3...)")

    # songs
    subparsers.add_parser("songs", help="List all 10 authentic Manipuri songs and anthems")

    # lyrics
    lyrics_p = subparsers.add_parser("lyrics", help="Display complete lyrics of a song")
    lyrics_p.add_argument("song_id", help="Song identifier (e.g. sana_leibak_manipur)")
    lyrics_p.add_argument(
        "--script",
        default="meitei",
        choices=["meitei", "roman", "bengali", "english"],
        help="Script format for lyrics (default: meitei)",
    )

    # sentences
    sent_p = subparsers.add_parser("sentences", help="Browse daily usable conversational sentences")
    sent_p.add_argument("--category", default=None, help="Filter sentences by category")

    # word
    word_p = subparsers.add_parser("word", help="Lookup a word in the dictionary")
    word_p.add_argument("query", help="Word in Meitei Mayek or Roman transliteration")

    # search
    search_p = subparsers.add_parser("search", help="Search across vocabulary, books, songs, and sentences")
    search_p.add_argument("query", help="Search term")

    # transliterate
    trans_p = subparsers.add_parser("transliterate", help="Transliterate text between scripts")
    trans_p.add_argument("text", help="Text to transliterate")
    trans_p.add_argument(
        "--to",
        default="roman",
        choices=["roman", "meitei", "bengali"],
        help="Target script (default: roman)",
    )

    # interactive
    subparsers.add_parser("interactive", help="Start interactive text-based terminal explorer")

    args = parser.parse_args()

    if args.command == "info":
        cmd_info()
    elif args.command == "books":
        cmd_books()
    elif args.command == "book":
        cmd_book(args.book_id)
    elif args.command == "read":
        cmd_read(args.book_id, args.chapter)
    elif args.command == "songs":
        cmd_songs()
    elif args.command == "lyrics":
        cmd_lyrics(args.song_id, args.script)
    elif args.command == "sentences":
        cmd_sentences(args.category)
    elif args.command == "word":
        cmd_word(args.query)
    elif args.command == "search":
        cmd_search(args.query)
    elif args.command == "transliterate":
        cmd_transliterate(args.text, args.to)
    elif args.command == "interactive":
        cmd_interactive()
    else:
        # Default if no subcommand is given: show overview banner
        cmd_info()


if __name__ == "__main__":
    main()


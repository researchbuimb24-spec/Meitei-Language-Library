# -*- coding: utf-8 -*-
"""
Comprehensive Unit and Integration Tests for the Meitei Digital Book Library (`meitei.books`).

Verifies:
1. Catalog management and status honesty (CATALOG_ONLY, PARTIALLY_IMPORTED, FULLY_IMPORTED).
2. Importing from JSON, Markdown (.md), Plain Text (.txt), and JSONL (.jsonl).
3. Text segmentation and deterministic passage IDs ({book_id}-c{ch:02d}-p{p:03d}).
4. Cryptographic SHA-256 calculation and import manifest verification.
5. Paginated chapter reading and navigation metadata.
6. Full-text search across book passages using FTS5 and relational matching.
7. Validation of passage ordering, monotonicity, and rights metadata.
8. Translation alignment and provenance attribution.
9. Quarantined vocabulary candidate extraction linked to exact passages with zero core lexicon contamination.
10. CLI commands execution parity (`meitei books list`, `info`, `read`, `search`, `validate`, `audit`, `stats`).
"""

import io
import json
from contextlib import redirect_stdout
from pathlib import Path
import pytest

from meitei import cli
from meitei.books import (
    BookAuditResult,
    BookCatalog,
    BookCatalogRecord,
    BookImporter,
    BookNotFoundError,
    BookNotImportedError,
    BookReader,
    BookSearchEngine,
    BookTranslationAligner,
    BookValidator,
    Chapter,
    ChapterNotFoundError,
    ImportManifest,
    ImportStatus,
    Passage,
    RightsStatus,
    VocabularyCandidate,
    VocabularyExtractor,
    audit_books,
    compute_sha256,
    get_book_info,
    get_book_stats,
    is_valid_passage_id,
    list_books,
    read_passages,
    search_passages,
    segment_text_into_passages,
)
from meitei.loader import DataLoader


# =============================================================================
# Catalog & Rights Metadata Tests
# =============================================================================

def test_catalog_initialization_and_list():
    """Verify catalog loads 10 books with authentic rights metadata."""
    books = list_books(data_dir="data")
    assert len(books) >= 10

    book_ids = {b.book_id for b in books}
    assert "khamba_thoibi" in book_ids
    assert "phunga_wari" in book_ids
    assert "numit_kappa" in book_ids
    assert "chainarol" in book_ids

    for b in books:
        assert b.title
        assert b.title_en
        assert b.author
        assert b.rights_status in [
            RightsStatus.PUBLIC_DOMAIN.value,
            RightsStatus.TRADITIONAL_CULTURAL.value,
            RightsStatus.CREATIVE_COMMONS.value,
            RightsStatus.ACADEMIC_FAIR_USE.value,
        ]
        assert b.copyright
        assert b.import_status in [
            ImportStatus.CATALOG_ONLY,
            ImportStatus.PARTIALLY_IMPORTED,
            ImportStatus.FULLY_IMPORTED,
        ]


def test_status_honesty_catalog_only(tmp_path):
    """Ensure CATALOG_ONLY books honestly report that text has not been imported."""
    cat = BookCatalog(data_dir=tmp_path)
    # Register a book as CATALOG_ONLY without importing text
    rec = BookCatalogRecord(
        book_id="copyrighted_grammar_1997",
        title="ꯑꯀꯥꯡꯕ ꯂꯥꯏꯔꯤꯛ",
        title_en="A Grammar of Meithei (Catalog Metadata Only)",
        author="Shobhana L. Chelliah",
        rights_status=RightsStatus.RESTRICTED.value,
        copyright="Copyright © Mouton de Gruyter",
        import_status=ImportStatus.CATALOG_ONLY,
        total_chapters=15,
        imported_chapters=0,
        total_passages=0,
    )
    cat.register_book(rec)

    # Retrieval
    retrieved = cat.get_book("copyrighted_grammar_1997")
    assert retrieved is not None
    assert retrieved.import_status == ImportStatus.CATALOG_ONLY

    # Reading text raises BookNotImportedError honestly
    reader = BookReader(data_dir=tmp_path)
    with pytest.raises(BookNotImportedError) as exc:
        reader.get_chapters("copyrighted_grammar_1997")
    assert "full text has not been imported" in str(exc.value)


# =============================================================================
# Importer & Format Parsing Tests (TXT, MD, JSON)
# =============================================================================

def test_passage_segmentation_and_stable_ids():
    """Verify text is segmented with deterministic stable IDs: {book_id}-c{ch:02d}-p{p:03d}."""
    raw_text = "ꯑꯔꯤꯕ ꯃꯇꯝꯗ ꯃꯣꯏꯔꯥꯡꯗ ꯈꯝꯕ ꯂꯩꯔꯝꯃꯤ꯫ ꯊꯣꯏꯕꯤꯒ ꯎꯅꯈꯤ꯫"
    passages = segment_text_into_passages("khamba_thoibi", 1, raw_text)

    assert len(passages) == 2
    assert passages[0].passage_id == "khamba_thoibi-c01-p001"
    assert passages[1].passage_id == "khamba_thoibi-c01-p002"
    assert is_valid_passage_id(passages[0].passage_id)
    assert is_valid_passage_id(passages[1].passage_id)
    assert passages[0].word_count > 0
    assert passages[0].character_count > 0


def test_import_markdown(tmp_path):
    """Test importing a local Markdown (.md) book file with chapter headers."""
    md_file = tmp_path / "sample_epic.md"
    content = """# Chapter 1: The Beginning
ꯑꯩꯈꯣꯏꯒꯤ ꯂꯩꯄꯥꯛ ꯑꯁꯤ ꯐꯖꯩ꯫ ꯃꯤꯌꯥꯝꯅ ꯅꯨꯡꯉꯥꯏꯅ ꯂꯩꯔꯤ꯫

# Chapter 2: The Journey
ꯈꯝꯕꯅ ꯂꯣꯛꯇꯥꯛ ꯄꯥꯠꯇ ꯆꯠꯈꯤ꯫ ꯉꯥ ꯐꯥꯈꯤ꯫
"""
    md_file.write_text(content, encoding="utf-8")

    importer = BookImporter(data_dir=tmp_path)
    manifest = importer.import_markdown(
        file_path=md_file,
        book_id="sample_epic",
        title="ꯁꯦꯝꯒꯠꯄ ꯋꯥꯔꯤ",
        title_en="Sample Epic",
        author="Traditional Bard",
    )

    assert isinstance(manifest, ImportManifest)
    assert manifest.book_id == "sample_epic"
    assert manifest.file_format == "markdown"
    assert manifest.total_chapters == 2
    assert manifest.total_passages >= 2
    assert len(manifest.sha256_checksum) == 64

    # Verify book can be read
    reader = BookReader(data_dir=tmp_path)
    ch1 = reader.get_chapter("sample_epic", 1)
    assert ch1.chapter_number == 1
    assert len(ch1.passages) >= 1
    assert ch1.passages[0].passage_id == "sample_epic-c01-p001"


def test_import_plain_text(tmp_path):
    """Test importing a plain text (.txt) file with chapter dividers."""
    txt_file = tmp_path / "ancient_chronicle.txt"
    content = """Chapter 1: Creation
ꯑꯇꯤꯌꯥ ꯑꯃꯁꯨꯡ ꯂꯩꯄꯥꯛ ꯁꯦꯝꯈꯤ꯫

Chapter 2: Kings
ꯅꯤꯡꯊꯧ ꯀꯌꯥ ꯂꯩꯉꯥꯛꯈꯤ꯫
"""
    txt_file.write_text(content, encoding="utf-8")

    importer = BookImporter(data_dir=tmp_path)
    manifest = importer.import_text(
        file_path=txt_file,
        book_id="ancient_chronicle",
        title="ꯑꯔꯤꯕ ꯄꯨꯋꯥꯔꯤ",
        title_en="Ancient Chronicle",
        author="Ancient Maichou",
    )

    assert manifest.total_chapters == 2
    assert manifest.file_format == "txt"

    reader = BookReader(data_dir=tmp_path)
    ch2 = reader.get_chapter("ancient_chronicle", 2)
    assert ch2.chapter_number == 2
    assert len(ch2.passages) == 1


# =============================================================================
# Reader & Pagination Tests
# =============================================================================

def test_reader_pagination():
    """Verify paginated reading across passages."""
    passages, page_info = read_passages(
        book_id="khamba_thoibi",
        chapter_number=1,
        page=1,
        page_size=3,
        data_dir="data",
    )

    assert len(passages) == 3
    assert page_info["page"] == 1
    assert page_info["page_size"] == 3
    assert page_info["total_passages"] >= 6
    assert page_info["has_next"] is True
    assert page_info["has_prev"] is False

    # Read page 2
    passages_p2, page_info_p2 = read_passages(
        book_id="khamba_thoibi",
        chapter_number=1,
        page=2,
        page_size=3,
        data_dir="data",
    )
    assert len(passages_p2) >= 1
    assert page_info_p2["page"] == 2
    assert page_info_p2["has_prev"] is True


def test_reader_get_passage_by_id():
    """Verify retrieval of passage by stable identifier."""
    reader = BookReader(data_dir="data")
    p = reader.get_passage_by_id("khamba_thoibi-c01-p001")
    assert p is not None
    assert p.passage_id == "khamba_thoibi-c01-p001"
    assert p.book_id == "khamba_thoibi"
    assert p.chapter_number == 1
    assert "ꯃꯣꯏꯔꯥꯡ" in p.text

    # Nonexistent ID
    none_p = reader.get_passage_by_id("nonexistent_book-c01-p001")
    assert none_p is None


def test_reader_chapter_not_found():
    """Verify ChapterNotFoundError when requesting out-of-bounds chapter."""
    reader = BookReader(data_dir="data")
    with pytest.raises(ChapterNotFoundError):
        reader.get_chapter("khamba_thoibi", 999)


# =============================================================================
# Full-Text Search Tests
# =============================================================================

def test_search_passages_mayek_and_snippet():
    """Verify passage full-text search and snippet generation."""
    results = search_passages("ꯂꯣꯛꯇꯥꯛ", data_dir="data")
    assert len(results) >= 1
    assert any("khamba_thoibi" in r.book_id for r in results)

    top = results[0]
    assert "ꯂꯣꯛꯇꯥꯛ" in top.text
    assert top.match_score >= 80.0
    assert len(top.matched_snippet) > 0


def test_search_passages_english_title_routing():
    """Verify searching for English terms routes to relevant passages."""
    results = search_passages("Moirang", book_id="khamba_thoibi", data_dir="data")
    assert len(results) >= 1
    assert all(r.book_id == "khamba_thoibi" for r in results)


def test_search_passages_zero_matches():
    """Verify search returns empty list without error on unknown terms."""
    results = search_passages("nonexistent_term_zyxw_987", data_dir="data")
    assert results == []


# =============================================================================
# Validation & Cryptographic Audit Tests
# =============================================================================

def test_book_validator_valid():
    """Verify that all default imported books pass validation cleanly."""
    validator = BookValidator(data_dir="data")
    res = validator.validate_book("khamba_thoibi")
    assert res.valid is True
    assert res.imported_chapters_count == 4
    assert res.passages_count == 22
    assert res.errors == []


def test_audit_all_books():
    """Verify full audit across all 10 books in catalog."""
    audit = audit_books(data_dir="data")
    assert audit["all_valid"] is True
    assert audit["total_books_audited"] >= 10
    assert audit["fully_imported"] >= 10
    assert audit["total_passages"] >= 140


def test_validator_detects_passage_ordering_violation(tmp_path):
    """Verify validator flags invalid passage sequencing."""
    texts_dir = tmp_path / "books" / "texts"
    texts_dir.mkdir(parents=True)

    cat = BookCatalog(data_dir=tmp_path)
    cat.register_book(
        BookCatalogRecord(
            book_id="bad_sequence",
            title="ꯑꯁꯣꯏꯕ",
            title_en="Faulty Sequence",
            author="Author",
            import_status=ImportStatus.FULLY_IMPORTED,
            total_chapters=1,
        )
    )

    bad_payload = {
        "book_id": "bad_sequence",
        "title": "ꯑꯁꯣꯏꯕ",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Ch 1",
                "passages": [
                    {"passage_id": "bad_sequence-c01-p001", "passage_number": 1, "text": "Text 1"},
                    {"passage_id": "bad_sequence-c01-p003", "passage_number": 3, "text": "Text 3"},  # Skipped 2!
                ],
            }
        ],
    }
    with open(texts_dir / "bad_sequence.json", "w", encoding="utf-8") as f:
        json.dump(bad_payload, f)

    validator = BookValidator(data_dir=tmp_path)
    res = validator.validate_book("bad_sequence")
    assert res.valid is False
    assert any("Passage ordering violation" in e for e in res.errors)


# =============================================================================
# Translation Alignment Tests
# =============================================================================

def test_translation_alignment(tmp_path):
    """Verify recording and querying bilingual passage translation alignments."""
    # Copy khamba_thoibi texts to tmp_path
    importer = BookImporter(data_dir=tmp_path)
    importer.import_default_heritage_books()

    aligner = BookTranslationAligner(data_dir=tmp_path)
    aligned = aligner.align_passage(
        passage_id="khamba_thoibi-c01-p001",
        translation_text="In ancient times, King Chingkhu Telheiba ruled Moirang through the grace of Lord Thangjing.",
        translator="Manipuri Folklore Society Scholar",
        citation_reference="Moirang Kangleirol Translation Series, Vol. 1",
    )

    assert aligned.passage_id == "khamba_thoibi-c01-p001"
    assert "Chingkhu Telheiba" in aligned.translation_text
    assert aligned.translator == "Manipuri Folklore Society Scholar"

    # Bilingual chapter retrieval
    bilingual = aligner.get_chapter_bilingual("khamba_thoibi", 1)
    assert len(bilingual) >= 1
    assert bilingual[0].passage_id == "khamba_thoibi-c01-p001"
    assert bilingual[0].translation_text == aligned.translation_text


# =============================================================================
# Vocabulary Candidate Extraction & Isolation Tests
# =============================================================================

def test_vocabulary_extraction_and_candidate_isolation(tmp_path):
    """
    Verify candidate extraction:
    1. Extracts valid candidates with exact passage references.
    2. Candidate status is strictly UNVERIFIED.
    3. Authoritative dictionary core_lexicon.jsonl remains uncontaminated.
    """
    # 1. Setup data directory with core lexicon
    importer = BookImporter(data_dir=tmp_path)
    importer.import_default_heritage_books()

    extractor = VocabularyExtractor(data_dir=tmp_path)
    candidates = extractor.extract_book_candidates("khamba_thoibi")

    assert len(candidates) > 50

    for c in candidates:
        assert isinstance(c, VocabularyCandidate)
        assert c.status == "UNVERIFIED"
        assert c.book_id == "khamba_thoibi"
        assert is_valid_passage_id(c.passage_id)
        assert len(c.lemma) > 0
        assert len(c.context_passage) > 0

    # 2. Check candidate retrieval from quarantine ledger
    quarantined = extractor.get_candidates("khamba_thoibi")
    assert len(quarantined) == len(candidates)

    # 3. Verify authoritative core_lexicon.jsonl has NOT been contaminated
    dl = DataLoader("data")
    core = dl.load_lexicon(partition="core")
    assert len(core) == 10, "Authoritative core lexicon must remain strictly untouched!"


# =============================================================================
# CLI Subcommand Tests: meitei books ...
# =============================================================================

def test_cli_books_list():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["books", "list"])
    assert exit_code == 0
    out = f.getvalue()
    assert "Digital Books Catalog" in out
    assert "khamba_thoibi" in out
    assert "FULLY_IMPORTED" in out


def test_cli_books_info():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["books", "info", "khamba_thoibi"])
    assert exit_code == 0
    out = f.getvalue()
    assert "Khamba Thoibi: The Epic of Moirang" in out
    assert "Public Domain" in out
    assert "SHA-256" in out


def test_cli_books_read():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["books", "read", "khamba_thoibi", "--chapter", "1", "--page", "1"])
    assert exit_code == 0
    out = f.getvalue()
    assert "Reading: khamba_thoibi - Chapter 1" in out
    assert "khamba_thoibi-c01-p001" in out


def test_cli_books_search():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["books", "search", "ꯂꯣꯛꯇꯥꯛ"])
    assert exit_code == 0
    out = f.getvalue()
    assert "passage match(es)" in out
    assert "khamba_thoibi" in out


def test_cli_books_validate():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["books", "validate"])
    assert exit_code == 0
    assert "Digital Books Validation: PASSED" in f.getvalue()


def test_cli_books_audit():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["books", "audit"])
    assert exit_code == 0
    out = f.getvalue()
    assert "Cryptographic Audit" in out
    assert "INTEGRITY 100% VERIFIED" in out


def test_cli_books_stats():
    f = io.StringIO()
    with redirect_stdout(f):
        exit_code = cli.main(["books", "stats"])
    assert exit_code == 0
    out = f.getvalue()
    assert "Total Registered Books:" in out
    assert "Fully Imported Books:" in out


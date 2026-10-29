# -*- coding: utf-8 -*-
"""
Data Models for the Meitei Digital Book Library Subsystem.

Defines typed dataclasses and status enumerations for:
- Books, Chapters, and Passages with stable identifiers
- Import status (CATALOG_ONLY, PARTIALLY_IMPORTED, FULLY_IMPORTED)
- Bibliographic and rights metadata
- Import manifests and SHA-256 checksums
- Translation alignments with provenance
- Vocabulary candidate records isolated from the authoritative dictionary
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ImportStatus(str, Enum):
    """
    Controlled vocabulary of book ingestion statuses.

    - CATALOG_ONLY: Bibliographic and rights metadata cataloged; full text NOT imported.
    - PARTIALLY_IMPORTED: Sample chapters or excerpt passages imported into local ledger.
    - FULLY_IMPORTED: Complete text imported, verified, checksummed, and segmented.
    """
    CATALOG_ONLY = "CATALOG_ONLY"
    PARTIALLY_IMPORTED = "PARTIALLY_IMPORTED"
    FULLY_IMPORTED = "FULLY_IMPORTED"


class RightsStatus(str, Enum):
    """Rights and copyright legal status."""
    PUBLIC_DOMAIN = "Public Domain"
    CREATIVE_COMMONS = "Creative Commons"
    ACADEMIC_FAIR_USE = "Academic Fair Use"
    TRADITIONAL_CULTURAL = "Traditional Cultural Expressions"
    RESTRICTED = "Restricted / Copyright Protected"


# Stable Passage ID format regex: {book_id}-c{ch:02d}-p{p:03d}
REGEX_PASSAGE_ID = re.compile(r"^[a-zA-Z0-9_\-]+-c\d{2}-p\d{3,4}$")


def is_valid_passage_id(val: str) -> bool:
    """Check if string is a valid deterministic passage identifier."""
    return bool(REGEX_PASSAGE_ID.match(val)) if isinstance(val, str) else False


@dataclass
class Passage:
    """
    A single segmented passage within a chapter.

    Attributes:
        passage_id: Deterministic stable identifier (e.g. khamba_thoibi-c01-p001).
        book_id: Parent book identifier.
        chapter_number: Chapter index (1-based).
        passage_number: Passage index within the chapter (1-based).
        text: Primary text content in Meitei Mayek.
        text_roman: Roman transliteration if available.
        text_bengali: Historical Bengali-script representation if available.
        translation_en: English translation if aligned.
        translation_provenance: Authority, source, or translator attribution.
        word_count: Number of words in passage.
        character_count: Number of characters in passage.
    """
    passage_id: str
    book_id: str
    chapter_number: int
    passage_number: int
    text: str
    text_roman: Optional[str] = None
    text_bengali: Optional[str] = None
    translation_en: Optional[str] = None
    translation_provenance: Optional[str] = None
    word_count: int = 0
    character_count: int = 0

    def __post_init__(self) -> None:
        if not self.character_count and self.text:
            self.character_count = len(self.text)
        if not self.word_count and self.text:
            self.word_count = len(self.text.split())

    def to_dict(self) -> Dict[str, Any]:
        """Convert passage to JSON-serializable dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Passage:
        """Construct Passage from dictionary."""
        return cls(
            passage_id=data.get("passage_id", ""),
            book_id=data.get("book_id", ""),
            chapter_number=int(data.get("chapter_number", 1)),
            passage_number=int(data.get("passage_number", 1)),
            text=data.get("text", ""),
            text_roman=data.get("text_roman"),
            text_bengali=data.get("text_bengali"),
            translation_en=data.get("translation_en"),
            translation_provenance=data.get("translation_provenance"),
            word_count=int(data.get("word_count", 0)),
            character_count=int(data.get("character_count", 0)),
        )


@dataclass
class Chapter:
    """
    A structured chapter comprising ordered passages.

    Attributes:
        chapter_id: Deterministic identifier (e.g. khamba_thoibi-c01).
        book_id: Parent book identifier.
        chapter_number: Numeric chapter index.
        title: Meitei Mayek chapter title.
        title_en: English translation of chapter title.
        passages: List of ordered Passage objects.
        summary: Chapter synopsis.
        translation_en: Full English chapter translation if aligned.
        translation_provenance: Provenance attribution for chapter translation.
    """
    chapter_id: str
    book_id: str
    chapter_number: int
    title: str
    title_en: str
    passages: List[Passage] = field(default_factory=list)
    summary: Optional[str] = None
    translation_en: Optional[str] = None
    translation_provenance: Optional[str] = None

    def word_count(self) -> int:
        """Calculate total words across all passages."""
        return sum(p.word_count for p in self.passages)

    def character_count(self) -> int:
        """Calculate total characters across all passages."""
        return sum(p.character_count for p in self.passages)

    def full_text(self) -> str:
        """Assemble full chapter text from constituent passages."""
        return "\n\n".join(p.text for p in self.passages)

    def to_dict(self) -> Dict[str, Any]:
        """Convert chapter to serializable dictionary."""
        data = asdict(self)
        data["passages"] = [p.to_dict() if isinstance(p, Passage) else p for p in self.passages]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Chapter:
        """Construct Chapter from dictionary."""
        passages_raw = data.get("passages", [])
        passages = [
            Passage.from_dict(p) if isinstance(p, dict) else p
            for p in passages_raw
        ]
        return cls(
            chapter_id=data.get("chapter_id", ""),
            book_id=data.get("book_id", ""),
            chapter_number=int(data.get("chapter_number", 1)),
            title=data.get("title", ""),
            title_en=data.get("title_en", ""),
            passages=passages,
            summary=data.get("summary"),
            translation_en=data.get("translation_en"),
            translation_provenance=data.get("translation_provenance"),
        )


@dataclass
class BookCatalogRecord:
    """
    Bibliographic catalog record tracking publication, legal rights, and import status.

    Attributes:
        book_id: Unique book identifier (e.g. khamba_thoibi).
        title: Primary title in Meitei Mayek.
        title_en: English title / subtitle.
        author: Author, bard, or oral heritage attribution.
        language: Language specification (default: Meitei (Manipuri)).
        script: Script specification (default: Meitei Mayek).
        genre: Literary or folklore genre.
        description: Comprehensive thematic description.
        source: Physical archive, publisher, or institutional source.
        copyright: Copyright notice.
        rights_status: Legal access status (Public Domain, Creative Commons, etc.).
        import_status: Ingestion status (CATALOG_ONLY, PARTIALLY_IMPORTED, FULLY_IMPORTED).
        total_chapters: Total documented chapters in the work.
        imported_chapters: Number of chapters imported into local storage.
        total_passages: Number of passages imported.
        checksum_sha256: Cryptographic SHA-256 hash of imported source file.
        source_file: Local filename from which data was ingested.
        last_imported_at: ISO timestamp of last import.
    """
    book_id: str
    title: str
    title_en: str
    author: str
    language: str = "Meitei (Manipuri)"
    script: str = "Meitei Mayek"
    genre: str = "Literary Heritage"
    description: str = ""
    source: str = ""
    copyright: str = "Public Domain"
    rights_status: str = RightsStatus.PUBLIC_DOMAIN.value
    import_status: ImportStatus = ImportStatus.CATALOG_ONLY
    total_chapters: int = 0
    imported_chapters: int = 0
    total_passages: int = 0
    checksum_sha256: Optional[str] = None
    source_file: Optional[str] = None
    last_imported_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert catalog record to serializable dictionary."""
        data = asdict(self)
        if isinstance(self.import_status, ImportStatus):
            data["import_status"] = self.import_status.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BookCatalogRecord:
        """Construct BookCatalogRecord from dictionary."""
        status_val = data.get("import_status", ImportStatus.CATALOG_ONLY.value)
        if isinstance(status_val, ImportStatus):
            import_status = status_val
        else:
            try:
                import_status = ImportStatus(status_val)
            except ValueError:
                import_status = ImportStatus.CATALOG_ONLY

        return cls(
            book_id=data.get("book_id", ""),
            title=data.get("title", ""),
            title_en=data.get("title_en", ""),
            author=data.get("author", ""),
            language=data.get("language", "Meitei (Manipuri)"),
            script=data.get("script", "Meitei Mayek"),
            genre=data.get("genre", "Literary Heritage"),
            description=data.get("description", ""),
            source=data.get("source", ""),
            copyright=data.get("copyright", "Public Domain"),
            rights_status=data.get("rights_status", RightsStatus.PUBLIC_DOMAIN.value),
            import_status=import_status,
            total_chapters=int(data.get("total_chapters", 0)),
            imported_chapters=int(data.get("imported_chapters", 0)),
            total_passages=int(data.get("total_passages", 0)),
            checksum_sha256=data.get("checksum_sha256"),
            source_file=data.get("source_file"),
            last_imported_at=data.get("last_imported_at"),
        )


@dataclass
class ImportManifest:
    """
    Cryptographic import manifest recording provenance and file hashes.

    Attributes:
        manifest_id: Stable manifest identifier.
        book_id: Associated book identifier.
        source_file_path: Relative or absolute path to the imported file.
        file_format: Source format (txt, markdown, json, jsonl).
        sha256_checksum: Cryptographic SHA-256 digest of input file.
        imported_at: ISO timestamp of import execution.
        total_chapters: Number of imported chapters.
        total_passages: Number of segmented passages.
        total_word_count: Total words imported.
        importer: Attribution or identity of import agent.
        notes: Procedural notes or segmentation details.
    """
    manifest_id: str
    book_id: str
    source_file_path: str
    file_format: str
    sha256_checksum: str
    imported_at: str
    total_chapters: int
    total_passages: int
    total_word_count: int
    importer: str = "meitei-books-importer"
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert manifest to serializable dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ImportManifest:
        """Construct ImportManifest from dictionary."""
        return cls(
            manifest_id=data.get("manifest_id", ""),
            book_id=data.get("book_id", ""),
            source_file_path=data.get("source_file_path", ""),
            file_format=data.get("file_format", "json"),
            sha256_checksum=data.get("sha256_checksum", ""),
            imported_at=data.get("imported_at", ""),
            total_chapters=int(data.get("total_chapters", 0)),
            total_passages=int(data.get("total_passages", 0)),
            total_word_count=int(data.get("total_word_count", 0)),
            importer=data.get("importer", "meitei-books-importer"),
            notes=data.get("notes"),
        )


@dataclass
class VocabularyCandidate:
    """
    Lexical candidate extracted from book texts.

    Strict quarantine guarantee:
    Unreviewed vocabulary extracted computationally from book passages
    is marked UNVERIFIED and stored in candidate ledgers. It is NEVER
    merged into the authoritative dictionary until vetted.

    Attributes:
        candidate_id: Stable identifier (e.g. MEI-CAN-0000001).
        lemma: Headword candidate in Meitei Mayek.
        lemma_roman: Roman transliteration.
        book_id: Source book where candidate was observed.
        chapter_number: Chapter index.
        passage_id: Exact passage where candidate was attested.
        context_passage: Immediate sentence or passage context.
        frequency: Term frequency within the book.
        suggested_pos: Optional grammatical tag proposal.
        status: Verification status (strictly UNVERIFIED by default).
        extracted_at: ISO timestamp of extraction.
    """
    candidate_id: str
    lemma: str
    lemma_roman: str
    book_id: str
    chapter_number: int
    passage_id: str
    context_passage: str
    frequency: int = 1
    suggested_pos: Optional[str] = None
    status: str = "UNVERIFIED"
    extracted_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert candidate to serializable dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> VocabularyCandidate:
        """Construct VocabularyCandidate from dictionary."""
        return cls(
            candidate_id=data.get("candidate_id", ""),
            lemma=data.get("lemma", ""),
            lemma_roman=data.get("lemma_roman", ""),
            book_id=data.get("book_id", ""),
            chapter_number=int(data.get("chapter_number", 1)),
            passage_id=data.get("passage_id", ""),
            context_passage=data.get("context_passage", ""),
            frequency=int(data.get("frequency", 1)),
            suggested_pos=data.get("suggested_pos"),
            status=data.get("status", "UNVERIFIED"),
            extracted_at=data.get("extracted_at", ""),
        )


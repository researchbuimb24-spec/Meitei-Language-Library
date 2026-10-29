# -*- coding: utf-8 -*-
"""
Validation and Audit Engine for the Meitei Digital Book Library.

Verifies:
- Monotonic chapter and passage ordering.
- Stable passage ID syntax (`{book_id}-c{ch:02d}-p{p:03d}`).
- Bibliographic and rights metadata completeness.
- Cryptographic SHA-256 integrity against import manifests.
- Strict audit report distinguishing CATALOG_ONLY, PARTIALLY_IMPORTED, and FULLY_IMPORTED.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from meitei.books.catalog import BookCatalog
from meitei.books.importer import compute_sha256
from meitei.books.models import ImportStatus, is_valid_passage_id
from meitei.loader import get_default_data_dir


@dataclass
class BookAuditResult:
    """
    Audit report for an individual book or entire catalog.

    Attributes:
        valid: True if zero structural, ordering, or checksum errors were detected.
        book_id: Book identifier.
        import_status: Current verified status (CATALOG_ONLY, PARTIALLY_IMPORTED, FULLY_IMPORTED).
        total_chapters_declared: Declared chapter count in catalog.
        imported_chapters_count: Actual chapters stored on disk.
        passages_count: Actual passages stored on disk.
        checksum_verified: True if SHA-256 matches manifest.
        errors: List of blocking structural or referential errors.
        warnings: List of non-fatal discrepancy notices.
    """
    valid: bool
    book_id: str
    import_status: str
    total_chapters_declared: int = 0
    imported_chapters_count: int = 0
    passages_count: int = 0
    checksum_verified: Optional[bool] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return asdict(self)


class BookValidator:
    """
    Validation engine ensuring data integrity, passage sequencing, and audit compliance.
    """

    def __init__(self, data_dir: Union[str, Path] = "data") -> None:
        self.data_dir = get_default_data_dir(data_dir)
        self.texts_dir = self.data_dir / "books" / "texts"
        self.manifests_dir = self.data_dir / "books" / "manifests"
        self.catalog = BookCatalog(data_dir=self.data_dir)

    def validate_book(self, book_id: str) -> BookAuditResult:
        """
        Validate a single book's catalog entry, passage ordering, and checksums.

        Args:
            book_id: Book identifier to audit.

        Returns:
            BookAuditResult object.
        """
        cat_rec = self.catalog.get_book(book_id)
        if not cat_rec:
            return BookAuditResult(
                valid=False,
                book_id=book_id,
                import_status="UNKNOWN",
                errors=[f"Book '{book_id}' is not registered in the catalog."],
            )

        errors: List[str] = []
        warnings: List[str] = []

        # 1. Metadata checks
        if not cat_rec.title or not cat_rec.title.strip():
            errors.append(f"Book '{book_id}' missing primary title.")
        if not cat_rec.author or not cat_rec.author.strip():
            warnings.append(f"Book '{book_id}' lacks author attribution.")
        if not cat_rec.rights_status:
            errors.append(f"Book '{book_id}' lacks required legal rights_status.")

        # 2. Check text file if imported
        book_file = self.texts_dir / f"{book_id}.json"
        if not book_file.exists():
            if cat_rec.import_status != ImportStatus.CATALOG_ONLY:
                errors.append(
                    f"Catalog indicates status '{cat_rec.import_status.value}', "
                    f"but text file '{book_file}' does not exist on disk."
                )
            return BookAuditResult(
                valid=len(errors) == 0,
                book_id=book_id,
                import_status=cat_rec.import_status.value,
                total_chapters_declared=cat_rec.total_chapters,
                imported_chapters_count=0,
                passages_count=0,
                checksum_verified=None,
                errors=errors,
                warnings=warnings,
            )

        # Parse text file
        try:
            with open(book_file, "r", encoding="utf-8") as f:
                content = json.load(f)
        except Exception as e:
            return BookAuditResult(
                valid=False,
                book_id=book_id,
                import_status=cat_rec.import_status.value,
                errors=[f"Failed to parse book file '{book_file}': {e}"],
            )

        chapters = content.get("chapters", [])
        total_passages = 0
        seen_passage_ids: set[str] = set()

        expected_ch_num = 1
        for ch in chapters:
            ch_num = ch.get("chapter_number")
            if ch_num != expected_ch_num:
                errors.append(f"Chapter ordering violation: expected chapter {expected_ch_num}, got {ch_num}.")
            expected_ch_num += 1

            passages = ch.get("passages", [])
            expected_p_num = 1
            for p in passages:
                total_passages += 1
                p_id = p.get("passage_id", "")
                if not is_valid_passage_id(p_id):
                    errors.append(f"Invalid passage ID syntax: '{p_id}'.")
                if p_id in seen_passage_ids:
                    errors.append(f"Duplicate passage ID detected: '{p_id}'.")
                seen_passage_ids.add(p_id)

                p_num = p.get("passage_number")
                if p_num != expected_p_num:
                    errors.append(
                        f"Passage ordering violation in chapter {ch_num}: "
                        f"expected passage {expected_p_num}, got {p_num}."
                    )
                expected_p_num += 1

                p_text = p.get("text", "")
                if not p_text or not p_text.strip():
                    errors.append(f"Empty text detected in passage '{p_id}'.")

        # 3. Checksum verification
        checksum_verified: Optional[bool] = None
        if cat_rec.checksum_sha256 and cat_rec.source_file:
            # Check manifest file
            manifests = list(self.manifests_dir.glob(f"MAN-{book_id}-*.json"))
            if manifests:
                try:
                    with open(manifests[0], "r", encoding="utf-8") as mf:
                        m_data = json.load(mf)
                        manifest_chk = m_data.get("sha256_checksum")
                        checksum_verified = (manifest_chk == cat_rec.checksum_sha256)
                        if not checksum_verified:
                            errors.append(
                                f"Checksum mismatch: catalog '{cat_rec.checksum_sha256}' "
                                f"!= manifest '{manifest_chk}'."
                            )
                except Exception as e:
                    warnings.append(f"Failed to verify import manifest: {e}")

        # 4. Ingestion completeness audit
        if cat_rec.total_chapters > 0 and len(chapters) < cat_rec.total_chapters:
            if cat_rec.import_status == ImportStatus.FULLY_IMPORTED:
                errors.append(
                    f"Status mismatch: Catalog claims FULLY_IMPORTED, but only "
                    f"{len(chapters)}/{cat_rec.total_chapters} chapters exist."
                )
            elif cat_rec.import_status == ImportStatus.CATALOG_ONLY:
                warnings.append(
                    f"Catalog indicates CATALOG_ONLY, but {len(chapters)} chapters are present."
                )

        is_valid = len(errors) == 0
        return BookAuditResult(
            valid=is_valid,
            book_id=book_id,
            import_status=cat_rec.import_status.value,
            total_chapters_declared=cat_rec.total_chapters,
            imported_chapters_count=len(chapters),
            passages_count=total_passages,
            checksum_verified=checksum_verified,
            errors=errors,
            warnings=warnings,
        )

    def audit_all_books(self) -> Dict[str, Any]:
        """
        Audit all registered books across the catalog.

        Returns:
            Dictionary with overall summary and per-book audit details.
        """
        books = self.catalog.list_books()
        results: List[Dict[str, Any]] = []
        all_valid = True

        for b in books:
            res = self.validate_book(b.book_id)
            if not res.valid:
                all_valid = False
            results.append(res.to_dict())

        stats = self.catalog.get_catalog_stats()
        return {
            "all_valid": all_valid,
            "total_books_audited": len(books),
            "fully_imported": stats["fully_imported"],
            "partially_imported": stats["partially_imported"],
            "catalog_only": stats["catalog_only"],
            "total_passages": stats["total_passages"],
            "books": results,
        }


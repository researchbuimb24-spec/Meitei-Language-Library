# -*- coding: utf-8 -*-
"""
Bibliographic Book Catalog for the Meitei Digital Book Library.

Manages book registration, rights metadata, and honest tracking of ingestion
statuses (CATALOG_ONLY, PARTIALLY_IMPORTED, FULLY_IMPORTED).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from meitei.books.models import BookCatalogRecord, ImportStatus, RightsStatus
from meitei.loader import get_default_data_dir


DEFAULT_CATALOG_BOOKS: List[Dict[str, Any]] = [
    {
        "book_id": "khamba_thoibi",
        "title": "ꯈꯝꯕ ꯊꯣꯏꯕꯤ",
        "title_en": "Khamba Thoibi: The Epic of Moirang",
        "author": "Hijam Anganghal Singh (adapted from ancient Moirang Kangleirol oral folklore)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Epic Folklore / Narrative Poetry",
        "description": "The national epic of the Meitei people chronicling the legendary love, chivalric trials, and spiritual heroism of orphan youth Khuman Khamba and princess Thoibi of Moirang.",
        "source": "Moirang Kangleirol Epic Cycles & Manipuri Sahitya Parishad Folklore Archives",
        "copyright": "Public Domain (Traditional Meitei Epic Folklore and Oral Heritage)",
        "rights_status": RightsStatus.PUBLIC_DOMAIN.value,
        "import_status": ImportStatus.CATALOG_ONLY.value,
        "total_chapters": 7,
        "imported_chapters": 0,
        "total_passages": 0,
    },
    {
        "book_id": "phunga_wari",
        "title": "ꯃꯩꯇꯩ ꯐꯨꯡꯒꯥ ꯋꯥꯔꯤ",
        "title_en": "Meitei Phunga Wari: Hearth-Side Folktales of Manipur",
        "author": "Traditional Folklorists (Oral Heritage of Manipur)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Traditional Folktales & Moral Fables",
        "description": "Beloved oral folktales recited around the traditional domestic hearth (Phunga Lairu) during winter evenings across Meitei homes, including Pebet and Tapta.",
        "source": "Directorate of Language Planning & Manipuri Folklore Heritage Society",
        "copyright": "Public Domain (Traditional Cultural Expressions)",
        "rights_status": RightsStatus.TRADITIONAL_CULTURAL.value,
        "import_status": ImportStatus.CATALOG_ONLY.value,
        "total_chapters": 7,
        "imported_chapters": 0,
        "total_passages": 0,
    },
    {
        "book_id": "sana_leibak_chronicles",
        "title": "ꯁꯅꯥ ꯂꯩꯕꯥꯛ ꯃꯅꯤꯄꯨꯔ ꯄꯨꯋꯥꯔꯤ",
        "title_en": "The Golden Land: Chronicles, Puyas and Heritage of Manipur",
        "author": "Court Chroniclers and Maichous of Kangleipak",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Historical Chronicles & Cultural Philosophy",
        "description": "Historical chronicle synthesizing sovereign heritage, Kangla coronation rituals, and royal statecraft of ancient Manipur.",
        "source": "Kangla Palace Historical Archives & State Archives of Manipur",
        "copyright": "Public Domain (Historical Royal Heritage Documentation)",
        "rights_status": RightsStatus.PUBLIC_DOMAIN.value,
        "import_status": ImportStatus.CATALOG_ONLY.value,
        "total_chapters": 5,
        "imported_chapters": 0,
        "total_passages": 0,
    },
    {
        "book_id": "ramayana",
        "title": "ꯔꯥꯃꯥꯌꯟ",
        "title_en": "Ramayana: The Epic of Rama in Meitei Tradition",
        "author": "Angom Gopi & Classical Meitei Translators (reign of King Garibniwaz)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Religious Epic / Classical Meitei Translation",
        "description": "Classical 18th-century Meitei adaptation of the epic Ramayana translated during the religious renaissance of King Pamheiba.",
        "source": "Manipuri Sahitya Parishad Classical Text Archives",
        "copyright": "Public Domain (Classical 18th Century Translation)",
        "rights_status": RightsStatus.PUBLIC_DOMAIN.value,
        "import_status": ImportStatus.CATALOG_ONLY.value,
        "total_chapters": 6,
        "imported_chapters": 0,
        "total_passages": 0,
    },
    {
        "book_id": "mahabharata",
        "title": "ꯃꯍꯥꯚꯥꯔꯠ ꯑꯃꯁꯨꯡ ꯃꯅꯤꯄꯨꯔ",
        "title_en": "Mahabharata: The Great Epic and the Manipur Connection",
        "author": "Court Pandits of Manipur (adapted from Vyasa's epic tradition)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Epic Narrative & Genealogical Chronicle",
        "description": "Celebrated episodes linking the Mahabharata with ancient Manipur, including Arjuna's arrival, union with Chitrangada, and the heroism of Babruvahana.",
        "source": "Directorate of Art & Culture, Government of Manipur",
        "copyright": "Public Domain (Traditional Cultural Expressions)",
        "rights_status": RightsStatus.PUBLIC_DOMAIN.value,
        "import_status": ImportStatus.CATALOG_ONLY.value,
        "total_chapters": 6,
        "imported_chapters": 0,
        "total_passages": 0,
    },
    {
        "book_id": "numit_kappa",
        "title": "ꯅꯨꯃꯤꯠ ꯀꯥꯞꯄ",
        "title_en": "Numit Kappa: The Shooting of the Sun",
        "author": "Ancient Meitei Bards (Maichous of Kangleipak)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Archaic Puya / Solar Mythology & Ritual Poetry",
        "description": "One of the oldest documented literary and cosmological texts of the Meitei people, narrating how archer Khwai Nongchenbam heroically shot down one of two scorching suns.",
        "source": "National Manuscript Mission & Puya Preservation Archives",
        "copyright": "Public Domain (Ancient Meitei Puya Heritage)",
        "rights_status": RightsStatus.PUBLIC_DOMAIN.value,
        "import_status": ImportStatus.CATALOG_ONLY.value,
        "total_chapters": 5,
        "imported_chapters": 0,
        "total_passages": 0,
    },
    {
        "book_id": "chainarol",
        "title": "ꯆꯥꯏꯅꯔꯣꯜ",
        "title_en": "Chainarol: The Ancient Code of Chivalry and Warrior Duels",
        "author": "Ancient Maichous (Preservers of Martial Tradition)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Archaic Martial Puya / Chivalric Chronicles",
        "description": "Archaic martial puya detailing ethical duels, chivalric codes of honor, fair combat protocols, and warrior ethics in pre-colonial Manipur.",
        "source": "Manipur State Kala Akademi & Thang-Ta Cultural Archives",
        "copyright": "Public Domain (Ancient Meitei Martial Lore)",
        "rights_status": RightsStatus.PUBLIC_DOMAIN.value,
        "import_status": ImportStatus.CATALOG_ONLY.value,
        "total_chapters": 5,
        "imported_chapters": 0,
        "total_passages": 0,
    },
    {
        "book_id": "panthoibi_khonggul",
        "title": "ꯄꯥꯟꯊꯣꯏꯕꯤ ꯈꯣꯡꯒꯨꯜ",
        "title_en": "Panthoibi Khonggul: The Trail and Glory of Goddess Panthoibi",
        "author": "Ancient Meitei Seers (Sanamahi Religious Lore)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Sacred Puya / Mythological Romance & Divine Allegory",
        "description": "Sacred puya chronicling the fearless spirit, spiritual wanderings, and cosmic union of goddess Panthoibi and lord Nongpok Ningthou.",
        "source": "Sanamahi Lainingkol Heritage Preservation Center",
        "copyright": "Public Domain (Ancient Sanamahi Theological Text)",
        "rights_status": RightsStatus.PUBLIC_DOMAIN.value,
        "import_status": ImportStatus.CATALOG_ONLY.value,
        "total_chapters": 5,
        "imported_chapters": 0,
        "total_passages": 0,
    },
    {
        "book_id": "poireiton_khunthok",
        "title": "ꯄꯣꯏꯔꯩꯇꯣꯟ ꯈꯨꯟꯊꯣꯛ",
        "title_en": "Poireiton Khunthok: The Great Migration of King Poireiton",
        "author": "Ancient Chroniclers of the Luwang Dynasty",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Archaic Settlement Puya / Historical Geography",
        "description": "Ancient prose puya recording King Poireiton's pioneering civilizational migration from the netherworld Khamnung into the fertile valley of Manipur.",
        "source": "Manuscript Division, Manipur University Central Library",
        "copyright": "Public Domain (Archaic Meitei Settlement History)",
        "rights_status": RightsStatus.PUBLIC_DOMAIN.value,
        "import_status": ImportStatus.CATALOG_ONLY.value,
        "total_chapters": 5,
        "imported_chapters": 0,
        "total_passages": 0,
    },
    {
        "book_id": "pakhangba_laihui",
        "title": "ꯄꯥꯈꯪꯕ ꯂꯥꯏꯍꯨꯏ",
        "title_en": "Pakhangba Laihui: The Divine Chronicle of Sovereign Pakhangba",
        "author": "Royal Court Priests and Pandits of Kangleipak",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Theological Chronicle & Royal Genealogy",
        "description": "Sacred royal genealogy recording divine manifestations, royal coronation rituals, and cosmic origins of sovereign Ibudhou Pakhangba.",
        "source": "Govindaji Temple Royal Trust & Manipur State Archives",
        "copyright": "Public Domain (Sacred Royal Religious Chronicle)",
        "rights_status": RightsStatus.PUBLIC_DOMAIN.value,
        "import_status": ImportStatus.CATALOG_ONLY.value,
        "total_chapters": 5,
        "imported_chapters": 0,
        "total_passages": 0,
    },
]


class BookCatalog:
    """
    Catalog registry tracking bibliographic metadata and import status.
    """

    def __init__(self, data_dir: Union[str, Path] = "data") -> None:
        self.data_dir = get_default_data_dir(data_dir)
        self.catalog_file = self.data_dir / "books" / "catalog.json"
        self._records: Dict[str, BookCatalogRecord] = {}
        self._load()

    def _load(self) -> None:
        """Load catalog from disk or initialize default records."""
        if not self.catalog_file.exists():
            # Initialize with default catalog entries
            self.catalog_file.parent.mkdir(parents=True, exist_ok=True)
            self._records = {
                b["book_id"]: BookCatalogRecord.from_dict(b)
                for b in DEFAULT_CATALOG_BOOKS
            }
            self.save()
            return

        with open(self.catalog_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                items = data.get("books", []) if isinstance(data, dict) else data
                self._records = {
                    item["book_id"]: BookCatalogRecord.from_dict(item)
                    for item in items
                    if isinstance(item, dict) and "book_id" in item
                }
            except Exception:
                self._records = {}

    def save(self) -> None:
        """Persist catalog to disk."""
        self.catalog_file.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": "1.0",
            "description": "Meitei Language Library Digital Book Catalog",
            "books": [r.to_dict() for r in self._records.values()],
        }
        with open(self.catalog_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def list_books(
        self,
        status: Optional[Union[str, ImportStatus]] = None,
    ) -> List[BookCatalogRecord]:
        """
        List all registered books, optionally filtered by ImportStatus.

        Args:
            status: Optional status filter ('CATALOG_ONLY', 'PARTIALLY_IMPORTED', 'FULLY_IMPORTED').

        Returns:
            List of BookCatalogRecord objects.
        """
        records = list(self._records.values())
        if status is not None:
            status_val = status.value if isinstance(status, ImportStatus) else str(status).upper()
            records = [r for r in records if r.import_status.value == status_val]
        return sorted(records, key=lambda b: b.book_id)

    def get_book(self, book_id: str) -> Optional[BookCatalogRecord]:
        """Retrieve catalog record by book_id."""
        return self._records.get(book_id)

    def register_book(self, record: BookCatalogRecord) -> None:
        """Register or update a book catalog record."""
        self._records[record.book_id] = record
        self.save()

    def update_import_status(
        self,
        book_id: str,
        status: ImportStatus,
        imported_chapters: int,
        total_passages: int,
        checksum_sha256: Optional[str] = None,
        source_file: Optional[str] = None,
        imported_at: Optional[str] = None,
    ) -> Optional[BookCatalogRecord]:
        """Update the import progress and integrity checksum for a book."""
        rec = self.get_book(book_id)
        if not rec:
            return None
        rec.import_status = status
        rec.imported_chapters = imported_chapters
        rec.total_passages = total_passages
        if checksum_sha256:
            rec.checksum_sha256 = checksum_sha256
        if source_file:
            rec.source_file = source_file
        if imported_at:
            rec.last_imported_at = imported_at
        self.save()
        return rec

    def get_catalog_stats(self) -> Dict[str, Any]:
        """Compute statistical summary of catalog holdings and import completeness."""
        records = list(self._records.values())
        total = len(records)
        fully = sum(1 for r in records if r.import_status == ImportStatus.FULLY_IMPORTED)
        partially = sum(1 for r in records if r.import_status == ImportStatus.PARTIALLY_IMPORTED)
        catalog_only = sum(1 for r in records if r.import_status == ImportStatus.CATALOG_ONLY)
        total_passages = sum(r.total_passages for r in records)
        total_imported_ch = sum(r.imported_chapters for r in records)

        return {
            "total_books": total,
            "fully_imported": fully,
            "partially_imported": partially,
            "catalog_only": catalog_only,
            "total_imported_chapters": total_imported_ch,
            "total_passages": total_passages,
        }


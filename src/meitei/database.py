# -*- coding: utf-8 -*-
"""
Database layer for the Meitei Language Library (meitei).

Implements a clean, zero-external-dependency storage architecture:
1. SQLite Database: Indexed offline relational database for high-performance
   lookups, filtering, and linguistic provenance tracking.
2. JSON Lines (JSONL): Human-readable, diff-friendly, streaming file format
   for repository storage, collaborative editing, and version control.

All database operations use the standard library `sqlite3` and `json` modules.
"""

from __future__ import annotations

import json
import sqlite3
import unicodedata
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

from meitei.models import (
    BibliographicSource,
    Entry,
    ExampleSentence,
    PartOfSpeech,
    ProvenanceRecord,
    Sense,
    VerificationStatus,
)


# SQLite Schema DDL
SCHEMA_DDL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT,
    editor_or_translator TEXT,
    year INTEGER,
    source_type TEXT NOT NULL,
    publisher TEXT,
    description TEXT,
    url_or_doi TEXT,
    metadata_json TEXT
);

CREATE TABLE IF NOT EXISTS entries (
    entry_id TEXT PRIMARY KEY,
    headword_meitei TEXT NOT NULL,
    headword_roman TEXT NOT NULL,
    headword_bengali TEXT,
    phonetic_ipa TEXT,
    etymology TEXT,
    variants_json TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS senses (
    sense_id TEXT PRIMARY KEY,
    entry_id TEXT NOT NULL,
    definition_en TEXT NOT NULL,
    definition_mni TEXT,
    part_of_speech TEXT NOT NULL,
    domain TEXT,
    examples_json TEXT,
    notes TEXT,
    FOREIGN KEY (entry_id) REFERENCES entries(entry_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS provenance (
    provenance_id TEXT PRIMARY KEY,
    entry_id TEXT NOT NULL,
    source_id TEXT NOT NULL,
    attestation_type TEXT NOT NULL,
    attestation_reference TEXT,
    attested_date TEXT,
    verification_status TEXT NOT NULL,
    verified_by TEXT,
    verification_notes TEXT,
    FOREIGN KEY (entry_id) REFERENCES entries(entry_id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES sources(source_id)
);

-- Fast lookup indexes
CREATE INDEX IF NOT EXISTS idx_entries_meitei ON entries(headword_meitei);
CREATE INDEX IF NOT EXISTS idx_entries_roman ON entries(headword_roman);
CREATE INDEX IF NOT EXISTS idx_entries_bengali ON entries(headword_bengali);
CREATE INDEX IF NOT EXISTS idx_senses_entry ON senses(entry_id);
CREATE INDEX IF NOT EXISTS idx_senses_pos ON senses(part_of_speech);
CREATE INDEX IF NOT EXISTS idx_senses_domain ON senses(domain);
CREATE INDEX IF NOT EXISTS idx_prov_entry ON provenance(entry_id);
CREATE INDEX IF NOT EXISTS idx_prov_source ON provenance(source_id);
CREATE INDEX IF NOT EXISTS idx_prov_status ON provenance(verification_status);
"""


class MeiteiDatabase:
    """
    Offline SQLite database manager for Meitei language records.

    Provides high-performance indexing, relational provenance tracking,
    and bi-directional streaming conversion with JSON Lines (JSONL).
    """

    def __init__(self, db_path: Optional[Union[str, Path]] = None) -> None:
        """
        Initialize the database connection and schema.

        Args:
            db_path: Path to the SQLite database file, or None / ':memory:' for an in-memory database.
        """
        if db_path is None or str(db_path) == ":memory:":
            self._db_path = ":memory:"
        else:
            self._db_path = str(db_path)
            Path(self._db_path).parent.mkdir(parents=True, exist_ok=True)

        self._conn = sqlite3.connect(self._db_path)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        """Execute DDL statements to set up tables and indexes."""
        with self._conn:
            self._conn.executescript(SCHEMA_DDL)

    def close(self) -> None:
        """Close the database connection."""
        if self._conn:
            self._conn.close()

    def __enter__(self) -> MeiteiDatabase:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    @property
    def db_path(self) -> str:
        """Return the database file path or ':memory:'."""
        return self._db_path

    # =========================================================================
    # Sources Operations
    # =========================================================================

    def upsert_source(self, source: BibliographicSource) -> None:
        """Insert or replace a bibliographic source record."""
        query = """
        INSERT OR REPLACE INTO sources (
            source_id, title, author, editor_or_translator, year,
            source_type, publisher, description, url_or_doi, metadata_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        meta_json = json.dumps(source.metadata, ensure_ascii=False) if source.metadata else "{}"
        with self._conn:
            self._conn.execute(query, (
                source.source_id,
                source.title,
                source.author,
                source.editor_or_translator,
                source.year,
                source.source_type,
                source.publisher,
                source.description,
                source.url_or_doi,
                meta_json,
            ))

    def get_source(self, source_id: str) -> Optional[BibliographicSource]:
        """Retrieve a bibliographic source by its identifier."""
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM sources WHERE source_id = ?", (source_id.strip(),))
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_source(row)

    def list_sources(self) -> List[BibliographicSource]:
        """List all bibliographic sources registered in the database."""
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM sources ORDER BY source_id ASC")
        return [self._row_to_source(row) for row in cur.fetchall()]

    def count_sources(self) -> int:
        """Return total count of bibliographic sources."""
        cur = self._conn.cursor()
        cur.execute("SELECT COUNT(*) FROM sources")
        return cur.fetchone()[0]

    def _row_to_source(self, row: sqlite3.Row) -> BibliographicSource:
        meta = json.loads(row["metadata_json"]) if row["metadata_json"] else {}
        return BibliographicSource(
            source_id=row["source_id"],
            title=row["title"],
            author=row["author"],
            editor_or_translator=row["editor_or_translator"],
            year=row["year"],
            source_type=row["source_type"],
            publisher=row["publisher"],
            description=row["description"],
            url_or_doi=row["url_or_doi"],
            metadata=meta,
        )

    # =========================================================================
    # Entries Operations
    # =========================================================================

    def upsert_entry(self, entry: Entry) -> None:
        """
        Insert or update a lexical entry and its associated senses and provenance records.

        Executes atomically within a single SQLite transaction.
        """
        with self._conn:
            # 1. Upsert entry record
            self._conn.execute(
                """
                INSERT OR REPLACE INTO entries (
                    entry_id, headword_meitei, headword_roman, headword_bengali,
                    phonetic_ipa, etymology, variants_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry.entry_id,
                    entry.headword_meitei,
                    entry.headword_roman,
                    entry.headword_bengali,
                    entry.phonetic_ipa,
                    entry.etymology,
                    json.dumps(entry.variants, ensure_ascii=False),
                    entry.created_at,
                    entry.updated_at,
                ),
            )

            # 2. Delete and re-insert senses
            self._conn.execute("DELETE FROM senses WHERE entry_id = ?", (entry.entry_id,))
            for sense in entry.senses:
                ex_json = json.dumps([ex.to_dict() for ex in sense.examples], ensure_ascii=False)
                self._conn.execute(
                    """
                    INSERT INTO senses (
                        sense_id, entry_id, definition_en, definition_mni,
                        part_of_speech, domain, examples_json, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        sense.sense_id,
                        entry.entry_id,
                        sense.definition_en,
                        sense.definition_mni,
                        sense.part_of_speech.value,
                        sense.domain,
                        ex_json,
                        sense.notes,
                    ),
                )

            # 3. Delete and re-insert provenance records
            self._conn.execute("DELETE FROM provenance WHERE entry_id = ?", (entry.entry_id,))
            for prov in entry.provenance:
                self._conn.execute(
                    """
                    INSERT INTO provenance (
                        provenance_id, entry_id, source_id, attestation_type,
                        attestation_reference, attested_date, verification_status,
                        verified_by, verification_notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        prov.provenance_id,
                        entry.entry_id,
                        prov.source_id,
                        prov.attestation_type,
                        prov.attestation_reference,
                        prov.attested_date,
                        prov.verification_status.value,
                        prov.verified_by,
                        prov.verification_notes,
                    ),
                )

    def get_entry(self, entry_id: str) -> Optional[Entry]:
        """Retrieve an entry by its ID, with fully populated senses and provenance."""
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM entries WHERE entry_id = ?", (entry_id.strip(),))
        row = cur.fetchone()
        if not row:
            return None
        return self._populate_entry(row)

    def lookup_headword(self, word: str) -> List[Entry]:
        """
        Look up entries matching a given headword in Meitei Mayek, Roman, or Bengali script.
        """
        w = unicodedata.normalize("NFC", word.strip())
        w_lower = w.lower()

        cur = self._conn.cursor()
        query = """
        SELECT * FROM entries
        WHERE headword_meitei = ?
           OR LOWER(headword_roman) = ?
           OR headword_bengali = ?
        ORDER BY entry_id ASC
        """
        cur.execute(query, (w, w_lower, w))
        return [self._populate_entry(r) for r in cur.fetchall()]

    def search_entries(self, query: str, limit: int = 50) -> List[Entry]:
        """
        Search entries across headwords (Mayek, Roman, Bengali) and sense definitions.
        """
        q = unicodedata.normalize("NFC", query.strip())
        if not q:
            return []
        q_like = f"%{q}%"
        q_lower_like = f"%{q.lower()}%"

        cur = self._conn.cursor()
        sql = """
        SELECT DISTINCT e.*
        FROM entries e
        LEFT JOIN senses s ON e.entry_id = s.entry_id
        WHERE e.headword_meitei LIKE ?
           OR LOWER(e.headword_roman) LIKE ?
           OR e.headword_bengali LIKE ?
           OR LOWER(s.definition_en) LIKE ?
           OR s.definition_mni LIKE ?
        ORDER BY e.entry_id ASC
        LIMIT ?
        """
        cur.execute(sql, (q_like, q_lower_like, q_like, q_lower_like, q_like, limit))
        return [self._populate_entry(r) for r in cur.fetchall()]

    def list_entries(self, offset: int = 0, limit: int = 100) -> List[Entry]:
        """Return a paginated list of entries."""
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM entries ORDER BY entry_id ASC LIMIT ? OFFSET ?", (limit, offset))
        return [self._populate_entry(r) for r in cur.fetchall()]

    def delete_entry(self, entry_id: str) -> bool:
        """Delete an entry and cascade-delete its senses and provenance."""
        with self._conn:
            cur = self._conn.execute("DELETE FROM entries WHERE entry_id = ?", (entry_id.strip(),))
            return cur.rowcount > 0

    def count_entries(self) -> int:
        """Return total count of lexical entries."""
        cur = self._conn.cursor()
        cur.execute("SELECT COUNT(*) FROM entries")
        return cur.fetchone()[0]

    def count_senses(self) -> int:
        """Return total count of senses across all entries."""
        cur = self._conn.cursor()
        cur.execute("SELECT COUNT(*) FROM senses")
        return cur.fetchone()[0]

    def count_provenance(self) -> int:
        """Return total count of provenance records."""
        cur = self._conn.cursor()
        cur.execute("SELECT COUNT(*) FROM provenance")
        return cur.fetchone()[0]

    def get_verification_breakdown(self) -> Dict[str, int]:
        """Return counts of provenance records grouped by verification status."""
        cur = self._conn.cursor()
        cur.execute(
            """
            SELECT verification_status, COUNT(*) as cnt
            FROM provenance
            GROUP BY verification_status
            """
        )
        return {row["verification_status"]: row["cnt"] for row in cur.fetchall()}

    def get_stats(self) -> Dict[str, Any]:
        """Return comprehensive repository and database statistics."""
        return {
            "entries_count": self.count_entries(),
            "senses_count": self.count_senses(),
            "sources_count": self.count_sources(),
            "provenance_count": self.count_provenance(),
            "verification_breakdown": self.get_verification_breakdown(),
            "db_path": self._db_path,
        }

    def _populate_entry(self, row: sqlite3.Row) -> Entry:
        entry_id = row["entry_id"]
        cur = self._conn.cursor()

        # Load Senses
        cur.execute("SELECT * FROM senses WHERE entry_id = ? ORDER BY sense_id ASC", (entry_id,))
        senses: List[Sense] = []
        for s_row in cur.fetchall():
            ex_raw = json.loads(s_row["examples_json"]) if s_row["examples_json"] else []
            examples = [ExampleSentence.from_dict(ex) for ex in ex_raw]
            senses.append(
                Sense(
                    sense_id=s_row["sense_id"],
                    definition_en=s_row["definition_en"],
                    definition_mni=s_row["definition_mni"],
                    part_of_speech=s_row["part_of_speech"],
                    domain=s_row["domain"],
                    examples=examples,
                    notes=s_row["notes"],
                )
            )

        # Load Provenance
        cur.execute("SELECT * FROM provenance WHERE entry_id = ? ORDER BY provenance_id ASC", (entry_id,))
        provenance: List[ProvenanceRecord] = []
        for p_row in cur.fetchall():
            provenance.append(
                ProvenanceRecord(
                    provenance_id=p_row["provenance_id"],
                    source_id=p_row["source_id"],
                    attestation_type=p_row["attestation_type"],
                    attestation_reference=p_row["attestation_reference"],
                    attested_date=p_row["attested_date"],
                    verification_status=p_row["verification_status"],
                    verified_by=p_row["verified_by"],
                    verification_notes=p_row["verification_notes"],
                )
            )

        variants = json.loads(row["variants_json"]) if row["variants_json"] else []

        return Entry(
            entry_id=entry_id,
            headword_meitei=row["headword_meitei"],
            headword_roman=row["headword_roman"],
            headword_bengali=row["headword_bengali"],
            phonetic_ipa=row["phonetic_ipa"],
            senses=senses,
            provenance=provenance,
            etymology=row["etymology"],
            variants=variants,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    # =========================================================================
    # JSONL Streaming Import & Export Architecture
    # =========================================================================

    def import_entries_from_jsonl(self, jsonl_path: Union[str, Path]) -> int:
        """
        Streamingly ingest entries from a JSON Lines (.jsonl) file into the database.

        Reads line by line to support large datasets with minimal memory footprint.
        Inserts all records in a single database transaction.

        Returns:
            The number of entries successfully imported.
        """
        p = Path(jsonl_path)
        if not p.is_file():
            raise FileNotFoundError(f"JSONL file not found: {jsonl_path}")

        count = 0
        with open(p, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                clean_line = line.strip()
                if not clean_line:
                    continue
                try:
                    data = json.loads(clean_line)
                    entry = Entry.from_dict(data)
                    self.upsert_entry(entry)
                    count += 1
                except Exception as e:
                    raise ValueError(f"Failed to parse JSONL line {line_no} in {p}: {e}") from e

        return count

    def export_entries_to_jsonl(self, jsonl_path: Union[str, Path]) -> int:
        """
        Streamingly export all entries from the SQLite database to a JSON Lines (.jsonl) file.

        Each entry is serialized as a single, newline-terminated JSON object.

        Returns:
            The number of entries exported.
        """
        p = Path(jsonl_path)
        p.parent.mkdir(parents=True, exist_ok=True)

        cur = self._conn.cursor()
        cur.execute("SELECT entry_id FROM entries ORDER BY entry_id ASC")
        entry_ids = [row[0] for row in cur.fetchall()]

        count = 0
        with open(p, "w", encoding="utf-8") as f:
            for eid in entry_ids:
                entry = self.get_entry(eid)
                if entry:
                    f.write(entry.to_json() + "\n")
                    count += 1

        return count

    def import_sources_from_jsonl(self, jsonl_path: Union[str, Path]) -> int:
        """Streamingly ingest bibliographic sources from a JSON Lines (.jsonl) file."""
        p = Path(jsonl_path)
        if not p.is_file():
            raise FileNotFoundError(f"Sources JSONL file not found: {jsonl_path}")

        count = 0
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line:
                    continue
                data = json.loads(clean_line)
                source = BibliographicSource.from_dict(data)
                self.upsert_source(source)
                count += 1
        return count

    def export_sources_to_jsonl(self, jsonl_path: Union[str, Path]) -> int:
        """Streamingly export all bibliographic sources to a JSON Lines (.jsonl) file."""
        p = Path(jsonl_path)
        p.parent.mkdir(parents=True, exist_ok=True)

        sources = self.list_sources()
        with open(p, "w", encoding="utf-8") as f:
            for s in sources:
                f.write(json.dumps(s.to_dict(), ensure_ascii=False) + "\n")
        return len(sources)


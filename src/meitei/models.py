# -*- coding: utf-8 -*-
"""
Typed data models for the Meitei Language Library (meitei).

This module defines the core architectural data models for dictionary entries,
lexical senses, bibliographic sources, and provenance records.

Linguistic Provenance & Attestation Model:
    A foundational principle of this library is the rigorous distinction
    between:
    1. Historical Source Attestation: Lexical forms, archaic morphology, or
       orthographic variants documented in ancient manuscripts (Puyas),
       royal chronicles (Cheitharol Kumbaba), or classical literature.
    2. Contemporary Native-Speaker Verification: Living language forms actively
       used, confirmed, and recognized by modern native speakers of Meiteilon
       in Manipur, conforming to modern orthographic standards.

All models adhere to Python 3.9+ typing and require zero runtime dependencies.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class VerificationStatus(str, Enum):
    """
    Provenance verification status of an entry or sense.

    - UNVERIFIED: Ingested from raw field notes or preliminary text without
      formal editorial or native-speaker vetting.
    - HISTORICAL_ATTESTED: Attested in historical manuscripts, classical Puyas,
      royal chronicles, or early lexicography. May preserve archaic phonology
      or vocabulary not in contemporary active use.
    - CONTEMPORARY_VERIFIED: Confirmed in active, contemporary usage by native
      speakers of Meiteilon in Manipur, adhering to modern orthography.
    - BOTH: Continuous linguistic lineage; attested in historical sources and
      actively confirmed in contemporary vernacular speech.
    - DISPUTED: Competing orthographic traditions, unresolved dialectal variation,
      or debated semantic shifts between archaic texts and modern usage.
    """
    UNVERIFIED = "unverified"
    HISTORICAL_ATTESTED = "historical_attested"
    CONTEMPORARY_VERIFIED = "contemporary_verified"
    BOTH = "both"
    DISPUTED = "disputed"


class ScriptType(str, Enum):
    """
    Writing systems used for the Meitei language.

    - MEITEI_MAYEK: The official, indigenous writing system of Manipur
      (Unicode blocks U+ABC0-U+ABFF and extensions U+AAE0-U+AAFF).
    - BENGALI: Eastern Nagari / Bengali-Assamese script historically utilized
      in Manipur from the 18th century until the revitalization of Meitei Mayek.
    - LATIN: Standard Latin Romanization used in international linguistics,
      digital communication, and academic phonology.
    """
    MEITEI_MAYEK = "meitei_mayek"
    BENGALI = "bengali"
    LATIN = "latin"


class PartOfSpeech(str, Enum):
    """Grammatical categories in Meitei grammar."""
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    POSTPOSITION = "postposition"
    CONJUNCTION = "conjunction"
    INTERJECTION = "interjection"
    CLASSIFIER = "classifier"
    NUMERAL = "numeral"
    PREFIX = "prefix"
    SUFFIX = "suffix"
    PARTICLE = "particle"
    OTHER = "other"


@dataclass
class ExampleSentence:
    """An attested or verified example sentence demonstrating usage."""
    meitei: str
    roman: str
    english: str
    bengali: Optional[str] = None
    source_ref: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ExampleSentence:
        return cls(
            meitei=str(data.get("meitei", "")),
            roman=str(data.get("roman", "")),
            english=str(data.get("english", "")),
            bengali=data.get("bengali"),
            source_ref=data.get("source_ref"),
        )


@dataclass
class BibliographicSource:
    """
    A documented source providing historical or contemporary attestation.

    Sources may include classical Puyas (e.g. Numit Kappa, Poireiton Khunthok),
    royal chronicles (Cheitharol Kumbaba), modern dictionaries, academic corpora,
    or recorded native-speaker fieldwork sessions.
    """
    source_id: str
    title: str
    author: Optional[str] = None
    editor_or_translator: Optional[str] = None
    year: Optional[int] = None
    source_type: str = "puya"  # puya, chronicle, dictionary, fieldwork, corpus
    publisher: Optional[str] = None
    description: Optional[str] = None
    url_or_doi: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BibliographicSource:
        return cls(
            source_id=str(data.get("source_id", "")),
            title=str(data.get("title", "")),
            author=data.get("author"),
            editor_or_translator=data.get("editor_or_translator"),
            year=data.get("year"),
            source_type=str(data.get("source_type", "puya")),
            publisher=data.get("publisher"),
            description=data.get("description"),
            url_or_doi=data.get("url_or_doi"),
            metadata=data.get("metadata", {}) or {},
        )

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass
class ProvenanceRecord:
    """
    Traceable evidence supporting a lexical entry, sense, or reading.

    Explicitly links a word or sense to either a historical source citation
    or a contemporary native-speaker verification session.
    """
    provenance_id: str
    source_id: str
    attestation_type: str = "historical_attestation"  # historical_attestation, contemporary_fieldwork, editorial_review
    attestation_reference: Optional[str] = None  # e.g., "Folio 4b", "Page 112", "Speaker ID MNI-002"
    attested_date: Optional[str] = None
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    verified_by: Optional[str] = None  # Linguist or verified reviewer identifier
    verification_notes: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.verification_status, str):
            self.verification_status = VerificationStatus(self.verification_status)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["verification_status"] = self.verification_status.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProvenanceRecord:
        raw_status = data.get("verification_status", VerificationStatus.UNVERIFIED.value)
        try:
            status = VerificationStatus(raw_status)
        except ValueError:
            status = VerificationStatus.UNVERIFIED

        return cls(
            provenance_id=str(data.get("provenance_id", "")),
            source_id=str(data.get("source_id", "")),
            attestation_type=str(data.get("attestation_type", "historical_attestation")),
            attestation_reference=data.get("attestation_reference"),
            attested_date=data.get("attested_date"),
            verification_status=status,
            verified_by=data.get("verified_by"),
            verification_notes=data.get("verification_notes"),
        )

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass
class Sense:
    """A semantic definition belonging to an entry."""
    sense_id: str
    definition_en: str
    definition_mni: Optional[str] = None  # Meitei Mayek definition
    part_of_speech: PartOfSpeech = PartOfSpeech.NOUN
    domain: Optional[str] = None  # flora, fauna, agriculture, ritual, daily
    examples: List[ExampleSentence] = field(default_factory=list)
    notes: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.part_of_speech, str):
            try:
                self.part_of_speech = PartOfSpeech(self.part_of_speech)
            except ValueError:
                self.part_of_speech = PartOfSpeech.OTHER

        # Normalize examples list
        normalized_examples: List[ExampleSentence] = []
        for ex in self.examples:
            if isinstance(ex, dict):
                normalized_examples.append(ExampleSentence.from_dict(ex))
            elif isinstance(ex, ExampleSentence):
                normalized_examples.append(ex)
        self.examples = normalized_examples

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sense_id": self.sense_id,
            "definition_en": self.definition_en,
            "definition_mni": self.definition_mni,
            "part_of_speech": self.part_of_speech.value,
            "domain": self.domain,
            "examples": [ex.to_dict() for ex in self.examples],
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Sense:
        raw_pos = data.get("part_of_speech", PartOfSpeech.NOUN.value)
        try:
            pos = PartOfSpeech(raw_pos)
        except ValueError:
            pos = PartOfSpeech.OTHER

        raw_examples = data.get("examples", []) or []
        examples = [
            ExampleSentence.from_dict(e) if isinstance(e, dict) else e
            for e in raw_examples
        ]

        return cls(
            sense_id=str(data.get("sense_id", "")),
            definition_en=str(data.get("definition_en", "")),
            definition_mni=data.get("definition_mni"),
            part_of_speech=pos,
            domain=data.get("domain"),
            examples=examples,
            notes=data.get("notes"),
        )

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass
class Entry:
    """
    A comprehensive lexical entry in the Meitei dictionary.

    Represents a headword across Meitei Mayek, Roman transliteration, and
    historical Bengali script, complete with senses, provenance records,
    and morphological variants.
    """
    entry_id: str
    headword_meitei: str  # Meitei Mayek script (e.g. ꯃꯤ)
    headword_roman: str   # Romanized transliteration (e.g. mi)
    headword_bengali: Optional[str] = None  # Bengali script (e.g. মী)
    phonetic_ipa: Optional[str] = None
    senses: List[Sense] = field(default_factory=list)
    provenance: List[ProvenanceRecord] = field(default_factory=list)
    etymology: Optional[str] = None
    variants: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        # Normalize senses
        normalized_senses: List[Sense] = []
        for s in self.senses:
            if isinstance(s, dict):
                normalized_senses.append(Sense.from_dict(s))
            elif isinstance(s, Sense):
                normalized_senses.append(s)
        self.senses = normalized_senses

        # Normalize provenance
        normalized_prov: List[ProvenanceRecord] = []
        for p in self.provenance:
            if isinstance(p, dict):
                normalized_prov.append(ProvenanceRecord.from_dict(p))
            elif isinstance(p, ProvenanceRecord):
                normalized_prov.append(p)
        self.provenance = normalized_prov

        now_iso = datetime.now(timezone.utc).isoformat()
        if not self.created_at:
            self.created_at = now_iso
        if not self.updated_at:
            self.updated_at = now_iso

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "headword_meitei": self.headword_meitei,
            "headword_roman": self.headword_roman,
            "headword_bengali": self.headword_bengali,
            "phonetic_ipa": self.phonetic_ipa,
            "senses": [s.to_dict() for s in self.senses],
            "provenance": [p.to_dict() for p in self.provenance],
            "etymology": self.etymology,
            "variants": list(self.variants),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Entry:
        senses = [
            Sense.from_dict(s) if isinstance(s, dict) else s
            for s in data.get("senses", []) or []
        ]
        provenance = [
            ProvenanceRecord.from_dict(p) if isinstance(p, dict) else p
            for p in data.get("provenance", []) or []
        ]
        return cls(
            entry_id=str(data.get("entry_id", "")),
            headword_meitei=str(data.get("headword_meitei", "")),
            headword_roman=str(data.get("headword_roman", "")),
            headword_bengali=data.get("headword_bengali"),
            phonetic_ipa=data.get("phonetic_ipa"),
            senses=senses,
            provenance=provenance,
            etymology=data.get("etymology"),
            variants=list(data.get("variants", []) or []),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def to_json(self) -> str:
        """Serialize entry to a compact single-line JSON string (suitable for JSONL)."""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> Entry:
        """Deserialize entry from a JSON string."""
        return cls.from_dict(json.loads(json_str))

    def get_primary_definition(self) -> str:
        """Return the primary English definition from the first sense, if available."""
        if self.senses:
            return self.senses[0].definition_en
        return ""

    def get_verification_status(self) -> VerificationStatus:
        """
        Derive the aggregate verification status of the entry.

        If any provenance record indicates BOTH, returns BOTH.
        If both HISTORICAL_ATTESTED and CONTEMPORARY_VERIFIED records exist, returns BOTH.
        Otherwise returns the highest specific verification status recorded.
        """
        if not self.provenance:
            return VerificationStatus.UNVERIFIED

        statuses = {p.verification_status for p in self.provenance}
        if VerificationStatus.BOTH in statuses:
            return VerificationStatus.BOTH
        if (
            VerificationStatus.HISTORICAL_ATTESTED in statuses
            and VerificationStatus.CONTEMPORARY_VERIFIED in statuses
        ):
            return VerificationStatus.BOTH
        if VerificationStatus.CONTEMPORARY_VERIFIED in statuses:
            return VerificationStatus.CONTEMPORARY_VERIFIED
        if VerificationStatus.HISTORICAL_ATTESTED in statuses:
            return VerificationStatus.HISTORICAL_ATTESTED
        if VerificationStatus.DISPUTED in statuses:
            return VerificationStatus.DISPUTED
        return VerificationStatus.UNVERIFIED

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)


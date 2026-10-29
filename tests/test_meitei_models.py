# -*- coding: utf-8 -*-
"""Unit tests for meitei.models."""

import json
import pytest

from meitei.models import (
    BibliographicSource,
    Entry,
    ExampleSentence,
    PartOfSpeech,
    ProvenanceRecord,
    ScriptType,
    Sense,
    VerificationStatus,
)


def test_verification_status_and_script_enums():
    assert VerificationStatus.UNVERIFIED.value == "unverified"
    assert VerificationStatus.HISTORICAL_ATTESTED.value == "historical_attested"
    assert VerificationStatus.CONTEMPORARY_VERIFIED.value == "contemporary_verified"
    assert VerificationStatus.BOTH.value == "both"
    assert VerificationStatus.DISPUTED.value == "disputed"

    assert ScriptType.MEITEI_MAYEK.value == "meitei_mayek"
    assert ScriptType.BENGALI.value == "bengali"
    assert ScriptType.LATIN.value == "latin"

    assert PartOfSpeech.NOUN.value == "noun"
    assert PartOfSpeech.VERB.value == "verb"


def test_bibliographic_source_creation_and_dict():
    source = BibliographicSource(
        source_id="src_numit_kappa",
        title="Numit Kappa: The Ancient Sun-Shooting Puya",
        author="Ancient Meitei Scholars",
        year=1500,
        source_type="puya",
        description="Classical cosmological puya recording the two suns myth.",
        metadata={"century": "15th or earlier", "manuscript_type": "handwritten_puya"},
    )

    # Test attributes and dict-like access
    assert source.source_id == "src_numit_kappa"
    assert source["title"] == "Numit Kappa: The Ancient Sun-Shooting Puya"
    assert source.get("year") == 1500
    assert source.get("nonexistent", "default") == "default"

    # Serialization
    d = source.to_dict()
    assert d["source_id"] == "src_numit_kappa"
    assert d["metadata"]["century"] == "15th or earlier"

    # Deserialization
    restored = BibliographicSource.from_dict(d)
    assert restored.source_id == source.source_id
    assert restored.title == source.title
    assert restored.year == source.year
    assert restored.metadata == source.metadata


def test_provenance_record():
    p = ProvenanceRecord(
        provenance_id="prov_001",
        source_id="src_cheitharol_kumbaba",
        attestation_type="historical_attestation",
        attestation_reference="Page 45, entry for year 1604",
        verification_status=VerificationStatus.HISTORICAL_ATTESTED,
        verified_by="Researcher-01",
        verification_notes="Confirmed in Royal Chronicle manuscript.",
    )

    assert p.verification_status == VerificationStatus.HISTORICAL_ATTESTED
    assert p["attestation_reference"] == "Page 45, entry for year 1604"

    d = p.to_dict()
    assert d["verification_status"] == "historical_attested"

    restored = ProvenanceRecord.from_dict(d)
    assert restored.provenance_id == "prov_001"
    assert restored.verification_status == VerificationStatus.HISTORICAL_ATTESTED


def test_sense_and_example_sentence():
    ex = ExampleSentence(
        meitei="ꯏꯁꯤꯡ ꯊꯛꯎ꯫",
        roman="Ising thak-u.",
        english="Drink water.",
        bengali="ঈশিং থকউ।",
    )
    assert ex.meitei == "ꯏꯁꯤꯡ ꯊꯛꯎ꯫"

    sense = Sense(
        sense_id="sense_001",
        definition_en="Water (liquid necessary for life)",
        definition_mni="ꯏꯁꯤꯡ",
        part_of_speech=PartOfSpeech.NOUN,
        domain="nature",
        examples=[ex],
        notes="Universal liquid substance.",
    )

    assert sense.part_of_speech == PartOfSpeech.NOUN
    assert len(sense.examples) == 1
    assert sense["definition_en"] == "Water (liquid necessary for life)"

    d = sense.to_dict()
    assert d["part_of_speech"] == "noun"
    assert d["examples"][0]["meitei"] == "ꯏꯁꯤꯡ ꯊꯛꯎ꯫"

    restored = Sense.from_dict(d)
    assert restored.sense_id == "sense_001"
    assert len(restored.examples) == 1
    assert restored.examples[0].roman == "Ising thak-u."


def test_entry_lifecycle_and_verification_status():
    source_puya = BibliographicSource(
        source_id="src_puya_01",
        title="Ancient Chronicle",
        source_type="puya",
    )
    source_modern = BibliographicSource(
        source_id="src_fieldwork_01",
        title="Imphal Valley Fieldwork 2026",
        source_type="fieldwork",
    )

    prov_hist = ProvenanceRecord(
        provenance_id="prov_h_01",
        source_id="src_puya_01",
        attestation_type="historical_attestation",
        verification_status=VerificationStatus.HISTORICAL_ATTESTED,
    )
    prov_contemp = ProvenanceRecord(
        provenance_id="prov_c_01",
        source_id="src_fieldwork_01",
        attestation_type="contemporary_fieldwork",
        verification_status=VerificationStatus.CONTEMPORARY_VERIFIED,
    )

    sense = Sense(
        sense_id="sense_sing_01",
        definition_en="Firewood, timber",
        definition_mni="ꯁꯤꯡ",
        part_of_speech=PartOfSpeech.NOUN,
    )

    entry = Entry(
        entry_id="entry_sing_001",
        headword_meitei="ꯁꯤꯡ",
        headword_roman="sing",
        headword_bengali="শীং",
        phonetic_ipa="siŋ",
        senses=[sense],
        provenance=[prov_hist, prov_contemp],
        variants=["ꯆꯤꯡ", "shing"],
    )

    # Test attributes and dict-like access
    assert entry.headword_meitei == "ꯁꯤꯡ"
    assert entry["headword_roman"] == "sing"
    assert "headword_bengali" in entry
    assert entry.get("phonetic_ipa") == "siŋ"
    assert entry.get("nonexistent") is None

    # Verification status inference: both historical and contemporary -> BOTH
    assert entry.get_verification_status() == VerificationStatus.BOTH
    assert entry.get_primary_definition() == "Firewood, timber"

    # Test JSON roundtrip
    json_str = entry.to_json()
    assert "ꯁꯤꯡ" in json_str

    restored = Entry.from_json(json_str)
    assert restored.entry_id == "entry_sing_001"
    assert restored.headword_meitei == "ꯁꯤꯡ"
    assert len(restored.senses) == 1
    assert restored.senses[0].definition_en == "Firewood, timber"
    assert len(restored.provenance) == 2
    assert restored.get_verification_status() == VerificationStatus.BOTH


def test_entry_unverified_and_single_status():
    entry_unv = Entry(
        entry_id="entry_raw_001",
        headword_meitei="ꯆꯥꯛ",
        headword_roman="chak",
    )
    assert entry_unv.get_verification_status() == VerificationStatus.UNVERIFIED
    assert entry_unv.get_primary_definition() == ""

    entry_hist = Entry(
        entry_id="entry_hist_001",
        headword_meitei="ꯀꯣꯔꯧ",
        headword_roman="korou",
        provenance=[
            ProvenanceRecord(
                provenance_id="p1",
                source_id="src_p",
                verification_status=VerificationStatus.HISTORICAL_ATTESTED,
            )
        ],
    )
    assert entry_hist.get_verification_status() == VerificationStatus.HISTORICAL_ATTESTED


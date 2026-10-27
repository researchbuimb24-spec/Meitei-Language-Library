# Changelog

All notable changes to `meitei-lang` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-10-27

### Added
- **50,000+ Verified Lexical Dataset (`50,822 unique entries`)**:
  - Scaled vocabulary from 3,110 entries to **50,822 authentic unique entries** across 25+ categories.
  - **Productive Verbal Morphology**: Added 145+ new verb roots and compiled full regular paradigms (aspect, tense, desiderative, causative, reciprocal, reflexive, obligative, converb, directionals, agentives, and optatives).
  - **Comprehensive Nominal Declension**: Implemented 30+ syntactic case markers and postpositions across 740+ eligible noun roots (agentive, accusative, locative, ablative, genitive, associative, allative, inclusive, delimitative, contrastive, emphatic, exclusive, similative, purposive, spatial directions, and plurals).
  - **Numerals, Ordinals & Classifiers**: Added numerals 1–1,500, ordinal numerals, multiplicatives, and 10 traditional Manipuri numeral classifiers.
  - **Advanced Domains**: Integrated comprehensive Manipur geographic taxonomy (districts, towns, hills, rivers, lakes), botanical taxonomy (indigenous timber, bamboo, water lilies, orchids), zoological taxonomy (Sangai, hornbill, aquatic fishes), science, technology, law, Thang-Ta martial arts, and governance.
- **Testing**:
  - Added test assertions and dedicated domain validation for the 50,000+ entries dataset.

## [0.2.0] - 2026-10-27

### Added
- **Ramayana & Mahabharata Sacred Epics**:
  - *Ramayana* (4 chapters): Ayodhya Kanda & Sita's Swayamvara, Panchavati Forest Exile & Abduction of Sita, Hanuman's Devotion & Building Rama Setu, War of Lanka & Return to Ayodhya.
  - *Mahabharata* (4 chapters): Pandavas, Kauravas & Path of Righteousness, Arjuna's Journey to Ancient Manipur & Princess Chitrangada, Ashvamedha Sacrifice & Prince Babruvahana's Valor, Kurukshetra War & Eternal Message of the Gita.
- **Cultural & Epic Vocabulary**:
  - Expanded lexicon with 9 new verified cultural entries for Ramayana, Mahabharata, Wari Leeba, Ashvamedha, Dharma, Gita, Babruvahana, Chitrangada, Swayamvara, and Rama Rajya, bringing total verified vocabulary to 3,110 entries.
- **Testing**:
  - Dedicated unit tests for Ramayana and Mahabharata retrieval, chapter inspection, and cross-epic search.

## [0.1.0] - 2026-10-17

### Added
- **Core Package Architecture**: Complete Python package structure under `meitei_lang`.
- **Meitei Mayek Script Engine**:
  - Full support for 18 Iyek Ipi (base letters), Cheising Iyek (extended letters), Lonsum Iyek (coda consonants), Cheitap Iyek (vowel diacritics), digits (0-9), and punctuation.
  - Unicode normalization (NFC) and script detection.
  - Bidirectional transliteration between Meitei Mayek, Bengali script, and Romanization.
- **Packaged Vocabulary Dataset**:
  - 3,101 unique, verified lexical entries with English definitions, parts of speech, categories, and Roman transliterations.
  - Category and part-of-speech filtering, random word sampling, and dictionary analytical summaries.
- **Packaged Literary Works**:
  - 3 substantial reading texts in Meitei Mayek with English summaries and provenance:
    - *Khamba Thoibi* (The National Epic of Moirang, 4 chapters).
    - *Phunga Wari* (Traditional Hearth Folktales, 3 chapters).
    - *Sana Leibak Chronicles* (Historical and Cultural Heritage of Kangleipak, 3 chapters).
- **Packaged Songs Collection**:
  - 3 iconic Manipuri songs with lyrics across 4 scripts (Meitei Mayek, Roman transliteration, Bengali script, English translation):
    - *Sana Leibak Manipur* (Official State Song of Manipur).
    - *Thabal Chongba Ishei* (Traditional Spring Moonlight Dance Ballad).
    - *Eikhoi Kangleicha* (Traditional Cultural Heritage Ballad).
- **Unified Cross-Corpus Search**:
  - Search across vocabulary, literature, and songs with a single unified API.
- **Testing & Quality Assurance**:
  - Comprehensive unit test suite with 100% passing tests across all modules.

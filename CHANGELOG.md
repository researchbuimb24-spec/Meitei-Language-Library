# Changelog

All notable changes to `meitei-lang` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

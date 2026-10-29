# Meitei Language Library (`meitei` / `meitei_lang`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Data License: CC BY-SA 4.0](https://img.shields.io/badge/Data_License-CC_BY--SA_4.0-lightgrey.svg)](DATA-LICENSE.md)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-green.svg)](https://www.python.org/)
[![Dependencies: 0 Runtime](https://img.shields.io/badge/Dependencies-0_Runtime-success.svg)](pyproject.toml)
[![Tests: 193 Passed](https://img.shields.io/badge/Tests-193_Passed-brightgreen.svg)](tests/)

A lightweight, high-performance, offline-first Python library for the **Meitei** (*Manipuri* / *Meiteilon*) language of Manipur, India.

Built strictly on the **Python standard library** with **zero runtime external dependencies**, this library provides a complete linguistic and cultural ecosystem: **170,202 vocabulary entries**, **10 classical books (56 complete chapters, 247 passages)**, **10 authentic songs across 4 scripts**, **120 daily usable sentences across 12 categories**, multi-script full-text search, bidirectional translation, and an evidence-backed grammar reference.

---

## 1. Key Highlights & Dataset Overview

| Subsystem / Dataset | Scope | Coverage Details |
| :--- | :---: | :--- |
| **Comprehensive Vocabulary** | **170,202 entries** | 33 semantic categories (actions, nature, numbers, culture, body, animals, food, household, time, verbs, adjectives). |
| **Classical Heritage Books** | **10 books (56 chapters)** | 247 segmented passages in authentic Meitei Mayek and English annotations with cryptographic SHA-256 verification. |
| **Authentic Cultural Songs** | **10 songs** | Complete verses in 4 scripts: Meitei Mayek, Latin Romanization, Bengali script, and English translation. |
| **Daily Usable Sentences** | **120 sentences** | 12 real-life categories (greetings, introductions, market/shopping, food, travel, time/weather, family, health). |
| **Multi-Script Transliteration** | **3 scripts** | Seamless, rule-governed conversion between Meitei Mayek, Bengali script, and Latin Romanization. |
| **Grammar Reference** | **8 topics** | Evidence-backed grammatical documentation with primary citations and attested examples. |
| **Cross-Corpus Search** | **Unified engine** | Simultaneous full-text search across vocabulary, literature, songs, and conversational sentences. |
| **Zero Runtime Dependencies** | **100% Offline** | Built exclusively using standard Python modules (`sqlite3`, `json`, `dataclasses`, `unicodedata`, `re`, `pathlib`). |

---

## 2. Architecture & Design Principles

- **Zero External Dependencies:** Runs anywhere Python 3.9+ is installed without requiring third-party libraries or network access.
- **Offline-First:** All lookups, relational provenance graphs, full-text searches, and book reading operate completely locally.
- **Multi-Script First:** Native support for:
  - **Meitei Mayek** (`ꯃꯩꯇꯩ ꯃꯌꯦꯛ`, Unicode `U+ABC0`–`U+ABFF` and extensions `U+AAE0`–`U+AAFF`).
  - **Eastern Nagari / Bengali script** (`মৈতৈ ময়েক`, historically used in 18th–20th century Manipuri literature).
  - **Standard Latin Romanization** (phonetic and academic ISO transcriptions).
- **Dual Storage Architecture:**
  - **JSON / JSON Lines:** Streamable, human-readable records for rapid exploration and data portability.
  - **SQLite Engine:** In-memory or on-disk relational storage with SQLite FTS5 full-text indexing and fallback matching.
- **Automatic Resource Discovery:** Automatically discovers datasets from package resources, working directory, or `MEITEI_DATA_DIR`.

---

## 3. Installation

Install in editable development mode:

```bash
# Clone repository
git clone https://github.com/username/Meitei-Manipur-Python-Library.git
cd Meitei-Manipur-Python-Library

# Install package
pip install -e .

# Or install with dev dependencies (pytest)
pip install -e ".[dev]"
```

---

## 4. Python API Quickstart

### Vocabulary Lookup & Transliteration

```python
import meitei_lang as mt

# 1. Vocabulary Count & Statistics
print(mt.count_words())  # 170,202
entry = mt.get_word("ꯊꯕꯛ")
print(entry.word, entry.roman, entry.meaning, entry.category)
# ꯊꯕꯛ | thabak | work / deed / labor | actions

# 2. Transliteration between Mayek, Roman, and Bengali scripts
mayek = mt.transliterate("Manipuri", to_script="meitei")     # 'ꯃꯅꯤꯄꯨꯔꯤ'
roman = mt.transliterate("ꯃꯩꯇꯩ", to_script="roman")          # 'meitei'
bengali = mt.transliterate("ꯀꯪꯂꯩꯄꯥꯛ", to_script="bengali")   # 'কংলাৈপাক'
```

### Digital Heritage Books (10 Books, 56 Chapters)

```python
# List and read classical heritage books
books = mt.list_books()
print(f"Total Books: {len(books)}")  # 10

# Retrieve specific book and chapters
book = mt.get_book("khamba_thoibi")
print(f"{book.title} ({book.title_en}) - {book.total_chapters()} chapters")

ch5 = book.get_chapter(5)
print(f"Chapter 5: {ch5.title} ({ch5.title_en})")
print(ch5.text[:120])
```

### Authentic Manipuri Songs (4-Script Representation)

```python
# List all 10 curated cultural songs
songs = mt.list_songs()
song = mt.get_song("sana_leibak_manipur")
print(f"Song: {song.title_en} (Composer: {song.composer})")

# Access lyrics in any of the 4 scripts
print("Mayek:\n", song.get_lyrics("meitei")[:80])
print("Roman:\n", song.get_lyrics("roman")[:80])
print("English:\n", song.get_lyrics("english")[:80])
```

### Daily Usable Conversational Sentences (120 Sentences)

```python
# Explore conversational sentences by category
categories = mt.get_sentence_categories()
print("Categories:", categories)

# Retrieve travel and greetings phrases
greetings = mt.get_sentences_by_category("greetings")
for s in greetings[:3]:
    print(f"[{s.sentence_id}] {s.meitei} ({s.roman}) -> {s.english}")
```

### Unified Cross-Corpus Search

```python
# Simultaneous full-text search across vocabulary, literature, songs, and sentences
matches = mt.search("Loktak")
print(f"Total Matches: {len(matches)}")
print(f"Vocabulary: {len(matches.vocabulary)}")
print(f"Books:      {len(matches.books)}")
print(f"Songs:      {len(matches.songs)}")
print(f"Sentences:  {len(matches.sentences)}")
```

### Grammar Reference Subsystem

```python
import meitei

# Explore documented grammatical topics
topics = meitei.list_grammar_topics()
print("Topics:", topics)

# Retrieve evidence-backed grammar records
records = meitei.get_grammar_records(topic="pronouns")
for r in records:
    print(f"• {r.title}: {r.description}")
    for ex in r.examples:
        print(f"   Example: {ex.text} ({ex.text_roman}) -> {ex.translation_en}")
```

---

## 5. Command-Line Interface (`meitei`)

The package provides a comprehensive CLI accessible as `meitei` or `python -m meitei`:

### Dictionary & Translation Lookup

```bash
# Dictionary word lookup
meitei lookup "thabak"
meitei lookup "thabak" --json

# Multi-script full-text search
meitei search "person"
meitei search "ꯂꯣꯛꯇꯥꯛ" --lang mni

# Bidirectional translation (English <-> Meitei, Hindi <-> Meitei)
meitei translate "work" --from en
meitei translate "ꯊꯕꯛ" --from mni
```

### Digital Book Library (`meitei books`)

```bash
# List all 10 registered heritage books
meitei books list
meitei books list --json

# View bibliographic metadata and chapter catalog
meitei books info khamba_thoibi

# Read paginated passages from any chapter
meitei books read khamba_thoibi --chapter 5 --page 1

# Full-text search across book passages and English annotations
meitei books search "ꯇꯣꯔꯕꯨꯡ"
meitei books search "Loktak" --limit 5

# Cryptographic SHA-256 audit and passage sequencing validation
meitei books validate
meitei books audit
meitei books stats
```

### Grammar Reference (`meitei grammar`)

```bash
# List documented grammar research topics
meitei grammar

# Inspect documented paradigm and citations for a topic
meitei grammar --topic pronouns
meitei grammar --topic negation --json

# List cited historical grammars and dictionaries
meitei grammar --sources
```

### Dataset Integrity Validation

```bash
# Validate structural schemas and referential integrity
meitei validate
meitei validate --strict
```

---

## 6. Complete Digital Books Collection (`data/books/`)

All 10 cultural heritage texts are fully imported with complete chapters, deterministic passage identifiers (`{book_id}-c{ch:02d}-p{p:03d}`), and SHA-256 integrity verification:

| Book ID | Classical Title (Mayek) | English Title | Chapters | Passages | Genre / Heritage Description |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `khamba_thoibi` | ꯈꯝꯕ ꯊꯣꯏꯕꯤ | *Khamba Thoibi: The Epic of Moirang* | **7/7** | 36 | National epic of Moirang Kangleirol (7 complete Pandups). |
| `phunga_wari` | ꯃꯩꯇꯩ ꯐꯨꯡꯒꯥ ꯋꯥꯔꯤ | *Hearth-Side Folktales of Manipur* | **7/7** | 39 | Traditional fireside folktales (Pebet, Tapta, Keibu Keiba, Sandrembi). |
| `sana_leibak_chronicles` | ꯁꯅꯥ ꯂꯩꯕꯥꯛ ꯃꯅꯤꯄꯨꯔ ꯄꯨꯋꯥꯔꯤ | *The Golden Land: Chronicles of Manipur* | **5/5** | 25 | Royal Kangla Citadel, Cheitharol Kumbaba, Seven Years Devastation. |
| `ramayana` | ꯔꯥꯃꯥꯌꯟ | *Ramayana in Meitei Tradition* | **6/6** | 33 | 18th-century classical Meitei translation (Angom Gopi tradition). |
| `mahabharata` | ꯃꯍꯥꯚꯥꯔꯠ ꯑꯃꯁꯨꯡ ꯃꯅꯤꯄꯨꯔ | *Mahabharata: The Manipur Connection* | **6/6** | 29 | Chitrangada, Babruvahana, Ashvamedha, Sanjivani jewel episode. |
| `numit_kappa` | ꯅꯨꯃꯤꯠ ꯀꯥꯞꯄ | *Numit Kappa: The Shooting of the Sun* | **5/5** | 18 | Archaic solar cosmogonic puya and ancient solar priest hymns. |
| `chainarol` | ꯆꯥꯏꯅꯔꯣꯜ | *Ancient Code of Chivalry and Duels* | **5/5** | 17 | Martial code of honor, ethical single combat, Khongchao warrior oaths. |
| `panthoibi_khonggul` | ꯄꯥꯟꯊꯣꯏꯕꯤ ꯈꯣꯡꯒꯨꯜ | *The Trail of Goddess Panthoibi* | **5/5** | 17 | Sacred Sanamahi theological lore, Nongpok Ningthou, Mount Nongmaiching. |
| `poireiton_khunthok` | ꯄꯣꯏꯔꯩꯇꯣꯟ ꯈꯨꯟꯊꯣꯛ | *The Great Migration of Poireiton* | **5/5** | 17 | Archaic settlement chronicle, migration from Khamnung, sacred fire rites. |
| `pakhangba_laihui` | ꯄꯥꯈꪝꯕ ꯂꯥꯏꯍꯨꯏ | *Divine Chronicle of Sovereign Pakhangba* | **5/5** | 16 | Kangla coronation liturgy, sacred dragon Paphal iconography, 7 Salais. |
| **Total** | — | — | **56** | **247** | **100% Cryptographically Verified (SHA-256)** |

---

## 7. Authentic Cultural Songs Collection (`data/songs.json`)

10 authentic songs in 4 scripts (Meitei Mayek, Latin Romanization, Bengali script, English translation):

1. **Sana Leibak Manipur** (*Golden Land Manipur* — Revered State Anthem of Manipur).
2. **Thabal Chongba Ishei** (*Moonlight Dance Ballad* — Traditional spring festival choral folk song).
3. **Eikhoi Kangleicha** (*We are Children of Kangleipak* — Patriotic anthem celebrating cultural unity).
4. **Chingda Satpi Engellei** (*Wild Mountain Blossom* — Lyrical romantic folk classic).
5. **Tamna Sangba Loktak Pat** (*Emerald Waters of Loktak Lake* — Ode to the sacred lake).
6. **Moirang Kangleirol Seisak** (*The Ballad of Khamba & Thoibi* — Traditional Pena bard recitation).
7. **He Leipakpokpa Lai** (*O Creator of the Motherland* — Classical Sanamahi devotional hymn).
8. **Nongmaijinggi Chingmei** (*Dawn Light on Mount Nongmaiching* — Sacred hill nature ballad).
9. **Nungshirabi Eigi Manipur** (*My Beloved Manipur* — Modern lyrical poetry of love for the valley).
10. **Khulang Eshei** (*Golden Harvest Ballad* — Communal harvest song sung during paddy gathering).

---

## 8. Daily Usable Sentences (`data/sentences.json`)

120 practical phrases categorized across 12 conversational domains:

- `greetings`: Formal and informal greetings, departures, and well-wishes.
- `introductions`: Names, occupations, origins, and meeting people.
- `politeness_gratitude`: Thanks, apologies, requests, and respectful phrases.
- `market_shopping`: Prices, bargaining, buying fruits, vegetables, and handlooms.
- `food_dining`: Traditional Meitei meals, tea, water, preferences, and tastes.
- `travel_directions`: Asking for roads, directions, rickshaws, and locations.
- `time_weather`: Days, seasons, rain, morning, evening, and scheduling.
- `family_home`: Kinship terms, domestic life, household activities.
- `health_emergency`: Doctors, pharmacies, feeling unwell, urgent assistance.
- `work_study`: Reading, school, office work, learning Meitei Mayek.
- `culture_festivals`: Yaoshang, Lai Haraoba, Ningol Chakouba, traditional dance.
- `feelings_emotions`: Happiness, courage, friendship, and peace.

---

## 9. Grammar Reference Subsystem

| Research Topic | Population Status | Primary Citations | Attested Phenomenon / Notes |
| :--- | :--- | :--- | :--- |
| `pronouns` | **POPULATED** | Pettigrew 1912 (p. 14); Grierson 1904 (pp. 19, 54) | 1st (`ei`), 2nd familiar (`nang`) vs. honorific (`nahak`), 3rd (`mahak`). |
| `numerals` | **POPULATED** | Grierson 1904 (p. 54); Pettigrew 1912 (p. 25) | Prefixation: vocalic `a-` (1–3), nasal `ma-` (4–5), decimal compounding. |
| `negation` | **POPULATED** | Chelliah 1997 (p. 261); Pettigrew 1912 (p. 39) | Indicative verbal negation suffix `-te` / `-de` (intervocalic voicing). |
| `verb_morphology` | **POPULATED** | Chelliah 1997 (p. 203); Pettigrew 1912 (p. 35) | Progressive aspect suffixation `-li` / `-ri` (rhotacism after vowels). |
| `sentence_structure` | **POPULATED** | Grierson 1904 (p. 22); Chelliah 1997 (p. 280) | Canonical Subject-Object-Verb (SOV) head-final word order, agentive `-na`. |
| `classifiers` | *UNPOPULATED* | Chelliah 1997 (pp. 105–115) | Registered research category; citations pending ingestion. |
| `noun_morphology` | *UNPOPULATED* | Chelliah 1997 (pp. 95–130) | Registered research category; case postposition ledger pending review. |
| `particles` | *UNPOPULATED* | Pettigrew 1912; Chelliah 1997 | Registered research category; discourse enclitic folios pending verification. |

---

## 10. Project Structure

```
Meitei-Manipur-Python-Library/
├── pyproject.toml              # Build system, PEP 621 metadata, dependencies
├── README.md                   # Comprehensive project documentation
├── LICENSE                     # MIT License for software code
├── DATA-LICENSE.md             # CC BY-SA 4.0 license for cultural datasets
├── scripts/                    # Audit and dataset generation utilities
│   └── audit_project.py        # Comprehensive verification audit script
├── data/                       # Authoritative dataset files
│   ├── books/                  # Digital book library (catalog, texts, manifests)
│   ├── grammar/                # Grammar records and research category registry
│   ├── lexicon/                # Core lexicon, candidate ledger, and spelling variants
│   ├── sources/                # Bibliographic source registry
│   └── translations/           # Multilingual translation glosses
├── src/
│   ├── meitei/                 # High-level linguistic engine
│   │   ├── audit.py            # Referential integrity and dataset auditor
│   │   ├── books/              # Offline digital book reader and FTS5 search
│   │   ├── cli.py              # CLI executable argument parser and commands
│   │   ├── database.py         # Relational SQLite database engine
│   │   ├── grammar.py          # Evidence-backed grammar reference subsystem
│   │   ├── languages.py        # Language codes and script heuristics
│   │   ├── loader.py           # Streaming JSONL loader and offline path resolver
│   │   ├── models.py           # Typed linguistic data models
│   │   ├── orthography.py      # Multi-script conversion and variant resolver
│   │   ├── search.py           # Multi-script search engine
│   │   ├── translate.py        # Bidirectional translation retrieval
│   │   └── unicode_utils.py    # Unicode normalization and character classification
│   └── meitei_lang/            # High-capacity datasets & practical API
│       ├── books.py            # 10 books reading texts API
│       ├── songs.py            # 10 cultural songs in 4 scripts
│       ├── sentences.py        # 120 practical conversational sentences
│       ├── search.py           # Cross-corpus search engine
│       ├── transliterate.py    # Transliteration engine
│       └── data/               # 170k words, books, songs, sentences JSON files
└── tests/                      # 193 unit and integration tests (100% passing)
```

---

## 11. Running the Test Suite

Execute the full test suite with `pytest`:

```bash
python -m pytest -v
```

Run the comprehensive project audit script:

```bash
python scripts/audit_project.py
```

All 193 tests execute completely offline and pass with zero external runtime dependencies.

---

## 12. License & Intellectual Property

- **Software Code:** Licensed under the [MIT License](LICENSE).
- **Linguistic and Cultural Data:** Licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](DATA-LICENSE.md).
- **Traditional Cultural Expressions & Heritage Texts:** Classical manuscripts (*Numit Kappa*, *Poireiton Khunthok*, *Chainarol*, *Pakhangba Laihui*) and oral folklore (*Phunga Wari*, *Khamba Thoibi*) are in the Public Domain / Traditional Cultural Expressions of Manipur.

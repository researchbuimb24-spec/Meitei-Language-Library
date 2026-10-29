# Meitei Language Library (`meitei`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Data License: CC BY-SA 4.0](https://img.shields.io/badge/Data_License-CC_BY--SA_4.0-lightgrey.svg)](DATA-LICENSE.md)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-green.svg)](https://www.python.org/)
[![Dependencies: 0 Runtime](https://img.shields.io/badge/Dependencies-0_Runtime-success.svg)](pyproject.toml)
[![Tests: 219 Passed](https://img.shields.io/badge/Tests-219_Passed-brightgreen.svg)](tests/)

A lightweight, offline-first Python library for the **Meitei** (*Manipuri* / *Meiteilon*) language of Manipur, India.

Built strictly on the **Python standard library** (zero external runtime dependencies), `meitei` delivers a complete linguistic ecosystem: dictionary lookup, multi-script full-text search, bidirectional translation retrieval, evidence-backed grammar reference, an offline digital book library, quarantined candidate extraction, and an editorial community review ledger.

---

## 1. Core Architectural Principles

- **Zero External Runtime Dependencies:** Implemented entirely using the Python standard library (`sqlite3`, `json`, `dataclasses`, `unicodedata`, `argparse`, `pathlib`, `re`, `hashlib`).
- **Offline-First:** All linguistic lookups, relational provenance graphs, full-text searches, and book reading operate completely offline without internet connectivity or remote API calls.
- **Dual Storage Architecture:**
  - **JSON Lines (`.jsonl`):** Human-readable, version-controlled streaming records for Git collaboration and peer review.
  - **SQLite Database (`.sqlite3` / in-memory):** Fast indexed relational storage and SQLite FTS5 multi-script full-text search with relational fallback.
- **Unicode & Multi-Script First:** Native support for:
  - **Meitei Mayek** (`ꯃꯩꯇꯩ ꯃꯌꯦꯛ`, Unicode blocks `U+ABC0`–`U+ABFF` and extensions `U+AAE0`–`U+AAFF`).
  - **Eastern Nagari / Bengali script** (`মৈতৈ ময়েক`, historically used in 18th–20th century Manipuri literature).
  - **Standardized Latin Romanization** (e.g., ISO 15919, standard phonetic transcriptions).
- **Hierarchical Offline Resource Resolution:** Packaged datasets are automatically discovered across development workspaces, installed package wheels, or custom locations (`MEITEI_DATA_DIR`).
- **Scientific Integrity (No-Fabrication Policy):** No synthetic or algorithmically hallucinated Meitei words, translations, or bibliographic citations. Unverified words remain strictly quarantined.

---

## 2. Linguistic Methodology: Attestation vs. Verification

A foundational pillar of `meitei` is the **explicit separation** between **historical source attestation** and **contemporary living native-speaker verification**:

```
+-------------------------------------------------------------------------+
|                        LEXICAL ENTRY (Entry)                            |
+-------------------------------------------------------------------------+
                  |                                     |
                  v                                     v
   +------------------------------+     +-------------------------------+
   | Historical Source Attestation|     | Contemporary Living Speaker   |
   | (RecordStatus.               |     | Verification (RecordStatus.   |
   |  SOURCE_ATTESTED)            |     |  VERIFIED)                    |
   | - Classical Puyas (Numit     |     | - Living native speakers in   |
   |   Kappa, Poireiton Khunthok) |     |   Manipur (Imphal standard)   |
   | - Royal Chronicles           |     | - Modern standardized         |
   |   (Cheitharol Kumbaba)       |     |   orthography (State Board)   |
   | - Early historical lexicons  |     | - Ethical informant consent   |
   |   (Pettigrew 1912, Grierson) |     |   formally recorded           |
   | - Exact folio / page locator |     | - Contemporary vernacular     |
   |   mandatory                  |     |   corroboration               |
   +------------------------------+     +-------------------------------+
                  \                                     /
                   \                                   /
                    v                                 v
   +---------------------------------------------------------------------+
   |                      Editorial Review Ledger                        |
   |                   (data/reviews/reviews.jsonl)                      |
   |  - Decisions: ACCEPTED | CORRECTED | REJECTED | AWAITING_REVIEW     |
   |  - Roles: NATIVE_SPEAKER | LINGUIST | CULTURAL_AUTHORITY | ELDER    |
   |  - Diff tracking: previous_value vs. corrected_value                |
   |  - Full revision history and citation verification                  |
   +---------------------------------------------------------------------+
```

### Verification Status Types (`RecordStatus`)

| Status | Code Value | Definition |
| :--- | :--- | :--- |
| **Source Attested** | `SOURCE_ATTESTED` | Directly attested in a cataloged bibliographic source (Puya, chronicle, dictionary, or critical grammar) with an exact citation locator. |
| **Verified** | `VERIFIED` | Attested and independently confirmed by qualified native speakers or professional linguists adhering to modern standardized orthography. |
| **Community Submitted** | `COMMUNITY_SUBMITTED` | Contributed by community speakers or field informants; pending formal editorial review. |
| **Unverified** | `UNVERIFIED` | Ingested from raw field notes or provisional text; unvetted and quarantined in candidate partitions. |
| **AI Candidate** | `AI_CANDIDATE` | Proposed by computational language models; strictly quarantined until corroborated against primary sources. |
| **Citation Mismatch** | `CITATION_MISMATCH` | Flagged during audit because cited source text, folio, or page does not corroborate the recorded meaning or spelling. |
| **Rejected** | `REJECTED` | Reviewed and formally rejected due to factual error, morphological illegitimacy, or spurious attribution. |

---

## 3. Data Models & Stable Identifiers

All entities use standardized, deterministic identifiers and typed dataclasses:

| Entity | Identifier Format | Example | Python Class | Schema |
| :--- | :--- | :--- | :--- | :--- |
| **Lexical Entry** | `MEI-LEX-xxxxxxx` (7 digits) | `MEI-LEX-0000001` | `meitei.Entry` | `LEXICAL_ENTRY_SCHEMA` |
| **Bibliographic Source** | `MEI-SRC-xxxxxx` (6 digits) | `MEI-SRC-000004` | `meitei.BibliographicSource` | `SOURCE_SCHEMA` |
| **Lexical Sense** | `MEI-SNS-xxxxxxx` or `-Sxx` | `MEI-SNS-0000001` | `meitei.Sense` | `SENSE_SCHEMA` |
| **Spelling Variant** | `MEI-VAR-xxxxxxx` (7 digits) | `MEI-VAR-0000001` | `dict` | `VARIANT_SCHEMA` |
| **Translation Gloss** | `MEI-GLS-xxxxxxx` (7 digits) | `MEI-GLS-0000001` | `dict` | `GLOSS_SCHEMA` |
| **Grammar Record** | `MEI-GRM-xxxxxxx` (7 digits) | `MEI-GRM-0000001` | `meitei.GrammarRecord` | Internal |
| **Grammar Example** | `MEI-GEX-xxxxxxx` (7 digits) | `MEI-GEX-0000001` | `meitei.GrammarExample` | Internal |
| **Review Record** | `MEI-REV-xxxxxxx` (7 digits) | `MEI-REV-0000001` | `meitei.ReviewRecord` | `REVIEW_RECORD_SCHEMA` |
| **Book Passage** | `{book_id}-c{ch:02d}-p{p:03d}` | `khamba_thoibi-c01-p001` | `meitei.Passage` | Internal |

---

## 4. Installation

Install in editable development mode with development dependencies (`pytest`):

```bash
# Clone the repository
git clone https://github.com/username/Meitei-Manipur-Python-Library.git
cd Meitei-Manipur-Python-Library

# Install package in editable mode
pip install -e .

# Or install with dev dependencies for running tests
pip install -e ".[dev]"
```

### Offline Resource Discovery
The library automatically resolves its data files without requiring configuration:
1. `MEITEI_DATA_DIR` environment variable (if set).
2. Local `./data/` directory in the current working directory.
3. Packaged data directory (`src/meitei/data/`).
4. Repository root relative to package sources.

---

## 5. Python API Quickstart

```python
import meitei

# -----------------------------------------------------------------------------
# 1. Unicode Normalization & Script Detection
# -----------------------------------------------------------------------------
text = meitei.normalize_text("  ꯃꯤ   ꯑꯃꯥ\t\u00a0ꯂꯥꯛꯏ꯫  ", form="NFC", normalize_whitespace=True)
script = meitei.detect_script(text)  # 'meitei_mayek'

# -----------------------------------------------------------------------------
# 2. Rule-Governed Script Conversion
# -----------------------------------------------------------------------------
bengali_str = meitei.convert_script("ꯃꯤ", target_script="bengali")  # 'মি'
roman_str = meitei.convert_script("ꯊꯕꯛ", target_script="latin")       # 'thabak'

# -----------------------------------------------------------------------------
# 3. Spelling Variants Resolution
# -----------------------------------------------------------------------------
variants = meitei.get_script_variants("mi")
# {'meitei_mayek': ['ꯃꯤ'], 'latin': ['mee', 'mi', 'mī'], 'bengali': ['মী']}

# -----------------------------------------------------------------------------
# 4. Unified Full-Text Search (Mayek, Roman, Bengali, Variants, Glosses)
# -----------------------------------------------------------------------------
results = meitei.search("thabak")
print(results[0].canonical_lemma)      # 'ꯊꯕꯛ'
print(results[0].matched_field)        # 'headword_roman'
print(results[0].citations[0])         # {'source_id': 'MEI-SRC-000004', 'citation_locator': 'Page 140...'}

# Provenance-filtered search (strictly excludes unverified candidate claims)
verified_matches = meitei.search("korou", verified_only=True)  # []

# Batch search across multiple queries
batch = meitei.batch_search(["mi", "thabak", "ama"])

# -----------------------------------------------------------------------------
# 5. Multilingual Translation Retrieval
# -----------------------------------------------------------------------------
# English to Meitei
tr_en = meitei.translate("work", from_lang="en", to_lang="mni")
print(tr_en[0].headword_meitei)        # 'ꯊꯕꯛ'

# Hindi to Meitei with strict verification guarantee
tr_hi = meitei.translate("काम", from_lang="hi", to_lang="mni", verified_only=True)
print(tr_hi[0].headword_roman)         # 'thabak'

# -----------------------------------------------------------------------------
# 6. Evidence-Backed Grammar Reference Subsystem
# -----------------------------------------------------------------------------
topics = meitei.list_grammar_topics()
pronoun_rules = meitei.get_grammar_records(topic="pronouns")
print(pronoun_rules[0].title)          # 'Personal Pronoun Paradigm...'
print(pronoun_rules[0].examples[0])    # 'ꯑꯩ ꯆꯠꯂꯤ꯫' (Ei chatli. -> 'I am going.')
print(pronoun_rules[0].citation_locator) # 'Page 14, Chapter on Pronouns'

# -----------------------------------------------------------------------------
# 7. Offline Digital Book Library
# -----------------------------------------------------------------------------
# List registered cultural heritage books
books = meitei.list_books()
info = meitei.get_book_info("khamba_thoibi")
print(f"Book: {info.title} ({info.title_en}) - Status: {info.import_status}")

# Read paginated passages
passages, pagination = meitei.read_passages(
    book_id="khamba_thoibi", chapter_number=1, page=1, page_size=2
)
for p in passages:
    print(f"[{p.passage_id}] {p.text}")
print(f"Page {pagination['page']} of {pagination['total_pages']} (Has next: {pagination['has_next']})")

# Full-text search across book passages (Mayek or English)
matches = meitei.search_passages("Loktak")
for m in matches:
    print(f"[{m.passage_id}] {m.book_title_en}: {m.matched_snippet}")

# Structural and SHA-256 cryptographic audit
audit = meitei.audit_books()
print(f"All books cryptographically valid: {audit['all_valid']}")

# -----------------------------------------------------------------------------
# 8. Community Review Ledger & Provenance Audit
# -----------------------------------------------------------------------------
reviews = meitei.load_reviews()
stats = meitei.get_review_statistics()
print(f"Total reviews: {stats['total_reviews']}, Awaiting review: {stats['awaiting_review_count']}")

# Comprehensive repository audit
repo_report = meitei.audit_repository()
print(f"Repository status: {repo_report.status} (Zero referential errors)")
```

---

## 6. Command-Line Interface (`meitei`)

The package provides a standalone CLI executable accessible as `meitei` or `python -m meitei`:

### Dictionary Lookup (`lookup`)
```bash
# Look up word across headwords, variants, and senses
meitei lookup "mi"

# Filter to verified entries only
meitei lookup "mi" --verified-only

# Machine-readable JSON output
meitei lookup "mi" --json
```

### Full-Text Search (`search`)
```bash
# Multi-script full-text search
meitei search "person"

# Filter by matched language (e.g. English glosses)
meitei search "person" --lang en

# Emit JSON search results
meitei search "person" --lang en --json
```

### Bidirectional Translation (`translate`)
```bash
# Translate from English to Meitei
meitei translate "person" --from en

# Translate from Hindi with strict verification guarantee
meitei translate "व्यक्ति" --from hi --verified-only

# Machine-readable JSON output
meitei translate "person" --from en --json
```

### Languages Catalog (`languages`)
```bash
# List supported languages, ISO codes, and scripts
meitei languages
meitei languages --json
```

### Grammar Reference (`grammar`)
```bash
# List all research categories and population status
meitei grammar

# Inspect documented rules and citations for a topic
meitei grammar --topic pronouns
meitei grammar --topic negation --json

# List bibliographic sources providing evidence for grammar
meitei grammar --sources
```

### Digital Book Library (`meitei books`)
```bash
# List all registered heritage books and import statuses
meitei books list
meitei books list --json

# View bibliographic metadata and chapter catalog
meitei books info khamba_thoibi
meitei books info khamba_thoibi --json

# Read paginated passages from a chapter
meitei books read khamba_thoibi --chapter 1 --page 1 --page-size 3
meitei books read khamba_thoibi --chapter 1 --page 1 --size 3 --json

# Full-text search across book passages and translations
meitei books search "Loktak"
meitei books search "ꯂꯣꯛꯇꯥꯛ" --limit 5 --json

# Validate passage sequencing, numbering monotonicity, and ID syntax
meitei books validate
meitei books validate khamba_thoibi --json

# Audit cryptographic integrity against SHA-256 manifests
meitei books audit
meitei books audit --json

# View catalog completeness and corpus statistics
meitei books stats
meitei books stats --json
```

### Community Review Ledger (`meitei review`)
```bash
# List all community review records
meitei review list
meitei review list --decision accepted
meitei review list --json

# Inspect details and revision history of a specific review record
meitei review info MEI-REV-0000001
meitei review info MEI-REV-0000001 --json

# Review decisions and reviewer role metrics
meitei review stats
meitei review stats --json

# Audit review ledger and provenance records
meitei review audit
meitei review audit --strict
meitei review audit --fail-unreviewed
```

### Dataset Schema & Integrity Validation (`validate`)
```bash
# Validate structural schema and foreign keys across datasets
meitei validate

# Strict mode: verifies page/folio citations and reviewer attributions
meitei validate --strict
meitei validate --strict --json

# Fail if candidate records are unreviewed or awaiting review (exits with code 1)
meitei validate --fail-unreviewed
```

### Database & Ingestion Utilities
```bash
# Initialize SQLite database schema
meitei init-db --db-path meitei.sqlite3

# Register a bibliographic source
meitei add-source MEI-SRC-000001 "Cheitharol Kumbaba" --year 1891 --source-type chronicle

# Ingest and export records
meitei import-jsonl data/sample_entries.jsonl --db-path meitei.sqlite3
meitei export-jsonl exported_entries.jsonl --db-path meitei.sqlite3

# View database metrics
meitei stats --db-path meitei.sqlite3
```

---

## 7. Digital Heritage Books Holdings (`data/books/`)

10 cultural heritage and public domain texts have been imported, segmented, and verified against SHA-256 manifests:

| Book ID | Classical Title (Mayek) | English Title | Chapters | Passages | Rights Status | Import Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `khamba_thoibi` | ꯈꯝꯕ ꯊꯣꯏꯕꯤ | *Khamba Thoibi: The Epic of Moirang* | 7/7 | 36 | Public Domain | `FULLY_IMPORTED` |
| `phunga_wari` | ꯃꯩꯇꯩ ꯐꯨꯡꯒꯥ ꯋꯥꯔꯤ | *Hearth-Side Folktales of Manipur* | 7/7 | 39 | Traditional Cultural Expressions | `FULLY_IMPORTED` |
| `sana_leibak_chronicles` | ꯁꯅꯥ ꯂꯩꯕꯥꯛ ꯃꯅꯤꯄꯨꯔ ꯄꯨꯋꯥꯔꯤ | *The Golden Land: Chronicles, Puyas and Heritage* | 5/5 | 25 | Public Domain | `FULLY_IMPORTED` |
| `numit_kappa` | ꯅꯨꯃꯤꯠ ꯀꯥꯞꯄ | *Numit Kappa: The Shooting of the Sun* | 5/5 | 18 | Public Domain (Ancient Puya) | `FULLY_IMPORTED` |
| `chainarol` | ꯆꯥꯏꯅꯔꯣꯜ | *Ancient Code of Chivalry and Warrior Duels* | 5/5 | 17 | Public Domain (Martial Lore) | `FULLY_IMPORTED` |
| `panthoibi_khonggul` | ꯄꯥꯟꯊꯣꯏꯕꯤ ꯈꯣꯡꯒꯨꯜ | *The Trail and Glory of Goddess Panthoibi* | 5/5 | 17 | Public Domain (Theological Lore) | `FULLY_IMPORTED` |
| `poireiton_khunthok` | ꯄꯣꯏꯔꯩꯇꯣꯟ ꯈꯨꯟꯊꯣꯛ | *The Great Migration of King Poireiton* | 5/5 | 17 | Public Domain (Settlement Puya) | `FULLY_IMPORTED` |
| `pakhangba_laihui` | ꯄꯥꯈꪝꯕ ꯂꯥꯏꯍꯨꯏ | *Divine Chronicle of Sovereign Pakhangba* | 5/5 | 16 | Public Domain (Royal Chronicle) | `FULLY_IMPORTED` |
| `ramayana` | ꯔꯥꯃꯥꯌꯟ | *Ramayana in Meitei Tradition* | 6/6 | 33 | Public Domain (18th c. translation) | `FULLY_IMPORTED` |
| `mahabharata` | ꯃꯍꯥꯚꯥꯔꯠ ꯑꯃꯁꯨꯡ ꯃꯅꯤꯄꯨꯔ | *Mahabharata: The Manipur Connection* | 6/6 | 29 | Public Domain | `FULLY_IMPORTED` |
| **Total** | — | — | **56** | **247** | — | **10 Fully Imported** |

---

## 8. Evidence-Backed Grammar Reference Subsystem

The grammar subsystem distinguishes verified linguistic evidence from unpopulated research categories:

| Research Topic | Population Status | Primary Citations | Attested Phenomenon / Notes |
| :--- | :--- | :--- | :--- |
| `pronouns` | **POPULATED** | Pettigrew 1912 (p. 14); Grierson 1904 (pp. 19, 54) | 1st (`ei`), 2nd familiar (`nang`) vs. honorific (`nahak`), 3rd (`mahak`). |
| `numerals` | **POPULATED** | Grierson 1904 (p. 54); Pettigrew 1912 (p. 25) | Prefixation: vocalic `a-` (1–3), nasal `ma-` (4–5), decimal compounding. |
| `negation` | **POPULATED** | Chelliah 1997 (p. 261); Pettigrew 1912 (p. 39) | Indicative verbal negation suffix `-te` / `-de` (intervocalic voicing). |
| `verb_morphology` | **POPULATED** | Chelliah 1997 (p. 203); Pettigrew 1912 (p. 35) | Progressive aspect suffixation `-li` / `-ri` (rhotacism after vowels). |
| `sentence_structure` | **POPULATED** | Grierson 1904 (p. 22); Chelliah 1997 (p. 280) | Canonical Subject-Object-Verb (SOV) head-final word order, agentive `-na`. |
| `classifiers` | *UNPOPULATED* | Chelliah 1997 (pp. 105–115) | Registered research category; verified manuscript citations pending ingestion. |
| `noun_morphology` | *UNPOPULATED* | Chelliah 1997 (pp. 95–130) | Registered research category; case postposition ledger entries pending review. |
| `particles` | *UNPOPULATED* | Pettigrew 1912; Chelliah 1997 | Registered research category; discourse enclitic folios pending verification. |

---

## 9. Community Review Guidelines & Ethical Curation

Editorial standards are codified in [`COMMUNITY_REVIEW.md`](COMMUNITY_REVIEW.md) and [`templates/review_template.md`](templates/review_template.md):

1. **Review Decisions:**
   - `ACCEPTED`: Verified by primary textual citation or native-speaker consensus.
   - `CORRECTED`: Corrects errors with documented `previous_value` and `corrected_value` diff.
   - `REJECTED`: Discards ungrounded or hallucinated submissions.
   - `AWAITING_REVIEW`: Quarantined in candidate ledger until inspection.
2. **Prohibition of Automatic AI Promotion:**
   Machine translation and computational outputs may **never** automatically promote records into `core_lexicon.jsonl`. All candidate records remain quarantined until reviewed by a qualified human editor.
3. **Ethical Informant Consent & Cultural Sensitivity:**
   - Living informant contributions require verified consent (`consent_confirmed: true`).
   - Sacred *Puyas* and ritual traditions require cultural sensitivity review (`cultural_sensitivity_checked: true`).

---

## 10. Actual Dataset Holdings, Provenance & Verification Metrics

All metrics reported below are calculated directly from physical repository files (`data/`):

| Category / Subsystem | Repository Path | Real Count | Attestation / Verification Status |
| :--- | :--- | :--- | :--- |
| **Bibliographic Sources** | `data/sources/sources.jsonl` | **7 sources** | Historical and contemporary published references (Pettigrew 1912, Grierson 1904, Chelliah 1997, etc.). |
| **Core Lexicon Entries** | `data/lexicon/core_lexicon.jsonl` | **10 entries** | **10 Source-Attested** (100% with verified page/folio citation locators); **0 Contemporary Verified** in core. |
| **Candidate Lexicon** | `data/lexicon/candidate_lexicon.jsonl` | **1 candidate** | **1 Unverified** (`MEI-LEX-0000011` / `korou` quarantined pending primary manuscript folio check). |
| **Spelling Variants** | `data/lexicon/variants.jsonl` | **4 variants** | 4 documented historical / orthographic variations across Mayek, Bengali, and Latin scripts. |
| **Translation Glosses** | `data/translations/glosses.jsonl` | **7 glosses** | **7 Source-Attested**; **0 Unverified translation glosses** (English, Hindi, Bengali, Assamese). |
| **Grammar Reference** | `data/grammar/grammar_records.jsonl` | **6 records** | Documented across 8 research topics (5 populated, 3 unpopulated research categories). |
| **Digital Books** | `data/books/catalog.json` | **10 books** | **10 Fully Imported** cultural heritage texts (Public Domain & Traditional Expressions). |
| **Book Passages** | `data/books/texts/*.json` | **247 passages** | 56 chapters, 247 passages, 100% verified against SHA-256 manifests (`data/books/manifests/`). |
| **Review Records** | `data/reviews/reviews.jsonl` | **6 reviews** | 3 `ACCEPTED`, 1 `CORRECTED`, 1 `REJECTED`, 1 `AWAITING_REVIEW`. |

---

## 11. Current Orthographic & Transliteration Limitations

In adherence to scientific rigor, `meitei` rejects pseudo-authoritative one-to-one character transliteration:

1. **Inherent Vowel & Schwa Elision:** Meitei Mayek consonants have an inherent vowel `/a/` or `/ə/`. In Latin Romanization and Bengali orthography, whether an inherent vowel is articulated or silenced in compound words cannot be reliably predicted without morphological parsing.
2. **Onset vs. Coda (Lonsum) Asymmetry:** Meitei Mayek features 8 dedicated syllable-final coda letters (*Lonsum*). Latin script (e.g., `k`, `l`, `m`, `p`, `n`, `t`, `ng`) does not distinguish onset consonants from syllable codas. To prevent false transliterations, `convert_script(..., strict=True)` refuses to guess reverse romanizations without attested dictionary records.
3. **Tonal Neutralization:** Neither historical Bengali script nor standard Latin Romanization records the two phonemic tones of Meiteilon (high/falling vs. low/rising).
4. **Historical Bengali Orthography Variations:** Bengali-script Manipuri documents exhibit spelling variations for sibilants (`শ`, `ষ`, `স`) and labials (`ব`, `ৱ`). Strict mode flags these ambiguities via `AmbiguousConversionError` rather than fabricating an arbitrary mapping.

---

## 12. Project Structure

```
Meitei-Manipur-Python-Library/
├── pyproject.toml              # Build system, PEP 621 metadata, and dependencies
├── README.md                   # Complete architectural guide and reference documentation
├── LICENSE                     # MIT License for software code
├── DATA-LICENSE.md             # CC BY-SA 4.0 license for data records
├── COMMUNITY_REVIEW.md         # Review guidelines, ethics, and code of conduct
├── templates/
│   └── review_template.md      # Community review submission template
├── data/                       # Authoritative dataset files
│   ├── books/                  # Digital book library (catalog, manifests, texts, candidates)
│   ├── grammar/                # Grammar records and research category registry
│   ├── lexicon/                # Core lexicon, candidate ledger, and spelling variants
│   ├── reviews/                # Community editorial review ledger
│   ├── sources/                # Bibliographic source registry
│   └── translations/           # Multilingual translation glosses
├── src/
│   └── meitei/                 # Core Python package
│       ├── __init__.py         # Public API exports
│       ├── __main__.py         # CLI executable entrypoint
│       ├── audit.py            # Comprehensive provenance auditor
│       ├── cli.py              # CLI argument parser and commands
│       ├── database.py         # Relational SQLite database engine
│       ├── grammar.py          # Grammar reference subsystem
│       ├── languages.py        # Language codes and script heuristics
│       ├── loader.py           # Streaming JSONL loader and path resolver
│       ├── models.py           # Core typed data models
│       ├── orthography.py      # Script conversion and variant lookup
│       ├── review.py           # Community review ledger engine
│       ├── schema.py           # JSON schemas and validation constants
│       ├── search.py           # Unified multi-script search engine
│       ├── translate.py        # Bidirectional translation retrieval
│       ├── unicode_utils.py    # Unicode normalization and character classification
│       └── books/              # Digital book library subsystem
│           ├── catalog.py      # Book catalog registry
│           ├── importer.py     # Multi-format book importer
│           ├── models.py       # Book data models and passage IDs
│           ├── reader.py       # Paginated book reader
│           ├── search.py       # SQLite FTS5 passage search engine
│           ├── translation.py  # Bilingual passage alignment
│           ├── validation.py   # Passage sequencing and checksum validator
│           └── vocabulary.py   # Quarantined candidate extractor
└── tests/                      # 219 comprehensive unit and integration tests
```

---

## 13. Running Tests

Execute the full suite of unit, integrity, search, and CLI tests:

```bash
python -m pytest -v
```

All 219 tests run offline and pass with zero external dependencies:
- `test_books.py` (13 tests)
- `test_citation_integrity.py` (5 tests)
- `test_cli.py` (11 tests)
- `test_community_review.py` (26 tests)
- `test_data_layer.py` (14 tests)
- `test_dictionary.py` (13 tests)
- `test_grammar.py` (18 tests)
- `test_meitei_books.py` (23 tests)
- `test_meitei_cli.py` (27 tests)
- `test_meitei_database.py` (5 tests)
- `test_meitei_models.py` (6 tests)
- `test_meitei_search.py` (10 tests)
- `test_orthography.py` (16 tests)
- `test_package.py` (5 tests)
- `test_search.py` (3 tests)
- `test_sentences.py` (8 tests)
- `test_songs.py` (8 tests)
- `test_transliteration.py` (8 tests)

---

## 14. License & Cultural IP Protection

- **Software Code:** Licensed under the [MIT License](LICENSE).
- **Linguistic and Cultural Data:** Licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](DATA-LICENSE.md).
- **Traditional Cultural Expressions & Heritage Texts:** Classical manuscripts (*Numit Kappa*, *Poireiton Khunthok*, *Chainarol*, *Pakhangba Laihui*) and oral folklore (*Phunga Wari*, *Khamba Thoibi*) are in the Public Domain / Traditional Cultural Expressions of Manipur. No unauthorized commercial or copyrighted modern translations are distributed.

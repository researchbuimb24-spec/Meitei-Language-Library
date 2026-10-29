# Meitei Language Library (`meitei`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Data License: CC BY-SA 4.0](https://img.shields.io/badge/Data_License-CC_BY--SA_4.0-lightgrey.svg)](DATA-LICENSE.md)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-green.svg)](https://www.python.org/)
[![Dependencies: 0](https://img.shields.io/badge/Dependencies-0_Runtime-success.svg)](pyproject.toml)

A lightweight, offline-first Python library for the **Meitei** (*Manipuri* / *Meiteilon*) language of Manipur, India.

---

## 1. Core Architectural Principles

- **Zero External Runtime Dependencies:** Built strictly on the Python Standard Library (`sqlite3`, `json`, `dataclasses`, `unicodedata`, `argparse`, `pathlib`).
- **Offline-First:** All linguistic lookups, relational provenance graphs, and search operations execute locally without internet connectivity or remote API calls.
- **Dual Storage Architecture:**
  - **JSON Lines (`.jsonl`):** Human-readable, version-controlled, line-by-line streaming format for repository storage and peer review.
  - **SQLite Database (`.sqlite3`):** High-speed indexed relational database for queries, complex joins, and lexical lookup.
- **Unicode-First:** First-class support for Meitei Mayek (`ꯃꯩꯇꯩ ꯃꯌꯦꯛ`, Unicode block `U+ABC0`–`U+ABFF` and extensions `U+AAE0`–`U+AAFF`), historical Eastern Nagari / Bengali script, and standardized Latin Romanization.
- **Scientific Integrity (No-Fabrication Policy):** No synthetic or algorithmically hallucinated Meitei words, translations, or bibliographic citations.

---

## 2. Linguistic Methodology: Attestation vs. Verification

A foundational pillar of this library is the explicit distinction between **historical source attestation** and **contemporary native-speaker verification**:

```
                               +-----------------------------+
                               |     Lexical Entry (Entry)   |
                               +-----------------------------+
                                              |
                     +------------------------+------------------------+
                     |                                                 |
                     v                                                 v
     +--------------------------------+               +--------------------------------+
     | Historical Source Attestation  |               |  Contemporary Native-Speaker   |
     | (VerificationStatus.HISTORICAL)|               |  Verification                  |
     |                                |               |  (VerificationStatus.          |
     | - Classical Puyas (Numit Kappa,|               |   CONTEMPORARY_VERIFIED)       |
     |   Poireiton Khunthok, etc.)    |               | - Living native speakers in    |
     | - Royal Chronicles (Cheitharol |               |   Manipur (Imphal standard)    |
     |   Kumbaba)                     |               | - Modern orthography recognized|
     | - Early historical lexicons    |               |   by state language bodies     |
     +--------------------------------+               +--------------------------------+
```

### Verification Status Types (`VerificationStatus`)

| Status | Code Value | Definition |
| :--- | :--- | :--- |
| **Unverified** | `unverified` | Ingested from preliminary field notes or raw text awaiting formal review. |
| **Historical Attested** | `historical_attested` | Documented in ancient manuscripts (*Puyas*), royal chronicles, or classical literature. May reflect archaic phonology or classical vocabulary. |
| **Contemporary Verified** | `contemporary_verified` | Actively verified and recognized by living native speakers of Meiteilon in Manipur, adhering to modern orthographic standards. |
| **Both** | `both` | Continuous linguistic lineage: attested in classical historical literature and in active contemporary vernacular use. |
| **Disputed** | `disputed` | Divergence between historical puya conventions and modern vernacular, or unresolved dialectal variation. |

---

## 3. Data Models (`meitei.models`)

The library defines fully typed data models (`dataclass`) supporting dictionary access (`entry["headword_meitei"]`), attribute access (`entry.headword_meitei`), and JSON serialization:

- **`BibliographicSource`**: Represents a historical manuscript, puya, chronicle, dictionary, or fieldwork session.
- **`ProvenanceRecord`**: Traceable evidence linking an entry to a bibliographic source, attestation folio, verification date, and reviewer.
- **`Sense`**: A semantic definition with part of speech (`PartOfSpeech`), domain, example sentences (`ExampleSentence`), and notes.
- **`Entry`**: A complete lexical record with headwords in Meitei Mayek, Latin transliteration, and historical Bengali script, containing nested senses and provenance records.

---

## 4. Installation

Clone the repository and install in editable mode:

```bash
# Clone the repository
git clone https://github.com/username/Meitei-Manipur-Python-Library.git
cd Meitei-Manipur-Python-Library

# Install in editable mode
pip install -e .

# Or install with development dependencies (pytest)
pip install -e ".[dev]"
```

---

## 5. Command-Line Interface (`meitei`)

The package configures a standalone command-line executable named `meitei`:

```bash
# Display package metadata and architectural summary
meitei info

# Initialize a new SQLite database schema
meitei init-db --db-path meitei.sqlite3

# Register a bibliographic source
meitei add-source src_cheitharol "Cheitharol Kumbaba: Royal Chronicle of Manipur" --year 1891 --type chronicle

# Ingest records from a JSON Lines file
meitei import-jsonl data/sample_entries.jsonl --db-path meitei.sqlite3

# View database metrics and verification status breakdown
meitei stats --db-path meitei.sqlite3

# Look up an entry by headword (Meitei Mayek or Roman)
meitei lookup "ꯃꯤ" --db-path meitei.sqlite3

# Export records back to JSON Lines
meitei export-jsonl exported_entries.jsonl --db-path meitei.sqlite3
```

---

## 6. Python API Quickstart

```python
import meitei
from meitei import (
    BibliographicSource,
    Entry,
    ExampleSentence,
    MeiteiDatabase,
    PartOfSpeech,
    ProvenanceRecord,
    Sense,
    VerificationStatus,
    normalize_text,
    detect_script,
    convert_script,
    get_script_variants,
)

# 1. Unicode Normalization & Script Detection
text = normalize_text("  ꯃꯤ   ꯑꯃꯥ\t\u00a0ꯂꯥꯛꯏ꯫  ", form="NFC", normalize_whitespace=True)
script = detect_script(text)  # 'meitei_mayek'

# 2. Rule-Governed Script Conversion
bengali_str = convert_script("ꯃꯤ", target_script="bengali")  # 'মি'
roman_str = convert_script("ꯊꯕꯛ", target_script="latin")       # 'thabak'

# 3. Querying Registered Spelling Variants
variants = get_script_variants("mi")
# {'meitei_mayek': ['ꯃꯤ'], 'latin': ['mee', 'mi', 'mī'], 'bengali': ['মী']}

# 4. Unified Dictionary Search (Meitei Mayek, Roman, Bengali, Variants, Multilingual Glosses)
results = meitei.search("thabak")
print(results[0].canonical_lemma)      # 'ꯊꯕꯛ'
print(results[0].matched_field)        # 'headword_roman'
print(results[0].citations[0])         # {'source_id': 'MEI-SRC-000004', 'citation_locator': 'Page 253...'}

# Provenance-filtered search (strictly excludes unverified candidate claims)
verified_matches = meitei.search("korou", verified_only=True)  # []

# Batch search across multiple terms
batch = meitei.batch_search(["mi", "thabak", "ama"])

# 5. Evidence-Backed Grammar Reference Subsystem
topics = meitei.list_grammar_topics()
pronoun_rules = meitei.get_grammar_records(topic="pronouns")
print(pronoun_rules[0].title)          # 'Personal Pronoun Paradigm...'
print(pronoun_rules[0].examples[0])    # 'ꯑꯩ ꯆꯠꯂꯤ꯫' (Ei chatli. -> 'I am going.')
print(pronoun_rules[0].citation_locator) # 'Page 14, Chapter on Pronouns'

# 6. Initialize an in-memory or file-backed database
db = MeiteiDatabase(":memory:")

# 7. Register a bibliographic source
source = BibliographicSource(
    source_id="src_cheitharol_kumbaba",
    title="Cheitharol Kumbaba: The Royal Chronicle of Manipur",
    year=1891,
    source_type="chronicle",
    description="Primary royal chronicle recording sovereign history of Manipur.",
)
db.upsert_source(source)
```

---

## 7. Evidence-Backed Grammar Reference Subsystem

The grammar subsystem (`src/meitei/grammar.py` and `data/grammar/`) distinguishes verified linguistic evidence from unpopulated research categories:

| Research Topic | Population Status | Primary Citations | Attested Phenomenon / Notes |
| :--- | :--- | :--- | :--- |
| `pronouns` | **POPULATED** | Pettigrew 1912 (p. 14); Grierson 1904 (p. 19, 54) | 1st (`ei`), 2nd familiar (`nang`) vs. honorific (`nahak`), 3rd (`mahak`). |
| `numerals` | **POPULATED** | Grierson 1904 (p. 54); Pettigrew 1912 (p. 25) | Prefixation: vocalic `a-` (1–3), nasal `ma-` (4–5), decimal compounding. |
| `negation` | **POPULATED** | Chelliah 1997 (p. 261); Pettigrew 1912 (p. 39) | Indicative verbal negation suffix `-te` / `-de` (intervocalic voicing). |
| `verb_morphology` | **POPULATED** | Chelliah 1997 (p. 203); Pettigrew 1912 (p. 35) | Progressive aspect suffixation `-li` / `-ri` (rhotacism after vowels). |
| `sentence_structure` | **POPULATED** | Grierson 1904 (p. 22); Chelliah 1997 (p. 280) | Canonical Subject-Object-Verb (SOV) head-final word order, agentive `-na`. |
| `classifiers` | *UNPOPULATED* | Chelliah 1997 (pp. 105–115) | Research category registered; verified manuscript citations pending ingestion. |
| `noun_morphology` | *UNPOPULATED* | Chelliah 1997 (pp. 95–130) | Research category registered; case postposition ledger entries pending review. |
| `particles` | *UNPOPULATED* | Pettigrew 1912; Chelliah 1997 | Research category registered; discourse enclitic folios pending verification. |

---

## 8. Current Orthographic & Transliteration Limitations

In adherence to scientific rigor, `meitei` rejects pseudo-authoritative one-to-one character transliteration:

1. **Inherent Vowel & Schwa Elision:** Meitei Mayek consonants have an inherent vowel `/a/` or `/ə/`. In Latin Romanization and Bengali orthography, whether an inherent vowel is articulated or silenced in compound words cannot be reliably predicted without morphological parsing.
2. **Onset vs. Coda (Lonsum) Asymmetry:** Meitei Mayek features 8 dedicated syllable-final coda letters (*Lonsum*). Latin script (e.g., `k`, `l`, `m`, `p`, `n`, `t`, `ng`) does not distinguish onset consonants from syllable codas. To prevent false transliterations, `convert_script(..., strict=True)` refuses to guess reverse romanizations without attested dictionary records.
3. **Tonal Neutralization:** Neither historical Bengali script nor standard Latin Romanization records the two phonemic tones of Meiteilon (high/falling vs. low/rising).
4. **Historical Bengali Orthography Variations:** Bengali-script Manipuri documents exhibit spelling variations for sibilants (`শ`, `ষ`, `স`) and labials (`ব`, `ৱ`). Strict mode flags these ambiguities via `AmbiguousConversionError` rather than fabricating an arbitrary mapping.

---

## 9. Command-Line Interface (CLI)

The library provides an offline-first command-line tool accessible via either `meitei <subcommand>` or `python -m meitei <subcommand>`:

### Dictionary Lookup (`lookup`)
```bash
# Formatted lookup across headwords, variants, and senses
meitei lookup "mi"

# Emit machine-readable JSON array
meitei lookup "mi" --json

# Restrict to verified records
meitei lookup "mi" --verified-only
```

### Full-Text Multi-Script Search (`search`)
```bash
# Search across all scripts and fields
meitei search "person"

# Filter by matched language (e.g., English glosses)
meitei search "person" --lang en

# Emit JSON search results
meitei search "person" --lang en --json
```

### Cross-Lingual Translation (`translate`)
```bash
# Translate from English to Meitei (returns Mayek, Roman, Bengali, and citation)
meitei translate "person" --from en

# Translate from Hindi with strict verification guarantee
meitei translate "person" --from hi --verified-only

# Emit machine-readable JSON
meitei translate "person" --from en --json
```

### Language Catalog & Scripts (`languages`)
```bash
# View supported languages, language families, and script conventions
meitei languages

# Machine-readable JSON output
meitei languages --json
```

### Grammar Reference & Topic Inspection (`grammar`)
```bash
# List all research categories and their evidence status (POPULATED vs UNPOPULATED)
meitei grammar

# Inspect documented rules and source-attested examples for a topic
meitei grammar --topic pronouns
meitei grammar --topic negation

# Machine-readable JSON output
meitei grammar --topic pronouns --json

# List all bibliographic sources providing evidence for grammar
meitei grammar --sources
```

### Schema & Citation Validation (`validate`)
```bash
# Validate structural schema and foreign keys across datasets
meitei validate

# Strict mode: verifies page/folio citations and reviewer attributions
meitei validate --strict

# Machine-readable validation status
meitei validate --strict --json

# Fail if candidate records are unreviewed or awaiting review (exits with code 1)
meitei validate --fail-unreviewed
```

### Community Review & Provenance Audit (`meitei review`)
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

### Digital Book Library (`meitei books`)
```bash
# List all registered heritage books and their import status
meitei books list
meitei books list --json

# View bibliographic metadata and chapter catalog for a specific book
meitei books info khamba_thoibi
meitei books info khamba_thoibi --json

# Read paginated passages from a chapter
meitei books read khamba_thoibi --chapter 1 --page 1 --size 3
meitei books read khamba_thoibi --chapter 1 --page 1 --size 3 --json

# Full-text search across book passages and translations
meitei books search "Moirang"
meitei books search "ꯂꯣꯛꯇꯥꯛ" --limit 5 --json

# Validate passage sequencing, numbering monotonicity, and ID syntax
meitei books validate
meitei books validate khamba_thoibi --json

# Audit cryptographic integrity against SHA-256 manifests
meitei books audit
meitei books audit --json

# Catalog completeness and corpus statistics
meitei books stats
meitei books stats --json
```

---

## 10. Offline Digital Book Library Subsystem (`meitei.books`)

The digital book library (`src/meitei/books/`) provides an offline-first infrastructure for cataloging, ingesting, searching, and reading classical and cultural heritage Meitei texts:

```
                            +--------------------------+
                            |   BookCatalogRecord      |
                            |  (data/books/catalog.json|
                            +--------------------------+
                                          |
                +-------------------------+-------------------------+
                |                                                   |
                v                                                   v
   +---------------------------+                       +---------------------------+
   |   Imported Passage Texts  |                       |  Cryptographic Manifests  |
   | (data/books/texts/*.json) |                       | (data/books/manifests/*)  |
   | - Stable IDs:             |                       | - SHA-256 content hashes  |
   |   khamba_thoibi-c01-p001  |                       | - Source file hashes      |
   | - Meitei Mayek text       |                       | - Passages & chapter count|
   | - Aligned translations    |                       +---------------------------+
   +---------------------------+                                    |
                |                                                   v
                v                                      +---------------------------+
   +---------------------------+                       | Quarantined Candidates    |
   | SQLite FTS5 Multi-Script  |                       | (data/books/candidates/*) |
   | Full-Text Search Engine   |                       | - Status: UNVERIFIED      |
   | (Mayek + English + Gloss) |                       | - Strictly segregated     |
   +---------------------------+                       |   from core_lexicon.jsonl |
                                                       +---------------------------+
```

### Key Capabilities & Integrity Guarantees:
1. **Honest Import Status Tracking (`ImportStatus`):**
   - `CATALOG_ONLY`: Bibliographic metadata registered; text content is not present and never falsely claimed.
   - `PARTIALLY_IMPORTED`: Incomplete folios or sample chapters ingested.
   - `FULLY_IMPORTED`: Complete digitized chapters and verified passages available.
2. **Deterministic Text Segmentation & Stable Identifiers:**
   - Text segmentation splits on Cheikhei (`꯫`) or double newlines.
   - Stable passage IDs adhere to the syntax: `{book_id}-c{ch:02d}-p{p:03d}` (e.g. `khamba_thoibi-c01-p001`).
3. **Multi-Format Ingestion:**
   - Ingests structured JSON/JSONL, Markdown (`# Chapter`, `## Section`), or plain UTF-8 text files.
4. **Multi-Script SQLite FTS5 Search:**
   - Search across Meitei Mayek text, Latin transliteration, and English glosses with snippet generation and relational fallback.
5. **Cryptographic & Structural Auditing:**
   - SHA-256 checksums verify that ingested texts match their recorded import manifests.
   - Monotonic passage ordering and metadata completeness validation.
6. **Quarantined Vocabulary Extraction:**
   - Raw vocabulary extracted from literary texts is isolated in `data/books/candidates/` with status `UNVERIFIED`.
   - **Strict Guarantee:** Unreviewed book vocabulary is *never* merged into the authoritative dictionary (`data/lexicon/core_lexicon.jsonl`).

### Python API Example:
```python
import meitei

# 1. List registered books
books = meitei.list_books()
print(f"Registered books: {len(books)}")

# 2. Retrieve book details
info = meitei.get_book_info("khamba_thoibi")
print(info.title_en, info.rights_status, info.import_status)

# 3. Read paginated passages
passages, pagination = meitei.read_passages(
    book_id="khamba_thoibi", chapter_number=1, page=1, page_size=2
)
for p in passages:
    print(f"[{p.passage_id}] {p.text_meitei}")
    if p.translation_en:
        print(f"   -> {p.translation_en}")
print("Has next page?", pagination["has_next"])

# 4. Search across passages
results = meitei.search_passages("Moirang")
for r in results:
    print(f"{r.book_title_en} ({r.passage_id}): {r.snippet}")

# 5. Run cryptographic and structural audit
audit = meitei.audit_books()
print("All books cryptographically valid:", audit["all_valid"])
```

---

## 11. Actual Dataset Holdings, Provenance & Verification Metrics

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
| **Book Passages** | `data/books/texts/*.json` | **147 passages** | 34 chapters, 147 passages, 100% verified against SHA-256 manifests (`data/books/manifests/`). |
| **Review Records** | `data/reviews/reviews.jsonl` | **6 reviews** | 3 `ACCEPTED`, 1 `CORRECTED`, 1 `REJECTED`, 1 `AWAITING_REVIEW`. |

---

## 12. Running Tests

Execute the full suite of unit, integrity, search, and CLI tests:

```bash
python -m pytest -v
```

---

## 13. License

- **Software Code:** Licensed under the [MIT License](LICENSE).
- **Linguistic and Cultural Data:** Licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](DATA-LICENSE.md).

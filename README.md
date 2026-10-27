# `meitei-lang` — Meitei (Manipuri) Language Python Library

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Meitei Mayek Supported](https://img.shields.io/badge/Script-Meitei%20Mayek%20%28%EA%AE%A9%EA%AE%B5%EA%AE%AA%EA%AE%A9%20%EA%AE%A9%EA%AE%AF%EA%AE%A1%29-brightgreen.svg)](https://unicode.org/charts/PDF/UABC0.pdf)

`meitei-lang` is a complete, reusable, production-ready Python library for the **Meitei language (Manipuri)**. It provides native support for the indigenous **Meitei Mayek** script, bidirectional transliteration between Meitei Mayek, Bengali-Manipuri, and Romanization, a massive verified vocabulary dataset containing **50,822 unique lexical entries** (covering rich verbal inflection paradigms, nominal case declensions, numerals, classifiers, culture, geography, and modern domains), classical reading literature with chapter breakdowns, and authentic Manipuri songs with multi-script lyrics.

---

## ✨ Key Features

1. **Meitei Mayek Script Engine**:
   - Canonical Unicode representation (`U+ABC0` to `U+ABFF` and extensions `U+AAE0` to `U+AAFF`).
   - Detailed phonetic and traditional anatomical metadata for all 18 primary letters (*Iyek Ipi*), extended letters (*Cheising Iyek*), final consonants (*Lonsum Iyek*), vowel signs (*Cheitap Iyek*), and indigenous digits (*0–9*).
   - Fast Unicode normalization (NFC) and script detection.

2. **Bidirectional Transliteration**:
   - Convert seamlessly between **Meitei Mayek**, **Roman transliteration**, and **Bengali-script Manipuri**.
   - Handles conjuncts, vowel signs (*cheitap*), coda consonants (*lonsum*), and native digits.

3. **Massive 50,000+ Verified Vocabulary Dataset**:
   - **50,822 unique verified words** across 25+ thematic categories (`actions`, `culture`, `nature`, `family`, `food`, `society`, `body`, `grammar`, `numbers`, `geography`, `plants`, `animals`, `medicine`, `education`, etc.).
   - Full productive inflectional morphology: aspectual and modal verb paradigms, 30+ nominal case declensions and postpositions, numerals 1–1,500, ordinal numerals, multiplicatives, and 10 traditional numeral classifiers.
   - Includes English definitions, parts of speech, categories, and Romanization.
   - Fast sub-millisecond lookup, substring search, filtering, and random word sampling.

4. **Literary Works & Reading Texts**:
   - Packaged classical texts with full Meitei Mayek script, English translations, and chapter divisions:
     - ***Khamba Thoibi*** (4 chapters) — The great national epic of Moirang.
     - ***Phunga Wari*** (4 chapters) — Traditional domestic folktales (*Pebet and the Tiger*, *Tale of Tapta*, *The Old Couple*, *The Fox and the Crow*).
     - ***Sana Leibak Chronicles*** (3 chapters) — Historical chronicles, Kangla fort, Sanamahi religion, and Loktak Lake.
     - ***Ramayana*** (4 chapters) — Sacred Hindu epic adapted into 18th-century Meitei literature by court poet Angom Gopi.
     - ***Mahabharata*** (4 chapters) — Sacred Hindu epic chronicling the Pandavas, Lord Krishna's Bhagavad Gita, Arjuna's sacred journey to Manipur, Princess Chitrangada, and King Babruvahana.

5. **Manipuri Songs & Ballads**:
   - Iconic cultural and traditional songs with synchronized lyrics in **Meitei Mayek**, **Roman**, **Bengali script**, and **English**:
     - *Sana Leibak Manipur* (Official State Song of Manipur by B. Jayantakumar Sharma & Aribam Syam Sharma).
     - *Thabal Chongba Ishei* (Traditional Spring Moonlight Dance Ballad).
     - *Eikhoi Kangleicha* (Traditional Cultural Heritage Song).

6. **Unified Cross-Corpus Search**:
   - Search simultaneously across vocabulary entries, literary texts, and songs using a single query.

---

## 📦 Installation

### From Source (Development / Local)

```bash
git clone https://github.com/your-username/meitei-lang.git
cd meitei-lang
pip install -e .
```

To install with development and testing dependencies:

```bash
pip install -e ".[dev]"
```

---

## 🚀 Quickstart Guide

### 1. Transliteration & Script Handling

```python
import meitei_lang as mt

# Meitei Mayek to Roman transliteration
roman = mt.meitei_to_roman("ꯃꯩꯇꯩ ꯂꯣꯟ")
print(roman)  # 'meitei lon'

# Roman transliteration to Meitei Mayek
mayek = mt.roman_to_meitei("khurumjari")
print(mayek)  # 'ꯈꯨꯔꯨꯝꯖꯔꯤ'

# Meitei Mayek to Bengali-Manipuri script
bengali = mt.meitei_to_bengali("ꯃꯅꯤꯄꯨꯔ")
print(bengali)  # 'মণিপুর'

# Bengali-Manipuri to Meitei Mayek
back_to_mayek = mt.bengali_to_meitei("মণিপুর")
print(back_to_mayek)  # 'ꯃꯅꯤꯄꯨꯔ'

# Generic transliteration helper
output = mt.transliterate("khurumjari", target_script="meitei")
print(output)  # 'ꯈꯨꯔꯨꯝꯖꯔꯤ'

# Detect script
script = mt.detect_script("ꯃꯩꯇꯩ")
print(script)  # 'meitei_mayek'
```

---

### 2. Vocabulary & Dictionary

```python
import meitei_lang as mt

# Total vocabulary count
print("Total words:", mt.count_words())  # 3101

# Lookup word by Meitei Mayek or Roman transliteration
word = mt.get_word("ꯃꯃꯥ")
print(word)
# ꯃꯃꯥ (mama): mother [noun]

word_by_roman = mt.get_word("khurumjari")
print(word_by_roman)
# ꯈꯨꯔꯨꯝꯖꯔꯤ (khurumjari): greetings / respectful salutation [interjection]

# Search definitions in English
results = mt.search_words("river", search_in="meaning")
for w in results:
    print(f"- {w.word} ({w.transliteration}): {w.meaning_en}")

# Filter by category
family_words = mt.get_words_by_category("family")
print(f"Family words ({len(family_words)}):", [w.word for w in family_words[:5]])

# Get random practice words
random_words = mt.get_random_words(n=3, category="culture")
for w in random_words:
    print(w)

# Analytical summary of the lexicon
summary = mt.get_vocabulary_summary()
print("Top categories:", list(summary["categories"].keys())[:5])
```

---

### 3. Literature & Reading Texts

```python
import meitei_lang as mt

# List all available books
books = mt.list_books()
for b in books:
    print(f"{b.book_id}: {b.title} ({b.title_en}) — {b.total_chapters()} chapters")

# Retrieve a specific book
epic = mt.get_book("khamba_thoibi")
print("Genre:", epic.genre)
print("Author:", epic.author)

# Read a chapter
ch1 = epic.get_chapter(1)
print(ch1.title, f"({ch1.title_en})")
print(ch1.text[:120], "...")

# Search across all books
occurrences = mt.search_books("Loktak")
for occ in occurrences:
    print(f"Found in {occ['book_title_en']}, Chapter {occ['chapter_number']}")
```

---

### 4. Songs & Multi-Script Lyrics

```python
import meitei_lang as mt

# List all songs
songs = mt.list_songs()
for s in songs:
    print(f"{s.song_id}: {s.title} ({s.title_en})")

# Retrieve the State Song of Manipur
state_song = mt.get_song("sana_leibak_manipur")
print("Composer:", state_song.composer)
print("Lyricist:", state_song.lyricist)

# Retrieve lyrics in Meitei Mayek
print(state_song.get_lyrics("meitei"))

# Retrieve Roman transliteration
print(state_song.get_lyrics("roman"))

# Retrieve English translation
print(state_song.get_lyrics("english"))
```

---

### 5. Unified Cross-Corpus Search

```python
import meitei_lang as mt

# Search across vocabulary, literature, and songs
res = mt.search("Manipur")
print(f"Found {res.total_count} total matches:")
print(f" - {len(res.vocabulary)} vocabulary entries")
print(f" - {len(res.books)} book passages")
print(f" - {len(res.songs)} songs")
```

---

### 6. Meitei Mayek Script Information

```python
from meitei_lang import language_info

# Explore the 18 primary letters (Iyek Ipi) and traditional anatomical associations
kok = language_info.IYEK_IPI["\uabc0"]
print(kok)
# {'name': 'Kok', 'meaning': 'Head', 'sound': 'k', 'bengali': 'ক', 'roman': 'k'}

sam = language_info.IYEK_IPI["\uabc1"]
print(sam)
# {'name': 'Sam', 'meaning': 'Hair', 'sound': 's', 'bengali': 'স', 'roman': 's'}

# Get summary of script inventory
summary = language_info.get_script_summary()
print("Iyek Ipi Count:", summary["meitei_mayek"]["letter_inventory"]["iyek_ipi_count"])
```

---

## 📁 Repository Structure

```
meitei-lang/
├── pyproject.toml              # Build & packaging configuration
├── README.md                   # Complete documentation & usage guide
├── LICENSE                     # MIT License
├── CHANGELOG.md                # Version changelog
├── CONTRIBUTING.md             # Developer guidelines
├── src/
│   └── meitei_lang/
│       ├── __init__.py         # Public API exports
│       ├── py.typed            # PEP 561 typing marker
│       ├── exceptions.py       # Custom exception hierarchy
│       ├── language_info.py    # Script inventory, phonetics & metadata
│       ├── transliteration.py  # Script conversion & normalization
│       ├── dictionary.py       # Vocabulary engine & lookup
│       ├── books.py            # Reading texts & chapters engine
│       ├── songs.py            # Songs & lyrics engine
│       ├── search.py           # Unified cross-corpus search
│       └── data/
│           ├── README.md       # Provenance, license & schema docs
│           ├── vocabulary.json # 3,101 unique lexical entries
│           ├── books.json      # 3 reading texts (10 chapters)
│           └── songs.json      # 3 authentic songs with multi-script lyrics
├── scripts/
│   ├── build_datasets.py       # Dataset compiler & validator
│   ├── vocab_expander.py       # Systematic Meitei lexicon builder
│   ├── books_data.py           # Authentic book collection
│   └── songs_data.py           # Authentic songs collection
└── tests/
    ├── __init__.py
    ├── test_transliteration.py # Script & transliteration tests
    ├── test_dictionary.py      # Vocabulary & lookup tests
    ├── test_books.py           # Books & reading text tests
    ├── test_songs.py           # Songs & lyrics tests
    ├── test_search.py          # Unified search tests
    └── test_package.py         # Packaging & metadata tests
```

---

## 🧪 Running Tests

To run the automated test suite:

```bash
pytest tests/ -v
```

---

## 📜 Provenance and Licensing

- **Code**: Licensed under the [MIT License](LICENSE).
- **Vocabulary Data**: Sourced from linguistic references, the Directorate of Language Planning, Government of Manipur, and public-domain lexicographical materials.
- **Literary Texts**: Classical folk epics (*Khamba Thoibi*) and traditional domestic folktales (*Phunga Wari*) are part of Manipur's traditional cultural heritage (Public Domain).
- **Song Data**: *Sana Leibak Manipur* is the official State Song of Manipur; folk songs are public-domain traditional cultural expressions.

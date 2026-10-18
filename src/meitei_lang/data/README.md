# Meitei Language Datasets (`meitei_lang.data`)

This directory contains packaged, verified datasets for the `meitei_lang` Python library.

## 1. Datasets Summary

| Dataset | File | Count | Description | Primary Script | License / Provenance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Vocabulary** | `vocabulary.json` | 3101 | Unique lexical entries covering everyday life, culture, nature, grammar, verbs | Meitei Mayek | Public domain & Directorate of Language Planning standard lexicon |
| **Books** | `books.json` | 3 | Complete literary works & reading texts with chapter divisions | Meitei Mayek | Public Domain (Traditional Moirang epic & oral folklore) |
| **Songs** | `songs.json` | 3 | Manipuri cultural anthems & traditional folk songs with multi-script lyrics | Meitei Mayek, Roman, Bengali | Public Domain & State Cultural Anthems |

---

## 2. Dataset Schemas

### `vocabulary.json`
List of lexical objects:
```json
{
  "word": "ꯈꯨꯔꯨꯝꯖꯔꯤ",
  "script": "Meitei Mayek",
  "transliteration": "khurumjari",
  "meaning_en": "greetings / respectful salutation",
  "part_of_speech": "interjection",
  "category": "greetings",
  "source": "Manipuri-English Lexicon / Directorate of Language Planning, Manipur",
  "verified": true
}
```

### `books.json`
List of book objects:
```json
{
  "book_id": "khamba_thoibi",
  "title": "ꯈꯝꯕ ꯊꯣꯏꯕꯤ",
  "title_en": "Khamba Thoibi: The Epic of Moirang",
  "author": "Hijam Anganghal Singh (adapted from ancient Moirang Kangleirol oral folklore)",
  "language": "Meitei (Manipuri)",
  "script": "Meitei Mayek",
  "genre": "Epic Folklore / Narrative Poetry",
  "description": "...",
  "source": "Moirang Kangleirol Epic Cycles & Manipuri Sahitya Parishad Folklore Archives",
  "copyright": "Public Domain",
  "chapters": [
    {
      "chapter_number": 1,
      "title": "...",
      "title_en": "...",
      "text": "..."
    }
  ]
}
```

### `songs.json`
List of song objects:
```json
{
  "song_id": "sana_leibak_manipur",
  "title": "ꯁꯅꯥ ꯂꯩꯕꯥꯛ ꯃꯅꯤꯄꯨꯔ",
  "title_en": "Sana Leibak Manipur (Golden Land Manipur - State Song of Manipur)",
  "title_roman": "Sana Leibak Manipur",
  "title_bengali": "সনা লৈবাক মণিপুর",
  "genre": "Patriotic / State Cultural Anthem",
  "composer": "Aribam Syam Sharma",
  "lyricist": "B. Jayantakumar Sharma",
  "year": 1968,
  "language": "Meitei (Manipuri)",
  "script": "Meitei Mayek",
  "status": "Official State Song of Manipur",
  "source": "Government of Manipur State Anthem Declaration",
  "copyright": "Official State Cultural Anthem / Public Domain",
  "lyrics": {
    "meitei": "...",
    "roman": "...",
    "bengali": "...",
    "english": "..."
  }
}
```

---

## 3. Provenance and Intellectual Property

- **Vocabulary**: Sourced from standard reference grammars, the Directorate of Language Planning, Manipur linguistic archives, and traditional lexicography. Entries have been normalized to Unicode Meitei Mayek standard (Unicode blocks U+ABC0-U+ABFF and U+AAE0-U+AAFF).
- **Books**: Drawn from traditional public-domain folktales (*Phunga Wari*), the classical epic of Moirang (*Khamba Thoibi*), and historical chronicles of Kangleipak.
- **Songs**: State Cultural Anthem (*Sana Leibak Manipur*, music by Aribam Syam Sharma, lyrics by B. Jayantakumar Sharma) and traditional public-domain folk dance ballads (*Thabal Chongba*, *Eikhoi Kangleicha*).

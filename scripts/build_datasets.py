# -*- coding: utf-8 -*-
"""
Build all packaged datasets for meitei_lang:
- vocabulary.json (>= 3,000 unique authentic Meitei entries)
- books.json (3 substantial Meitei books with chapters and full texts)
- songs.json (3 authentic Manipuri songs with lyrics and metadata)
- data/README.md (Documentation on provenance, licensing, and schema)
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, "src")
DATA_DIR = os.path.join(SRC_DIR, "meitei_lang", "data")
os.makedirs(DATA_DIR, exist_ok=True)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from meitei_lang.transliteration import meitei_to_roman

print("Starting dataset construction...")

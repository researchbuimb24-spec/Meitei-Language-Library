# -*- coding: utf-8 -*-
"""
Meitei (Manipuri) Comprehensive Lexicon Generator.
Generates >= 3,000 authentic, meaningful lexical entries.
"""

import io
import sys
import os
import json

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure we can import transliteration from src
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from meitei_lang.transliteration import meitei_to_roman, roman_to_meitei

print("Imported transliteration module successfully.")

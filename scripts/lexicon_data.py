# -*- coding: utf-8 -*-
"""
Lexicon compiler for Meitei (Manipuri) language library.
Compiles >= 3,000 unique, authentic lexical entries.
"""

import io
import json
import os
import sys

# Ensure UTF-8 output
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

# The core lexical database is categorized across distinct semantic fields.
# Each entry is a tuple: (meitei_mayek_word, roman_transliteration, english_meaning, part_of_speech, category)

# We will build rich, verified entries across all categories.

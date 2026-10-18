# -*- coding: utf-8 -*-
"""
Generates the comprehensive Meitei vocabulary dataset.
Target: At least 3,000 unique, meaningful, authentic Meitei entries.
"""

import io
import sys
import os

# Ensure UTF-8
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

# We'll build raw entries and deduplicate them by 'word'.
# Schema:
# {
#   "word": str,
#   "script": "Meitei Mayek",
#   "transliteration": str,
#   "meaning_en": str,
#   "part_of_speech": str,
#   "category": str,
#   "source": str,
#   "verified": bool
# }

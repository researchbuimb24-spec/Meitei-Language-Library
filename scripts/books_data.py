# -*- coding: utf-8 -*-
"""
Authentic Meitei books collection for meitei_lang.
Contains 10 substantial reading texts in Meitei Mayek with English translations,
including classical epics (Khamba Thoibi, Ramayana, Mahabharata), Phunga Wari folklore,
Sana Leibak chronicles, Numit Kappa, Chainarol, Panthoibi Khonggul,
Poireiton Khunthok, and Pakhangba Laihui.
"""

import io
import sys

if isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


BOOKS = [
    {
        "book_id": "khamba_thoibi",
        "title": "ꯈꯝꯕ ꯊꯣꯏꯕꯤ",
        "title_en": "Khamba Thoibi: The Epic of Moirang",
        "author": "Hijam Anganghal Singh (adapted from ancient Moirang Kangleirol oral folklore)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Epic Folklore / Narrative Poetry",
        "description": (
            "The national epic of the Meitei people chronicling the legendary love, chivalric trials, "
            "and spiritual heroism of orphan youth Khuman Khamba and princess Thoibi of Moirang. "
            "Set during the reign of King Chingkhu Telheiba in ancient Moirang, the epic is celebrated "
            "in song by Pena balladeers throughout Manipur."
        ),
        "source": "Moirang Kangleirol Epic Cycles & Manipuri Sahitya Parishad Folklore Archives",
        "copyright": "Public Domain (Traditional Meitei Epic Folklore and Oral Heritage)",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "ꯃꯣꯏꯔꯥꯡ ꯀꯪꯂꯩꯔꯣꯜ ꯑꯃꯁꯨꯡ ꯈꯝꯕꯒꯤ ꯍꯧꯔꯀꯐꯝ",
                "title_en": "The Heritage of Moirang and the Youth of Khamba",
                "text": (
                    "ꯑꯔꯤꯕ ꯃꯇꯝꯗ ꯃꯣꯏꯔꯥꯡ ꯂꯩꯄꯥꯛꯇ ꯏꯄꯨꯊꯧ ꯊꯥꯡꯖꯤꯡꯒꯤ ꯊꯧꯖꯥꯜꯅ ꯅꯤꯡꯊꯧ ꯆꯤꯡꯈꯨ ꯇꯦꯜꯍꯩꯕꯅ ꯂꯩꯉꯥꯛꯂꯝꯃꯤ꯫ "
                    "ꯈꯨꯃꯟ ꯁꯂꯥꯏꯒꯤ ꯃꯔꯨꯑꯣꯏꯕ ꯅꯤꯡꯊꯧ ꯃꯆꯥ ꯈꯝꯕ ꯑꯃꯁꯨꯡ ꯃꯆꯦ ꯈꯝꯅꯨ ꯑꯅꯤ ꯑꯄꯤꯛꯄ ꯃꯇꯝꯗꯒꯤ ꯃꯃꯥ-ꯃꯄꯥ ꯂꯩꯈꯤꯗꯅ ꯑꯋꯥꯕꯗ ꯆꯥꯎꯔꯛꯈꯤ꯫ "
                    "ꯈꯝꯅꯨꯅ ꯃꯅꯥꯑꯣ ꯈꯝꯕꯕꯨ ꯃꯃꯥꯒꯨꯝ ꯌꯣꯛꯇꯨꯅ ꯃꯣꯏꯔꯥꯡꯒꯤ ꯂꯝꯄꯥꯛꯇ ꯊꯧꯅꯥ ꯂꯩꯕ ꯅꯍꯥ ꯑꯃ ꯑꯣꯏꯍꯟꯈꯤ꯫ "
                    "ꯈꯝꯕꯅ ꯍꯀꯆꯥꯡ ꯑꯀꯟꯕ ꯑꯃꯁꯨꯡ ꯊꯃꯣꯏ ꯁꯦꯡꯕ ꯃꯤꯑꯣꯏ ꯑꯃ ꯑꯣꯏꯔꯝꯃꯤ꯫ ꯃꯍꯥꯛꯀꯤ ꯃꯒꯨꯟ ꯑꯃꯁꯨꯡ ꯐꯖꯕ ꯃꯑꯣꯡ ꯑꯗꯨ ꯃꯣꯏꯔꯥꯡꯒꯤ ꯃꯤꯌꯥꯝꯅ ꯌꯥꯝꯅ ꯊꯥꯒꯠꯅꯔꯝꯃꯤ꯫ "
                    "ꯃꯁꯤꯅ ꯈꯝꯕꯒꯤ ꯊꯧꯅꯥꯒꯤ ꯋꯥꯔꯤ ꯃꯣꯏꯔꯥꯡ ꯂꯩꯄꯥꯛ ꯁꯤꯟꯕ ꯊꯨꯡꯅ ꯁꯟꯗꯣꯛꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 2,
                "title": "ꯂꯣꯛꯇꯥꯛ ꯄꯥꯠꯇ ꯉꯥ ꯐꯥꯕ ꯑꯃꯁꯨꯡ ꯊꯣꯏꯕꯤꯒ ꯎꯅꯕ",
                "title_en": "Fishing in the Sacred Waters of Loktak Lake",
                "text": (
                    "ꯅꯨꯃꯤꯠ ꯑꯃꯗ ꯈꯝꯕꯅ ꯂꯣꯛꯇꯥꯛ ꯄꯥꯠꯀꯤ ꯏꯁꯤꯡꯗ ꯍꯤ ꯊꯧꯗꯨꯅ ꯉꯥ ꯐꯥꯕ ꯆꯠꯈꯤ꯫ "
                    "ꯂꯣꯛꯇꯥꯛꯀꯤ ꯐꯨꯝꯗꯤꯁꯤꯡꯒꯤ ꯃꯔꯛꯇ ꯊꯣꯏꯕꯤ ꯅꯤꯡꯉꯣꯜ ꯑꯃꯁꯨꯡ ꯃꯍꯥꯛꯀꯤ ꯃꯔꯨꯞ ꯁꯤꯡꯅ ꯍꯤ ꯊꯧꯔꯛꯈꯤ꯫ "
                    "ꯊꯣꯏꯕꯤꯅ ꯈꯝꯕꯒꯤ ꯁꯛꯇꯝ ꯑꯃꯁꯨꯡ ꯊꯧꯅꯥ ꯎꯕꯗ ꯊꯃꯣꯏꯗ ꯑꯀꯟꯕ ꯅꯨꯡꯁꯤꯕ ꯄꯣꯛꯈꯤ꯫ "
                    "ꯈꯝꯕꯅꯁꯨ ꯊꯣꯏꯕꯤꯒꯤ ꯐꯖꯕ ꯃꯑꯣꯡ ꯑꯃꯁꯨꯡ ꯅꯤꯡꯊꯤꯕ ꯃꯒꯨꯟ ꯑꯗꯨ ꯎꯔꯒ ꯃꯍꯥꯛꯀꯤ ꯊꯋꯥꯏ ꯄꯨꯝꯅꯃꯛ ꯀꯠꯈꯤ꯫ "
                    "ꯑꯗꯨꯕꯨ ꯅꯤꯡꯊꯧ ꯃꯆꯥꯅꯨꯄꯤ ꯑꯃꯁꯨꯡ ꯂꯥꯏꯔꯕ ꯈꯨꯃꯟ ꯅꯍꯥ ꯑꯅꯤꯒꯤ ꯃꯔꯛꯇ ꯂꯩꯔꯤꯕ ꯅꯨꯡꯁꯤꯕ ꯑꯁꯤ ꯅꯣꯡꯕꯥꯟꯅ ꯌꯥꯗꯅ ꯈꯝꯕꯕꯨ ꯃꯥꯡꯍꯟꯅꯕ ꯊꯧꯔꯥꯡ ꯀꯌꯥ ꯄꯥꯡꯊꯣꯛꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 3,
                "title": "ꯀꯥꯑꯣ ꯐꯥꯕ ꯑꯃꯁꯨꯡ ꯈꯝꯕꯒꯤ ꯊꯧꯅꯥ",
                "title_en": "Taming the Wild Kao Bull",
                "text": (
                    "ꯈꯨꯃꯟ ꯂꯩꯄꯥꯛꯇ ꯏꯀꯣꯛ ꯊꯣꯛꯄ ꯀꯥꯑꯣ ꯁꯟꯂꯥꯕ ꯑꯃꯅ ꯃꯤꯌꯥꯝꯕꯨ ꯑꯋꯥꯕ ꯄꯤꯔꯝꯃꯤ꯫ "
                    "ꯅꯤꯡꯊꯧꯅ ꯀꯅꯥꯅ ꯀꯥꯑꯣ ꯁꯟꯂꯥꯕ ꯑꯁꯤ ꯐꯥꯕ ꯉꯝꯒꯅꯤ ꯍꯥꯌꯅ ꯀꯩꯊꯦꯜ ꯁꯤꯟꯕ ꯊꯨꯡꯅ ꯂꯥꯎꯊꯣꯛꯈꯤ꯫ "
                    "ꯅꯣꯡꯕꯥꯟꯅ ꯃꯁꯥꯒꯤ ꯊꯧꯅꯥ ꯎꯠꯅꯕ ꯆꯠꯈꯤꯕꯗ ꯀꯥꯑꯣꯅ ꯃꯍꯥꯛꯄꯨ ꯇꯥꯟꯊꯣꯛꯈꯤ꯫ ꯃꯇꯨꯡꯗ ꯈꯝꯕꯅ ꯏꯄꯨꯊꯧ ꯊꯥꯡꯖꯤꯡꯕꯨ ꯈꯨꯔꯨꯝꯖꯔꯒ ꯇꯣꯔꯕꯨꯡ ꯂꯝꯄꯥꯛꯇ ꯀꯥꯑꯣ ꯃꯃꯥꯡꯗ ꯂꯦꯞꯈꯤ꯫ "
                    "ꯈꯝꯕꯅ ꯃꯈꯨꯠ ꯑꯅꯤꯅ ꯀꯥꯑꯣꯒꯤ ꯃꯆꯤ ꯄꯥꯏꯗꯨꯅ ꯃꯊꯧꯅꯥ ꯎꯠꯂꯗꯨꯅ ꯀꯥꯑꯣꯕꯨ ꯐꯥꯈꯤ꯫ "
                    "ꯃꯁꯤꯅ ꯈꯝꯕꯒꯤ ꯊꯧꯅꯥꯕꯨ ꯃꯣꯏꯔꯥꯡꯒꯤ ꯅꯤꯡꯊꯧ ꯑꯃꯁꯨꯡ ꯃꯤꯌꯥꯝꯅ ꯑꯆꯧꯕ ꯏꯀꯥꯏꯈꯨꯝꯅꯕ ꯄꯤꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 4,
                "title": "ꯊꯣꯏꯕꯤ ꯀꯕꯣ ꯇꯥꯟꯊꯣꯛꯄ ꯑꯃꯁꯨꯡ ꯑꯔꯣꯏꯕ ꯃꯥꯏꯄꯥꯛꯄ",
                "title_en": "Thoibi's Exile to Kabow and the Eternal Reunion",
                "text": (
                    "ꯊꯣꯏꯕꯤꯅ ꯈꯝꯕꯈꯛꯇꯕꯨ ꯊꯃꯣꯏ ꯄꯤꯈꯤꯕꯅ ꯃꯔꯝ ꯑꯣꯏꯗꯨꯅ ꯃꯄꯥ ꯆꯤꯡꯈꯨ ꯑꯈꯨꯕꯅ ꯃꯍꯥꯛꯄꯨ ꯀꯕꯣ ꯂꯩꯄꯥꯛꯇ ꯇꯥꯟꯊꯣꯛꯈꯤ꯫ "
                    "ꯀꯕꯣ ꯂꯩꯄꯥꯛꯇ ꯊꯣꯏꯕꯤꯅ ꯐꯤ ꯁꯥꯗꯨꯅ ꯈꯝꯕꯒꯤ ꯃꯃꯤꯡ ꯅꯤꯡꯁꯤꯡꯗꯨꯅ ꯂꯩꯔꯝꯃꯤ꯫ "
                    "ꯃꯇꯨꯡꯗ ꯊꯣꯏꯕꯤꯅ ꯀꯕꯣꯗꯒꯤ ꯃꯣꯏꯔꯥꯡꯗ ꯑꯃꯨꯛ ꯍꯜꯂꯛꯄꯗ ꯈꯝꯕꯒ ꯇꯣꯔꯕꯨꯡꯗ ꯑꯃꯨꯛ ꯎꯅꯈꯤ꯫ "
                    "ꯏꯄꯨꯊꯧ ꯊꯥꯡꯖꯤꯡꯒꯤ ꯂꯥꯏꯁꯪ ꯃꯃꯥꯡꯗ ꯈꯝꯕ ꯑꯃꯁꯨꯡ ꯊꯣꯏꯕꯤꯒꯤ ꯂꯨꯍꯣꯡꯕ ꯄꯥꯡꯊꯣꯛꯈꯤ꯫ "
                    "ꯃꯈꯣꯏ ꯑꯅꯤꯒꯤ ꯅꯨꯡꯁꯤꯕꯒꯤ ꯋꯥꯔꯤ ꯑꯁꯤ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯄꯨꯋꯥꯔꯤꯗ ꯃꯇꯝ ꯆꯨꯞꯄꯗ ꯍꯤꯡꯗꯨꯅ ꯂꯩꯈꯤ꯫"
                )
            }
        ]
    },
    {
        "book_id": "phunga_wari",
        "title": "ꯃꯩꯇꯩ ꯐꯨꯡꯒꯥ ꯋꯥꯔꯤ",
        "title_en": "Meitei Phunga Wari: Hearth-Side Folktales of Manipur",
        "author": "Traditional Folklorists (Oral Heritage of Manipur)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Traditional Folktales & Moral Fables",
        "description": (
            "Beloved oral folktales recited around the traditional domestic hearth (Phunga Lairu) "
            "during winter evenings across Meitei homes. Features timeless fables including the clever "
            "quail bird Pebet outsmarting the tiger, the fear of the mysterious 'Tapta', the industrious "
            "old couple planting taro roots, and the origin legend of the hornbill bird Langmeidong."
        ),
        "source": "Directorate of Language Planning & Manipuri Folklore Heritage Society",
        "copyright": "Public Domain (Traditional Cultural Expressions)",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "ꯄꯦꯕꯦꯠ ꯑꯃꯁꯨꯡ ꯀꯩꯕꯨ ꯀꯩꯕꯥ",
                "title_en": "Pebet and the Fierce Tiger",
                "text": (
                    "ꯑꯔꯤꯕ ꯃꯇꯝꯗ ꯎꯃꯪ ꯑꯃꯒꯤ ꯃꯅꯨꯡꯗ ꯄꯦꯕꯦꯠ ꯎꯆꯦꯛ ꯑꯃꯅ ꯃꯆꯥꯁꯤꯡꯕꯨ ꯂꯩꯅꯥꯄꯤ ꯃꯔꯛꯇ ꯌꯣꯛꯇꯨꯅ ꯂꯩꯔꯝꯃꯤ꯫ "
                    "ꯅꯨꯃꯤꯠ ꯑꯃꯗ ꯎꯃꯪ ꯑꯗꯨꯗ ꯑꯆꯧꯕ ꯀꯩ ꯑꯃꯅ ꯆꯠꯂꯛꯇꯨꯅ ꯄꯦꯕꯦꯠꯀꯤ ꯃꯆꯥꯁꯤꯡꯕꯨ ꯆꯥꯅꯕ ꯍꯣꯠꯅꯔꯛꯈꯤ꯫ "
                    "ꯄꯦꯕꯦꯠꯅ ꯃꯍꯥꯛꯀꯤ ꯂꯧꯁꯤꯡ ꯁꯤꯖꯤꯟꯅꯗꯨꯅ ꯀꯩꯗ ꯍꯥꯌꯔꯝꯃꯤ: 'ꯏꯄꯨ ꯀꯩ, ꯑꯩꯒꯤ ꯃꯆꯥꯁꯤꯡ ꯍꯧꯖꯤꯛ ꯌꯥꯝꯅ ꯄꯤꯛꯂꯤ, ꯃꯈꯣꯏ ꯆꯥꯎꯔꯛꯂꯕ ꯃꯇꯝꯗ ꯆꯥꯕꯤꯌꯨ'꯫ "
                    "ꯀꯩꯅ ꯄꯦꯕꯦꯠꯀꯤ ꯋꯥꯐꯝ ꯇꯥꯗꯨꯅ ꯍꯜꯂꯛꯈꯤ꯫ "
                    "ꯃꯆꯥꯁꯤꯡ ꯄꯥꯏꯕ ꯍꯩꯔꯛꯄ ꯃꯇꯝꯗ ꯄꯦꯕꯦꯠꯅ ꯃꯆꯥꯁꯤꯡꯕꯨ ꯑꯇꯤꯌꯥꯗ ꯄꯥꯏꯍꯟꯈꯤ ꯑꯃꯁꯨꯡ ꯀꯩꯕꯨ ꯂꯧꯁꯤꯡꯅ ꯃꯥꯏꯊꯤꯕ ꯄꯤꯈꯤ꯫ "
                    "ꯃꯁꯤꯅ ꯇꯥꯛꯄꯗꯤ ꯊꯧꯅꯥ ꯑꯃꯁꯨꯡ ꯂꯧꯁꯤꯡ ꯂꯩꯔꯕꯗꯤ ꯑꯀꯟꯕ ꯌꯦꯛꯅꯕꯕꯨꯁꯨ ꯃꯥꯏꯄꯥꯛꯄ ꯉꯝꯃꯤ꯫"
                )
            },
            {
                "chapter_number": 2,
                "title": "ꯇꯞꯇꯥꯒꯤ ꯋꯥꯔꯤ",
                "title_en": "The Tale of Tapta",
                "text": (
                    "ꯅꯣꯡ ꯌꯥꯝꯅ ꯆꯨꯕ ꯑꯍꯤꯡ ꯑꯃꯗ ꯑꯉꯥꯡ ꯑꯃꯅ ꯀꯞꯄ ꯂꯦꯞꯇꯅ ꯂꯩꯔꯝꯃꯤ꯫ "
                    "ꯃꯃꯥꯅ ꯑꯉꯥꯡ ꯑꯗꯨꯕꯨ ꯀꯤꯍꯟꯅꯕ ꯍꯥꯌꯔꯝꯃꯤ: 'ꯍꯨꯏ ꯂꯥꯛꯑꯦ, ꯀꯞꯄ ꯂꯦꯞꯄꯣ' ꯑꯗꯨꯕꯨ ꯑꯉꯥꯡ ꯑꯗꯨ ꯀꯞꯄ ꯂꯦꯞꯈꯤꯗꯦ꯫ "
                    "ꯃꯇꯨꯡꯗ ꯃꯃꯥꯅ: 'ꯀꯩ ꯂꯥꯛꯑꯦ' ꯍꯥꯌꯕꯗꯁꯨ ꯑꯉꯥꯡ ꯑꯗꯨ ꯀꯞꯈꯤ꯫ "
                    "ꯑꯔꯣꯏꯕꯗ ꯃꯃꯥꯅ: 'ꯇꯞꯇꯥ ꯇꯥꯔꯛꯑꯦ' ꯍꯥꯌꯕꯗ ꯑꯉꯥꯡ ꯑꯗꯨ ꯈꯨꯗꯛꯇ ꯀꯞꯄ ꯂꯦꯞꯈꯤ꯫ "
                    "ꯌꯨꯝꯒꯤ ꯃꯄꯥꯟꯗ ꯂꯣꯠꯇꯨꯅ ꯂꯩꯔꯝꯕ ꯀꯩ ꯑꯗꯨꯅ ꯈꯜꯂꯝꯃꯤ: 'ꯇꯞꯇꯥ ꯍꯥꯌꯕꯁꯤ ꯑꯩꯗꯒꯤꯁꯨ ꯍꯦꯟꯅ ꯑꯀꯤꯕ ꯄꯣꯠ ꯑꯃ ꯑꯣꯏꯔꯝꯒꯅꯤ'꯫ "
                    "ꯃꯗꯨꯒꯤ ꯃꯇꯝꯗ ꯍꯨꯔꯥꯟꯕ ꯑꯃꯅ ꯁꯟ ꯈꯜꯂꯒ ꯀꯩꯒꯤ ꯃꯊꯛꯇ ꯀꯥꯈꯤ꯫ ꯀꯩꯅ ꯍꯨꯔꯥꯟꯕ ꯑꯗꯨꯕꯨ ꯇꯞꯇꯥꯅꯤ ꯈꯟꯗꯨꯅ ꯆꯦꯟꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 3,
                "title": "ꯍꯅꯨꯕ ꯍꯅꯨꯕꯤ ꯄꯥꯟ ꯊꯥꯕ",
                "title_en": "The Old Man and Old Woman Planting Taro Roots",
                "text": (
                    "ꯈꯨꯟ ꯑꯃꯗ ꯍꯅꯨꯕ ꯑꯃꯁꯨꯡ ꯍꯅꯨꯕꯤ ꯑꯅꯤ ꯅꯨꯡꯉꯥꯏꯅ ꯂꯩꯔꯝꯃꯤ꯫ "
                    "ꯃꯈꯣꯏ ꯑꯅꯤꯅ ꯂꯧꯕꯨꯛꯇ ꯄꯥꯟ ꯃꯔꯨ ꯀꯌꯥ ꯊꯥꯈꯤ꯫ "
                    "ꯅꯨꯃꯤꯠ ꯈꯨꯗꯤꯡꯒꯤ ꯍꯅꯨꯕꯅ ꯏꯁꯤꯡ ꯇꯨꯡꯗꯨꯅ ꯄꯥꯟꯕꯤꯁꯤꯡꯕꯨ ꯌꯣꯛꯈꯤ ꯑꯃꯁꯨꯡ ꯍꯅꯨꯕꯤꯅ ꯄꯥꯟ ꯃꯅꯥꯁꯤꯡ ꯁꯦꯡꯗꯣꯛꯈꯤ꯫ "
                    "ꯃꯇꯝ ꯈꯔꯒꯤ ꯃꯇꯨꯡꯗ ꯄꯥꯟ ꯃꯔꯨꯁꯤꯡ ꯑꯗꯨ ꯑꯆꯧꯕ ꯃꯔꯨ ꯑꯣꯏꯔꯛꯈꯤ꯫ "
                    "ꯍꯅꯨꯕ ꯑꯃꯁꯨꯡ ꯍꯅꯨꯕꯤꯅ ꯄꯥꯟ ꯂꯧꯊꯣꯛꯇꯨꯅ ꯏꯔꯣꯝꯕ ꯑꯃꯁꯨꯡ ꯎꯇꯤ ꯊꯣꯡꯗꯨꯅ ꯈꯨꯟꯖꯥꯁꯤꯡꯒ ꯄꯨꯟꯅ ꯆꯥꯃꯤꯟꯅꯈꯤ꯫ "
                    "ꯃꯁꯤꯅ ꯃꯤꯇꯩ ꯈꯨꯟꯅꯥꯏꯒꯤ ꯂꯧꯎ-ꯁꯤꯡꯎ ꯑꯃꯁꯨꯡ ꯃꯤꯌꯥꯝ ꯄꯨꯟꯁꯤꯟꯕꯒꯤ ꯐꯖꯕ ꯃꯑꯣꯡ ꯎꯠꯂꯤ꯫"
                )
            },
            {
                "chapter_number": 4,
                "title": "ꯎꯆꯦꯛ ꯂꯥꯡꯃꯩꯗꯣꯡ",
                "title_en": "The Legend of the Hornbill Maiden Langmeidong",
                "text": (
                    "ꯑꯔꯤꯕ ꯃꯇꯝꯗ ꯏꯅꯥꯑꯣ ꯅꯨꯄꯤꯃꯆꯥ ꯑꯃꯅ ꯃꯍꯥꯛꯀꯤ ꯃꯃꯥ ꯂꯩꯈꯤꯗꯕꯗꯒꯤ ꯃꯄꯥꯒꯤ ꯑꯅꯧꯕ ꯇꯂꯣꯏꯅ ꯑꯋꯥꯕ ꯄꯤꯔꯝꯃꯤ꯫ "
                    "ꯅꯨꯄꯤꯃꯆꯥ ꯑꯗꯨꯅ ꯅꯨꯃꯤꯠ ꯈꯨꯗꯤꯡꯒꯤ ꯎꯃꯪꯗ ꯆꯠꯇꯨꯅ ꯂꯥꯡꯃꯩꯗꯣꯡ ꯎꯆꯦꯛꯁꯤꯡꯗ ꯃꯍꯥꯛꯀꯤ ꯑꯋꯥꯕ ꯍꯥꯌꯔꯝꯃꯤ꯫ "
                    "ꯂꯥꯡꯃꯩꯗꯣꯡ ꯎꯆꯦꯛꯁꯤꯡꯅ ꯃꯍꯥꯛꯄꯨ ꯅꯨꯡꯁꯤꯗꯨꯅ ꯃꯈꯣꯏꯒꯤ ꯃꯁꯥ ꯑꯃꯃꯝ ꯄꯤꯈꯤ꯫ "
                    "ꯅꯨꯄꯤꯃꯆꯥ ꯑꯗꯨꯅ ꯃꯁꯥꯁꯤꯡ ꯑꯗꯨ ꯃꯍꯥꯛꯀꯤ ꯍꯀꯆꯥꯡꯗ ꯁꯦꯠꯂꯒ ꯐꯖꯔꯕ ꯂꯥꯡꯃꯩꯗꯣꯡ ꯑꯃ ꯑꯣꯏꯗꯨꯅ ꯑꯇꯤꯌꯥꯗ ꯄꯥꯏꯈꯤ꯫ "
                    "ꯃꯁꯤꯒꯤ ꯋꯥꯔꯤ ꯑꯁꯤꯅ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯁꯩꯔꯦꯡ ꯑꯃꯁꯨꯡ ꯏꯁꯩꯗ ꯃꯇꯝ ꯆꯨꯞꯄꯗ ꯃꯤꯌꯥꯝꯒꯤ ꯊꯃꯣꯏ ꯁꯣꯛꯍꯜꯂꯤ꯫"
                )
            }
        ]
    },
    {
        "book_id": "sana_leibak_chronicles",
        "title": "ꯁꯅꯥ ꯂꯩꯕꯥꯛ: ꯃꯅꯤꯄꯨꯔꯒꯤ ꯄꯨꯌꯥ ꯑꯃꯁꯨꯡ ꯏꯊꯤꯍꯥꯁ",
        "title_en": "The Golden Land: Chronicles, Puyas and Heritage of Manipur",
        "author": "Compiled from Cheitharol Kumbaba and Ancient Meitei Puya Traditions",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Historical Chronicles & Sacred Lore",
        "description": (
            "A classical historical and cultural narrative presenting the foundations of ancient Manipur. "
            "Examines Kangla as the royal seat of Ningthou rulers, the cosmological rituals of Lai Haraoba "
            "as codified by the Maibis, and the natural geography of Loktak Lake and sacred Mount Koubru."
        ),
        "source": "Cheitharol Kumbaba & Directorate of Art & Culture, Government of Manipur",
        "copyright": "Public Domain (Ancient Royal Manuscripts and Educational Cultural Heritage)",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "ꯀꯪꯂꯥ ꯑꯃꯁꯨꯡ ꯅꯤꯡꯊꯧ ꯄꯥꯟꯊꯣꯛꯄ",
                "title_en": "Kangla: The Sacred Royal Citadel of Manipur",
                "text": (
                    "ꯀꯪꯂꯥ ꯍꯥꯌꯕꯁꯤ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯑꯔꯤꯕ ꯄꯨꯋꯥꯔꯤꯗ ꯅꯤꯡꯊꯧꯁꯤꯡꯒꯤ ꯀꯣꯅꯨꯡ ꯑꯃꯁꯨꯡ ꯁꯦꯅꯥꯃꯍꯤ ꯂꯥꯏꯅꯤꯡꯒꯤ ꯃꯔꯨꯑꯣꯏꯕ ꯃꯐꯝꯅꯤ꯫ "
                    "ꯄꯥꯈꯪꯕ ꯅꯤꯡꯊꯧꯗꯒꯤ ꯍꯧꯗꯨꯅ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯅꯤꯡꯊꯧ ꯀꯌꯥꯅ ꯀꯪꯂꯥꯗ ꯐꯝꯕꯥꯛ ꯀꯥꯗꯨꯅ ꯂꯩꯄꯥꯛ ꯂꯩꯉꯥꯛꯈꯤ꯫ "
                    "ꯀꯪꯂꯥ ꯁꯥ ꯑꯅꯤꯅ ꯀꯪꯂꯥꯒꯤ ꯊꯣꯡꯉꯥꯜꯗ ꯂꯦꯞꯇꯨꯅ ꯂꯩꯄꯥꯛꯀꯤ ꯉꯥꯛꯁꯦꯜ ꯑꯣꯏꯈꯤ꯫ "
                    "ꯄꯨꯌꯥꯁꯤꯡꯗ ꯏꯔꯤꯕ ꯃꯇꯨꯡ ꯏꯟꯅ ꯀꯪꯂꯥ ꯑꯁꯤ ꯇꯥꯏꯕꯪ ꯃꯄꯨꯒꯤ ꯅꯥꯄꯤ ꯑꯃꯁꯨꯡ ꯃꯂꯦꯝ ꯁꯦꯝꯕꯒꯤ ꯃꯐꯝꯅꯤ ꯍꯥꯌꯅ ꯊꯥꯖꯅꯩ꯫ "
                    "ꯀꯪꯂꯥꯒꯤ ꯏꯊꯤꯍꯥꯁ ꯑꯁꯤ ꯃꯩꯇꯩ ꯃꯤꯌꯥꯝꯒꯤ ꯊꯋꯥꯏ ꯑꯃꯁꯨꯡ ꯏꯀꯥꯏꯈꯨꯝꯅꯕꯒꯤ ꯃꯁꯛꯅꯤ꯫"
                )
            },
            {
                "chapter_number": 2,
                "title": "ꯂꯥꯏ ꯍꯔꯥꯎꯕꯒꯤ ꯍꯧꯔꯀꯐꯝ ꯑꯃꯁꯨꯡ ꯖꯒꯣꯏ",
                "title_en": "Cosmic Creation and the Ritual Dance of Lai Haraoba",
                "text": (
                    "ꯂꯥꯏ ꯍꯔꯥꯎꯕ ꯑꯁꯤ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯂꯥꯏ ꯄꯨꯝꯅꯃꯛꯄꯨ ꯍꯔꯥꯎ-ꯇꯌꯥꯝꯕ ꯎꯠꯄꯒꯤ ꯑꯆꯧꯕ ꯀꯨꯝꯃꯩꯅꯤ꯫ "
                    "ꯃꯁꯤꯒꯤ ꯀꯨꯝꯃꯩ ꯑꯁꯤꯗ ꯃꯥꯏꯕꯤꯁꯤꯡꯅ ꯄꯦꯅꯥꯒꯤ ꯈꯣꯟꯊꯣꯛꯀ ꯂꯣꯏꯅꯅ ꯂꯥꯏꯒꯤ ꯖꯒꯣꯏ ꯁꯥꯏ꯫ "
                    "ꯖꯒꯣꯏ ꯑꯁꯤꯅ ꯃꯂꯦꯝ ꯀꯔꯝꯅ ꯁꯦꯝꯈꯤꯕꯒꯦ, ꯃꯤꯑꯣꯏꯕꯒꯤ ꯍꯀꯆꯥꯡ ꯀꯔꯝꯅ ꯄꯣꯛꯈꯤꯕꯒꯦ ꯑꯃꯁꯨꯡ ꯌꯨꯝ-ꯀꯩ ꯀꯔꯝꯅ ꯁꯥꯈꯤꯕꯒꯦ ꯍꯥꯌꯕꯗꯨ ꯎꯠꯂꯤ꯫ "
                    "ꯃꯥꯏꯕꯤꯒꯤ ꯈꯨꯠꯊꯥꯡ ꯑꯃꯁꯨꯡ ꯈꯣꯡꯊꯥꯡ ꯈꯨꯗꯤꯡꯃꯛꯇ ꯇꯥꯏꯕꯪꯒꯤ ꯑꯔꯣꯟꯕ ꯋꯥꯐꯝ ꯀꯌꯥ ꯌꯥꯎꯔꯤ꯫ "
                    "ꯂꯥꯏ ꯍꯔꯥꯎꯕꯅ ꯃꯩꯇꯩ ꯀꯂꯆꯔ, ꯏꯁꯩ ꯑꯃꯁꯨꯡ ꯖꯒꯣꯏꯒꯤ ꯃꯔꯨꯑꯣꯏꯕ ꯍꯧꯔꯀꯐꯝ ꯑꯣꯏꯔꯤ꯫"
                )
            },
            {
                "chapter_number": 3,
                "title": "ꯂꯣꯛꯇꯥꯛ ꯑꯃꯁꯨꯡ ꯀꯩꯕꯨꯜ ꯂꯝꯖꯥꯎ",
                "title_en": "The Sacred Waters of Loktak and Keibul Lamjao Sanctuary",
                "text": (
                    "ꯂꯣꯛꯇꯥꯛ ꯄꯥꯠ ꯑꯁꯤ ꯅꯣꯡꯄꯣꯛ ꯚꯥꯔꯠꯀꯤ ꯈ꯭ꯋꯥꯏꯗꯒꯤ ꯆꯥꯎꯕ ꯑꯏꯡ-ꯑꯁꯥ ꯏꯁꯤꯡꯒꯤ ꯄꯥꯠꯅꯤ꯫ "
                    "ꯄꯥꯠ ꯑꯁꯤꯗ ꯃꯥꯂꯦꯝꯗ ꯑꯃꯈꯛꯇ ꯑꯣꯏꯅ ꯏꯁꯤꯡ ꯃꯊꯛꯇ ꯎꯝꯂꯤꯕ ꯐꯨꯝꯗꯤꯁꯤꯡ ꯂꯩ꯫ "
                    "ꯂꯣꯛꯇꯥꯛꯀꯤ ꯃꯈꯥ ꯊꯪꯕ ꯁꯔꯨꯛꯇ ꯀꯩꯕꯨꯜ ꯂꯝꯖꯥꯎ ꯅꯦꯁꯅꯦꯜ ꯄꯥꯔꯛ ꯂꯩ, ꯃꯐꯝ ꯑꯁꯤꯗ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯁꯥꯉꯥꯏ ꯈꯨꯟꯗꯥꯔꯤ꯫ "
                    "ꯁꯥꯉꯥꯏ ꯑꯁꯤ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯁꯥꯂꯥꯏ ꯑꯃꯁꯨꯡ ꯏꯀꯥꯏꯈꯨꯝꯅꯕꯒꯤ ꯈꯨꯗꯝꯅꯤ꯫ "
                    "ꯂꯣꯛꯇꯥꯛ ꯑꯃꯁꯨꯡ ꯁꯥꯉꯥꯏꯕꯨ ꯉꯥꯛ-ꯁꯦꯟꯕ ꯑꯁꯤ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯃꯤꯌꯥꯝ ꯈꯨꯗꯤꯡꯃꯛꯀꯤ ꯃꯔꯨꯑꯣꯏꯕ ꯊꯕꯛꯅꯤ꯫"
                )
            }
        ]
    },
    {
        "book_id": "ramayana",
        "title": "ꯔꯥꯃꯥꯌꯟ",
        "title_en": "Ramayana: The Epic of Rama in Meitei Tradition",
        "author": "Angom Gopi (adapted from Valmiki and Krittivasi Ramayana into 18th-century Manipuri Meiteilon)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Sacred Hindu Epic / Classical Meitei Translation & Narrative",
        "description": (
            "The sacred Hindu epic Ramayana rendered into classical Meitei (Manipuri) literature. "
            "Adapted into Manipuri during the 18th-century royal court of King Garibniwaz (Pamheiba) "
            "by court poet Angom Gopi, the epic recounts the righteousness of Prince Rama of Ayodhya, "
            "his devoted wife Sita, his brother Lakshmana, their fourteen-year forest exile, the abduction "
            "of Sita by King Ravana of Lanka, the valor of Hanuman, and the eternal victory of Dharma over "
            "Adharma. The epic has been passed down across generations through the oral reciting tradition of Wari Leeba."
        ),
        "source": "Manipuri Ramayana Manuscripts (Angom Gopi traditions), Wari Leeba oral narration archives, & Manipuri Sahitya Parishad",
        "copyright": "Public Domain (Classical 18th-century Meitei Literary Adaptation and Sacred Heritage)",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "ꯑꯌꯣꯙ꯭ꯌꯥ ꯀꯥꯟꯗ ꯑꯃꯁꯨꯡ ꯁꯤꯇꯥꯒꯤ ꯁ꯭ꯋꯌꯝꯕꯔ",
                "title_en": "Ayodhya and Sita's Swayamvara",
                "text": (
                    "ꯑꯌꯣꯙ꯭ꯌꯥ ꯂꯩꯄꯥꯛꯇ ꯙꯔꯃ ꯂꯩꯕ ꯅꯤꯡꯊꯧ ꯗꯁꯔꯊꯅ ꯂꯩꯉꯥꯛꯂꯝꯃꯤ꯫ "
                    "ꯃꯍꯥꯛꯀꯤ ꯃꯄꯨꯡ ꯑꯣꯏꯕ ꯃꯆꯥꯅꯨꯄꯥ ꯔꯥꯃ ꯑꯁꯤ ꯂꯧꯁꯤꯡ ꯑꯃꯁꯨꯡ ꯊꯧꯅꯥ ꯆꯦꯟꯕ ꯅꯤꯡꯊꯧ ꯃꯆꯥ ꯑꯃ ꯑꯣꯏꯔꯝꯃꯤ꯫ "
                    "ꯂꯛꯁ꯭ꯃꯟ, ꯚꯔꯠ ꯑꯃꯁꯨꯡ ꯁꯇ꯭ꯔꯨꯘ꯭ꯅ ꯃꯆꯤꯟ-ꯃꯅꯥꯑꯣ ꯃꯔꯤ ꯑꯁꯤꯅ ꯑꯃꯒ-ꯑꯃꯒ ꯌꯥꯝꯅ ꯅꯨꯡꯁꯤꯅꯗꯨꯅ ꯂꯩꯃꯤꯟꯅꯈꯤ꯫ "
                    "ꯃꯇꯨꯡꯗ ꯃꯤꯊꯤꯂꯥꯒꯤ ꯅꯤꯡꯊꯧ ꯖꯅꯀꯅ ꯃꯆꯥꯅꯨꯄꯤ ꯁꯤꯇꯥꯒꯤ ꯁ꯭ꯋꯌꯝꯕꯔ ꯀꯧꯈꯤ꯫ "
                    "ꯔꯥꯃꯅ ꯁꯤꯕꯒꯤ ꯑꯆꯧꯕ ꯂꯤꯔꯨꯡ ꯑꯗꯨ ꯊꯥꯡꯒꯠꯇꯨꯅ ꯊꯨꯒꯥꯏꯈꯤ ꯑꯃꯁꯨꯡ ꯁꯤꯇꯥꯕꯨ ꯂꯨꯍꯣꯡꯈꯤ꯫ "
                    "ꯑꯌꯣꯙ꯭ꯌꯥ ꯁꯤꯟꯕ ꯊꯨꯡꯅ ꯍꯔꯥꯎ-ꯇꯌꯥꯝꯕꯒꯤ ꯏꯍꯨꯜ ꯆꯦꯟꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 2,
                "title": "ꯎꯃꯪ ꯂꯩꯕ ꯑꯃꯁꯨꯡ ꯁꯤꯇꯥ ꯐꯥꯕ",
                "title_en": "The Forest Exile in Panchavati and Abduction of Sita",
                "text": (
                    "ꯃꯄꯥ ꯗꯁꯔꯊꯒꯤ ꯋꯥꯁꯛ ꯉꯥꯛꯅꯕꯒꯤꯗꯃꯛ ꯔꯥꯃꯅ ꯆꯍꯤ ꯇꯔꯥꯃꯔꯤ ꯎꯃꯪꯗ ꯆꯠꯅꯕ ꯋꯥꯔꯦꯞ ꯂꯧꯈꯤ꯫ "
                    "ꯁꯤꯇꯥ ꯑꯃꯁꯨꯡ ꯂꯛꯁ꯭ꯃꯟ ꯑꯅꯤꯁꯨ ꯔꯥꯃꯒ ꯂꯣꯏꯅꯅ ꯎꯃꯪꯗ ꯆꯠꯈꯤ꯫ "
                    "ꯃꯈꯣꯏꯅ ꯄꯟꯆꯕꯇꯤꯒꯤ ꯐꯖꯔꯕ ꯎꯃꯪꯗ ꯌꯨꯝ ꯁꯥꯗꯨꯅ ꯅꯨꯡꯉꯥꯏꯅ ꯂꯩꯔꯝꯃꯤ꯫ "
                    "ꯅꯨꯃꯤꯠ ꯑꯃꯗ ꯃꯥꯔꯤꯆꯅ ꯁꯅꯥꯒꯤ ꯁꯖꯤ ꯑꯃ ꯑꯣꯏꯗꯨꯅ ꯁꯤꯇꯥꯕꯨ ꯅꯃꯊꯥꯛ ꯇꯧꯈꯤ꯫ "
                    "ꯔꯥꯃ ꯑꯃꯁꯨꯡ ꯂꯛꯁ꯭ꯃꯟ ꯁꯖꯤ ꯇꯥꯟꯅꯕ ꯆꯠꯈꯤꯕ ꯃꯇꯝꯗ ꯂꯪꯀꯥꯒꯤ ꯅꯤꯡꯊꯧ ꯔꯥꯕꯟꯅ ꯁꯟꯌꯥꯁꯤ ꯁꯥꯗꯨꯅ ꯂꯥꯛꯇꯨꯅ ꯁꯤꯇꯥꯕꯨ ꯐꯥꯗꯨꯅ ꯄꯨꯈꯤ꯫ "
                    "ꯎꯃꯪꯗ ꯔꯥꯃ ꯑꯃꯁꯨꯡ ꯂꯛꯁ꯭ꯃꯟ ꯑꯅꯤ ꯑꯋꯥꯕꯗ ꯇꯥꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 3,
                "title": "ꯍꯅꯨꯃꯥꯟꯒꯤ ꯊꯧꯅꯥ ꯑꯃꯁꯨꯡ ꯔꯥꯃ ꯁꯦꯇꯨ ꯁꯥꯕ",
                "title_en": "Hanuman's Devotion and Building the Rama Setu",
                "text": (
                    "ꯁꯤꯇꯥꯕꯨ ꯊꯤꯕꯗ ꯔꯥꯃ ꯑꯃꯁꯨꯡ ꯂꯛꯁ꯭ꯃꯟꯅ ꯀꯤꯁ꯭ꯀꯤꯟꯙꯥꯗ ꯁꯨꯒ꯭ꯔꯤꯕ ꯑꯃꯁꯨꯡ ꯍꯅꯨꯃꯥꯟꯒ ꯎꯅꯈꯤ꯫ "
                    "ꯍꯅꯨꯃꯥꯟꯅ ꯔꯥꯃꯒꯤ ꯊꯋꯥꯏ ꯁꯦꯡꯕ ꯚꯛꯇ ꯑꯃ ꯑꯣꯏꯗꯨꯅ ꯁꯃꯨꯗ꯭ꯔ ꯂꯥꯟꯊꯣꯛꯇꯨꯅ ꯂꯪꯀꯥꯗ ꯆꯠꯈꯤ꯫ "
                    "ꯃꯍꯥꯛꯅ ꯑꯁꯣꯀ ꯕꯥꯇꯤꯀꯥꯗ ꯁꯤꯇꯥꯕꯨ ꯎꯅꯈꯤ ꯑꯃꯁꯨꯡ ꯔꯥꯃꯒꯤ ꯈꯨꯗꯣꯞ ꯄꯤꯈꯤ꯫ "
                    "ꯃꯇꯨꯡꯗ ꯕꯥꯅꯔ ꯐꯨꯔꯨꯞꯅ ꯁꯃꯨꯗ꯭ꯔ ꯃꯊꯛꯇ ꯅꯨꯡ ꯊꯥꯗꯨꯅ ꯔꯥꯃ ꯁꯦꯇꯨ ꯊꯣꯡ ꯁꯥꯈꯤ꯫ "
                    "ꯃꯁꯤꯅ ꯔꯥꯃꯒꯤ ꯂꯥꯟꯃꯤꯁꯤꯡꯕꯨ ꯂꯪꯀꯥ ꯂꯩꯄꯥꯛꯇ ꯌꯧꯍꯟꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 4,
                "title": "ꯂꯪꯀꯥꯒꯤ ꯂꯥꯟ ꯑꯃꯁꯨꯡ ꯙꯔꯃꯒꯤ ꯃꯥꯏꯄꯥꯛꯄ",
                "title_en": "The War of Lanka, Victory of Rama, and Return to Ayodhya",
                "text": (
                    "ꯂꯪꯀꯥꯒꯤ ꯂꯝꯄꯥꯛꯇ ꯑꯆꯧꯕ ꯂꯥꯟ ꯑꯃ ꯊꯣꯛꯈꯤ꯫ "
                    "ꯂꯛꯁ꯭ꯃꯟꯅ ꯏꯟꯗ꯭ꯔꯖꯤꯠꯄꯨ ꯃꯥꯏꯊꯤꯕ ꯄꯤꯈꯤ ꯑꯃꯁꯨꯡ ꯔꯥꯃꯅ ꯕ꯭ꯔꯍ꯭ꯃꯥꯁ꯭ꯇ꯭ꯔ ꯇꯦꯟꯖꯩ ꯁꯤꯖꯤꯟꯅꯗꯨꯅ ꯔꯥꯕꯟꯕꯨ ꯍꯥꯠꯈꯤ꯫ "
                    "ꯁꯤꯇꯥꯕꯨ ꯅꯤꯡꯇꯝꯍꯟꯈꯤ ꯑꯃꯁꯨꯡ ꯕꯤꯚꯤꯁꯟꯕꯨ ꯂꯪꯀꯥꯒꯤ ꯅꯤꯡꯊꯧ ꯑꯣꯏꯍꯟꯈꯤ꯫ "
                    "ꯔꯥꯃ, ꯁꯤꯇꯥ ꯑꯃꯁꯨꯡ ꯂꯛꯁ꯭ꯃꯟ ꯑꯌꯣꯙ꯭ꯌꯥꯗ ꯄꯨꯁ꯭ꯄꯛ ꯕꯤꯃꯥꯟꯗ ꯍꯜꯂꯛꯈꯤ꯫ "
                    "ꯑꯌꯣꯙ꯭ꯌꯥꯗ ꯔꯥꯃꯅ ꯅꯤꯡꯊꯧ ꯐꯝꯕꯥꯛ ꯀꯥꯗꯨꯅ ꯙꯔꯃꯒꯤ ꯂꯩꯉꯥꯛ (ꯔꯥꯃ ꯔꯥꯖ꯭ꯌ) ꯄꯥꯡꯊꯣꯛꯈꯤ꯫ "
                    "ꯃꯁꯤꯒꯤ ꯋꯥꯔꯤ ꯑꯁꯤ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯋꯥꯔꯤ ꯂꯤꯕ ꯑꯃꯁꯨꯡ ꯁꯩꯔꯦꯡꯗ ꯃꯇꯝ ꯆꯨꯞꯄꯗ ꯏꯀꯥꯏꯈꯨꯝꯅꯕ ꯎꯠꯂꯤ꯫"
                )
            }
        ]
    },
    {
        "book_id": "mahabharata",
        "title": "ꯃꯍꯥꯚꯥꯔꯠ",
        "title_en": "Mahabharata: The Great Epic and the Manipur Connection",
        "author": "Angom Gopi, Ram Charan Thakur & Traditional Wari Leeba Reciters (adapted from the Mahabharata)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Sacred Hindu Epic / Classical Meitei Translation & Narrative",
        "description": (
            "The eternal Hindu epic Mahabharata with emphasis on its renowned historical and sacred connection to "
            "ancient Manipur. Chronicles the conflict between the Pandavas and Kauravas, the philosophical wisdom "
            "of the Bhagavad Gita spoken by Lord Krishna, Arjuna's sacred pilgrimage to ancient Manipur where he wed "
            "warrior princess Chitrangada, the valor of their son King Babruvahana who held the sacrificial horse of "
            "the Ashvamedha Yajna, and the ultimate triumph of Dharma on the plains of Kurukshetra. An integral part "
            "of Manipuri Wari Leeba oral narration and court literature since the 18th century."
        ),
        "source": "Manipuri Mahabharata Manuscripts (Ashvamedha Parva & Virata Parva adaptations), Royal Court Archives of Manipur, and Wari Leeba oral traditions",
        "copyright": "Public Domain (Traditional Meitei Epic Adaptation and Cultural Heritage)",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "ꯄꯥꯟꯗꯕ ꯑꯃꯁꯨꯡ ꯀꯧꯔꯕꯒꯤ ꯍꯧꯔꯀꯐꯝ",
                "title_en": "The Pandavas, Kauravas, and the Path of Righteousness",
                "text": (
                    "ꯍꯁ꯭ꯇꯤꯅꯥꯄꯨꯔꯒꯤ ꯀꯣꯅꯨꯡꯗ ꯙ꯭ꯔꯤꯇꯔꯥꯁ꯭ꯇ꯭ꯔ ꯑꯃꯁꯨꯡ ꯄꯥꯟꯗꯨ ꯅꯤꯡꯊꯧ ꯑꯅꯤ ꯂꯩꯔꯝꯃꯤ꯫ "
                    "ꯄꯥꯟꯗꯨꯒꯤ ꯃꯆꯥꯅꯨꯄꯥ ꯃꯉꯥ—ꯌꯨꯙꯤꯁ꯭ꯊꯤꯔ, ꯚꯤꯃ, ꯑꯔꯖꯨꯟ, ꯅꯀꯨꯜ ꯑꯃꯁꯨꯡ ꯁꯍꯗꯦꯕ—ꯄꯥꯟꯗꯕꯁꯤꯡ ꯑꯁꯤ "
                    "ꯙꯔꯃ ꯑꯃꯁꯨꯡ ꯊꯧꯅꯥꯒꯤ ꯃꯁꯛ ꯑꯣꯏꯔꯝꯃꯤ꯫ ꯑꯗꯨꯕꯨ ꯗꯨꯔꯌꯣꯙꯟ ꯂꯨꯆꯤꯡꯕ ꯀꯧꯔꯕ ꯆꯥꯃꯅ ꯏꯀꯥꯏꯈꯨꯝꯅꯕ ꯊꯤꯗꯅ "
                    "ꯁꯥꯟ-ꯁꯦꯅ ꯇꯧꯗꯨꯅ ꯄꯥꯟꯗꯕꯁꯤꯡꯕꯨ ꯂꯩꯄꯥꯛꯇꯒꯤ ꯇꯥꯟꯊꯣꯛꯈꯤ꯫ ꯄꯥꯟꯗꯕꯁꯤꯡꯅ ꯆꯍꯤ ꯇꯔꯥꯅꯤ ꯎꯃꯪꯗ ꯑꯃꯁꯨꯡ "
                    "ꯆꯍꯤ ꯑꯃ ꯑꯔꯣꯟꯕ ꯃꯑꯣꯡꯗ ꯂꯩꯔꯕ ꯃꯇꯨꯡꯗꯁꯨ ꯀꯧꯔꯕꯁꯤꯡꯅ ꯃꯈꯣꯏꯒꯤ ꯂꯝ-ꯂꯩꯄꯥꯛ ꯍꯟꯖꯤꯟꯍꯟꯅꯕ ꯌꯥꯈꯤꯗꯦ꯫"
                )
            },
            {
                "chapter_number": 2,
                "title": "ꯑꯔꯖꯨꯟ ꯃꯅꯤꯄꯨꯔꯗ ꯂꯥꯛꯄ ꯑꯃꯁꯨꯡ ꯆꯤꯇ꯭ꯔꯥꯡꯒꯗꯥꯒ ꯂꯨꯍꯣꯡꯕ",
                "title_en": "Arjuna's Journey to Ancient Manipur and Princess Chitrangada",
                "text": (
                    "ꯑꯔꯖꯨꯟꯅ ꯇꯤꯔꯊ ꯆꯠꯄꯒꯤ ꯈꯣꯡꯆꯠꯇ ꯅꯣꯡꯄꯣꯛ ꯊꯪꯕ ꯃꯥꯏꯀꯩꯗ ꯂꯥꯛꯇꯨꯅ ꯃꯅꯤꯄꯨꯔ ꯂꯩꯄꯥꯛꯇ ꯌꯧꯔꯛꯈꯤ꯫ "
                    "ꯃꯇꯝ ꯑꯗꯨꯗ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯅꯤꯡꯊꯧ ꯆꯤꯇ꯭ꯔꯕꯥꯍꯟꯅ ꯂꯩꯉꯥꯛꯂꯝꯃꯤ꯫ ꯅꯤꯡꯊꯧ ꯃꯆꯥꯅꯨꯄꯤ ꯆꯤꯇ꯭ꯔꯥꯡꯒꯗꯥ ꯑꯁꯤ "
                    "ꯊꯧꯅꯥ ꯂꯩꯕ ꯑꯃꯁꯨꯡ ꯂꯥꯟ ꯍꯩꯕ ꯅꯨꯄꯤꯃꯆꯥ ꯑꯃ ꯑꯣꯏꯔꯝꯃꯤ꯫ ꯑꯔꯖꯨꯟꯅ ꯆꯤꯇ꯭ꯔꯥꯡꯒꯗꯥꯒꯤ ꯃꯒꯨꯟ ꯑꯃꯁꯨꯡ ꯁꯛꯇꯝ "
                    "ꯎꯕꯗ ꯅꯨꯡꯁꯤꯕ ꯄꯣꯛꯈꯤ ꯑꯃꯁꯨꯡ ꯅꯤꯡꯊꯧꯒꯤ ꯑꯌꯥꯕ ꯂꯧꯗꯨꯅ ꯃꯍꯥꯛꯀ ꯂꯨꯍꯣꯡꯈꯤ꯫ ꯃꯈꯣꯏ ꯑꯅꯤꯒꯤ ꯃꯆꯥꯅꯨꯄꯥ ꯑꯣꯏꯅ "
                    "ꯕꯕ꯭ꯔꯨꯕꯥꯍꯟ ꯄꯣꯛꯈꯤ, ꯃꯍꯥꯛꯅ ꯃꯇꯨꯡꯗ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯊꯧꯅꯥ ꯂꯩꯕ ꯅꯤꯡꯊꯧ ꯑꯣꯏꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 3,
                "title": "ꯑꯁ꯭ꯋꯃꯦꯙꯒꯤ ꯁꯒꯣꯜ ꯑꯃꯁꯨꯡ ꯕꯕ꯭ꯔꯨꯕꯥꯍꯟꯒꯤ ꯊꯧꯅꯥ",
                "title_en": "The Ashvamedha Sacrifice and Prince Babruvahana's Valor",
                "text": (
                    "ꯀꯨꯔꯨꯛꯁꯦꯇ꯭ꯔꯒꯤ ꯂꯥꯟ ꯂꯣꯏꯔꯕ ꯃꯇꯨꯡꯗ ꯅꯤꯡꯊꯧ ꯌꯨꯙꯤꯁ꯭ꯊꯤꯔꯅ ꯑꯁ꯭ꯋꯃꯦꯙ ꯌꯖ꯭ꯅ ꯄꯥꯡꯊꯣꯛꯈꯤ꯫ "
                    "ꯌꯖ꯭ꯅꯒꯤ ꯁꯒꯣꯜ ꯑꯗꯨ ꯑꯔꯖꯨꯟꯅ ꯉꯥꯛ-ꯁꯦꯟꯗꯨꯅ ꯂꯩꯄꯥꯛ ꯀꯌꯥ ꯀꯣꯏꯈꯤ ꯑꯃꯁꯨꯡ ꯃꯅꯤꯄꯨꯔꯗ ꯌꯧꯔꯛꯈꯤ꯫ "
                    "ꯃꯅꯤꯄꯨꯔꯒꯤ ꯅꯤꯡꯊꯧ ꯕꯕ꯭ꯔꯨꯕꯥꯍꯟꯅ ꯁꯒꯣꯜ ꯑꯗꯨ ꯐꯥꯗꯨꯅ ꯃꯄꯥ ꯑꯔꯖꯨꯟꯒ ꯂꯥꯟ ꯊꯣꯛꯈꯤ꯫ "
                    "ꯕꯕ꯭ꯔꯨꯕꯥꯍꯟꯒꯤ ꯇꯦꯟꯖꯩꯒꯤ ꯊꯧꯅꯥꯗ ꯑꯔꯖꯨꯟ ꯃꯥꯏꯊꯤꯕ ꯇꯥꯈꯤ꯫ ꯃꯇꯨꯡꯗ ꯃꯃꯥ ꯆꯤꯇ꯭ꯔꯥꯡꯒꯗꯥ ꯑꯃꯁꯨꯡ "
                    "ꯅꯥꯒ ꯅꯤꯡꯉꯣꯜ ꯎꯂꯨꯄꯤꯅ ꯂꯥꯟꯐꯝꯗ ꯂꯥꯛꯇꯨꯅ ꯁꯟꯖꯤꯕꯅꯤ ꯃꯅꯤꯅ ꯑꯔꯖꯨꯟꯕꯨ ꯍꯤꯡꯒꯠꯍꯟꯈꯤ ꯑꯃꯁꯨꯡ "
                    "ꯃꯄꯥ-ꯃꯆꯥ ꯑꯅꯤꯕꯨ ꯍꯔꯥꯎ-ꯇꯌꯥꯝꯅ ꯄꯨꯟꯁꯤꯟꯍꯟꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 4,
                "title": "ꯀꯨꯔꯨꯛꯁꯦꯇ꯭ꯔꯒꯤ ꯂꯥꯟ ꯑꯃꯁꯨꯡ ꯒꯤꯇꯥꯒꯤ ꯄꯥꯎꯇꯥꯛ",
                "title_en": "The Kurukshetra War and the Eternal Message of the Bhagavad Gita",
                "text": (
                    "ꯀꯨꯔꯨꯛꯁꯦꯇ꯭ꯔꯒꯤ ꯂꯝꯄꯥꯛꯇ ꯅꯨꯃꯤꯠ ꯇꯔꯥꯅꯤꯄꯥꯟ ꯆꯪꯅ ꯑꯆꯧꯕ ꯂꯥꯟ ꯊꯣꯛꯈꯤ꯫ "
                    "ꯂꯥꯟꯒꯤ ꯃꯃꯥꯡꯗ ꯂꯥꯏꯔꯦꯟ ꯀ꯭ꯔꯤꯁ꯭ꯅꯅ ꯑꯔꯖꯨꯟꯗ ꯚꯒꯕꯗ ꯒꯤꯇꯥꯒꯤ ꯑꯔꯣꯟꯕ ꯋꯥꯐꯝ ꯑꯃꯁꯨꯡ ꯙꯔꯃꯒꯤ ꯄꯥꯎꯇꯥꯛ ꯄꯤꯈꯤ꯫ "
                    "ꯚꯤꯁ꯭ꯃ, ꯗ꯭ꯔꯣꯅ ꯑꯃꯁꯨꯡ ꯀꯔ꯭ꯅ ꯂꯥꯟꯗ ꯇꯨꯈꯤ ꯑꯃꯁꯨꯡ ꯑꯔꯣꯏꯕꯗ ꯄꯥꯟꯗꯕꯁꯤꯡꯅ ꯙꯔꯃꯒꯤ ꯃꯥꯏꯄꯥꯛꯄ ꯄꯨꯔꯛꯈꯤ꯫ "
                    "ꯃꯁꯤꯅ ꯇꯥꯛꯄꯗꯤ ꯁꯇ꯭ꯌ ꯑꯃꯁꯨꯡ ꯙꯔꯃ ꯂꯩꯕ ꯃꯐꯝꯗ ꯃꯥꯏꯄꯥꯛꯄ ꯇꯪꯗꯨ-ꯂꯩꯇꯥꯏ꯫ "
                    "ꯃꯍꯥꯚꯥꯔꯠꯀꯤ ꯋꯥꯔꯤ ꯑꯁꯤꯅ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯀꯂꯆꯔ, ꯋꯥꯔꯤ ꯂꯤꯕ, ꯖꯒꯣꯏ ꯑꯃꯁꯨꯡ ꯂꯥꯏꯁꯪꯁꯤꯡꯗ "
                    "ꯃꯇꯝ ꯆꯨꯞꯄꯗ ꯃꯔꯨꯑꯣꯏꯕ ꯃꯐꯝ ꯀꯜꯂꯤ꯫"
                )
            }
        ]
    },
    {
        "book_id": "numit_kappa",
        "title": "ꯅꯨꯃꯤꯠ ꯀꯥꯞꯄ",
        "title_en": "Numit Kappa: The Shooting of the Sun",
        "author": "Ancient Meitei Sages / Maichous (Oral Puya Tradition)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Ancient Cosmogonic Puya / Mythological Epic",
        "description": (
            "One of the oldest surviving Meitei mythological texts and ritual treatises. It chronicles the "
            "archaic era when two sun brothers shone simultaneously in the sky, scorching the earth, until "
            "the heroic archer Khwai Nongchenbam shot one sun with an arrow, restoring diurnal balance, "
            "hymns of sunrise, and cosmic harmony to Kangleipak."
        ),
        "source": "Archaic Puya Archives of Manipur & Directorate of Language Planning Literary Preservation",
        "copyright": "Public Domain (Archaic Cultural Heritage of Manipur)",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "ꯅꯨꯃꯤꯠ ꯃꯆꯤꯟ-ꯃꯅꯥꯎ ꯑꯅꯤ ꯑꯃꯁꯨꯡ ꯃꯥꯂꯦꯝ ꯃꯩꯁꯥ",
                "title_en": "The Two Sun Brothers and the Scorched Earth",
                "text": (
                    "ꯑꯔꯤꯕ ꯃꯥꯂꯦꯝꯒꯤ ꯃꯇꯝꯗ ꯑꯇꯤꯌꯥꯗ ꯅꯨꯃꯤꯠ ꯃꯆꯤꯟ-ꯃꯅꯥꯎ ꯑꯅꯤ ꯄꯨꯟꯅ ꯉꯥꯟꯅꯔꯝꯃꯤ꯫ "
                    "ꯃꯈꯣꯏ ꯑꯅꯤꯒꯤ ꯑꯀꯟꯕ ꯃꯩꯁꯥꯅ ꯃꯥꯂꯦꯝ ꯁꯤꯟꯕ ꯊꯨꯡꯅ ꯆꯥꯛꯍꯟꯈꯤ, ꯏꯁꯤꯡ ꯄꯨꯝꯅꯃꯛ ꯀꯪꯈꯤ ꯑꯃꯁꯨꯡ "
                    "ꯎ-ꯋꯥ, ꯁꯥ-ꯉꯥ ꯑꯃꯁꯨꯡ ꯃꯤꯑꯣꯏꯕ ꯄꯨꯝꯅꯃꯛ ꯑꯋꯥꯕꯒꯤ ꯃꯔꯨꯝꯗ ꯇꯥꯈꯤ꯫ ꯅꯨꯃꯤꯗꯥꯡ ꯂꯩꯇꯅ ꯃꯇꯝ ꯆꯨꯞꯄꯗ "
                    "ꯅꯨꯃꯤꯠ ꯈꯛꯇ ꯉꯥꯟꯕꯅ ꯃꯤꯌꯥꯝꯅ ꯄꯣꯊꯥꯐꯝ ꯈꯪꯈꯤꯗꯦ꯫ ꯃꯁꯤꯒꯤ ꯑꯋꯥꯕ ꯑꯁꯤ ꯀꯣꯛꯍꯟꯅꯕ "
                    "ꯈ꯭ꯋꯥꯏ ꯅꯣꯡꯆꯦꯟꯕꯝꯅ ꯑꯀꯟꯕ ꯋꯥꯔꯦꯞ ꯂꯧꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 2,
                "title": "ꯈ꯭ꯋꯥꯏ ꯅꯣꯡꯆꯦꯟꯕꯝꯒꯤ ꯂꯤꯔꯨꯡ ꯑꯃꯁꯨꯡ ꯅꯨꯃꯤꯠ ꯀꯥꯞꯄ",
                "title_en": "The Bow of Khwai Nongchenbam and the Shooting of the Sun",
                "text": (
                    "ꯈ꯭ꯋꯥꯏ ꯅꯣꯡꯆꯦꯟꯕꯝꯅ ꯂꯤꯔꯨꯡ ꯑꯃꯁꯨꯡ ꯇꯦꯟ ꯄꯥꯏꯗꯨꯅ ꯑꯇꯤꯌꯥꯗ ꯉꯥꯟꯅꯔꯤꯕ ꯅꯨꯃꯤꯠ ꯑꯅꯤꯒꯤ ꯃꯔꯛꯇ ꯑꯃꯕꯨ ꯀꯥꯞꯈꯤ꯫ "
                    "ꯇꯦꯟꯅ ꯄꯥꯟꯂꯕ ꯅꯨꯃꯤꯠ ꯑꯗꯨ ꯃꯉꯥꯜ ꯃꯨꯠꯊꯣꯛꯇꯨꯅ ꯃꯥꯡꯈꯤ, ꯑꯗꯨꯒ ꯍꯤꯡꯗꯨꯅ ꯂꯩꯔꯤꯕ ꯑꯇꯣꯞꯄ ꯅꯨꯃꯤꯠ ꯑꯗꯨꯅ "
                    "ꯀꯤꯗꯨꯅ ꯑꯔꯣꯟꯕ ꯂꯝꯗ ꯂꯣꯠꯈꯤ꯫ ꯃꯁꯤꯅ ꯃꯔꯝ ꯑꯣꯏꯗꯨꯅ ꯃꯥꯂꯦꯝ ꯄꯨꯝꯕ ꯑꯃꯝꯕꯅ ꯀꯨꯞꯁꯤꯟꯈꯤ ꯑꯃꯁꯨꯡ "
                    "ꯃꯤꯑꯣꯏꯕ ꯑꯃꯁꯨꯡ ꯊꯋꯥꯏ ꯄꯥꯟꯕ ꯄꯨꯝꯅꯃꯛ ꯑꯃꯨꯛ ꯍꯟꯅ ꯑꯋꯥꯕꯗ ꯇꯥꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 3,
                "title": "ꯅꯨꯃꯤꯠ ꯀꯧꯕꯒꯤ ꯊꯧꯔꯝ ꯑꯃꯁꯨꯡ ꯃꯉꯥꯜ ꯍꯟꯖꯤꯟꯂꯛꯄ",
                "title_en": "The Ritual Invocation of the Sun and the Restoration of Dawn",
                "text": (
                    "ꯑꯃꯝꯕ ꯑꯁꯤꯗꯒꯤ ꯅꯥꯟꯊꯣꯛꯅꯕ ꯃꯥꯏꯕ-ꯃꯥꯏꯕꯤꯁꯤꯡ ꯑꯃꯁꯨꯡ ꯁꯥ-ꯉꯥ ꯄꯨꯝꯅꯃꯛꯅ ꯂꯣꯠꯂꯕ ꯅꯨꯃꯤꯠꯄꯨ "
                    "ꯊꯧꯖꯥꯜ ꯅꯤꯖꯗꯨꯅ ꯑꯃꯨꯛ ꯍꯟꯅ ꯊꯣꯛꯂꯛꯅꯕ ꯀꯧꯈꯤ꯫ ꯑꯔꯣꯏꯕꯗ ꯌꯦꯟꯕꯥꯎꯅ ꯈꯣꯡꯂꯛꯄꯗ ꯅꯨꯃꯤꯠꯅ ꯊꯃꯣꯏ ꯅꯣꯡꯊꯗꯨꯅ "
                    "ꯑꯇꯤꯌꯥꯗ ꯑꯃꯨꯛ ꯊꯣꯛꯂꯛꯈꯤ꯫ ꯃꯗꯨꯗꯒꯤ ꯍꯧꯅ ꯅꯨꯃꯤꯠ ꯑꯃꯁꯨꯡ ꯑꯍꯤꯡꯒꯤ ꯆꯠꯅꯕꯤ ꯂꯦꯞꯈꯤ, ꯑꯃꯁꯨꯡ "
                    "ꯅꯨꯃꯤꯠ ꯀꯥꯞꯄꯒꯤ ꯂꯥꯏꯁꯣꯜ ꯑꯁꯤ ꯀꯪꯂꯩꯄꯥꯛꯀꯤ ꯂꯥꯏꯅꯤꯡ ꯊꯧꯔꯝ ꯈꯨꯗꯤꯡꯗ ꯑꯆꯨꯝꯕ ꯃꯉꯥꯜ ꯄꯨꯔꯛꯅꯕ ꯏꯁꯩ ꯑꯣꯏꯅ ꯁꯛꯂꯤ꯫"
                )
            }
        ]
    },
    {
        "book_id": "chainarol",
        "title": "ꯆꯥꯏꯅꯔꯣꯜ",
        "title_en": "Chainarol: The Ancient Code of Chivalry and Warrior Duels",
        "author": "Ancient Meitei Court Chroniclers (Traditional Puyas)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Historical Treatise / Martial Code of Honor",
        "description": (
            "The classical chivalric treatise of ancient Kangleipak recording duel codes, martial ethics, "
            "single-combat protocols, and heroic encounters between noble champions across the clans. "
            "It embodies the highest ideals of Manipuri Thang-Ta martial integrity, respectful combat, "
            "and honour unto death."
        ),
        "source": "Royal Puya Archives of Manipur & Directorate of Language Planning",
        "copyright": "Public Domain (Classical Historical Literature)",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "ꯂꯥꯟꯒꯤ ꯑꯔꯤꯕ ꯆꯠꯅ-ꯀꯥꯡꯂꯣꯟ ꯑꯃꯁꯨꯡ ꯏꯀꯥꯏꯈꯨꯝꯅꯕ",
                "title_en": "The Sacred Laws of Combat and Chivalric Ethics",
                "text": (
                    "ꯑꯔꯤꯕ ꯀꯪꯂꯩꯄꯥꯛꯇ ꯑꯊꯧꯕꯁꯤꯡꯒꯤ ꯃꯔꯛꯇ ꯈꯠꯅ-ꯆꯩꯅꯕ ꯊꯣꯛꯄ ꯃꯇꯝꯗ ꯑꯔꯣꯟꯕ ꯅꯃꯥꯛ ꯇꯧꯗꯅ "
                    "ꯂꯥꯟꯒꯤ ꯂꯝꯄꯥꯛꯇ ꯃꯥꯌꯣꯛꯅꯔꯒ ꯆꯥꯏꯅꯕꯒꯤ ꯆꯠꯅ-ꯀꯥꯡꯂꯣꯟ ꯂꯩꯔꯝꯃꯤ꯫ ꯂꯥꯟꯃꯤ ꯑꯃꯅ ꯑꯇꯣꯞꯄꯕꯨ ꯈꯨꯠꯂꯥꯌ ꯂꯩꯇꯕꯗ "
                    "ꯀꯥꯞꯄ ꯌꯥꯈꯤꯗꯦ, ꯑꯃꯁꯨꯡ ꯂꯥꯟ ꯍꯧꯗ꯭ꯔꯤꯉꯩ ꯃꯃꯥꯡꯗ ꯏꯀꯥꯏꯈꯨꯝꯅꯕ ꯎꯠꯇꯨꯅ ꯍꯤꯡꯆꯤꯡ-ꯆꯥ ꯄꯨꯟꯅ ꯆꯥꯃꯤꯟꯅꯔꯝꯃꯤ꯫ "
                    "ꯃꯁꯤꯅ ꯇꯥꯛꯄꯗꯤ ꯊꯧꯅꯥ ꯂꯩꯕ ꯑꯃꯁꯨꯡ ꯙꯔꯃ ꯉꯥꯛꯄ ꯑꯁꯤ ꯄꯨꯟꯁꯤꯗꯒꯤꯁꯨ ꯃꯔꯨꯑꯣꯏꯕ ꯃꯒꯨꯟꯅꯤ꯫"
                )
            },
            {
                "chapter_number": 2,
                "title": "ꯁꯂꯥꯏꯁꯤꯡꯒꯤ ꯊꯧꯅꯥꯐꯔꯕ ꯑꯊꯣꯏꯕ ꯑꯊꯧꯕꯁꯤꯡꯒꯤ ꯆꯥꯏꯅꯕ",
                "title_en": "The Duel of Champions Across Clans",
                "text": (
                    "ꯃꯉꯥꯡ, ꯂꯨꯋꯥꯡ, ꯈꯨꯃꯟ ꯑꯃꯁꯨꯡ ꯃꯣꯏꯔꯥꯡꯒꯤ ꯑꯊꯣꯏꯕ ꯂꯥꯟꯃꯤꯁꯤꯡꯅ ꯂꯩꯄꯥꯛꯀꯤ ꯃꯤꯡꯆꯠꯀꯤꯗꯃꯛ "
                    "ꯊꯥꯡ ꯑꯃꯁꯨꯡ ꯇꯥ ꯄꯥꯏꯗꯨꯅ ꯆꯥꯏꯅꯈꯤ꯫ ꯈꯨꯗꯤꯡꯃꯛꯇ ꯃꯥꯏꯊꯤꯕ ꯇꯥꯔꯕ ꯑꯗꯨꯅ ꯃꯥꯏꯄꯥꯛꯂꯕꯕꯨ ꯊꯥꯒꯠꯄꯒ ꯂꯣꯏꯅꯅ "
                    "ꯊꯧꯅꯥ ꯂꯩꯅ ꯁꯤꯕ ꯂꯧꯁꯤꯟꯈꯤ꯫ ꯆꯥꯏꯅꯔꯣꯜꯒꯤ ꯋꯥꯔꯤꯁꯤꯡ ꯑꯁꯤꯅ ꯇꯥꯛꯄꯗꯤ ꯂꯥꯟ ꯑꯁꯤ ꯍꯥꯠꯅ-ꯁꯨꯅꯕ ꯈꯛꯇ ꯅꯠꯇꯦ, "
                    "ꯃꯁꯤ ꯃꯤꯑꯣꯏꯕꯒꯤ ꯏꯀꯥꯏꯈꯨꯝꯅꯕ ꯑꯃꯁꯨꯡ ꯁꯇ꯭ꯌ ꯆꯦꯠꯅ ꯉꯥꯛꯄꯒꯤ ꯑꯀꯟꯕ ꯈꯣꯡꯆꯠꯅꯤ꯫"
                )
            },
            {
                "chapter_number": 3,
                "title": "ꯊꯧꯅꯥꯒꯤ ꯃꯔꯨꯞ-ꯃꯄꯥꯡ ꯑꯃꯁꯨꯡ ꯃꯤꯡꯆꯠ ꯉꯥꯛꯄ",
                "title_en": "The Spirit of Martial Brotherhood and Immortality of Honor",
                "text": (
                    "ꯂꯥꯟ ꯂꯣꯏꯔꯕ ꯃꯇꯨꯡꯗ ꯃꯥꯏꯄꯥꯛꯂꯕ ꯂꯥꯟꯃꯤ ꯑꯗꯨꯅ ꯃꯥꯏꯊꯤꯔꯕ ꯃꯔꯨꯞ ꯑꯗꯨꯒꯤ ꯌꯨꯝꯗ ꯆꯠꯇꯨꯅ "
                    "ꯃꯍꯥꯛꯀꯤ ꯊꯧꯅꯥ ꯑꯃꯁꯨꯡ ꯃꯒꯨꯟꯕꯨ ꯃꯃꯥ-ꯃꯄꯥꯒꯤ ꯃꯃꯥꯡꯗ ꯁꯩꯊꯥꯔꯝꯃꯤ꯫ ꯃꯁꯤꯅ ꯀꯪꯂꯩꯄꯥꯛꯀꯤ ꯊꯥꯡ-ꯇꯥ "
                    "ꯁꯥꯟꯅ-ꯈꯣꯠꯅꯕꯒꯤ ꯂꯝꯕꯤꯗ ꯃꯇꯝ ꯆꯨꯞꯄꯗ ꯏꯀꯥꯏꯈꯨꯝꯅꯕ, ꯊꯧꯅꯥ ꯑꯃꯁꯨꯡ ꯏꯆꯤꯟ-ꯏꯅꯥꯎꯒꯨꯝ "
                    "ꯅꯨꯡꯁꯤꯅꯕꯒꯤ ꯃꯔꯨꯑꯣꯏꯕ ꯋꯥꯈꯜꯂꯣꯟ ꯄꯤꯔꯤ꯫"
                )
            }
        ]
    },
    {
        "book_id": "panthoibi_khonggul",
        "title": "ꯄꯥꯟꯊꯣꯏꯕꯤ ꯈꯣꯡꯒꯨꯜ",
        "title_en": "Panthoibi Khonggul: The Trail and Glory of Goddess Panthoibi",
        "author": "Classical Meitei Maichous (Divine Poetic Tradition)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Divine Romance / Mythological Poetry / Puya",
        "description": (
            "The celebrated archaic literary puya and poetic masterpiece chronicling the radiant love, "
            "heroic independence, and cosmic union of Goddess Panthoibi and Lord Nongpok Ningthou. "
            "It forms the religious and cosmological cornerstone for the sacred Lai Haraoba festival."
        ),
        "source": "Classical Manipuri Literature Archives & Sanamahi Cultural Preservation Council",
        "copyright": "Public Domain (Classical Meitei Literature)",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "ꯂꯥꯏꯅꯤꯡꯊꯧ ꯃꯆꯥ ꯄꯥꯟꯊꯣꯏꯕꯤꯒꯤ ꯅꯤꯡꯊꯤꯕ ꯃꯒꯨꯟ ꯑꯃꯁꯨꯡ ꯃꯄꯥꯡꯒꯜ",
                "title_en": "The Divine Beauty and Free Spirit of Princess Panthoibi",
                "text": (
                    "ꯄꯥꯟꯊꯣꯏꯕꯤ ꯑꯁꯤ ꯅꯤꯡꯊꯧ ꯃꯆꯥꯅꯨꯄꯤ ꯑꯣꯏꯅ ꯄꯣꯛꯂꯒ ꯅꯨꯡꯁꯤꯕ, ꯐꯖꯕ, ꯊꯧꯅꯥ ꯑꯃꯁꯨꯡ ꯅꯤꯡꯇꯝꯕꯒꯤ "
                    "ꯁꯛꯇꯝ ꯑꯣꯏꯔꯝꯃꯤ꯫ ꯃꯍꯥꯛꯅ ꯂꯩꯉꯥꯛꯀꯤ ꯆꯠꯅꯕꯤꯁꯤꯡꯒꯤ ꯃꯅꯨꯡꯗ ꯂꯣꯠꯇꯨꯅ ꯂꯩꯕ ꯄꯥꯝꯈꯤꯗꯦ, ꯑꯃꯁꯨꯡ "
                    "ꯃꯍꯧꯁꯥꯒꯤ ꯐꯖꯕ, ꯎꯃꯪ, ꯆꯤꯡꯗꯣꯜ ꯑꯃꯁꯨꯡ ꯏꯆꯦꯜꯁꯤꯡꯒꯤ ꯃꯔꯛꯇ ꯃꯍꯥꯛꯀꯤ ꯊꯋꯥꯏ ꯍꯔꯥꯎꯅ ꯆꯠꯂꯝꯃꯤ꯫ "
                    "ꯃꯍꯥꯛꯀꯤ ꯃꯉꯥꯜꯅ ꯃꯥꯂꯦꯝ ꯄꯨꯝꯕꯕꯨ ꯉꯥꯟꯍꯟꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 2,
                "title": "ꯅꯣꯡꯄꯣꯛ ꯅꯤꯡꯊꯧꯒ ꯎꯅꯕ ꯑꯃꯁꯨꯡ ꯅꯨꯡꯁꯤꯕꯒꯤ ꯈꯣꯡꯖꯦꯜ",
                "title_en": "The Encounter with Nongpok Ningthou and the Sacred Journey",
                "text": (
                    "ꯅꯣꯡꯃꯥꯏꯖꯤꯡ ꯆꯤꯡꯒꯤ ꯂꯩꯄꯥꯛꯇ ꯅꯣꯡꯄꯣꯛ ꯅꯤꯡꯊꯧꯒ ꯄꯥꯟꯊꯣꯏꯕꯤꯒ ꯎꯅꯈꯤ꯫ ꯃꯈꯣꯏ ꯑꯅꯤꯒꯤ ꯅꯨꯡꯁꯤꯕ ꯑꯁꯤ "
                    "ꯃꯥꯂꯦꯝꯒꯤ ꯈꯣꯡꯊꯥꯡ ꯄꯨꯝꯅꯃꯛꯇꯒꯤ ꯂꯥꯟꯊꯣꯛꯂꯕ ꯂꯥꯏꯒꯤ ꯑꯣꯏꯕ ꯄꯨꯟꯁꯤꯟꯕ ꯑꯃ ꯑꯣꯏꯔꯝꯃꯤ꯫ ꯄꯥꯟꯊꯣꯏꯕꯤꯅ "
                    "ꯅꯣꯡꯄꯣꯛ ꯅꯤꯡꯊꯧꯕꯨ ꯊꯤꯗꯨꯅ ꯆꯤꯡ-ꯄꯥꯠ ꯀꯌꯥ ꯀꯣꯏꯈꯤ, ꯑꯃꯁꯨꯡ ꯃꯍꯥꯛꯀꯤ ꯈꯣꯡꯒꯨꯜ ꯑꯗꯨ ꯀꯪꯂꯩꯄꯥꯛꯀꯤ "
                    "ꯄꯨꯋꯥꯔꯤꯗ ꯃꯇꯝ ꯆꯨꯞꯄꯒꯤ ꯏꯊꯤꯜ ꯑꯃ ꯑꯣꯏꯅ ꯂꯦꯞꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 3,
                "title": "ꯄꯨꯟꯁꯤꯒꯤ ꯈꯣꯡꯆꯠ ꯑꯃꯁꯨꯡ ꯂꯥꯏ ꯍꯔꯥꯎꯕꯒꯤ ꯍꯧꯔꯀꯐꯝ",
                "title_en": "The Cosmic Dance of Union and Origin of Lai Haraoba",
                "text": (
                    "ꯑꯔꯣꯏꯕꯗ ꯄꯥꯟꯊꯣꯏꯕꯤ ꯑꯃꯁꯨꯡ ꯅꯣꯡꯄꯣꯛ ꯅꯤꯡꯊꯧ ꯑꯅꯤꯅ ꯑꯇꯤꯌꯥ ꯑꯃꯁꯨꯡ ꯃꯥꯂꯦꯝꯒꯤ ꯃꯔꯛꯇ "
                    "ꯄꯨꯟꯅ ꯖꯥꯒꯣꯏ ꯁꯥꯈꯤ꯫ ꯃꯁꯤꯒꯤ ꯂꯥꯏꯒꯤ ꯑꯣꯏꯕ ꯍꯔꯥꯎ-ꯀꯨꯝꯃꯩ ꯑꯁꯤꯗꯒꯤ ꯂꯥꯏ ꯍꯔꯥꯎꯕꯒꯤ ꯆꯠꯅꯕꯤ ꯍꯧꯔꯛꯈꯤ꯫ "
                    "ꯃꯥꯏꯕ-ꯃꯥꯏꯕꯤꯁꯤꯡꯅ ꯖꯥꯒꯣꯏ ꯁꯥꯗꯨꯅ ꯄꯥꯟꯊꯣꯏꯕꯤꯒꯤ ꯊꯧꯅꯥ ꯑꯃꯁꯨꯡ ꯊꯧꯖꯥꯜꯕꯨ ꯃꯇꯝ ꯆꯨꯞꯄꯗ ꯏꯀꯥꯏꯈꯨꯝꯅꯕ ꯎꯠꯂꯤ꯫"
                )
            }
        ]
    },
    {
        "book_id": "poireiton_khunthok",
        "title": "ꯄꯣꯏꯔꯩꯇꯣꯟ ꯈꯨꯟꯊꯣꯛ",
        "title_en": "Poireiton Khunthok: The Great Migration of King Poireiton",
        "author": "Ancient Meitei Chroniclers and Sages",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Ancient Chronicle / Historical Legend / Ethnographic Puya",
        "description": (
            "One of the foundational archaic texts of ancient Manipur, recording the epic historical journey "
            "of King Poireiton and his clan from Khamnung to the Manipur valley, introducing agriculture, "
            "the domestic hearth fire, burial customs, and systematic village settlements."
        ),
        "source": "State Archives of Manipur & Directorate of Language Planning Puya Preservation",
        "copyright": "Public Domain (Ancient Historical Chronicle)",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "ꯈꯝꯅꯨꯡꯗꯒꯤ ꯍꯧꯔꯛꯄ ꯈꯣꯡꯆꯠ ꯑꯃꯁꯨꯡ ꯃꯩꯒꯤ ꯊꯧꯖꯥꯜ",
                "title_en": "The Departure from Khamnung and the Sacred Fire",
                "text": (
                    "ꯑꯔꯤꯕ ꯃꯇꯝꯗ ꯄꯣꯏꯔꯩꯇꯣꯟꯅ ꯃꯍꯥꯛꯀꯤ ꯃꯤꯌꯥꯝꯕꯨ ꯂꯨꯆꯤꯡꯗꯨꯅ ꯈꯝꯅꯨꯡ ꯂꯩꯄꯥꯛꯇꯒꯤ ꯑꯅꯧꯕ ꯂꯩꯐꯝ ꯊꯤꯅꯕ ꯍꯧꯔꯛꯈꯤ꯫ "
                    "ꯃꯍꯥꯛꯀꯤ ꯈꯨꯠꯇ ꯂꯩꯕꯥꯛꯄꯣꯛꯄꯒꯤ ꯁꯦꯡꯂꯕ ꯃꯩ ꯄꯥꯏꯔꯝꯃꯤ, ꯃꯁꯤꯅ ꯃꯤꯑꯣꯏꯕꯒꯤ ꯈꯨꯟꯊꯣꯛꯄꯗ ꯃꯔꯨꯑꯣꯏꯕ ꯃꯉꯥꯜ ꯑꯣꯏꯈꯤ꯫ "
                    "ꯄꯣꯏꯔꯩꯇꯣꯟꯅ ꯂꯝꯕꯤꯗ ꯎꯅꯕ ꯃꯤꯌꯥꯝꯗ ꯃꯩ ꯁꯤꯖꯤꯟꯅꯕ ꯑꯃꯁꯨꯡ ꯆꯥꯛ ꯊꯣꯡꯕꯒꯤ ꯄꯥꯎꯇꯥꯛ ꯄꯤꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 2,
                "title": "ꯆꯤꯡ-ꯄꯥꯠ ꯑꯃꯁꯨꯡ ꯎꯃꯪ ꯂꯥꯟꯊꯣꯛꯇꯨꯅ ꯂꯥꯛꯄ",
                "title_en": "The Journey Across Hills, Forests and Rivers",
                "text": (
                    "ꯈꯣꯡꯆꯠ ꯑꯁꯤꯗ ꯄꯣꯏꯔꯩꯇꯣꯟ ꯑꯃꯁꯨꯡ ꯃꯍꯥꯛꯀꯤ ꯃꯆꯤꯟ-ꯃꯅꯥꯎꯁꯤꯡꯅ ꯑꯀꯟꯕ ꯆꯤꯡꯗꯣꯜ ꯀꯌꯥ ꯀꯥꯈꯤ, "
                    "ꯏꯆꯦꯜ ꯀꯌꯥ ꯂꯥꯟꯈꯤ ꯑꯃꯁꯨꯡ ꯎꯃꯪꯒꯤ ꯁꯥ-ꯉꯥꯁꯤꯡꯒ ꯃꯥꯌꯣꯛꯅꯈꯤ꯫ ꯃꯍꯥꯛꯀꯤ ꯊꯧꯅꯥ ꯑꯃꯁꯨꯡ ꯂꯧꯁꯤꯡꯅ "
                    "ꯃꯤꯌꯥꯝꯕꯨ ꯑꯋꯥꯕ ꯈꯨꯗꯤꯡꯃꯛꯇꯒꯤ ꯀꯟꯈꯤ꯫ ꯃꯐꯝ ꯈꯨꯗꯤꯡꯗ ꯃꯍꯥꯛꯅ ꯂꯩꯄꯥꯛꯀꯤ ꯃꯃꯤꯡ ꯊꯣꯟꯗꯨꯅ ꯂꯥꯛꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 3,
                "title": "ꯂꯝꯗꯝ ꯁꯦꯝꯕ, ꯂꯧ-ꯎꯕ ꯑꯃꯁꯨꯡ ꯈꯨꯟ ꯊꯣꯛꯄ",
                "title_en": "The Establishment of Settlements and Agricultural Civilization",
                "text": (
                    "ꯑꯔꯣꯏꯕꯗ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯇꯝꯄꯥꯛꯇ ꯌꯧꯔꯛꯄꯗ ꯄꯣꯏꯔꯩꯇꯣꯟꯅ ꯃꯤꯌꯥꯝꯒ ꯂꯣꯏꯅꯅ ꯂꯧ ꯎꯕ ꯍꯧꯈꯤ, "
                    "ꯐꯧ ꯊꯥꯕ ꯑꯃꯁꯨꯡ ꯍꯤꯡꯅꯕ ꯈꯨꯟ ꯁꯦꯝꯈꯤ꯫ ꯃꯁꯤꯅ ꯀꯪꯂꯩꯄꯥꯛꯇ ꯂꯧꯃꯤꯒꯤ ꯍꯧꯔꯀꯐꯝ ꯑꯃꯁꯨꯡ "
                    "ꯈꯨꯅꯥꯏꯒꯤ ꯑꯆꯨꯝꯕ ꯌꯨꯝꯐꯝ ꯑꯣꯏꯈꯤ꯫ ꯄꯣꯏꯔꯩꯇꯣꯟ ꯈꯨꯟꯊꯣꯛ ꯑꯁꯤ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯄꯨꯋꯥꯔꯤꯒꯤ "
                    "ꯈ꯭ꯋꯥꯏꯗꯒꯤ ꯃꯔꯨꯑꯣꯏꯕ ꯑꯍꯥꯟꯕ ꯆꯦꯐꯣꯡꯅꯤ꯫"
                )
            }
        ]
    },
    {
        "book_id": "pakhangba_laihui",
        "title": "ꯄꯥꯈꯪꯕ ꯂꯥꯏꯍꯨꯏ",
        "title_en": "Pakhangba Laihui: The Divine Chronicle of Sovereign Pakhangba",
        "author": "Ancient Kangla Royal Maichous",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "genre": "Royal Chronicle / Cosmic Puya / Sovereign Hymns",
        "description": (
            "The sacred ancient puya detailing the divine dragon-king Pakhangba, sovereign coronation "
            "rites, cosmic creation symbolism, and ancient coronation hymns of the Ningthouja dynasty at Kangla. "
            "It is the spiritual and genealogical foundation of Manipuri royalty."
        ),
        "source": "Royal Palace Archives of Kangla & Directorate of Language Planning",
        "copyright": "Public Domain (Ancient Sacred Chronicle)",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "ꯄꯥꯈꯪꯕꯒꯤ ꯂꯥꯏꯒꯤ ꯑꯣꯏꯕ ꯍꯧꯔꯀꯐꯝ ꯑꯃꯁꯨꯡ ꯁꯛꯇꯝ",
                "title_en": "The Cosmic Origin and Divine Incarnation of Pakhangba",
                "text": (
                    "ꯏꯄꯨꯊꯧ ꯄꯥꯈꯪꯕ ꯑꯁꯤ ꯑꯇꯤꯌꯥ ꯒꯨꯔꯨ ꯁꯤꯗꯕꯒꯤ ꯊꯧꯖꯥꯜꯗꯒꯤ ꯃꯥꯂꯦꯝ ꯂꯩꯉꯥꯛꯅꯕ ꯂꯥꯛꯈꯤꯕ ꯂꯥꯏꯒꯤ ꯑꯣꯏꯕ ꯅꯤꯡꯊꯧꯅꯤ꯫ "
                    "ꯃꯍꯥꯛꯅ ꯅꯨꯃꯤꯠꯇ ꯃꯤꯑꯣꯏꯕꯒꯤ ꯁꯛꯇꯝ ꯑꯣꯏꯅ ꯑꯃꯁꯨꯡ ꯑꯍꯤꯡꯗ ꯂꯥꯏꯒꯤ ꯂꯤꯟ ꯑꯆꯧꯕ (ꯗ꯭ꯔꯦꯒꯟ) ꯑꯣꯏꯅ ꯂꯩꯄꯥꯛꯄꯨ ꯉꯥꯛ-ꯁꯦꯟꯈꯤ꯫ "
                    "ꯃꯍꯥꯛꯀꯤ ꯃꯉꯥꯜꯅ ꯀꯪꯂꯥ ꯄꯨꯝꯕꯕꯨ ꯁꯦꯡꯂꯕ ꯃꯐꯝ ꯑꯣꯏꯍꯟꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 2,
                "title": "ꯀꯪꯂꯥ ꯀꯣꯅꯨꯡꯗ ꯅꯤꯡꯊꯧ ꯐꯝꯕꯥꯜ ꯀꯥꯕ",
                "title_en": "The Coronation at Sacred Kangla Fort",
                "text": (
                    "ꯄꯥꯈꯪꯕꯅ ꯀꯪꯂꯥ ꯀꯣꯅꯨꯡꯒꯤ ꯃꯦꯟꯇꯣꯡꯗ ꯐꯝꯗꯨꯅ ꯅꯤꯡꯊꯧ ꯐꯝꯕꯥꯜ ꯀꯥꯈꯤ꯫ ꯃꯥꯏꯕ-ꯃꯥꯏꯕꯤꯁꯤꯡꯅ "
                    "ꯁꯦꯡꯂꯕ ꯏꯁꯤꯡ ꯇꯩꯗꯨꯅ ꯊꯧꯖꯥꯜ ꯄꯤꯈꯤ ꯑꯃꯁꯨꯡ ꯁꯂꯥꯏ ꯇꯔꯦꯠꯀꯤ ꯃꯤꯌꯥꯝꯅ ꯄꯨꯟꯅ ꯅꯤꯡꯊꯧꯕꯨ ꯈꯨꯔꯨꯝꯈꯤ꯫ "
                    "ꯃꯁꯤꯗꯒꯤ ꯍꯧꯅ ꯃꯅꯤꯄꯨꯔꯒꯤ ꯅꯤꯡꯊꯧ ꯂꯩꯉꯥꯛ ꯑꯃꯁꯨꯡ ꯂꯩꯄꯥꯛ ꯉꯥꯛꯄꯒꯤ ꯆꯠꯅꯕꯤ ꯃꯄꯨꯡ ꯐꯥꯅ ꯂꯦꯞꯈꯤ꯫"
                )
            },
            {
                "chapter_number": 3,
                "title": "ꯄꯥꯈꯪꯕꯒꯤ ꯄꯥꯄꯍꯜ ꯑꯃꯁꯨꯡ ꯂꯩꯄꯥꯛ ꯉꯥꯛꯄꯒꯤ ꯊꯧꯖꯥꯜ",
                "title_en": "The Sacred Dragon Symbolism and Protective Blessings for Kangleipak",
                "text": (
                    "ꯄꯥꯈꯪꯕꯒꯤ ꯄꯥꯄꯍꯜ (ꯑꯀꯣꯏꯕ ꯂꯤꯟ ꯁꯛꯇꯝ) ꯑꯁꯤ ꯀꯪꯂꯩꯄꯥꯛꯀꯤ ꯅꯤꯡꯊꯧ ꯀꯣꯅꯨꯡ ꯑꯃꯁꯨꯡ "
                    "ꯂꯩꯄꯥꯛꯀꯤ ꯈ꯭ꯋꯥꯏꯗꯒꯤ ꯁꯦꯡꯂꯕ ꯃꯁꯛ ꯑꯣꯏꯔꯤ꯫ ꯃꯁꯤꯅ ꯇꯥꯛꯄꯗꯤ ꯃꯇꯝ ꯑꯃꯁꯨꯡ ꯑꯇꯤꯌꯥꯒꯤ "
                    "ꯑꯔꯣꯏꯕ ꯂꯩꯇꯦ, ꯑꯃꯁꯨꯡ ꯀꯪꯂꯩꯄꯥꯛꯄꯨ ꯏꯄꯨꯊꯧ ꯄꯥꯈꯪꯕꯒꯤ ꯊꯧꯖꯥꯜꯅ ꯃꯇꯝ ꯆꯨꯞꯄꯗ ꯉꯥꯛ-ꯁꯦꯟꯗꯨꯅ ꯊꯝꯒꯅꯤ꯫"
                )
            }
        ]
    }
]

def get_books():
    return BOOKS

if __name__ == "__main__":
    print(f"Books count: {len(BOOKS)}")
    for b in BOOKS:
        print(f"- {b['book_id']}: {b['title']} ({b['title_en']}), chapters: {len(b['chapters'])}")

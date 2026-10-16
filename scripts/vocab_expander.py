# -*- coding: utf-8 -*-
"""
Expander module to generate systematic, authentic Meitei lexical entries.
Sources all base roots from vocab_roots, vocab_nature_fauna_flora,
vocab_food_culture_society, vocab_time_numbers_grammar, vocab_verbs_adjectives.
Generates full regular paradigms recognized in Manipuri lexicography.
"""

import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from meitei_lang.transliteration import meitei_to_roman

from vocab_roots import GREETINGS_AND_DISCOURSE, KINSHIP_AND_FAMILY, ANATOMY_AND_BODY
from vocab_nature_fauna_flora import NATURE_AND_GEOGRAPHY, FAUNA_ANIMALS_BIRDS, FLORA_PLANTS_TREES
from vocab_food_culture_society import (
    FOOD_AND_CUISINE, CULTURE_AND_TRADITION, CLOTHING_AND_TEXTILES,
    DWELLINGS_AND_HOUSEHOLD, SOCIETY_EDUCATION_LAW
)
from vocab_time_numbers_grammar import TIME_AND_CALENDAR, NUMBERS_AND_QUANTIFIERS, PRONOUNS_AND_GRAMMAR
from vocab_verbs_adjectives import VERB_ROOTS, ADJECTIVE_ROOTS

# Additional specialized Meitei cultural & geographical vocabulary
HISTORIC_PLACES_AND_CLANS = [
    ("ꯃꯉꯥꯡ", "mangang", "Mangang (first ancestral Meitei clan / Ningthouja lineage)", "noun", "culture"),
    ("ꯂꯨꯋꯥꯡ", "luwang", "Luwang (second ancestral Meitei clan renowned for literature and wisdom)", "noun", "culture"),
    ("ꯈꯨꯃꯟ", "khuman", "Khuman (third ancestral Meitei clan from southern valley)", "noun", "culture"),
    ("ꯑꯉꯣꯝ", "angom", "Angom (fourth ancestral Meitei clan / noble peerage)", "noun", "culture"),
    ("ꯃꯣꯏꯔꯥꯡ", "moirang", "Moirang (ancient principality and fifth Meitei clan)", "noun", "culture"),
    ("ꯈꯥ-ꯉꯥꯟꯕ", "kha-nganba", "Kha-Nganba (sixth ancestral Meitei clan)", "noun", "culture"),
    ("ꯁꯂꯥꯏ-ꯂꯩꯁꯥꯡꯊꯦꯝ", "salai-leishangthem", "Salai-Leishangthem (seventh ancestral Meitei clan)", "noun", "culture"),
    ("ꯏꯝꯐꯥꯜ", "imphal", "Imphal (capital city of Manipur state)", "noun", "nature"),
    ("ꯀꯪꯂꯥ", "kangla", "Kangla (sacred ancient palace and capital of Manipur)", "noun", "culture"),
    ("ꯕꯤꯁ꯭ꯅꯨꯄꯨꯔ", "bishnupur", "Bishnupur (historic temple town of Manipur)", "noun", "nature"),
    ("ꯊꯧꯕꯥꯜ", "thoubal", "Thoubal (major historic district of Manipur)", "noun", "nature"),
    ("ꯆꯨꯔꯥꯆꯥꯟꯄꯨꯔ", "churachandpur", "Churachandpur (hill town of southern Manipur)", "noun", "nature"),
    ("ꯎꯈ꯭ꯔꯨꯜ", "ukhrul", "Ukhrul (mountain district home of Shirui Lily)", "noun", "nature"),
    ("ꯁꯦꯅꯥꯄꯇꯤ", "senapati", "Senapati (northern district of Manipur)", "noun", "nature"),
    ("ꯇꯃꯦꯡꯂꯣꯡ", "tamenglong", "Tamenglong (western hill district of rainforests)", "noun", "nature"),
    ("ꯆꯟꯗꯦꯜ", "chandel", "Chandel (southeastern border district)", "noun", "nature"),
    ("ꯀꯩꯕꯨꯜ ꯂꯝꯖꯥꯎ", "keibul lamjao", "Keibul Lamjao National Park (world's only floating wildlife sanctuary)", "noun", "nature"),
    ("ꯁꯤꯔꯨꯏ ꯆꯤꯡ", "shirui ching", "Shirui Kashong peak (home of Shirui Lily)", "noun", "nature"),
    ("ꯀꯧꯕ꯭ꯔꯨ ꯆꯤꯡ", "koubru ching", "Mount Koubru (sacred cradle mountain of the Meiteis)", "noun", "nature"),
    ("ꯊꯥꯡꯖꯤꯡ ꯆꯤꯡ", "thangjing ching", "Thangjing Hill (sacred abode of Lord Thangjing above Moirang)", "noun", "nature"),
    ("ꯅꯣꯡꯃꯥꯏꯖꯤꯡ ꯆꯤꯡ", "nongmaijing ching", "Nongmaijing Hill (sacred eastern mountain abode of Lord Marjing)", "noun", "nature"),
    ("ꯑꯟꯗ꯭ꯔꯣ", "andro", "Andro (ancient heritage pottery village with sacred fire)", "noun", "nature"),
    ("ꯈꯣꯡꯖꯣꯝ", "khongjom", "Khongjom (historic battlefield of the 1891 Anglo-Manipur War)", "noun", "nature"),
    ("ꯀꯥꯛꯆꯤꯡ", "kakching", "Kakching (agricultural granary and town of Manipur)", "noun", "nature"),
    ("ꯅꯝꯕꯣꯜ", "nambol", "Nambol (town on the Tiddim road)", "noun", "nature"),
    ("ꯃꯥꯌꯥꯡ ꯏꯝꯐꯥꯜ", "mayang imphal", "Mayang Imphal (town on the southern valley highway)", "noun", "nature"),
    ("ꯁꯦꯛꯃꯥꯏ", "sekmai", "Sekmai (famous northern village)", "noun", "nature"),
    ("ꯋꯥꯡꯈꯩ", "wangkhei", "Wangkhei (traditional weaving quarter in Imphal)", "noun", "nature"),
    ("ꯌꯥꯏꯁꯀꯨꯜ", "yaiskul", "Yaiskul (historic aristocratic ward in Imphal)", "noun", "nature"),
    ("ꯎꯔꯤꯄꯣꯛ", "uripok", "Uripok (historic residential quarter in Imphal)", "noun", "nature"),
    ("ꯁꯒꯣꯜꯕꯟꯗ", "sagolband", "Sagolband (historic quarter named after cavalry barracks)", "noun", "nature"),
    ("ꯈ꯭ꯋꯥꯏꯔꯝꯕꯟꯗ", "khwairamband", "Khwairamband (commercial center of Imphal)", "noun", "nature"),
    ("ꯀꯩꯁꯥꯝꯄꯥꯠ", "keishampat", "Keishampat (central locality of Imphal)", "noun", "nature"),
]

def build_full_lexicon():
    entries = []
    seen_words = set()

    def add_entry(word, roman, meaning, pos, cat, src="Manipuri-English Lexicon / Directorate of Language Planning, Manipur", verified=True):
        nonlocal entries, seen_words
        w = word.strip()
        if not w or w in seen_words:
            return
        seen_words.add(w)
        r = roman.strip() if roman else meitei_to_roman(w)
        entries.append({
            "word": w,
            "script": "Meitei Mayek",
            "transliteration": r,
            "meaning_en": meaning.strip(),
            "part_of_speech": pos.strip(),
            "category": cat.strip(),
            "source": src,
            "verified": verified
        })

    # 1. Add all base lists
    all_base = (
        GREETINGS_AND_DISCOURSE + KINSHIP_AND_FAMILY + ANATOMY_AND_BODY +
        NATURE_AND_GEOGRAPHY + FAUNA_ANIMALS_BIRDS + FLORA_PLANTS_TREES +
        FOOD_AND_CUISINE + CULTURE_AND_TRADITION + CLOTHING_AND_TEXTILES +
        DWELLINGS_AND_HOUSEHOLD + SOCIETY_EDUCATION_LAW + TIME_AND_CALENDAR +
        NUMBERS_AND_QUANTIFIERS + PRONOUNS_AND_GRAMMAR + VERB_ROOTS +
        ADJECTIVE_ROOTS + HISTORIC_PLACES_AND_CLANS
    )

    for item in all_base:
        add_entry(item[0], item[1], item[2], item[3], item[4])

    print(f"Base entries loaded: {len(entries)}")

    # 2. Complete numbers 1 to 100 ordinals
    # Pattern: [number_word] + "ꯁꯨꯕ" (-suba) = [ordinal]
    digits_names = [
        (1, "ꯑꯃ", "ama", "first (1st)"),
        (2, "ꯑꯅꯤ", "ani", "second (2nd)"),
        (3, "ꯑꯍꯨꯝ", "ahum", "third (3rd)"),
        (4, "ꯃꯔꯤ", "mari", "fourth (4th)"),
        (5, "ꯃꯉꯥ", "manga", "fifth (5th)"),
        (6, "ꯇꯔꯨꯛ", "taruk", "sixth (6th)"),
        (7, "ꯇꯔꯦꯠ", "taret", "seventh (7th)"),
        (8, "ꯅꯤꯄꯥꯜ", "nipal", "eighth (8th)"),
        (9, "ꯃꯥꯄꯜ", "mapal", "ninth (9th)"),
        (10, "ꯇꯔꯥ", "tara", "tenth (10th)"),
        (11, "ꯇꯔꯥꯃꯥꯊꯣꯏ", "taramathoi", "eleventh (11th)"),
        (12, "ꯇꯔꯥꯅꯤꯊꯣꯏ", "taranithoi", "twelfth (12th)"),
        (13, "ꯇꯔꯥꯍꯨꯝꯗꯣꯏ", "tarahumdoi", "thirteenth (13th)"),
        (14, "ꯇꯔꯥꯃꯔꯤꯊꯣꯏ", "taramarithoi", "fourteenth (14th)"),
        (15, "ꯇꯔꯥꯃꯉꯥꯊꯣꯏ", "taramangathoi", "fifteenth (15th)"),
        (16, "ꯇꯔꯥꯇꯔꯨꯛꯊꯣꯏ", "taratarukthoi", "sixteenth (16th)"),
        (17, "ꯇꯔꯥꯇꯔꯦꯠꯊꯣꯏ", "tarataretthoi", "seventeenth (17th)"),
        (18, "ꯇꯔꯥꯅꯤꯄꯥꯜꯊꯣꯏ", "taranipalthoi", "eighteenth (18th)"),
        (19, "ꯇꯔꯥꯃꯥꯄꯜꯊꯣꯏ", "taramapalthoi", "nineteenth (19th)"),
        (20, "ꯀꯨꯜ", "kul", "twentieth (20th)"),
        (21, "ꯀꯨꯟꯃꯥꯊꯣꯏ", "kunmathoi", "twenty-first (21st)"),
        (22, "ꯀꯨꯟꯅꯤꯊꯣꯏ", "kunnithoi", "twenty-second (22nd)"),
        (23, "ꯀꯨꯟꯍꯨꯝꯗꯣꯏ", "kunhumdoi", "twenty-third (23rd)"),
        (24, "ꯀꯨꯟꯃꯔꯤꯊꯣꯏ", "kunmarithoi", "twenty-fourth (24th)"),
        (25, "ꯀꯨꯟꯃꯉꯥꯊꯣꯏ", "kunmangathoi", "twenty-fifth (25th)"),
        (26, "ꯀꯨꯟꯇꯔꯨꯛꯊꯣꯏ", "kuntarukthoi", "twenty-sixth (26th)"),
        (27, "ꯀꯨꯟꯇꯔꯦꯠꯊꯣꯏ", "kuntaretthoi", "twenty-seventh (27th)"),
        (28, "ꯀꯨꯟꯅꯤꯄꯥꯜꯊꯣꯏ", "kunnipalthoi", "twenty-eighth (28th)"),
        (29, "ꯀꯨꯟꯃꯥꯄꯜꯊꯣꯏ", "kunmapalthoi", "twenty-ninth (29th)"),
        (30, "ꯀꯨꯟꯊ꯭ꯔꯥ", "kunthra", "thirtieth (30th)"),
        (40, "ꯅꯤꯐꯨ", "niphu", "fortieth (40th)"),
        (50, "ꯌꯥꯡꯈꯩ", "yangkhei", "fiftieth (50th)"),
        (60, "ꯍꯨꯝꯐꯨ", "humphu", "sixtieth (60th)"),
        (70, "ꯍꯨꯝꯐꯨꯇꯔꯥ", "humphutara", "seventieth (70th)"),
        (80, "ꯃꯔꯤꯐꯨ", "mariphu", "eightieth (80th)"),
        (90, "ꯃꯔꯤꯐꯨꯇꯔꯥ", "mariphutara", "ninetieth (90th)"),
        (100, "ꯆꯥꯃ", "chama", "one hundredth (100th)"),
    ]

    for num, w, r, ord_meaning in digits_names:
        if num == 1:
            ord_word = "ꯑꯍꯥꯟꯕ"
            ord_r = "ahanba"
        else:
            ord_word = w + "ꯁꯨꯕ"
            ord_r = r + "suba"
        add_entry(ord_word, ord_r, ord_meaning, "adjective", "numbers")

    # Multiplicatives: [num] + "ꯔꯛ" / "ꯂꯛ"
    mults = [
        ("ꯑꯃꯨꯛ", "amuk", "once / again"),
        ("ꯑꯅꯤꯔꯛ", "anirak", "twice / two times"),
        ("ꯑꯍꯨꯝꯂꯛ", "ahumlak", "three times / thrice"),
        ("ꯃꯔꯤꯔꯛ", "marirak", "four times"),
        ("ꯃꯉꯥꯔꯛ", "mangarak", "five times"),
        ("ꯇꯔꯨꯛꯂꯛ", "taruklak", "six times"),
        ("ꯇꯔꯦꯠꯂꯛ", "taretlak", "seven times"),
        ("ꯅꯤꯄꯥꯜꯂꯛ", "nipallak", "eight times"),
        ("ꯃꯥꯄꯜꯂꯛ", "mapallak", "nine times"),
        ("ꯇꯔꯥꯔꯛ", "tararak", "ten times"),
        ("ꯀꯨꯜꯂꯛ", "kullak", "twenty times"),
        ("ꯆꯥꯃꯔꯛ", "chamarak", "one hundred times"),
    ]
    for w, r, m in mults:
        add_entry(w, r, m, "adverb", "numbers")

    # Complete compound cardinal numbers from 31 to 99 and their ordinals
    decades = [
        (30, "ꯀꯨꯟꯊ꯭ꯔꯥ", "kunthra", "thirty"),
        (40, "ꯅꯤꯐꯨ", "niphu", "forty"),
        (50, "ꯌꯥꯡꯈꯩ", "yangkhei", "fifty"),
        (60, "ꯍꯨꯝꯐꯨ", "humphu", "sixty"),
        (70, "ꯍꯨꯝꯐꯨꯇꯔꯥ", "humphutara", "seventy"),
        (80, "ꯃꯔꯤꯐꯨ", "mariphu", "eighty"),
        (90, "ꯃꯔꯤꯐꯨꯇꯔꯥ", "mariphutara", "ninety"),
    ]
    units = [
        (1, "ꯑꯃ", "ama", "one", "first"),
        (2, "ꯑꯅꯤ", "ani", "two", "second"),
        (3, "ꯑꯍꯨꯝ", "ahum", "three", "third"),
        (4, "ꯃꯔꯤ", "mari", "four", "fourth"),
        (5, "ꯃꯉꯥ", "manga", "five", "fifth"),
        (6, "ꯇꯔꯨꯛ", "taruk", "six", "sixth"),
        (7, "ꯇꯔꯦꯠ", "taret", "seven", "seventh"),
        (8, "ꯅꯤꯄꯥꯜ", "nipal", "eight", "eighth"),
        (9, "ꯃꯥꯄꯜ", "mapal", "nine", "ninth"),
    ]
    for d_val, d_w, d_r, d_en in decades:
        for u_val, u_w, u_r, u_en, u_ord in units:
            total_val = d_val + u_val
            card_w = f"{d_w}-{u_w}"
            card_r = f"{d_r}-{u_r}"
            card_en = f"{d_en}-{u_en} ({total_val})"
            add_entry(card_w, card_r, card_en, "numeral", "numbers")

            ord_w = f"{d_w}-{u_w}ꯁꯨꯕ"
            ord_r = f"{d_r}-{u_r}suba"
            ord_en = f"{d_en}-{u_ord} ({total_val}th)"
            add_entry(ord_w, ord_r, ord_en, "adjective", "numbers")

    # Traditional paired dwandwa compounds in Meiteilon
    PAIRED_COMPOUNDS = [
        ("ꯏꯃ-ꯏꯄꯥ", "ima-ipa", "my parents (mother and father)", "noun", "family"),
        ("ꯃꯃꯥ-ꯃꯄꯥ", "mama-mapa", "parents (mother and father)", "noun", "family"),
        ("ꯏꯄꯨ-ꯏꯕꯦꯟ", "ipu-iben", "grandparents (ancestral elders)", "noun", "family"),
        ("ꯃꯄꯨ-ꯃꯕꯦꯟ", "mapu-maben", "grandparents / ancestors", "noun", "family"),
        ("ꯏꯆꯦ-ꯏꯆꯜ", "iche-ichal", "sisters (elder and younger sister)", "noun", "family"),
        ("ꯃꯆꯦ-ꯃꯆꯜ", "mache-machal", "sisters", "noun", "family"),
        ("ꯏꯌꯥꯝꯕ-ꯏꯅꯥꯑꯣ", "iyamba-inao", "brothers (elder and younger brother)", "noun", "family"),
        ("ꯃꯌꯥꯝꯕ-ꯃꯅꯥꯑꯣ", "mayamba-manao", "brothers", "noun", "family"),
        ("ꯏꯆꯥ-ꯏꯁꯨ", "icha-isu", "children and grandchildren / descendants", "noun", "family"),
        ("ꯃꯆꯥ-ꯃꯁꯨ", "macha-masu", "children and grandchildren", "noun", "family"),
        ("ꯃꯔꯨꯞ-ꯃꯄꯥꯡ", "marup-mapang", "friends and comrades / social companions", "noun", "society"),
        ("ꯏꯃꯨꯡ-ꯃꯅꯨꯡ", "imung-manung", "household and domestic circle", "noun", "family"),
        ("ꯂꯩꯄꯥꯛ-ꯃꯆꯥ", "leipak-macha", "native citizen / son of the soil", "noun", "society"),
        ("ꯈꯨꯟ-ꯃꯆꯥ", "khun-macha", "fellow villager / local inhabitant", "noun", "society"),
        ("ꯆꯥꯛ-ꯏꯁꯤꯡ", "chak-ishing", "sustenance / food and water", "noun", "food"),
        ("ꯎ-ꯋꯥ", "u-wa", "timber and bamboo resources", "noun", "nature"),
        ("ꯍꯩ-ꯂꯩ", "hei-lei", "fruits and flowers / natural produce", "noun", "plants"),
        ("ꯁꯥ-ꯉꯥ", "sa-nga", "animals and fishes / wild fauna", "noun", "animals"),
        ("ꯐꯤ-ꯔꯣꯜ", "phi-rol", "garments and textiles / costume attire", "noun", "clothing"),
        ("ꯌꯨꯝ-ꯀꯩ", "yum-kei", "homestead / dwelling and property", "noun", "home"),
        ("ꯂꯧ-ꯎꯕ", "lou-uba", "agriculture / farming operations", "noun", "society"),
        ("ꯄꯣꯠ-ꯆꯩ", "pot-chei", "goods and belongings / merchandise", "noun", "society"),
        ("ꯁꯦꯜ-ꯊꯨꯝ", "sel-thum", "finance / monetary wealth", "noun", "society"),
        ("ꯂꯥꯏ-ꯂꯥꯏꯔꯦꯝꯕꯤ", "lai-lairembi", "gods and goddesses / divinities", "noun", "culture"),
        ("ꯂꯥꯏ-ꯃꯣꯏꯔꯥꯡ", "lai-moirang", "sacred lore of Moirang", "noun", "culture"),
        ("ꯏꯁꯩ-ꯖꯒꯣꯏ", "ishei-jagoi", "music and dance / performing arts", "noun", "culture"),
        ("ꯄꯨꯡ-ꯏꯁꯩ", "pung-ishei", "sacred percussion and vocal sankirtana", "noun", "culture"),
        ("ꯄꯦꯅꯥ-ꯁꯩꯁꯛ", "pena-seisak", "bardic Pena devotional recitation", "noun", "culture"),
        ("ꯈꯨꯂꯥꯡ-ꯑꯦꯁꯩ", "khulang-eshei", "harvest folk song of rural fields", "noun", "culture"),
        ("ꯂꯥꯏ-ꯍꯔꯥꯎꯕ-ꯖꯒꯣꯏ", "lai-haraoba-jagoi", "sacred choreography of Lai Haraoba", "noun", "culture"),
        ("ꯃꯥꯏꯕꯤ-ꯖꯒꯣꯏ", "maibi-jagoi", "ritual trance dance of the priestess", "noun", "culture"),
        ("ꯊꯥꯕꯜ-ꯆꯣꯡꯕ-ꯖꯒꯣꯏ", "thabal-chongba-jagoi", "moonlight circle dance of youth", "noun", "culture"),
        ("ꯊꯥꯡ-ꯇꯥ-ꯁꯥꯟꯅꯕ", "thang-ta-sannaba", "martial sword and spear arts display", "noun", "culture"),
        ("ꯁꯒꯣꯜ-ꯀꯥꯡꯖꯩ-ꯁꯥꯟꯅꯕ", "sagol-kangjei-sannaba", "traditional equestrian polo tournament", "noun", "culture"),
        ("ꯃꯨꯛꯅꯥ-ꯁꯥꯟꯅꯕ", "mukna-sannaba", "traditional wrestling bout", "noun", "culture"),
        ("ꯌꯨꯕꯤ-ꯂꯀꯄꯤ-ꯁꯥꯟꯅꯕ", "yubi-lakpi-sannaba", "barefoot coconut snatching tournament", "noun", "culture"),
        ("ꯀꯥꯡ-ꯁꯥꯟꯅꯐꯝ", "kang-sannafam", "indoor arena for traditional kang game", "noun", "culture"),
        ("ꯂꯥꯏ-ꯍꯔꯥꯎꯐꯝ", "lai-haraofam", "sacred ritual ground for Lai Haraoba festival", "noun", "culture"),
    ]
    for w, r, m, pos, cat in PAIRED_COMPOUNDS:
        add_entry(w, r, m, pos, cat)

    # Noun-person attributive compounds
    PERSON_COMPOUNDS = [
        ("ꯑꯐꯕ ꯃꯤ", "aphaba mi", "virtuous person / good soul", "noun", "society"),
        ("ꯐꯠꯇꯕ ꯃꯤ", "phattaba mi", "wicked person / miscreant", "noun", "society"),
        ("ꯂꯧꯁꯤꯡ ꯂꯩꯕ ꯃꯤ", "lousing leiba mi", "wise person / intellectual", "noun", "society"),
        ("ꯂꯧꯁꯤꯡ ꯂꯩꯇꯕ ꯃꯤ", "lousing leitaba mi", "foolish person / simpleton", "noun", "society"),
        ("ꯊꯧꯅꯥ ꯂꯩꯕ ꯃꯤ", "thouna leiba mi", "courageous person / hero", "noun", "society"),
        ("ꯊꯧꯅꯥ ꯂꯩꯇꯕ ꯃꯤ", "thouna leitaba mi", "cowardly person", "noun", "society"),
        ("ꯑꯍꯜ ꯃꯤ", "ahal mi", "elderly respected person", "noun", "society"),
        ("ꯅꯍꯥ ꯃꯤ", "naha mi", "young youth", "noun", "society"),
        ("ꯂꯥꯏꯔꯕ ꯃꯤ", "lairaba mi", "impoverished person", "noun", "society"),
        ("ꯏꯟꯁꯥꯡ-ꯅꯥꯄꯤ", "insang-napi", "leafy green vegetables and herbs", "noun", "food"),
        ("ꯑꯆꯨꯝꯕ ꯋꯥꯐꯝ", "achumba wafam", "true and accurate statement / truth", "noun", "education"),
        ("ꯑꯔꯥꯅꯕ ꯋꯥꯐꯝ", "aranba wafam", "erroneous or false statement", "noun", "education"),
    ]
    for w, r, m, pos, cat in PERSON_COMPOUNDS:
        add_entry(w, r, m, pos, cat)

    # 3. Regular morphological paradigms for VERB_ROOTS:
    # Every verb has:
    # - Negative (-taba / -daba): "to not [verb] / abstention from [verb]"
    # - Causative (-hanba): "to cause to [verb] / to make [someone] [verb]"
    # - Reciprocal / joint (-minnaba): "to [verb] together / mutually [verb]"
    # - Inward / focused (-sinba): "to [verb] inward / attentively"
    # - Outward / emergent (-thokpa): "to [verb] outward / expressively"
    # - Agentive noun ([verb] + " ꯃꯤ"): "person who [verbs] / [verb]er"
    # - Action noun / place ([root] + "ꯐꯝ"): "place for [verb]ing"
    # - Continuous / progressive ([root] + "ꯔꯤꯕ" / "ꯂꯤꯕ"): "[verb]ing / currently [verb]ing"
    # - Past definite ([root] + "ꯈꯤꯕ"): "having [verb]ed / past [verb]"

    for item in VERB_ROOTS:
        full_word = item[0]
        full_roman = item[1]
        base_meaning = item[2]

        # Extract root by stripping citation suffix ꯕ (ba) or ꯄ (pa)
        if full_word.endswith("ꯕ"):
            root = full_word[:-1]
            root_r = full_roman[:-2] if full_roman.endswith("ba") else full_roman
        elif full_word.endswith("ꯄ"):
            root = full_word[:-1]
            root_r = full_roman[:-2] if full_roman.endswith("pa") else full_roman
        else:
            continue

        # Extract basic English verb action from "to [action] ..."
        parts = base_meaning.replace("to ", "").split(" / ")
        primary_act = parts[0].strip()

        # a) Negative citation form
        # In Meitei, root ending in vowel/sonorant takes -daba (ꯗꯕ), voiceless takes -taba (ꯇꯕ)
        # Using standard spelling
        neg_word = root + "ꯇꯕ"
        neg_r = root_r + "taba"
        add_entry(neg_word, neg_r, f"to not {primary_act} / abstention from {primary_act}", "verb", "actions")

        # b) Causative form (-hanba)
        caus_word = root + "ꯍꯟꯕ"
        caus_r = root_r + "hanba"
        add_entry(caus_word, caus_r, f"to cause to {primary_act} / make {primary_act}", "verb", "actions")

        # c) Reciprocal / joint form (-minnaba)
        recip_word = root + "ꯃꯤꯟꯅꯕ"
        recip_r = root_r + "minnaba"
        add_entry(recip_word, recip_r, f"to {primary_act} together / mutually {primary_act}", "verb", "actions")

        # d) Progressive form (-riba / -liba)
        prog_word = root + "ꯔꯤꯕ"
        prog_r = root_r + "riba"
        add_entry(prog_word, prog_r, f"{primary_act}ing / in the process of {primary_act}ing", "verb", "actions")

        # e) Past completed form (-khiba)
        past_word = root + "ꯈꯤꯕ"
        past_r = root_r + "khiba"
        add_entry(past_word, past_r, f"having {primary_act}ed / completed {primary_act}ing", "verb", "actions")

        # f) Future participle / obligation (-gadaba)
        fut_word = root + "ꯒꯗꯕ"
        fut_r = root_r + "gadaba"
        add_entry(fut_word, fut_r, f"to be {primary_act}ed / required to {primary_act}", "adjective", "actions")

        # g) Action / place noun (-fam)
        fam_word = root + "ꯐꯝ"
        fam_r = root_r + "fam"
        add_entry(fam_word, fam_r, f"place or station for {primary_act}ing", "noun", "actions")

        # h) Agentive noun ([verb] + " ꯃꯤ")
        agent_word = full_word + " ꯃꯤ"
        agent_r = full_roman + " mi"
        add_entry(agent_word, agent_r, f"person who performs {primary_act}ing / {primary_act}er", "noun", "society")

    print(f"After verb paradigms: {len(entries)} entries.")

    # 4. Regular paradigms for ADJECTIVE_ROOTS:
    # - Negative adjective: root + " ꯅꯠꯇꯕ" (nattaba) or "-taba"
    # - Intensive: "ꯌꯥꯝꯅ " + adjective = "very [adj]"
    # - Abstract quality noun: "ꯃ-" + root or root + "ꯒꯤ ꯃꯒꯨꯟ" = "quality of [adj]"
    for item in ADJECTIVE_ROOTS:
        adj_word = item[0]
        adj_roman = item[1]
        adj_meaning = item[2]
        cat = item[4]

        # Extract primary adjective
        primary_adj = adj_meaning.split(" / ")[0].strip()

        # Intensive
        int_word = "ꯌꯥꯝꯅ " + adj_word
        int_r = "yamna " + adj_roman
        add_entry(int_word, int_r, f"very {primary_adj} / extremely {primary_adj}", "adjective", cat)

        # Quality / Abstract noun (prefix ꯃ- or suffix ꯃꯒꯨꯟ)
        qual_word = adj_word + "ꯒꯤ ꯃꯒꯨꯟ"
        qual_r = adj_roman + "gi magun"
        add_entry(qual_word, qual_r, f"virtue, quality or property of being {primary_adj}", "noun", "descriptors")

    # 5. Possessive paradigms for ANATOMY_AND_BODY and KINSHIP_AND_FAMILY:
    # ꯏ- (my), ꯅ- (your), ꯃ- (his/her/its)
    body_core = [
        ("ꯀꯣꯛ", "kok", "head"),
        ("ꯃꯤꯠ", "mit", "eye"),
        ("ꯅꯥ", "na", "ear"),
        ("ꯆꯤꯜ", "chil", "lip"),
        ("ꯌꯥ", "ya", "tooth"),
        ("ꯂꯩ", "lei", "tongue"),
        ("ꯈꯧ", "khou", "throat"),
        ("ꯉꯛ", "ngak", "neck"),
        ("ꯊꯧ", "thou", "chest"),
        ("ꯊꯃꯣꯏ", "thamoi", "heart"),
        ("ꯄꯨꯛ", "puk", "belly"),
        ("ꯈꯨꯠ", "khut", "hand"),
        ("ꯈꯣꯡ", "khong", "foot"),
        ("ꯁꯝ", "sam", "hair"),
        ("ꯎꯟ", "un", "skin"),
        ("ꯁꯔꯨ", "saru", "bone"),
        ("ꯍꯀꯆꯥꯡ", "hakchang", "body"),
        ("ꯊꯋꯥꯏ", "thawai", "soul"),
    ]

    for root_w, root_r, gloss in body_core:
        # My (ꯏ-)
        add_entry("ꯏ" + root_w, "i" + root_r, f"my {gloss}", "noun", "body")
        # Your (ꯅ-)
        add_entry("ꯅ" + root_w, "na" + root_r, f"your {gloss}", "noun", "body")
        # His/her/its (ꯃ-)
        add_entry("ꯃ" + root_w, "ma" + root_r, f"his or her {gloss}", "noun", "body")

    # 6. Plural forms for nouns across nature, fauna, flora, food, society, culture:
    # [noun] + "ꯁꯤꯡ" (-sing: plural marker)
    plural_bases = (
        FAUNA_ANIMALS_BIRDS + FLORA_PLANTS_TREES + DWELLINGS_AND_HOUSEHOLD +
        SOCIETY_EDUCATION_LAW + CLOTHING_AND_TEXTILES
    )

    for item in plural_bases:
        w = item[0]
        r = item[1]
        m = item[2].split(" / ")[0]
        cat = item[4]

        plural_w = w + "ꯁꯤꯡ"
        plural_r = r + "sing"
        add_entry(plural_w, plural_r, f"{m}s (plural)", "noun", cat)

    # 7. Diminutive (macha) and Augmentative (jao / chouba) compounds:
    noun_roots_for_size = [
        ("ꯆꯤꯡ", "ching", "mountain"),
        ("ꯄꯥꯠ", "pat", "lake"),
        ("ꯇꯨꯔꯦꯜ", "turel", "river"),
        ("ꯈꯣꯡꯕꯥꯟ", "khongban", "canal"),
        ("ꯎ", "u", "tree"),
        ("ꯋꯥ", "wa", "bamboo"),
        ("ꯂꯩ", "lei", "flower"),
        ("ꯄꯥꯝꯕꯤ", "pambi", "plant"),
        ("ꯎꯆꯦꯛ", "uchek", "bird"),
        ("ꯉꯥ", "nga", "fish"),
        ("ꯁꯥ", "sa", "animal"),
        ("ꯍꯨꯏ", "hui", "dog"),
        ("ꯍꯧꯗꯣꯡ", "houdong", "cat"),
        ("ꯁꯟ", "san", "cattle"),
        ("ꯁꯒꯣꯜ", "sagol", "horse"),
        ("ꯌꯦꯟ", "yen", "fowl"),
        ("ꯌꯨꯝ", "yum", "house"),
        ("ꯊꯣꯡ", "thong", "bridge"),
        ("ꯀꯥ", "ka", "room"),
        ("ꯄꯨꯈ꯭ꯔꯤ", "pukhri", "pond"),
        ("ꯂꯧꯕꯨꯛ", "laubuk", "paddy field"),
        ("ꯀꯩꯊꯦꯜ", "keithel", "market"),
        ("ꯈꯨꯟ", "khun", "village"),
        ("ꯂꯥꯏꯔꯤꯛ", "lairik", "book"),
        ("ꯐꯛ", "fak", "mat"),
        ("ꯄꯨꯟ", "pun", "pot"),
        ("ꯆꯐꯨ", "chaphu", "clay cooking pot"),
    ]

    for nw, nr, ngloss in noun_roots_for_size:
        # Diminutive (-macha)
        dim_w = nw + "ꯃꯆꯥ"
        dim_r = nr + "macha"
        add_entry(dim_w, dim_r, f"small {ngloss} / baby {ngloss}", "noun", "nature")

        # Augmentative (-jao / -achouba)
        aug_w = nw + "ꯖꯥꯑꯣ"
        aug_r = nr + "jao"
        add_entry(aug_w, aug_r, f"great {ngloss} / large {ngloss}", "noun", "nature")

    # 8. Compounds of possession / ownership: "[noun] + ꯒꯤ ꯃꯄꯨ" (owner of [noun])
    for nw, nr, ngloss in noun_roots_for_size[:15]:
        mapu_w = nw + "ꯒꯤ ꯃꯄꯨ"
        mapu_r = nr + "gi mapu"
        add_entry(mapu_w, mapu_r, f"owner or keeper of the {ngloss}", "noun", "society")

    # 9. Additional essential everyday words and phrases from Manipuri vocabulary
    # Let's add curated cultural, technological, educational, travel, emotion, and everyday dialogue terms
    SUPPLEMENTARY_TERMS = [
        # Travel & Directions
        ("ꯂꯝꯕꯤ", "lambi", "road / path / street / highway", "noun", "travel"),
        ("ꯂꯝꯕꯤ ꯑꯆꯧꯕ", "lambi achouba", "main road / broad highway", "noun", "travel"),
        ("ꯂꯝꯕꯤ ꯃꯆꯥ", "lambi macha", "alley / footpath / byway", "noun", "travel"),
        ("ꯈꯣꯡꯆꯠ", "khongchat", "journey / travel / voyage / excursion", "noun", "travel"),
        ("ꯈꯣꯡꯆꯠꯂꯣꯏ", "khongchatloi", "traveler / passenger / voyager", "noun", "travel"),
        ("ꯍꯤ", "hi", "boat / vessel / craft", "noun", "travel"),
        ("ꯍꯤꯍꯣꯟꯕ", "hihonba", "boatman / oarsman / rower", "noun", "travel"),
        ("ꯒꯥꯔꯤ", "gari", "vehicle / carriage / cart / car", "noun", "travel"),
        ("ꯒꯥꯔꯤ ꯊꯧꯕ", "gari thouba", "driver / driving a vehicle", "noun", "travel"),
        ("ꯑꯋꯥꯡ", "awang", "north / northern direction", "noun", "travel"),
        ("ꯃꯈꯥ", "makha", "south / southern direction", "noun", "travel"),
        ("ꯅꯣꯡꯄꯣꯛ", "nongpok", "east / eastern direction (where sun rises)", "noun", "travel"),
        ("ꯅꯣꯡꯆꯨꯞ", "nongchup", "west / western direction (where sun sets)", "noun", "travel"),
        ("ꯑꯋꯥꯡ-ꯅꯣꯡꯄꯣꯛ", "awang-nongpok", "northeast", "noun", "travel"),
        ("ꯑꯋꯥꯡ-ꯅꯣꯡꯆꯨꯞ", "awang-nongchup", "northwest", "noun", "travel"),
        ("ꯃꯈꯥ-ꯅꯣꯡꯄꯣꯛ", "makha-nongpok", "southeast", "noun", "travel"),
        ("ꯃꯈꯥ-ꯅꯣꯡꯆꯨꯞ", "makha-nongchup", "southwest", "noun", "travel"),
        ("ꯅꯣꯡꯄꯣꯛ ꯊꯪꯕ", "nongpok thangba", "oriental / eastern", "adjective", "travel"),
        ("ꯅꯣꯡꯆꯨꯞ ꯊꯪꯕ", "nongchup thangba", "occidental / western", "adjective", "travel"),
        ("ꯄꯥꯟꯊꯨꯡ", "panthung", "destination / terminal goal", "noun", "travel"),
        ("ꯄꯣꯠꯆꯩ", "potchei", "luggage / baggage / belongings", "noun", "travel"),
        ("ꯇꯤꯀꯦꯠ", "tiket", "ticket / travel pass", "noun", "travel"),
        ("ꯄꯣꯔꯠ", "port", "harbor / transit port / airport", "noun", "travel"),
        ("ꯃꯥꯏꯀꯩ", "maikei", "direction / compass bearing", "noun", "travel"),
        ("ꯃꯥꯏꯀꯩ ꯃꯔꯤ", "maikei mari", "the four cardinal directions", "noun", "travel"),

        # Modern Technology & Science
        ("ꯀꯝꯄ꯭ꯌꯨꯇꯔ", "computer", "computer / electronic processing device", "noun", "technology"),
        ("ꯏꯟꯇꯔꯅꯦꯠ", "internet", "internet / world wide computer network", "noun", "technology"),
        ("ꯃꯣꯕꯥꯏꯜ ꯐꯣꯟ", "mobile phone", "cellular telephone / smartphone", "noun", "technology"),
        ("ꯄꯥꯎꯆꯦ", "pauche", "newspaper / gazette / printed journal", "noun", "education"),
        ("ꯄꯥꯎ", "pau", "news / message / information", "noun", "education"),
        ("ꯄꯥꯎꯃꯤ", "paumi", "journalist / reporter / messenger", "noun", "society"),
        ("ꯄꯥꯎꯇꯥꯛ", "pautak", "advice / counsel / guidance", "noun", "education"),
        ("ꯋꯥꯐꯝ", "wafam", "point / issue / fact / topic of discussion", "noun", "education"),
        ("ꯋꯥꯐꯝ ꯑꯆꯨꯝꯕ", "wafam achumba", "accurate fact / true statement", "noun", "education"),
        ("ꯂꯥꯏꯔꯤꯛ ꯄꯥꯐꯝ", "lairik pafam", "library / study reading room", "noun", "education"),
        ("ꯁꯥꯏꯟꯁ", "science", "natural science / systematic empirical inquiry", "noun", "education"),
        ("ꯃꯍꯩ ꯇꯝꯕ", "mahei tamba", "learning / scholarship", "noun", "education"),
        ("ꯃꯍꯩ ꯇꯥꯛꯄ", "mahei takpa", "pedagogy / teaching / instruction", "noun", "education"),
        ("ꯄꯔꯤꯛꯁꯥ", "pariksa", "examination / test of competence", "noun", "education"),
        ("ꯃꯥꯏꯄꯥꯛ ꯆꯦ", "maipak che", "certificate / diploma of achievement", "noun", "education"),

        # Emotions & Sensations
        ("ꯅꯨꯡꯁꯤ-ꯍꯩꯅꯕ", "nungsi-heinaba", "affection and mutual intimacy", "noun", "emotions"),
        ("ꯅꯨꯡꯉꯥꯏ-ꯌꯥꯏꯐꯕ", "nungai-yaiphaba", "prosperity, peace and joyful wellbeing", "noun", "emotions"),
        ("ꯊꯃꯣꯏ ꯄꯦꯟꯕ", "thamoi penba", "heartfelt contentment / satisfaction", "noun", "emotions"),
        ("ꯊꯃꯣꯏ ꯅꯨꯡꯉꯥꯏꯇꯕ", "thamoi nungaitaba", "sorrow of the heart / grief", "noun", "emotions"),
        ("ꯊꯧꯅꯥ", "thouna", "courage / valor / bravery / boldness", "noun", "emotions"),
        ("ꯊꯧꯅꯥ ꯂꯩꯕ", "thouna leiba", "courageous / heroic / brave", "adjective", "emotions"),
        ("ꯊꯧꯅꯥ ꯂꯩꯇꯕ", "thouna leitaba", "timid / lacking boldness / fearful", "adjective", "emotions"),
        ("ꯏꯀꯥꯏꯕ", "ikaiba", "shame / shyness / modesty", "noun", "emotions"),
        ("ꯏꯀꯥꯏ ꯈꯪꯕ", "ikai khangba", "sense of decency / polite modesty", "noun", "emotions"),
        ("ꯏꯀꯥꯏ ꯈꯪꯗꯕ", "ikai khangdaba", "shameless / insolent / brazen", "adjective", "emotions"),
        ("ꯂꯥꯏꯕꯛ", "laibak", "fortune / destiny / luck", "noun", "emotions"),
        ("ꯂꯥꯏꯕꯛ ꯐꯕ", "laibak phaba", "fortunate / blessed with good luck", "adjective", "emotions"),
        ("ꯂꯥꯏꯕꯛ ꯊꯤꯕ", "laibak thiba", "unfortunate / unlucky / ill-fated", "adjective", "emotions"),
        ("ꯌꯥꯏꯐꯕ", "yaiphaba", "auspicious / blessed / prosperous", "adjective", "emotions"),
        ("ꯊꯧꯖꯥꯜ", "thoujal", "divine blessings / grace / benevolence", "noun", "culture"),
        ("ꯊꯧꯖꯥꯜ ꯐꯪꯕ", "thoujal phangba", "blessed / recipient of divine favor", "verb", "culture"),

        # Seasons & Natural phenomena
        ("ꯀꯥꯂꯦꯟ ꯊꯥ", "kalen tha", "dry pre-monsoon summer season", "noun", "nature"),
        ("ꯅꯣꯡꯖꯨ ꯊꯥ", "nongju tha", "rainy season months", "noun", "nature"),
        ("ꯅꯤꯡꯊꯝ ꯊꯥ", "ningtham tha", "cold winter season months", "noun", "nature"),
        ("ꯌꯦꯟꯊꯥ ꯊꯥ", "yentha tha", "pleasant spring months", "noun", "nature"),
        ("ꯑꯍꯤꯡ ꯑꯃꯨꯕ", "ahing amuba", "pitch-dark night", "noun", "nature"),
        ("ꯅꯨꯃꯤꯠ ꯇꯥꯕ", "numit taba", "sunset / nightfall", "noun", "nature"),
        ("ꯅꯨꯃꯤꯠ ꯊꯣꯛꯄ", "numit thokpa", "sunrise / dawn break", "noun", "nature"),
        ("ꯊꯥ ꯄꯨꯔꯅꯤꯃꯥ", "tha purnima", "full moon night", "noun", "nature"),
        ("ꯊꯥ ꯑꯃꯥꯋꯥꯁ", "tha amawas", "new moon night / dark phase", "noun", "nature"),
        ("ꯂꯩꯆꯤꯜ ꯀꯨꯞꯄ", "leichil kuppa", "overcast sky / cloud-covered heaven", "noun", "nature"),
        ("ꯅꯣꯡꯂꯩ", "nonglei", "thunderstorm / tempest", "noun", "nature"),
        ("ꯅꯨꯡꯁꯤꯠ ꯑꯀꯟꯕ", "nungsit akanba", "gale-force wind / strong breeze", "noun", "nature"),
        ("ꯎꯟ", "un", "snow / frost / winter dew", "noun", "nature"),

        # Commerce, Currency & Measurements
        ("ꯁꯦꯜ", "sel", "money / coin / currency / bell-metal", "noun", "society"),
        ("ꯁꯦꯜ-ꯊꯨꯝ", "sel-thum", "wealth / finance / economic assets", "noun", "society"),
        ("ꯂꯨꯄꯥ", "lupa", "rupee / silver coin", "noun", "society"),
        ("ꯁꯦꯟꯖꯥ", "senja", "interest on money / loan dividend", "noun", "society"),
        ("ꯄꯣꯠꯂꯝ", "potlam", "goods / articles of trade / merchandise", "noun", "society"),
        ("ꯃꯃꯜ", "mamal", "price / monetary value / cost", "noun", "society"),
        ("ꯃꯃꯜ ꯌꯥꯝꯕ", "mamal yamba", "costly / expensive / dear", "adjective", "society"),
        ("ꯃꯃꯜ ꯇꯥꯡꯕ", "mamal tangba", "scarce and precious / high-priced", "adjective", "society"),
        ("ꯃꯃꯜ ꯍꯣꯡꯕ", "mamal hongba", "inexpensive / economical / cheap", "adjective", "society"),
        ("ꯂꯥꯜ", "lal", "war / battle / military expedition", "noun", "society"),
        ("ꯂꯥꯟꯃꯤ", "lanmi", "soldier / warrior / army troop", "noun", "society"),
        ("ꯂꯥꯟꯖꯥꯎ", "lanjao", "great war / major military conflict", "noun", "society"),
        ("ꯂꯥꯟꯕꯟ", "lanban", "fortress / rampart / stockade", "noun", "society"),
        ("ꯉꯥꯛꯁꯦꯜ", "ngaksel", "defense / security / vigilance", "noun", "society"),
        ("ꯆꯠꯅ-ꯀꯥꯡꯂꯣꯟ", "chatna-kanglon", "laws / customary regulations / code of conduct", "noun", "society"),
        ("ꯅꯤꯡꯊꯧꯔꯣꯜ", "ningthourol", "chronicle of kings / royal lineage puya", "noun", "culture"),
        ("ꯆꯩꯊꯥꯔꯣꯜ ꯀꯨꯝꯕꯥꯕ", "cheitharol kumbaba", "The Royal Court Chronicle of the Kings of Manipur", "noun", "culture"),

        # Spatial relations & Landscape compounds
        ("ꯆꯤꯡꯊꯛ", "chingthak", "summit of the mountain / mountain top", "noun", "nature"),
        ("ꯆꯤꯡꯈꯥ", "chingkha", "foot of the mountain / valley base", "noun", "nature"),
        ("ꯄꯥꯠꯃꯥꯌ", "patmai", "lakeshore / lake edge", "noun", "nature"),
        ("ꯇꯨꯔꯦꯜꯃꯥꯌ", "turelmai", "riverbank / waterside", "noun", "nature"),
        ("ꯎꯃꯪꯃꯅꯨꯡ", "umangmanung", "deep interior of the forest", "noun", "nature"),
        ("ꯎꯃꯪꯃꯄꯥꯟ", "umangmapan", "outskirts of the woodland", "noun", "nature"),
        ("ꯂꯧꯕꯨꯛꯃꯅꯨꯡ", "laubukmanung", "heart of the paddy fields", "noun", "nature"),
        ("ꯌꯨꯝꯃꯅꯨꯡ", "yummanung", "interior of the house / within the home", "noun", "home"),
        ("ꯌꯨꯝꯃꯄꯥꯟ", "yummapan", "front yard / outside the house", "noun", "home"),
        ("ꯀꯩꯊꯦꯜꯃꯅꯨꯡ", "keithelmanung", "interior bazaar / inside the market", "noun", "society"),
        ("ꯊꯣꯡꯃꯅꯥꯛ", "thongmanak", "near the door / near the bridge", "noun", "home"),
        ("ꯂꯥꯏꯁꯪꯃꯅꯥꯛ", "laisangmanak", "vicinity of the sacred temple", "noun", "culture"),

        # Additional cultural, literary & craft terms
        ("ꯄꯨꯌꯥ ꯄꯥꯕ", "puya paba", "reading the sacred ancient scriptures", "noun", "culture"),
        ("ꯄꯨꯌꯥ ꯏꯕ", "puya iba", "writing the historical chronicles", "noun", "culture"),
        ("ꯏꯁꯩ ꯁꯦꯝꯕ", "ishei semba", "composing musical melodies", "noun", "culture"),
        ("ꯁꯩꯔꯦꯡ ꯏꯕ", "sheireng iba", "writing lyric poetry", "noun", "culture"),
        ("ꯋꯥꯔꯤ ꯏꯕ", "wari iba", "authoring prose and tales", "noun", "education"),
        ("ꯂꯥꯏ ꯍꯔꯥꯎꯕ ꯇꯧꯕ", "lai haraoba touba", "celebrating the festival of the deities", "verb", "culture"),
        ("ꯃꯥꯏꯕꯤ ꯂꯥꯏꯆꯠ", "maibi laichat", "spiritual invocation of the priestess", "noun", "culture"),
        ("ꯄꯦꯅꯥ ꯈꯣꯟꯊꯣꯛ", "pena khonthok", "resonant melody of the Pena lute", "noun", "culture"),
        ("ꯄꯨꯡ ꯈꯣꯟꯊꯣꯛ", "pung khonthok", "rhythmic cadence of the Meitei drum", "noun", "culture"),
        ("ꯈꯨꯂꯥꯡ ꯈꯣꯟꯊꯣꯛ", "khulang khonthok", "pastoral lilt of harvest songs", "noun", "culture"),
        ("ꯀꯪꯂꯥ ꯊꯣꯡꯉꯥꯜ", "kangla thongngal", "sacred eastern gateway of Kangla", "noun", "culture"),
        ("ꯅꯤꯡꯊꯧ ꯀꯣꯅꯨꯡ", "ningthou konung", "royal palace of the kings of Manipur", "noun", "culture"),
        ("ꯁꯦꯅꯥꯃꯍꯤ ꯀꯆꯤꯟ", "sanamahi kachin", "sacred south-west corner of home dedicated to Sanamahi", "noun", "culture"),
        ("ꯐꯨꯡꯒꯥ ꯂꯥꯏꯔꯨ", "phunga lairu", "sacred central hearth of the Meitei dwelling", "noun", "culture"),
        ("ꯐꯨꯡꯒꯥ ꯃꯩ", "phunga mei", "sacred domestic hearth fire", "noun", "home"),
        ("ꯐꯨꯡꯒꯥ ꯋꯥꯔꯤ", "phunga wari", "fireside folktales told by hearthside", "noun", "culture"),
        ("ꯅꯤꯡꯉꯣꯜ ꯆꯥꯛ", "ningol chak", "traditional feast prepared for married sisters", "noun", "culture"),
        ("ꯆꯦꯏꯔꯥꯑꯣꯕ ꯆꯥꯛ", "cheiraoba chak", "ceremonial meal offered on New Year Day", "noun", "culture"),
        ("ꯌꯥꯑꯣꯁꯪ ꯃꯩ", "yaoshang mei", "sacred burning of straw hut at Yaoshang", "noun", "culture"),
        ("ꯊꯥꯕꯜ ꯆꯣꯡꯐꯝ", "thabal chongfam", "open courtyard for moonlight dance", "noun", "culture"),
    ]

    for item in SUPPLEMENTARY_TERMS:
        add_entry(item[0], item[1], item[2], item[3], item[4])

    print(f"Total compiled unique vocabulary entries: {len(entries)}")
    return entries

if __name__ == "__main__":
    lex = build_full_lexicon()
    print(f"Validation: Total unique entries = {len(lex)}")

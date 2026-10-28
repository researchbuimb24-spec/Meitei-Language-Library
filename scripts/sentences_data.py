# -*- coding: utf-8 -*-
"""
Authentic Daily Usable Meitei / Manipuri Sentences Dataset.

Contains high-frequency everyday sentences across 12 practical categories
with authentic Meitei Mayek, Roman transliteration, Bengali script,
English translations, and conversational context annotations.
"""

import io
import sys
from typing import List, Dict, Any

if isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SENTENCES: List[Dict[str, Any]] = [
    # -------------------------------------------------------------
    # 1. Greetings & Salutations (ꯈꯨꯔꯨꯝꯖꯕ / Greetings)
    # -------------------------------------------------------------
    {
        "sentence_id": "greet_001",
        "meitei": "ꯈꯨꯔꯨꯝꯖꯔꯤ꯫",
        "roman": "Khurumjari.",
        "bengali": "খুরূমজরি।",
        "english": "Greetings / Respectful salutations.",
        "category": "greetings",
        "context": "Standard respectful greeting used at any time of day."
    },
    {
        "sentence_id": "greet_002",
        "meitei": "ꯅꯪ ꯀꯔꯝꯅ ꯂꯩꯔꯤ?",
        "roman": "Nang karamna leiri?",
        "bengali": "নং করম্না লৈরি?",
        "english": "How are you? (informal/peer)",
        "category": "greetings",
        "context": "Asking how a friend or peer is doing."
    },
    {
        "sentence_id": "greet_003",
        "meitei": "ꯑꯗꯣꯝ ꯀꯔꯝꯅ ꯂꯩꯕꯤꯔꯤ?",
        "roman": "Adom karamna leibiri?",
        "bengali": "অদোম করম্না লৈবিরি?",
        "english": "How are you? (honorific / respectful to elders)",
        "category": "greetings",
        "context": "Polite greeting used when addressing elders or respected individuals."
    },
    {
        "sentence_id": "greet_004",
        "meitei": "ꯑꯩ ꯅꯨꯡꯉꯥꯏꯅ ꯂꯩꯔꯤ꯫",
        "roman": "Ei nungngaina leiri.",
        "bengali": "ঐ নুংঙাইনা লৈরি।",
        "english": "I am doing well / I am fine.",
        "category": "greetings",
        "context": "Common response indicating good health and spirits."
    },
    {
        "sentence_id": "greet_005",
        "meitei": "ꯑꯌꯨꯛꯀꯤ ꯈꯨꯔꯨꯝꯖꯔꯤ꯫",
        "roman": "Ayuk-ki khurumjari.",
        "bengali": "অয়ুক্কী খুরূমজরি।",
        "english": "Good morning.",
        "category": "greetings",
        "context": "Morning salutation."
    },
    {
        "sentence_id": "greet_006",
        "meitei": "ꯅꯨꯃꯤꯗꯥꯡꯒꯤ ꯈꯨꯔꯨꯝꯖꯔꯤ꯫",
        "roman": "Numidang-gi khurumjari.",
        "bengali": "নুমিদাংগী খুরূমজরি।",
        "english": "Good evening.",
        "category": "greetings",
        "context": "Evening salutation."
    },
    {
        "sentence_id": "greet_007",
        "meitei": "ꯑꯩꯈꯣꯏ ꯀꯣꯟꯅ ꯑꯃꯨꯛ ꯎꯅꯁꯤ꯫",
        "roman": "Eikhoi konna amuk unasi.",
        "bengali": "ঐখোই কোন্না অমুক উনসী।",
        "english": "Let us meet again later / See you later.",
        "category": "greetings",
        "context": "Friendly parting phrase."
    },
    {
        "sentence_id": "greet_008",
        "meitei": "ꯇꯔꯥꯝꯅ ꯑꯣꯛꯆꯔꯤ꯫",
        "roman": "Taramna okchari.",
        "bengali": "তরাম্না ওকচরি।",
        "english": "Hearty welcome!",
        "category": "greetings",
        "context": "Welcoming guests warmly to one's home or gathering."
    },
    {
        "sentence_id": "greet_009",
        "meitei": "ꯅꯪ ꯆꯥꯛ ꯆꯥꯔꯕ꯭ꯔꯥ?",
        "roman": "Nang chak charabra?",
        "bengali": "নং চাক চারব্রা?",
        "english": "Have you eaten rice / Have you had your meal?",
        "category": "greetings",
        "context": "Quintessential caring Meitei greeting inquiry."
    },
    {
        "sentence_id": "greet_010",
        "meitei": "ꯍꯣꯏ, ꯑꯩ ꯆꯥꯔꯦ, ꯅꯪꯅ?",
        "roman": "Hoi, ei chare, nangna?",
        "bengali": "হোই, ঐ চারে, নংনা?",
        "english": "Yes, I have eaten, and you?",
        "category": "greetings",
        "context": "Polite response to meal inquiries."
    },

    # -------------------------------------------------------------
    # 2. Introductions & Personal Identity (ꯃꯁꯛ ꯇꯥꯛꯄ / Introductions)
    # -------------------------------------------------------------
    {
        "sentence_id": "intro_001",
        "meitei": "ꯅꯪꯒꯤ ꯃꯤꯡ ꯀꯔꯤ ꯀꯧꯏ?",
        "roman": "Nanggi ming kari koui?",
        "bengali": "নঙ্গী মিং করি কৌই?",
        "english": "What is your name?",
        "category": "introductions",
        "context": "Asking someone's name."
    },
    {
        "sentence_id": "intro_002",
        "meitei": "ꯑꯩꯒꯤ ꯃꯤꯡ ꯇꯣꯝꯕ ꯀꯧꯏ꯫",
        "roman": "Eigi ming Tomba koui.",
        "bengali": "ঐগী মিং তোম্বা কৌই।",
        "english": "My name is Tomba.",
        "category": "introductions",
        "context": "Introducing your name."
    },
    {
        "sentence_id": "intro_003",
        "meitei": "ꯅꯪ ꯀꯗꯥꯏꯗꯒꯤ ꯂꯥꯛꯄꯒꯦ?",
        "roman": "Nang kadaidagi lakpage?",
        "bengali": "নং কদাইদগী লাকপগে?",
        "english": "Where do you come from?",
        "category": "introductions",
        "context": "Inquiring about someone's origin."
    },
    {
        "sentence_id": "intro_004",
        "meitei": "ꯑꯩ ꯏꯝꯐꯥꯜꯗꯒꯤ ꯂꯥꯛꯄꯅꯤ꯫",
        "roman": "Ei Imphaldagi lakpani.",
        "bengali": "ঐ ইম্ফাল্দগী লাকপনী।",
        "english": "I come from Imphal.",
        "category": "introductions",
        "context": "Stating your place of origin."
    },
    {
        "sentence_id": "intro_005",
        "meitei": "ꯅꯪ ꯀꯗꯥꯏꯗ ꯂꯩꯔꯤ?",
        "roman": "Nang kadaida leiri?",
        "bengali": "নং কদাইদ লৈরি?",
        "english": "Where do you live / reside?",
        "category": "introductions",
        "context": "Asking someone's residence."
    },
    {
        "sentence_id": "intro_006",
        "meitei": "ꯑꯩ ꯃꯅꯤꯄꯨꯔꯗ ꯂꯩꯔꯤ꯫",
        "roman": "Ei Manipurda leiri.",
        "bengali": "ঐ মণিপুরদ লৈরি।",
        "english": "I live in Manipur.",
        "category": "introductions",
        "context": "Stating current residence."
    },
    {
        "sentence_id": "intro_007",
        "meitei": "ꯑꯩ ꯃꯩꯇꯩꯂꯣꯟ ꯇꯝꯂꯤ꯫",
        "roman": "Ei Meiteilon tamli.",
        "bengali": "ঐ মৈতৈলোন্ তম্লি।",
        "english": "I am learning the Meitei language.",
        "category": "introductions",
        "context": "Explaining language learning endeavor."
    },
    {
        "sentence_id": "intro_008",
        "meitei": "ꯅꯪ ꯃꯩꯇꯩꯂꯣꯟ ꯉꯥꯡꯕ ꯉꯝꯕ꯭ꯔꯥ?",
        "roman": "Nang Meiteilon ngangba ngambra?",
        "bengali": "নং মৈতৈলোন্ ঙাংবা ঙম্ব্রা?",
        "english": "Can you speak the Meitei language?",
        "category": "introductions",
        "context": "Asking about language ability."
    },
    {
        "sentence_id": "intro_009",
        "meitei": "ꯑꯩ ꯈꯔ ꯈꯔ ꯉꯥꯡꯕ ꯉꯝꯃꯤ꯫",
        "roman": "Ei khara khara ngangba ngammi.",
        "bengali": "ঐ খর খর ঙাংবা ঙম্মী।",
        "english": "I can speak a little bit.",
        "category": "introductions",
        "context": "Modest response regarding language proficiency."
    },
    {
        "sentence_id": "intro_010",
        "meitei": "ꯅꯪꯕꯨ ꯎꯅꯕꯗ ꯌꯥꯝꯅ ꯍꯔꯥꯎꯖꯔꯤ꯫",
        "roman": "Nangbu unabada yamna haraojari.",
        "bengali": "নংবু উনবদ য়াম্না হরাওজরি।",
        "english": "I am very pleased to meet you.",
        "category": "introductions",
        "context": "Expressing delight at meeting someone."
    },

    # -------------------------------------------------------------
    # 3. Politeness, Gratitude & Courtesies (ꯏꯀꯥꯏꯈꯨꯝꯅꯕ / Courtesies)
    # -------------------------------------------------------------
    {
        "sentence_id": "courtesy_001",
        "meitei": "ꯌꯥꯝꯅ ꯊꯥꯒꯠꯆꯔꯤ꯫",
        "roman": "Yamna thagatchari.",
        "bengali": "য়াম্না থাগৎচরি।",
        "english": "Thank you very much.",
        "category": "politeness_gratitude",
        "context": "Standard expression of gratitude."
    },
    {
        "sentence_id": "courtesy_002",
        "meitei": "ꯅꯨꯡꯉꯥꯏꯇꯕ ꯐꯥꯎꯒꯅꯨ꯫",
        "roman": "Nungngaitaba phaoganu.",
        "bengali": "নুংঙাইতবা ফাওগনু।",
        "english": "Please do not worry / You are welcome / No trouble at all.",
        "category": "politeness_gratitude",
        "context": "Gracious response to thank you or apologies."
    },
    {
        "sentence_id": "courtesy_003",
        "meitei": "ꯉꯥꯛꯄꯤꯌꯨ, ꯑꯩ ꯑꯁꯣꯏꯕ ꯇꯧꯔꯦ꯫",
        "roman": "Ngakpiyu, ei asoiba toure.",
        "bengali": "ঙাক্পীয়ু, ঐ অশোইবা তৌরে।",
        "english": "Please forgive me, I made a mistake.",
        "category": "politeness_gratitude",
        "context": "Polite apology."
    },
    {
        "sentence_id": "courtesy_004",
        "meitei": "ꯆꯥꯅꯕꯤꯗꯨꯅ ꯑꯃꯨꯛ ꯍꯥꯌꯕꯤꯌꯨ꯫",
        "roman": "Chanabiduna amuk haybiyu.",
        "bengali": "চানবীদুনা অমুক হায়বীয়ু।",
        "english": "Please say that once again.",
        "category": "politeness_gratitude",
        "context": "Polite request for repetition when not hearing clearly."
    },
    {
        "sentence_id": "courtesy_005",
        "meitei": "ꯆꯥꯅꯕꯤꯗꯨꯅ ꯇꯞꯅ ꯉꯥꯡꯕꯤꯌꯨ꯫",
        "roman": "Chanabiduna tapna ngangbiyu.",
        "bengali": "চানবীদুনা তপ্না ঙাংবীয়ু।",
        "english": "Please speak slowly.",
        "category": "politeness_gratitude",
        "context": "Asking a speaker to slow down for comprehension."
    },
    {
        "sentence_id": "courtesy_006",
        "meitei": "ꯑꯩ ꯈꯪꯗꯦ꯫",
        "roman": "Ei khangde.",
        "bengali": "ঐ খংদে।",
        "english": "I do not know / I am not aware.",
        "category": "politeness_gratitude",
        "context": "Honest expression of non-knowledge."
    },
    {
        "sentence_id": "courtesy_007",
        "meitei": "ꯑꯩ ꯈꯪꯂꯦ꯫",
        "roman": "Ei khangle.",
        "bengali": "ঐ খংলে।",
        "english": "I understand / I know now.",
        "category": "politeness_gratitude",
        "context": "Expressing that something has been understood."
    },
    {
        "sentence_id": "courtesy_008",
        "meitei": "ꯆꯥꯅꯕꯤꯗꯨꯅ ꯐꯝꯕꯤꯌꯨ꯫",
        "roman": "Chanabiduna phambiyu.",
        "bengali": "চানবীদুনা ফম্বীয়ু।",
        "english": "Please take a seat / Please sit down.",
        "category": "politeness_gratitude",
        "context": "Polite hospitality gesture offering a seat."
    },
    {
        "sentence_id": "courtesy_009",
        "meitei": "ꯏꯁꯤꯡ ꯈꯔ ꯊꯛꯄꯤꯌꯨ꯫",
        "roman": "Ishing khara thakpiyu.",
        "bengali": "ঈশিং খর থক্পীয়ু।",
        "english": "Please drink some water.",
        "category": "politeness_gratitude",
        "context": "Offering refreshment to a guest."
    },
    {
        "sentence_id": "courtesy_010",
        "meitei": "ꯑꯗꯣꯃꯒꯤ ꯃꯇꯦꯡ ꯀꯔꯤ ꯄꯥꯡꯒꯦ?",
        "roman": "Adomgi mateng kari pangge?",
        "bengali": "অদোমগী মতেং করি পাংগে?",
        "english": "How may I help you?",
        "category": "politeness_gratitude",
        "context": "Offering assistance politely."
    },

    # -------------------------------------------------------------
    # 4. Market, Shopping & Commerce (ꯀꯩꯊꯦꯜ ꯂꯩ-ꯌꯣꯟ / Shopping)
    # -------------------------------------------------------------
    {
        "sentence_id": "shop_001",
        "meitei": "ꯃꯁꯤꯒꯤ ꯃꯃꯜ ꯀꯌꯥꯅꯣ?",
        "roman": "Masigi mamal kayano?",
        "bengali": "মসীগী মমল কয়ানৌ?",
        "english": "How much does this cost?",
        "category": "market_shopping",
        "context": "Standard pricing inquiry at the market."
    },
    {
        "sentence_id": "shop_002",
        "meitei": "ꯃꯃꯜ ꯌꯥꯝꯅ ꯊꯥꯡꯉꯤ꯫",
        "roman": "Mamal yamna thangngi.",
        "bengali": "মমল য়াম্না থাংঙী।",
        "english": "The price is too high / It is expensive.",
        "category": "market_shopping",
        "context": "Bargaining statement at market stalls."
    },
    {
        "sentence_id": "shop_003",
        "meitei": "ꯈꯔ ꯍꯟꯊꯍꯟꯕꯤꯌꯨ꯫",
        "roman": "Khara hanthahanbiyu.",
        "bengali": "খর হন্থহনবীয়ু।",
        "english": "Please reduce the price a little.",
        "category": "market_shopping",
        "context": "Polite request for discount."
    },
    {
        "sentence_id": "shop_004",
        "meitei": "ꯑꯩ ꯃꯁꯤ ꯂꯧꯒꯦ꯫",
        "roman": "Ei masi louge.",
        "bengali": "ঐ মসী লৌগে।",
        "english": "I will take this / I want to buy this.",
        "category": "market_shopping",
        "context": "Confirming purchase decision."
    },
    {
        "sentence_id": "shop_005",
        "meitei": "ꯏꯃꯥ ꯀꯩꯊꯦꯜ ꯀꯗꯥꯏꯗ ꯂꯩꯕꯒꯦ?",
        "roman": "Ima Keithel kadaida leibage?",
        "bengali": "ইমা কৈথেল কদাইদ লৈবগে?",
        "english": "Where is the famous Ima Keithel (Mother's Market) located?",
        "category": "market_shopping",
        "context": "Asking directions to the world-renowned women-run market in Imphal."
    },
    {
        "sentence_id": "shop_006",
        "meitei": "ꯑꯅꯧꯕ ꯎꯍꯩ-ꯋꯥꯍꯩ ꯂꯩꯕ꯭ꯔꯥ?",
        "roman": "Anouba uhei-wahei leibra?",
        "bengali": "অনৌবা উহৈ-ৱাহৈ লৈব্রা?",
        "english": "Do you have fresh fruits?",
        "category": "market_shopping",
        "context": "Inquiring about fruit freshness."
    },
    {
        "sentence_id": "shop_007",
        "meitei": "ꯆꯥꯛ-ꯍꯥꯎ ꯐꯧ ꯂꯩꯕ꯭ꯔꯥ?",
        "roman": "Chak-hao phou leibra?",
        "bengali": "চাক-হাও ফৌ লৈব্রা?",
        "english": "Do you have aromatic black rice (Chak-hao)?",
        "category": "market_shopping",
        "context": "Inquiring about Manipur's famous indigenous GI-tagged black rice."
    },
    {
        "sentence_id": "shop_008",
        "meitei": "ꯃꯣꯏꯔꯥꯡ ꯐꯤ ꯂꯩꯕ꯭ꯔꯥ?",
        "roman": "Moirang phee leibra?",
        "bengali": "মোইরাং ফী লৈব্রা?",
        "english": "Do you have authentic Moirang Phee handloom fabric?",
        "category": "market_shopping",
        "context": "Asking for traditional Manipuri handloom textiles."
    },
    {
        "sentence_id": "shop_009",
        "meitei": "ꯁꯦꯜ ꯀꯗꯥꯏꯗ ꯄꯤꯒꯗꯕꯅꯣ?",
        "roman": "Sel kadaida pigadabano?",
        "bengali": "শেল কদাইদ পীগদবনৌ?",
        "english": "Where should I pay the money?",
        "category": "market_shopping",
        "context": "Inquiring at checkout."
    },
    {
        "sentence_id": "shop_010",
        "meitei": "ꯈꯨꯠꯄꯤ ꯑꯃ ꯄꯤꯕꯤꯌꯨ꯫",
        "roman": "Khutpi ama pibiyu.",
        "bengali": "খুৎপী অম পীবীয়ু।",
        "english": "Please give me a carry bag.",
        "category": "market_shopping",
        "context": "Requesting bag for purchased goods."
    },

    # -------------------------------------------------------------
    # 5. Food, Dining & Cuisine (ꯆꯥꯛ-ꯏꯁꯤꯡ / Dining)
    # -------------------------------------------------------------
    {
        "sentence_id": "food_001",
        "meitei": "ꯑꯩ ꯆꯥꯛ ꯂꯥꯃ꯭ꯃꯤ꯫",
        "roman": "Ei chak lammi.",
        "bengali": "ঐ চাক লাম্মী।",
        "english": "I am hungry.",
        "category": "food_dining",
        "context": "Expressing hunger."
    },
    {
        "sentence_id": "food_002",
        "meitei": "ꯑꯩ ꯏꯁꯤꯡ ꯇꯧꯔꯛꯑꯦ꯫",
        "roman": "Ei ishing tourake.",
        "bengali": "ঐ ঈশিং তৌরকএ।",
        "english": "I am thirsty.",
        "category": "food_dining",
        "context": "Expressing thirst."
    },
    {
        "sentence_id": "food_003",
        "meitei": "ꯆꯤꯟꯖꯥꯛ ꯑꯁꯤ ꯌꯥꯝꯅ ꯍꯥꯎꯋꯦ꯫",
        "roman": "Chinjak asi yamna haowe.",
        "bengali": "চিন্জাক অসী য়াম্না হাওৱে।",
        "english": "This food is very delicious!",
        "category": "food_dining",
        "context": "Complimenting meal or dish."
    },
    {
        "sentence_id": "food_004",
        "meitei": "ꯏꯔꯣꯝꯕ ꯑꯁꯤ ꯍꯥꯎꯕ ꯑꯗꯨꯝ ꯂꯩꯇꯦ꯫",
        "roman": "Iromba asi haoba adum leite.",
        "bengali": "ইরোম্বা অসী হাওবা অদুম লৈতে।",
        "english": "This traditional Iromba dish is incomparably delicious.",
        "category": "food_dining",
        "context": "Praising the signature Manipuri vegetable and fermented fish delicacy."
    },
    {
        "sentence_id": "food_005",
        "meitei": "ꯆꯥ ꯊꯛꯁꯤ꯫",
        "roman": "Cha thaksi.",
        "bengali": "চা থক্সী।",
        "english": "Let us drink tea.",
        "category": "food_dining",
        "context": "Inviting friends for tea."
    },
    {
        "sentence_id": "food_006",
        "meitei": "ꯆꯥꯅꯕꯤꯗꯨꯅ ꯊꯨꯝ ꯈꯔ ꯄꯤꯕꯤꯌꯨ꯫",
        "roman": "Chanabiduna thum khara pibiyu.",
        "bengali": "চানবীদুনা থুম খর পীবীয়ু।",
        "english": "Please pass some salt.",
        "category": "food_dining",
        "context": "Dining table request."
    },
    {
        "sentence_id": "food_007",
        "meitei": "ꯅꯪ ꯁꯥ-ꯉꯥ ꯆꯥꯕ꯭ꯔꯥ?",
        "roman": "Nang sa-nga chabra?",
        "bengali": "নং শা-ঙা চাব্রা?",
        "english": "Do you eat meat and fish?",
        "category": "food_dining",
        "context": "Inquiring dietary preferences."
    },
    {
        "sentence_id": "food_008",
        "meitei": "ꯑꯩ ꯎꯍꯩ-ꯃꯅꯥ-ꯃꯁꯤꯡ ꯈꯛꯇ ꯆꯥꯏ꯫",
        "roman": "Ei uhei-mana-masing khakta chai.",
        "bengali": "ঐ উহৈ-মনা-মশিং খক্তা চাই।",
        "english": "I am a vegetarian (I only eat fruits and vegetables).",
        "category": "food_dining",
        "context": "Explaining vegetarian preference."
    },
    {
        "sentence_id": "food_009",
        "meitei": "ꯑꯩꯒꯤ ꯄꯨꯛ ꯊꯜꯂꯦ꯫",
        "roman": "Eigi puk thalle.",
        "bengali": "ঐগী পুক থল্লে।",
        "english": "I am full / My stomach is full.",
        "category": "food_dining",
        "context": "Indicating satisfaction after finishing a meal."
    },
    {
        "sentence_id": "food_010",
        "meitei": "ꯁꯤꯡꯖꯨ ꯆꯥꯁꯤ꯫",
        "roman": "Singju chasi.",
        "bengali": "শিঞ্জু চাসী।",
        "english": "Let us eat Singju (traditional spicy herb and vegetable salad).",
        "category": "food_dining",
        "context": "Suggesting an afternoon traditional snack."
    },

    # -------------------------------------------------------------
    # 6. Travel, Roads & Directions (ꯂꯝꯕꯤ-ꯆꯠꯊꯣꯛ / Travel)
    # -------------------------------------------------------------
    {
        "sentence_id": "travel_001",
        "meitei": "ꯂꯝꯕꯤ ꯑꯁꯤ ꯀꯗꯥꯏꯗ ꯆꯠꯄꯒꯦ?",
        "roman": "Lambi asi kadaida chatpage?",
        "bengali": "লম্বী অসী কদাইদ চৎপগে?",
        "english": "Where does this road lead to?",
        "category": "travel_directions",
        "context": "Asking road destination."
    },
    {
        "sentence_id": "travel_002",
        "meitei": "ꯀꯪꯂꯥ ꯀꯗꯥꯏꯗ ꯂꯩꯕꯒꯦ?",
        "roman": "Kangla kadaida leibage?",
        "bengali": "কংলা কদাইদ লৈবগে?",
        "english": "Where is the historic Kangla Fort located?",
        "category": "travel_directions",
        "context": "Asking directions to Kangla."
    },
    {
        "sentence_id": "travel_003",
        "meitei": "ꯆꯨꯝꯊꯪ ꯂꯦꯝꯅ ꯆꯠꯂꯨ꯫",
        "roman": "Chumthang lemna chatlu.",
        "bengali": "চুম্থাং লেম্না চৎলু।",
        "english": "Go straight ahead.",
        "category": "travel_directions",
        "context": "Giving navigational direction."
    },
    {
        "sentence_id": "travel_004",
        "meitei": "ꯌꯦꯠꯊꯪꯕ ꯃꯥꯏꯀꯩꯗ ꯂꯩꯌꯨ꯫",
        "roman": "Yet-thangba maikeida leiyu.",
        "bengali": "য়েৎথাংবা মাইকৈদ লৈয়ু।",
        "english": "Turn to the right side.",
        "category": "travel_directions",
        "context": "Direction: turn right."
    },
    {
        "sentence_id": "travel_005",
        "meitei": "ꯑꯣꯏꯊꯪꯕ ꯃꯥꯏꯀꯩꯗ ꯂꯩꯌꯨ꯫",
        "roman": "Oi-thangba maikeida leiyu.",
        "bengali": "ওইথাংবা মাইকৈদ লৈয়ু।",
        "english": "Turn to the left side.",
        "category": "travel_directions",
        "context": "Direction: turn left."
    },
    {
        "sentence_id": "travel_006",
        "meitei": "ꯂꯣꯛꯇꯥꯛ ꯄꯥꯠ ꯆꯠꯅꯕ ꯒꯥꯔꯤ ꯂꯩꯕ꯭ꯔꯥ?",
        "roman": "Loktak Pat chatnaba gari leibra?",
        "bengali": "লোকতাক পাৎ চৎনবা গারী লৈব্রা?",
        "english": "Is there a vehicle or transport going to Loktak Lake?",
        "category": "travel_directions",
        "context": "Inquiring about transport to scenic destinations."
    },
    {
        "sentence_id": "travel_007",
        "meitei": "ꯃꯐꯝ ꯑꯁꯤ ꯌꯥꯝꯅ ꯂꯥꯞꯄ꯭ꯔꯥ?",
        "roman": "Mapham asi yamna lap-pra?",
        "bengali": "মফম অসী য়াম্না লাপ্প্রা?",
        "english": "Is this place very far away?",
        "category": "travel_directions",
        "context": "Asking about distance."
    },
    {
        "sentence_id": "travel_008",
        "meitei": "ꯂꯥꯞꯇꯦ, ꯌꯥꯝꯅ ꯅꯛꯏ꯫",
        "roman": "Lapte, yamna nak-i.",
        "bengali": "লাপ্তে, য়াম্না নকঈ।",
        "english": "It is not far, it is very close by.",
        "category": "travel_directions",
        "context": "Reassuring distance information."
    },
    {
        "sentence_id": "travel_009",
        "meitei": "ꯑꯩ ꯌꯨꯝꯗ ꯍꯜꯂꯒꯦ꯫",
        "roman": "Ei yumda hallage.",
        "bengali": "ঐ য়ুম্দ হল্লগে।",
        "english": "I will return home now.",
        "category": "travel_directions",
        "context": "Departing to go home."
    },
    {
        "sentence_id": "travel_010",
        "meitei": "ꯆꯠꯄꯗ ꯅꯨꯡꯉꯥꯏꯅ ꯆꯠꯂꯨ꯫",
        "roman": "Chatpada nungngaina chatlu.",
        "bengali": "চৎপদ নুংঙাইনা চৎলু।",
        "english": "Have a safe and pleasant journey! / Bon voyage!",
        "category": "travel_directions",
        "context": "Wishing someone well on their travels."
    },

    # -------------------------------------------------------------
    # 7. Time, Days & Weather (ꯃꯇꯝ ꯑꯃꯁꯨꯡ ꯅꯣꯡ-ꯅꯨꯃꯤꯠ / Weather & Time)
    # -------------------------------------------------------------
    {
        "sentence_id": "time_001",
        "meitei": "ꯄꯨꯡ ꯀꯌꯥ ꯇꯥꯔꯦ?",
        "roman": "Pung kaya tare?",
        "bengali": "পুং কয়া তারে?",
        "english": "What time is it now?",
        "category": "time_weather",
        "context": "Asking the current hour."
    },
    {
        "sentence_id": "time_002",
        "meitei": "ꯉꯁꯤ ꯀꯔꯤ ꯅꯨꯃꯤꯠꯅꯣ?",
        "roman": "Ngasi kari numitno?",
        "bengali": "ঙশী করি নুমিৎনৌ?",
        "english": "What day of the week is today?",
        "category": "time_weather",
        "context": "Asking today's day."
    },
    {
        "sentence_id": "time_003",
        "meitei": "ꯉꯁꯤ ꯂꯥꯡꯕꯟ ꯅꯣꯡꯃꯥꯏꯖꯤꯡ ꯅꯨꯃꯤꯠꯅꯤ꯫",
        "roman": "Ngasi Langban Nongmaijing numitni.",
        "bengali": "ঙশী লাংবন্ নোংমাইজিং নুমিৎনী।",
        "english": "Today is Sunday.",
        "category": "time_weather",
        "context": "Stating the day."
    },
    {
        "sentence_id": "time_004",
        "meitei": "ꯉꯁꯤ ꯅꯣꯡ ꯆꯨꯔꯤ꯫",
        "roman": "Ngasi nong churi.",
        "bengali": "ঙশী নোং চুরী।",
        "english": "It is raining today.",
        "category": "time_weather",
        "context": "Weather observation during rain."
    },
    {
        "sentence_id": "time_005",
        "meitei": "ꯉꯁꯤ ꯅꯨꯃꯤꯠ ꯌꯥꯝꯅ ꯁꯥꯏ꯫",
        "roman": "Ngasi numit yamna sai.",
        "bengali": "ঙশী নুমিৎ য়াম্না শাঈ।",
        "english": "It is very sunny and hot today.",
        "category": "time_weather",
        "context": "Weather observation on sunny days."
    },
    {
        "sentence_id": "time_006",
        "meitei": "ꯅꯣꯡꯖꯨ ꯊꯥ ꯂꯥꯛꯂꯦ꯫",
        "roman": "Nongju tha lakle.",
        "bengali": "নোংজু থা লাকলে।",
        "english": "The rainy monsoon season has arrived.",
        "category": "time_weather",
        "context": "Seasonal transition remark."
    },
    {
        "sentence_id": "time_007",
        "meitei": "ꯅꯤꯡꯊꯝ ꯊꯥ ꯂꯥꯛꯄꯗ ꯑꯩ ꯌꯥꯝꯅ ꯅꯨꯡꯉꯥꯏ꯫",
        "roman": "Ningtham tha lakpada ei yamna nungngai.",
        "bengali": "নিংথম থা লাক্পদ ঐ য়াম্না নুংঙাই।",
        "english": "I feel very happy when the crisp winter season arrives.",
        "category": "time_weather",
        "context": "Expressing preference for winter season."
    },
    {
        "sentence_id": "time_008",
        "meitei": "ꯍꯌꯦꯡ ꯑꯌꯨꯛ ꯑꯩ ꯂꯥꯛꯀꯅꯤ꯫",
        "roman": "Hayeng ayuk ei lakkani.",
        "bengali": "হয়েং অয়ুক ঐ লাক্কনী।",
        "english": "I will come tomorrow morning.",
        "category": "time_weather",
        "context": "Scheduling a visit."
    },
    {
        "sentence_id": "time_009",
        "meitei": "ꯉꯔꯥꯡ ꯑꯩ ꯌꯥꯝꯅ ꯊꯕꯛ ꯌꯥꯝꯈꯤ꯫",
        "roman": "Ngarang ei yamna thabak yamkhi.",
        "bengali": "ঙরাং ঐ য়াম্না থবক য়াম্খী।",
        "english": "Yesterday I had a lot of work.",
        "category": "time_weather",
        "context": "Speaking about past activities."
    },
    {
        "sentence_id": "time_010",
        "meitei": "ꯅꯣꯡꯃꯩ ꯄꯥꯏꯕꯗ ꯅꯨꯃꯤꯠ ꯆꯨꯝꯅ ꯂꯦꯞꯂꯤ꯫",
        "roman": "Nongmei paibada numit chumna lepli.",
        "bengali": "নোংমৈ পাইবদ নুমিৎ চুম্না লেপ্লী।",
        "english": "Time marches on steadfastly.",
        "category": "time_weather",
        "context": "Reflective saying on time."
    },

    # -------------------------------------------------------------
    # 8. Family, Kinship & Home (ꯏꯃꯨꯡ-ꯃꯅꯨꯡ / Family & Home)
    # -------------------------------------------------------------
    {
        "sentence_id": "fam_001",
        "meitei": "ꯃꯁꯤ ꯑꯩꯒꯤ ꯏꯃꯥꯅꯤ꯫",
        "roman": "Masi eigi Imani.",
        "bengali": "মসী ঐগী ইমানী।",
        "english": "This is my mother.",
        "category": "family_home",
        "context": "Introducing mother."
    },
    {
        "sentence_id": "fam_002",
        "meitei": "ꯃꯁꯤ ꯑꯩꯒꯤ ꯏꯄꯥꯅꯤ꯫",
        "roman": "Masi eigi Ipani.",
        "bengali": "মসী ঐগী ইপানী।",
        "english": "This is my father.",
        "category": "family_home",
        "context": "Introducing father."
    },
    {
        "sentence_id": "fam_003",
        "meitei": "ꯑꯩꯒꯤ ꯃꯆꯤꯟ-ꯃꯅꯥꯎ ꯑꯍꯨꯝ ꯂꯩ꯫",
        "roman": "Eigi machin-manao ahum lei.",
        "bengali": "ঐগী মচিন-মনাও অহুম লৈ।",
        "english": "I have three brothers and sisters.",
        "category": "family_home",
        "context": "Describing family siblings."
    },
    {
        "sentence_id": "fam_004",
        "meitei": "ꯑꯩꯒꯤ ꯏꯆꯦ ꯗꯣꯛꯇꯔ ꯑꯃꯅꯤ꯫",
        "roman": "Eigi Iche doctor amani.",
        "bengali": "ঐগী ইচে ডোক্তর অমনী।",
        "english": "My elder sister is a doctor.",
        "category": "family_home",
        "context": "Stating sibling profession."
    },
    {
        "sentence_id": "fam_005",
        "meitei": "ꯑꯩꯈꯣꯏꯒꯤ ꯌꯨꯝ ꯌꯥꯝꯅ ꯅꯨꯡꯉꯥꯏ꯫",
        "roman": "Eikhoigi yum yamna nungngai.",
        "bengali": "ঐখোইগী য়ুম য়াম্না নুংঙাই।",
        "english": "Our home is very peaceful and joyful.",
        "category": "family_home",
        "context": "Praising home environment."
    },
    {
        "sentence_id": "fam_006",
        "meitei": "ꯏꯃꯥ, ꯆꯥꯅꯕ ꯀꯔꯤ ꯊꯣꯡꯉꯤ?",
        "roman": "Ima, chanaba kari thong-ngi?",
        "bengali": "ইমা, চনবা করি থোংঙী?",
        "english": "Mother, what are you cooking for food?",
        "category": "family_home",
        "context": "Inquiring about home cooking."
    },
    {
        "sentence_id": "fam_007",
        "meitei": "ꯌꯨꯝ ꯑꯁꯤ ꯂꯨ-ꯅꯥꯅ ꯊꯝꯃꯨ꯫",
        "roman": "Yum asi lu-nana thammu.",
        "bengali": "য়ুম অসী লু-নানা থম্মু।",
        "english": "Keep this home tidy and clean.",
        "category": "family_home",
        "context": "Household cleanliness reminder."
    },
    {
        "sentence_id": "fam_008",
        "meitei": "ꯏꯕꯨꯡꯉꯣ, ꯂꯥꯏꯔꯤꯛ ꯍꯧꯖꯤꯛ ꯄꯥꯔꯣ꯫",
        "roman": "Ibungngo, layrik houjik paro.",
        "bengali": "ইবুংঙো, লাইরিক্ হৌজিক পারৌ।",
        "english": "Dear boy / son, study your books now.",
        "category": "family_home",
        "context": "Parental affectionate encouragement to study."
    },
    {
        "sentence_id": "fam_009",
        "meitei": "ꯏꯕꯦꯝꯃ, ꯆꯥ ꯊꯣꯡꯕ ꯇꯝꯃꯣ꯫",
        "roman": "Ibemma, cha thongba tammo.",
        "bengali": "ইবেম্ম, চা থোংবা তম্মৌ।",
        "english": "Dear daughter / girl, learn to brew tea.",
        "category": "family_home",
        "context": "Parental domestic instruction."
    },
    {
        "sentence_id": "fam_010",
        "meitei": "ꯑꯩꯈꯣꯏ ꯄꯨꯟꯅ ꯆꯥꯛ ꯆꯥꯁꯤ꯫",
        "roman": "Eikhoi punna chak chasi.",
        "bengali": "ঐখোই পুন্ন চাক চাসী।",
        "english": "Let us all eat our meal together.",
        "category": "family_home",
        "context": "Family dining gathering."
    },

    # -------------------------------------------------------------
    # 9. Health, Care & Wellbeing (ꯍꯛꯁꯦꯜ / Health)
    # -------------------------------------------------------------
    {
        "sentence_id": "health_001",
        "meitei": "ꯑꯩ ꯍꯛꯆꯥꯡ ꯅꯥꯏ꯫",
        "roman": "Ei hakchang nai.",
        "bengali": "ঐ হক্চাং নাঈ।",
        "english": "I am feeling unwell / my body hurts.",
        "category": "health_emergency",
        "context": "Reporting physical indisposition."
    },
    {
        "sentence_id": "health_002",
        "meitei": "ꯑꯩ ꯀꯣꯛ ꯅꯥꯏ꯫",
        "roman": "Ei kok nai.",
        "bengali": "ঐ কোক নাঈ।",
        "english": "I have a headache.",
        "category": "health_emergency",
        "context": "Describing headache."
    },
    {
        "sentence_id": "health_003",
        "meitei": "ꯑꯩ ꯄꯨꯛ ꯅꯥꯏ꯫",
        "roman": "Ei puk nai.",
        "bengali": "ঐ পুক নাঈ।",
        "english": "I have a stomach ache.",
        "category": "health_emergency",
        "context": "Describing stomach ache."
    },
    {
        "sentence_id": "health_004",
        "meitei": "ꯗꯣꯛꯇꯔ ꯀꯧꯕꯤꯌꯨ꯫",
        "roman": "Doctor koubiyu.",
        "bengali": "ডোক্তর কৌবীয়ু।",
        "english": "Please call a doctor.",
        "category": "health_emergency",
        "context": "Emergency medical request."
    },
    {
        "sentence_id": "health_005",
        "meitei": "ꯍꯤꯗꯥꯛ ꯑꯁꯤ ꯊꯛꯎ꯫",
        "roman": "Hidak asi thak-u.",
        "bengali": "হিদাক অসী থকউ।",
        "english": "Take / drink this medicine.",
        "category": "health_emergency",
        "context": "Administering medicine."
    },
    {
        "sentence_id": "health_006",
        "meitei": "ꯍꯤꯗꯥꯛ ꯐꯝꯕ ꯗꯨꯀꯥꯟ ꯀꯗꯥꯏꯗ ꯂꯩꯕꯒꯦ?",
        "roman": "Hidak phamba dukan kadaida leibage?",
        "bengali": "হিদাক ফম্বা দুকান কদাইদ লৈবগে?",
        "english": "Where is the pharmacy / medicine shop located?",
        "category": "health_emergency",
        "context": "Asking directions to a medical shop."
    },
    {
        "sentence_id": "health_007",
        "meitei": "ꯑꯩ ꯍꯧꯖꯤꯛ ꯐꯔꯦ꯫",
        "roman": "Ei houjik phare.",
        "bengali": "ঐ হৌজিক ফরে।",
        "english": "I feel better now / I have recovered.",
        "category": "health_emergency",
        "context": "Reporting health recovery."
    },
    {
        "sentence_id": "health_008",
        "meitei": "ꯄꯣꯊꯥꯕꯤꯌꯨ ꯑꯃꯁꯨꯡ ꯅꯨꯡꯉꯥꯏꯅ ꯂꯩꯌꯨ꯫",
        "roman": "Pothabiyu amasung nungngaina leiyu.",
        "bengali": "পোথাবীয়ু অমশুং নুংঙাইনা লৈয়ু।",
        "english": "Take good rest and take care of yourself.",
        "category": "health_emergency",
        "context": "Wishing good health and recuperation."
    },
    {
        "sentence_id": "health_009",
        "meitei": "ꯑꯩ ꯂꯥꯏꯅꯥ ꯊꯨꯅ ꯐꯍꯟꯒꯦ꯫",
        "roman": "Ei layna thuna phahange.",
        "bengali": "ঐ লাইনা থুনা ফহনগে।",
        "english": "I hope to overcome this illness soon.",
        "category": "health_emergency",
        "context": "Expressing wish for fast recovery."
    },
    {
        "sentence_id": "health_010",
        "meitei": "ꯃꯇꯦꯡ ꯇꯧꯕꯤꯌꯨ!",
        "roman": "Mateng toubiyu!",
        "bengali": "মতেং তৌবীয়ু!",
        "english": "Help please! / Assistance needed!",
        "category": "health_emergency",
        "context": "Emergency cry for help."
    },

    # -------------------------------------------------------------
    # 10. Education, Reading & Script Learning (ꯂꯥꯏꯔꯤꯛ ꯇꯝꯕ / Study)
    # -------------------------------------------------------------
    {
        "sentence_id": "edu_001",
        "meitei": "ꯑꯩ ꯃꯩꯇꯩ ꯃꯌꯦꯛ ꯏꯕ ꯇꯝꯂꯤ꯫",
        "roman": "Ei Meitei Mayek iba tamli.",
        "bengali": "ঐ মৈতৈ ময়েক ইবা তম্লি।",
        "english": "I am learning to write the Meitei Mayek script.",
        "category": "work_study",
        "context": "Script learning practice statement."
    },
    {
        "sentence_id": "edu_002",
        "meitei": "ꯃꯌꯦꯛ ꯑꯁꯤ ꯌꯥꯝꯅ ꯐꯖꯩ꯫",
        "roman": "Mayek asi yamna phajei.",
        "bengali": "ময়েক অসী য়াম্না ফজৈ।",
        "english": "This script is very beautiful.",
        "category": "work_study",
        "context": "Appreciating Meitei Mayek calligraphy."
    },
    {
        "sentence_id": "edu_003",
        "meitei": "ꯏꯌꯦꯛ ꯏꯄꯤ ꯱꯸ ꯂꯩ꯫",
        "roman": "Iyek Ipi tara-nipal lei.",
        "bengali": "ঈয়েক ঈপী তরানি romp লৈ।",
        "english": "There are eighteen primary alphabet letters (Iyek Ipi).",
        "category": "work_study",
        "context": "Linguistic fact about the core 18 letters."
    },
    {
        "sentence_id": "edu_004",
        "meitei": "ꯈꯝꯕ ꯊꯣꯏꯕꯤ ꯋꯥꯔꯤ ꯑꯁꯤ ꯄꯥꯔꯣ꯫",
        "roman": "Khamba Thoibi wari asi paro.",
        "bengali": "খম্বা থোইবী ৱারী অসী পারৌ।",
        "english": "Read this legendary story of Khamba and Thoibi.",
        "category": "work_study",
        "context": "Recommending classical reading."
    },
    {
        "sentence_id": "edu_005",
        "meitei": "ꯂꯥꯏꯔꯤꯛ ꯑꯁꯤ ꯑꯩꯅ ꯌꯥꯝꯅ ꯄꯥꯅꯤꯡꯏ꯫",
        "roman": "Layrik asi eina yamna paning-i.",
        "bengali": "লাইরিক অসী ঐনা য়াম্না পানীংঈ।",
        "english": "I really want to read this book.",
        "category": "work_study",
        "context": "Expressing desire to study a book."
    },
    {
        "sentence_id": "edu_006",
        "meitei": "ꯑꯣꯖꯥꯅ ꯋꯥꯍꯩ ꯑꯁꯤꯒꯤ ꯋꯥꯍꯟꯊꯣꯛ ꯇꯥꯛꯄꯤꯔꯦ꯫",
        "roman": "Ojana wahei asigi wahanthok takpire.",
        "bengali": "ওঝানা ৱাহৈ অসীগী ৱাহন্থোক তাক্পীরে।",
        "english": "The respected teacher explained the meaning of this word.",
        "category": "work_study",
        "context": "Classroom instruction acknowledgment."
    },
    {
        "sentence_id": "edu_007",
        "meitei": "ꯋꯥꯍꯩ ꯑꯁꯤꯒꯤ ꯋꯥꯍꯟꯊꯣꯛ ꯀꯔꯤꯅꯣ?",
        "roman": "Wahei asigi wahanthok karino?",
        "bengali": "ৱাহৈ অসীগী ৱাহন্থোক করীনৌ?",
        "english": "What is the meaning of this word?",
        "category": "work_study",
        "context": "Vocabulary query."
    },
    {
        "sentence_id": "edu_008",
        "meitei": "ꯀꯨꯄꯨꯝꯅ ꯄꯥꯕꯅ ꯂꯧꯁꯤꯡ ꯍꯦꯟꯒꯠꯍꯜꯂꯤ꯫",
        "roman": "Kupumna pabana lousing hengathalli.",
        "bengali": "কুপুম্না পাবনা লৌশিং হেঙ্গৎহল্লী।",
        "english": "Diligent reading enhances wisdom.",
        "category": "work_study",
        "context": "Proverbial educational advice."
    },
    {
        "sentence_id": "edu_009",
        "meitei": "ꯑꯩ ꯄꯔꯤꯛꯁꯥꯗ ꯃꯥꯏꯄꯥꯛꯂꯦ꯫",
        "roman": "Ei pariksada maipakle.",
        "bengali": "ঐ পরীহৃদ মাইপাক্লে।",
        "english": "I succeeded / passed in the examination.",
        "category": "work_study",
        "context": "Celebrating academic achievement."
    },
    {
        "sentence_id": "edu_010",
        "meitei": "ꯍꯧꯖꯤꯛ ꯀꯝꯄ꯭ꯌꯨꯇꯔ ꯇꯝꯁꯤ꯫",
        "roman": "Houjik computer tamsi.",
        "bengali": "হৌজিক কম্প্যুতর তমসী।",
        "english": "Let us learn computer and modern technology now.",
        "category": "work_study",
        "context": "Encouraging digital literacy."
    },

    # -------------------------------------------------------------
    # 11. Culture, Festivals & Heritage (ꯆꯠꯅꯕꯤ ꯑꯃꯁꯨꯡ ꯍꯔꯥꯎ-ꯀꯨꯝꯃꯩ / Culture)
    # -------------------------------------------------------------
    {
        "sentence_id": "cult_001",
        "meitei": "ꯂꯥꯏ ꯍꯔꯥꯎꯕ ꯀꯨꯝꯃꯩ ꯌꯦꯡꯁꯤ꯫",
        "roman": "Lai Haraoba kummei yengsi.",
        "bengali": "লাই হরাওবা কুম্মৈ য়েংসী।",
        "english": "Let us go watch the sacred Lai Haraoba festival.",
        "category": "culture_festivals",
        "context": "Inviting someone to attend the sacred creation ritual festival."
    },
    {
        "sentence_id": "cult_002",
        "meitei": "ꯌꯥꯑꯣꯁꯪ ꯊꯥꯕꯜ ꯆꯣꯡꯁꯤ꯫",
        "roman": "Yaoshang thabal chongsi.",
        "bengali": "য়াওশং থাবল চোংসী।",
        "english": "Let us join the moonlight Thabal Chongba circle dance at Yaoshang.",
        "category": "culture_festivals",
        "context": "Spring festive gathering invitation."
    },
    {
        "sentence_id": "cult_003",
        "meitei": "ꯅꯤꯉꯣꯜ ꯆꯥꯛꯀꯧꯕꯒꯤ ꯊꯧꯔꯝ ꯄꯥꯡꯊꯣꯛꯂꯦ꯫",
        "roman": "Ningol Chakoubagi thouram pangthokle.",
        "bengali": "নিংঙোল চাক্কৌবগী থৌরম্ব পাংথোクレ।",
        "english": "The joyous festival of Ningol Chakouba is being celebrated.",
        "category": "culture_festivals",
        "context": "Celebrating the festival honouring married sisters and daughters."
    },
    {
        "sentence_id": "cult_004",
        "meitei": "ꯆꯦꯏꯔꯥꯑꯣꯕ ꯀꯨꯝꯃꯩꯗ ꯆꯤꯡ ꯀꯥꯁꯤ꯫",
        "roman": "Cheiraoba kummeida ching kasi.",
        "bengali": "চৈরাওবা কুম্মৈদ চিং কাসী।",
        "english": "Let us climb the hills on Cheiraoba New Year's Day.",
        "category": "culture_festivals",
        "context": "Tradition of ascending sacred hilltops on Manipuri New Year."
    },
    {
        "sentence_id": "cult_005",
        "meitei": "ꯄꯦꯅꯥ ꯈꯣꯡꯕ ꯇꯥꯕ ꯌꯥꯝꯅ ꯅꯨꯡꯉꯥꯏ꯫",
        "roman": "Pena khongba taba yamna nungngai.",
        "bengali": "পেনা খোংবা তাবা য়াম্না নুংঙাই।",
        "english": "Listening to the resonant melody of the traditional Pena string instrument is deeply captivating.",
        "category": "culture_festivals",
        "context": "Appreciating ancient Meitei music."
    },
    {
        "sentence_id": "cult_006",
        "meitei": "ꯄꯨꯡ ꯆꯣꯂꯣꯝ ꯖꯥꯒꯣꯏ ꯌꯦꯡꯕꯤꯌꯨ꯫",
        "roman": "Pung Cholom jagoi yengbiyu.",
        "bengali": "পুং চোলম জাগোই য়েংবীয়ু।",
        "english": "Please watch the magnificent Pung Cholom drum acrobatic dance.",
        "category": "culture_festivals",
        "context": "Showcasing world-famous Manipuri dance forms."
    },
    {
        "sentence_id": "cult_007",
        "meitei": "ꯊꯥꯡ-ꯇꯥ ꯑꯁꯤ ꯑꯩꯈꯣꯏꯒꯤ ꯃꯔꯨꯑꯣꯏꯕ ꯁꯥꯟꯅ-ꯈꯣꯠꯅꯕꯅꯤ꯫",
        "roman": "Thang-Ta asi eikhoigi maruoiba sanna-khotnabani.",
        "bengali": "থাং-তা অসী ঐখোইগী মরূপোইবা শান্না-খোৎনবাণী।",
        "english": "Thang-Ta (sword and spear martial art) is our invaluable cultural heritage.",
        "category": "culture_festivals",
        "context": "Explaining the indigenous martial art of Manipur."
    },
    {
        "sentence_id": "cult_008",
        "meitei": "ꯍꯩꯀ꯭ꯔꯨ ꯍꯤꯗꯣꯡꯕ ꯍꯤ ꯂꯥꯝꯕ ꯌꯦꯡꯁꯤ꯫",
        "roman": "Heikru Hidongba hi lamba yengsi.",
        "bengali": "হৈক্রু হীদোংবা হী লাম্বা য়েংসী।",
        "english": "Let us watch the traditional royal boat race at Heikru Hidongba.",
        "category": "culture_festivals",
        "context": "Inviting friends to the autumn boat racing festival at the palace moat."
    },
    {
        "sentence_id": "cult_009",
        "meitei": "ꯁꯒꯣꯜ ꯀꯥꯡꯖꯩ ꯑꯁꯤ ꯃꯅꯤꯄꯨꯔꯗꯒꯤ ꯍꯧꯔꯛꯈꯤꯕꯅꯤ꯫",
        "roman": "Sagol Kangjei asi Manipur-dagi hourakkhibani.",
        "bengali": "শগোল কাংজৈ অসী মণিপুরদগী হৌরক্খীবণী।",
        "english": "Modern polo originated from Manipur's ancient game of Sagol Kangjei.",
        "category": "culture_festivals",
        "context": "Sharing cultural history with visitors."
    },
    {
        "sentence_id": "cult_010",
        "meitei": "ꯁꯅꯥ ꯂꯩꯕꯥꯛ ꯃꯅꯤꯄꯨꯔꯕꯨ ꯌꯥꯏꯐꯔꯦ!꯫",
        "roman": "Sana Leibak Manipur-bu yaiphare!",
        "bengali": "সনা লৈবাক মণিপুরবু য়াইফরে!",
        "english": "Long live and may prosperity bless the Golden Land of Manipur!",
        "category": "culture_festivals",
        "context": "Patriotic acclaim and prayer for the homeland."
    },

    # -------------------------------------------------------------
    # 12. Everyday Thoughts, Moods & Questions (ꯋꯥꯈꯜ ꯑꯃꯁꯨꯡ ꯋꯥꯍꯪ / General Daily)
    # -------------------------------------------------------------
    {
        "sentence_id": "daily_001",
        "meitei": "ꯀꯔꯤ ꯋꯥꯔꯤ ꯂꯩꯔꯤ?",
        "roman": "Kari wari leiri?",
        "bengali": "করি ৱারী লৈরি?",
        "english": "What is the news? / What's going on?",
        "category": "feelings_emotions",
        "context": "Casual conversation opener between friends."
    },
    {
        "sentence_id": "daily_002",
        "meitei": "ꯑꯩ ꯌꯥꯝꯅ ꯊꯋꯥꯏ ꯍꯔꯥꯎꯋꯦ꯫",
        "roman": "Ei yamna thawai haraowe.",
        "bengali": "ঐ য়াম্না থৱাই হরাওৱে।",
        "english": "I am feeling extremely cheerful and overjoyed.",
        "category": "feelings_emotions",
        "context": "Expressing intense happiness."
    },
    {
        "sentence_id": "daily_003",
        "meitei": "ꯑꯩ ꯍꯧꯖꯤꯛ ꯊꯕꯛ ꯂꯣꯏꯔꯦ꯫",
        "roman": "Ei houjik thabak loire.",
        "bengali": "ঐ হৌজিক থবক লোইরে।",
        "english": "I have finished my work now.",
        "category": "feelings_emotions",
        "context": "Completing daily tasks."
    },
    {
        "sentence_id": "daily_004",
        "meitei": "ꯀꯔꯤꯒꯤ ꯂꯥꯎꯔꯤꯕꯅꯣ?",
        "roman": "Karigi lauribano?",
        "bengali": "করীগী লাউরীবনৌ?",
        "english": "Why are you shouting?",
        "category": "feelings_emotions",
        "context": "Calming a noisy situation."
    },
    {
        "sentence_id": "daily_005",
        "meitei": "ꯇꯞꯅ ꯇꯞꯅ ꯂꯥꯛꯎ꯫",
        "roman": "Tapna tapna lak-u.",
        "bengali": "তপ্না তপ্না লাকউ।",
        "english": "Come slowly and gently.",
        "category": "feelings_emotions",
        "context": "Advising careful arrival."
    },
    {
        "sentence_id": "daily_006",
        "meitei": "ꯑꯩꯈꯣꯏ ꯄꯨꯟꯅ ꯍꯣꯠꯅꯔꯁꯤ꯫",
        "roman": "Eikhoi punna hotnarasi.",
        "bengali": "ঐখোই পুন্ন হোৎনরসী।",
        "english": "Let us make an effort together / Let us unite our efforts.",
        "category": "feelings_emotions",
        "context": "Encouraging collective collaboration."
    },
    {
        "sentence_id": "daily_007",
        "meitei": "ꯅꯨꯃꯤꯠ ꯈꯨꯗꯤꯡꯃꯛ ꯑꯅꯧꯕ ꯊꯋꯥꯏ ꯌꯥꯎꯅ ꯍꯤꯡꯁꯤ꯫",
        "roman": "Numit khudingmak anouba thawai yaona hingsi.",
        "bengali": "নুমিৎ খুদিংমক অনৌবা থৱাই য়াওনা হিংসী।",
        "english": "Let us live every single day with renewed enthusiasm.",
        "category": "feelings_emotions",
        "context": "Uplifting life philosophy."
    },
    {
        "sentence_id": "daily_008",
        "meitei": "ꯑꯆꯨꯝꯕ ꯉꯥꯡꯕꯅ ꯃꯤꯒꯤ ꯃꯒꯨꯟ ꯑꯣꯏ꯫",
        "roman": "Achumba ngangbana migi magun oi.",
        "bengali": "অচুম্বা ঙাংবনা মীগী মগুন ওই।",
        "english": "Speaking the truth is the true virtue of a person.",
        "category": "feelings_emotions",
        "context": "Moral wisdom."
    },
    {
        "sentence_id": "daily_009",
        "meitei": "ꯃꯅꯤꯄꯨꯔꯒꯤ ꯂꯝꯗꯝ ꯑꯁꯤ ꯅꯤꯡꯊꯤꯖꯅ ꯐꯖꯩ꯫",
        "roman": "Manipur-gi lamdam asi ningthijana phajei.",
        "bengali": "মণিপুরগী লম্দম অসী নিংথীজনা ফজৈ।",
        "english": "The scenic land of Manipur is exquisitely picturesque and beautiful.",
        "category": "feelings_emotions",
        "context": "Admiring the landscape."
    },
    {
        "sentence_id": "daily_010",
        "meitei": "ꯄꯨꯟꯅ ꯂꯩꯃꯤꯟꯅꯕꯅ ꯑꯩꯈꯣꯏꯒꯤ ꯄꯥꯉ꯭ꯒꯜꯅꯤ꯫",
        "roman": "Punna leiminnabana eikhoigi panggalni.",
        "bengali": "পুন্ন লৈমিন্নবনা ঐখোইগী পাংগল্নী।",
        "english": "Living together in unity is our greatest strength.",
        "category": "feelings_emotions",
        "context": "Communal solidarity motto."
    }
]


def get_sentences() -> List[Dict[str, Any]]:
    """Return all curated daily usable sentences."""
    return SENTENCES


if __name__ == "__main__":
    print(f"Loaded {len(SENTENCES)} authentic daily usable sentences across 12 categories.")
    for s in SENTENCES[:5]:
        print(f"[{s['category']}] {s['meitei']} ({s['roman']}) -> {s['english']}")


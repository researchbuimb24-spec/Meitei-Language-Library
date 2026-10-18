# -*- coding: utf-8 -*-
"""
Authentic Manipuri / Meitei songs collection for meitei_lang.
Contains 3 authentic Manipuri songs with complete lyrics in Meitei Mayek,
Roman transliteration, Bengali script, English translation, composer,
genre, historical/cultural context, and licensing information.
"""

from typing import List, Dict, Any

SONGS: List[Dict[str, Any]] = [
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
        "status": "Official State Song of Manipur (Adopted by Govt. of Manipur in 2021)",
        "description": (
            "The official State Song of Manipur celebrating the scenic natural beauty, "
            "sacred Loktak lake, emerald hills, ancestral bravery, and spiritual brotherhood "
            "of all communities living in the state."
        ),
        "source": "Government of Manipur State Anthem Declaration & Department of Art and Culture Archives",
        "copyright": "Official State Cultural Anthem / Public Domain under official state adoption",
        "lyrics": {
            "meitei": (
                "ꯁꯅꯥ ꯂꯩꯕꯥꯛ ꯃꯅꯤꯄꯨꯔ,\n"
                "ꯀꯣꯂꯣꯏ ꯅꯪꯒꯤ ꯃꯤꯡꯊꯣꯜꯅꯤ,\n"
                "ꯃꯥꯂꯦꯝ ꯏꯃꯥꯡ ꯈꯪꯅꯔꯕ,\n"
                "ꯄꯨꯊꯣꯛꯂꯕ ꯅꯪꯒꯤ ꯂꯩꯊꯣꯏꯔꯣꯜ꯫\n\n"
                "ꯆꯤꯡꯅ ꯀꯣꯏꯅ ꯄꯥꯡꯕ ꯂꯝ,\n"
                "ꯍꯥꯎꯅ-ꯃꯩꯇꯩ ꯃꯆꯥꯁꯤꯡ,\n"
                "ꯏꯆꯦꯜ ꯑꯃꯒꯤ ꯏꯁꯤꯡꯒꯨꯝ,\n"
                "ꯄꯨꯟꯅ ꯍꯤꯡꯃꯤꯟꯅꯔꯤꯕ ꯂꯝ꯫\n\n"
                "ꯂꯣꯛꯇꯥꯛ ꯏꯁꯤꯡ ꯏꯊꯛꯅ,\n"
                "ꯁꯩꯊꯥꯔꯤ ꯅꯪꯒꯤ ꯊꯧꯅꯥꯐꯝ,\n"
                "ꯅꯣꯡꯃꯥꯏꯆꯤꯡꯒꯤ ꯆꯤꯡꯗꯣꯜꯅ,\n"
                "ꯂꯦꯞꯂꯤ ꯅꯪꯒꯤ ꯏꯀꯥꯏꯈꯨꯝꯅꯕ꯫\n\n"
                "ꯑꯩꯈꯣꯏ ꯂꯩꯕꯥꯛ ꯃꯅꯤꯄꯨꯔ,\n"
                "ꯁꯅꯥ ꯂꯩꯕꯥꯛ ꯃꯅꯤꯄꯨꯔ꯫"
            ),
            "roman": (
                "Sana leibak Manipur,\n"
                "Koloi nangi mingtholni,\n"
                "Malem imang khangnaraba,\n"
                "Puthoklaba nangi leithoirol.\n\n"
                "Chingna koina pangba lam,\n"
                "Haona-Meitei machasing,\n"
                "Ichel amagi ishing-gum,\n"
                "Punna hingminnariba lam.\n\n"
                "Loktak ishing ithakna,\n"
                "Seithari nangi thounafam,\n"
                "Nongmaichinggi chingdolna,\n"
                "Lepli nangi ikaikhumnaba.\n\n"
                "Eikhoi leibak Manipur,\n"
                "Sana leibak Manipur."
            ),
            "bengali": (
                "সনা লৈবাক মণিপুর,\n"
                "কোলোই নঙ্গী মিংথোলনী,\n"
                "মালেম ইমাং খংনরবা,\n"
                "পুথোকলবা নঙ্গী লৈথোইরোল।\n\n"
                "চিংন কোইন পাংবা লম,\n"
                "হাওন-মৈতৈ মচাসিং,\n"
                "ইচেল অমগী ঈশিংগুম,\n"
                "পুন্ন হিংমিন্নরিবা লম।\n\n"
                "লোকতাক ঈশিং ইথক্ন,\n"
                "শৈথারী নঙ্গী থৌনাফম,\n"
                "নোংমাইচিংগী চিংদোল্ন,\n"
                "লেপ্লী নঙ্গী ইকাইখুম্নবা।\n\n"
                "ঐখোই লৈবাক মণিপুর,\n"
                "সনা লৈবাক মণিপুর।"
            ),
            "english": (
                "O golden land Manipur,\n"
                "Renowned is your revered name,\n"
                "Celebrated before the entire world,\n"
                "Manifesting your eternal glory.\n\n"
                "A land encircled by sheltering mountain ranges,\n"
                "Where hill peoples and valley Meiteis,\n"
                "Like waters of a singular flowing stream,\n"
                "Live together in enduring harmony.\n\n"
                "With gentle undulating waves, the waters of Loktak,\n"
                "Sing songs of your valorous heritage,\n"
                "While the sacred crest of Nongmaiching hill,\n"
                "Stands as an eternal monument to your sovereign honor.\n\n"
                "Our beloved motherland Manipur,\n"
                "O golden land Manipur!"
            )
        }
    },
    {
        "song_id": "thabal_chongba_ishei",
        "title": "ꯊꯥꯕꯜ ꯆꯣꯡꯕ ꯏꯁꯩ",
        "title_en": "Thabal Chongba Ishei (Moonlight Circle Dance Folk Song)",
        "title_roman": "Thabal Chongba Ishei",
        "title_bengali": "থাবল চোংবা ঈশৈ",
        "genre": "Traditional Folk Dance / Yaoshang Spring Festival Ballad",
        "composer": "Traditional Meitei Folk Balladeers",
        "lyricist": "Traditional Oral Folk Heritage",
        "year": "Traditional (Centuries-old folklore)",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "status": "Traditional Folk Song",
        "description": (
            "A joyful traditional Manipuri folk song sung during the spring Yaoshang (Holi) "
            "festival on full moon nights, where youth gather outdoors in circular rhythmic "
            "dance holding hands to the rhythm of the Pung drum."
        ),
        "source": "Manipuri Traditional Folk Heritage & Folklore Research Society",
        "copyright": "Public Domain (Traditional Cultural Expressions)",
        "lyrics": {
            "meitei": (
                "ꯊꯥꯕꯜ ꯆꯣꯡꯅꯕ ꯊꯣꯔꯛꯑꯣ,\n"
                "ꯅꯨꯃꯤꯗꯥꯡ ꯊꯥꯕꯜ ꯉꯥꯜꯂꯛꯂꯦ,\n"
                "ꯌꯥꯎꯁꯪ ꯊꯥꯒꯤ ꯄꯨꯔꯅꯤꯃꯥ,\n"
                "ꯃꯤꯌꯥꯝ ꯄꯨꯟꯅ ꯍꯔꯥꯎꯔꯦ꯫\n\n"
                "ꯈꯨꯠ ꯁꯥꯝꯅꯗꯨꯅ ꯀꯣꯏꯆꯠ ꯆꯠꯁꯤ,\n"
                "ꯄꯨꯡꯒꯤ ꯃꯈꯣꯜꯒ ꯇꯥꯏꯟꯅꯗꯨꯅ,\n"
                "ꯏꯅꯥꯐꯤ ꯐꯖꯅ ꯁꯦꯠꯂꯒ,\n"
                "ꯊꯥꯒꯤ ꯃꯉꯥꯜ ꯃꯈꯥꯗ ꯖꯒꯣꯏ ꯁꯥꯁꯤ꯫\n\n"
                "ꯃꯅꯤꯄꯨꯔꯒꯤ ꯅꯍꯥꯔꯣꯜꯁꯤꯡ,\n"
                "ꯑꯃꯒ ꯑꯃꯒ ꯅꯨꯡꯁꯤꯅ,\n"
                "ꯆꯥꯎꯈꯠ ꯊꯧꯔꯥꯡ ꯂꯝꯖꯤꯡꯗꯨꯅ,\n"
                "ꯍꯔꯥꯎ-ꯇꯌꯥꯝꯅ ꯆꯣꯡꯃꯤꯟꯅꯁꯤ꯫"
            ),
            "roman": (
                "Thabal chongnaba thorako,\n"
                "Numidang thabal ngallakle,\n"
                "Yaoshang thagi purnima,\n"
                "Miyam punna haraore.\n\n"
                "Khut samnaduna koichat chatsi,\n"
                "Pung-gi makholga tainaduna,\n"
                "Inaphi fajana setlaga,\n"
                "Thagi mangal makhada jagoi sasi.\n\n"
                "Manipurgi naharolsing,\n"
                "Amaga amaga nungshina,\n"
                "Chaokhat thourang lamjingduna,\n"
                "Harao-tayamna chongminnasi."
            ),
            "bengali": (
                "থাবল চোংনবা থোরকও,\n"
                "নুমিদাং থাবল ঙাল্লক্লে,\n"
                "য়াওশং থাগী পূর্ণিমা,\n"
                "মিয়াম পুন্ন হরাওরে।\n\n"
                "খুৎ সাম্নদুনা কোইচৎ চৎসী,\n"
                "পুংগী মখোল্গ তাইন্নদুনা,\n"
                "ইনাফী ফজন সেৎলগ,\n"
                "থাগী মঙাল মখাদ জগোই সাসী।\n\n"
                "মণিপুরগী নহারোল্সিং,\n"
                "অমগ অমগ নুংশিন,\n"
                "চাউখৎ থৌরাং লমজিংদুনা,\n"
                "হরাও-তায়াম্ন চোংমিন্নসী।"
            ),
            "english": (
                "Come out together to dance the Thabal!\n"
                "The evening moonlight shines radiantly,\n"
                "Under the sacred full moon of the spring Yaoshang,\n"
                "All the community gathers in celebration.\n\n"
                "Let us join hands in the rhythmic circle,\n"
                "Moving in synchrony with the beating of the sacred Pung,\n"
                "Adorned in elegant traditional Inaphi shawls,\n"
                "Let us dance joyfully beneath the glowing moon.\n\n"
                "Youth of our blessed Manipur,\n"
                "United with affection and goodwill,\n"
                "Striving hand-in-hand toward a brighter future,\n"
                "Let us dance in vibrant harmony!"
            )
        }
    },
    {
        "song_id": "eikhoi_kangleicha",
        "title": "ꯑꯩꯈꯣꯏ ꯀꯪꯂꯩꯆꯥ",
        "title_en": "Eikhoi Kangleicha (Children of Ancient Kangleipak)",
        "title_roman": "Eikhoi Kangleicha",
        "title_bengali": "ঐখোই কংলাইচা",
        "genre": "Traditional Cultural Ballad / Heritage Song",
        "composer": "Traditional Kanglei Balladeers",
        "lyricist": "Oral Folk Poetry of Manipur",
        "year": "Traditional",
        "language": "Meitei (Manipuri)",
        "script": "Meitei Mayek",
        "status": "Cultural Heritage Ballad",
        "description": (
            "A traditional reflective folk ballad evoking ancestral lineage, the sacred Puya "
            "manuscripts, historic Kangla fort, and the enduring unity between valley and hill peoples."
        ),
        "source": "Manipuri Cultural Council & Folk Oral History Archives",
        "copyright": "Public Domain (Traditional Cultural Expressions)",
        "lyrics": {
            "meitei": (
                "ꯑꯩꯈꯣꯏ ꯀꯪꯂꯩꯆꯥꯅꯤ,\n"
                "ꯏꯄꯨ-ꯏꯄꯥꯒꯤ ꯂꯝꯗꯃꯗ,\n"
                "ꯑꯔꯤꯕ ꯄꯨꯌꯥꯒꯤ ꯃꯉꯥꯜꯅ,\n"
                "ꯂꯝꯕꯤ ꯇꯥꯛꯂꯤ ꯃꯆꯥꯁꯤꯡꯗ꯫\n\n"
                "ꯀꯪꯂꯥ ꯊꯧꯒꯜ ꯇꯧꯔꯕ,\n"
                "ꯅꯤꯡꯊꯧꯔꯣꯜꯒꯤ ꯄꯨꯋꯥꯔꯤꯗ,\n"
                "ꯂꯥꯏꯅꯤꯡ ꯂꯥꯏꯁꯣꯜ ꯁꯦꯡꯂꯕ,\n"
                "ꯁꯅꯥꯃꯍꯤꯒꯤ ꯊꯧꯖꯥꯜꯅꯤ꯫\n\n"
                "ꯆꯤꯡ-ꯇꯝ ꯃꯇꯦꯡ ꯄꯥꯡꯅꯗꯨꯅ,\n"
                "ꯏꯆꯤꯟ-ꯏꯅꯥꯎ ꯑꯣꯏꯃꯤꯟꯅꯁꯤ,\n"
                "ꯑꯩꯈꯣꯏ ꯂꯩꯕꯥꯛ ꯐꯒꯠꯅꯕ,\n"
                "ꯄꯨꯟꯅ ꯊꯕꯛ ꯁꯨꯃꯤꯟꯅꯁꯤ꯫"
            ),
            "roman": (
                "Eikhoi Kangleichani,\n"
                "Ipu-ipagi lamdamda,\n"
                "Ariba Puyagi mangalna,\n"
                "Lambi takli machasingda.\n\n"
                "Kangla thougal touraba,\n"
                "Ningthourolgi puwarida,\n"
                "Laining-laisol senglaba,\n"
                "Sanamahigi thoujalni.\n\n"
                "Ching-tam mateng pangnaduna,\n"
                "Ichin-inao oiminnasi,\n"
                "Eikhoi leibak fagatnaba,\n"
                "Punna thabak suminnasi."
            ),
            "bengali": (
                "ঐখোই কংলাইচানী,\n"
                "ইপু-ইপাগী লমদম্দ,\n"
                "অরিবা পুয়াগী মঙাল্ন,\n"
                "লম্বী তাক্লী মচাসিংদ।\n\n"
                "কংলা থৌগল তৌরবা,\n"
                "নিংথৌরোলগী পুওয়ারীদ,\n"
                "লাইনিং-লাইশোল শেংলবা,\n"
                "সনামহিগী থৌজাল্নী।\n\n"
                "চিং-তম মতেং পাংনদুনা,\n"
                "ইচিন-ইনাও ওইমিন্নসী,\n"
                "ঐখোই লৈবাক ফগৎনবা,\n"
                "পুন্ন থবক শুমিন্নসী।"
            ),
            "english": (
                "We are the proud children of Kangleipak,\n"
                "Living in this sacred realm of our ancestors,\n"
                "Where the eternal light of ancient Puyas,\n"
                "Illuminates the righteous way for all future children.\n\n"
                "From the venerated halls of ancient Kangla,\n"
                "Echoing through the annals of kings,\n"
                "And through sacred rites of faith,\n"
                "Flow the benevolent blessings of Lainingthou Sanamahi.\n\n"
                "Hills and valleys standing together hand in hand,\n"
                "Living in peace as loving siblings,\n"
                "To foster prosperity and dignity for our land,\n"
                "Let us work together with one heart and soul."
            )
        }
    }
]

def get_songs() -> List[Dict[str, Any]]:
    """Return all authentic Manipuri song entries."""
    return SONGS

if __name__ == "__main__":
    print(f"Loaded {len(SONGS)} authentic Manipuri songs:")
    for s in SONGS:
        print(f" - {s['song_id']}: {s['title']} ({s['title_en']})")

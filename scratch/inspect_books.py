import json
import glob

print("=== data/books/texts/ ===")
for path in sorted(glob.glob("data/books/texts/*.json")):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    print(f"{d['book_id']}: {len(d['chapters'])} chapters, {sum(len(c['passages']) for c in d['chapters'])} passages")
    for c in d['chapters']:
        print(f"   Ch {c['chapter_number']}: {c['title_en']} ({len(c['passages'])} passages)")

print("\n=== src/meitei_lang/data/books.json ===")
with open("src/meitei_lang/data/books.json", encoding="utf-8") as f:
    books = json.load(f)
for b in books:
    print(f"{b['book_id']}: {len(b['chapters'])} chapters")


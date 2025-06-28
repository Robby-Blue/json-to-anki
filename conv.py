import hashlib
import json

def md5hash(text):
    return hashlib.md5(text.encode("UTF8")).hexdigest()

guids = set()
english_words = set()
japanese_words = set()

headers = [
    ("seperator", "semicolon"),
    ("html", "true"),
]

columns = [
    ("guid", 1),
    ("notetype", 2),
    ("deck", 3),
    ("tags", 6)
]

def process_word(word):
    notes = []

    english_word = word["english"]
    japanese_word = word["japanese"]

    word_key = word.get("key", english_word)

    if english_word in english_words:
        print("dup word:", english_word)
    english_words.add(english_word)
    if japanese_word in japanese_words:
        print("dup word:", japanese_word)
    japanese_words.add(japanese_word)

    # english to japanese
    # and japanese to english
    notes.append({
        "key": f"{word_key}/vocabulary",
        "note_type": "Zoe double sided typing",
        "front": english_word,
        "back": japanese_word
    })

    if "kanji" in word:
        # kanji to non kanji
        notes.append({
            "key": f"{word_key}/kanji",
            "note_type": "Zoe typing",
            "front": word["kanji"],
            "back": word["japanese"]
        })

    return notes

def process():
    notes_count = 0

    with open("words.json") as f:
        words = json.load(f)

    with open("deck.txt", "w") as f:
        for (key, value) in headers:
            f.write(f"#{key}:{value}\n")
        for (key, column) in columns:
            f.write(f"#{key} column:{column}\n")

        for word in words:            
            notes = process_word(word)

            for note in notes:
                notes_count += 1
                guid = md5hash(note["key"])
                
                if guid in guids:
                    print("duplicate guid from", note["key"])
                    return
                
                if not note["front"] or not note["back"]:
                    print("empty", note["key"])
                    return

                guids.add(guid)

                values = [guid, note["note_type"],
                          "Zoe's Japanese Words", note["front"], note["back"]]
                
                for value in values:
                    f.write(str(value)+";")

                f.write("\n")

    print("wrote", notes_count, "notes")

process()
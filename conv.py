import hashlib
import json

def md5hash(text):
    return hashlib.md5(text.encode("UTF8")).hexdigest()

with open("words.json") as f:
    words = json.load(f)

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

with open("deck.txt", "w") as f:
    for (key, value) in headers:
        f.write(f"#{key}:{value}\n")
    for (key, column) in columns:
        f.write(f"#{key} column:{column}\n")

    for word in words:
        english = word["english"]
        japanese = word["japanese"]
        guid = md5hash(english)
        
        values = [guid, "Double sided with typing", "Japanese Duolingo", english, japanese]
        
        for value in values:
            f.write(str(value)+";")

        f.write("\n")

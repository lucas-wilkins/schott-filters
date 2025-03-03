import json
import pickle

with open("data/index.json", 'r') as file:
    data = json.load(file)

downloads = data["downloads"]

english = []
german = []

for d in downloads:
    print(d["id"])
    if d["filename"].endswith("-de.pdf"):
        german.append((d["id"], d["filename"], d["url"]))
    else:
        english.append((d["id"], d["filename"], d["url"]))

# Just to check english and german are consistent (they seem to be)
english.sort(key=lambda x: x[0])
german.sort(key=lambda x: x[0])
for e, g in zip(english, german):
    if e[0] != g[0]:
        print("No match: ", e[0], g[0])

# Write

with open("data/english_datasheet_urls.pickle", 'wb') as file:
    pickle.dump(english, file)

with open("data/german_datasheet_urls.pickle", 'wb') as file:
    pickle.dump(german, file)

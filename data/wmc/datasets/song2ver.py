import csv
import json


def load_songs(csv_path):
    songs = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(row)
    return songs

songs=load_songs("dxdata.csv")
song2ver=[]
for song in songs:
    if song["CN"]:
        song2ver.append({song["索引"]:song["版本"]})

with open("song2ver.json", "w", encoding="utf-8") as f:
    json.dump(song2ver, f, ensure_ascii=False, indent=2)
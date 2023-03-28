import json
from text_sources import preprocess_text

with open("sources.json", "r") as f:
    raw_sources = json.load(f)

sources = [
    {"name": source["name"], "text": preprocess_text(source["text"])}
    for source in raw_sources
]

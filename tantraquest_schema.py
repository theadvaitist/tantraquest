import json

schema = [
    {
        "id": 0,
        "concept": "",
        "pratijna": "",
        "tantrayuktis": [
            {"name": "", "definition": "", "is_correct": False}
        ],
        "points": 10,
        "feedback": ""
    }
]

with open("tantraquest_blocks.json", "w", encoding="utf-8") as f:
    json.dump(schema, f, ensure_ascii=False, indent=4)

print("✅ TantraQuest schema file created: tantraquest_blocks.json")

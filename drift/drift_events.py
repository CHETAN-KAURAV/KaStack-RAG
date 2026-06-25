import json

with open("drift/drift_timeline.json", "r", encoding="utf-8") as f:
    timeline = json.load(f)

drifts = []

for i in range(1, len(timeline)):

    prev = timeline[i - 1]
    curr = timeline[i]

    if (
        prev["mood"] != curr["mood"]
        or prev["tone"] != curr["tone"]
    ):

        drifts.append({
            "from_day": prev["day"],
            "to_day": curr["day"],
            "old_mood": prev["mood"],
            "new_mood": curr["mood"],
            "old_tone": prev["tone"],
            "new_tone": curr["tone"],
            "trigger": curr["trigger"]
        })

with open("drift/drift_events.json", "w", encoding="utf-8") as f:
    json.dump(drifts, f, indent=2)

print(f"Detected {len(drifts)} drift events.")
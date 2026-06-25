import json
import re

# Load Topic Summaries

with open("outputs/topic_summaries.json", "r", encoding="utf-8") as f:
    topics = json.load(f)

QUERY = "sister"

results = []

# Retrieve Matching Topics

for topic in topics:

    text = json.dumps(topic).lower()

    if QUERY.lower() in text:

        results.append(topic)

print(f"\nFound {len(results)} matching topics\n")

# Emotional Weight

EMOTIONAL_WORDS = {
    "sad",
    "angry",
    "frustrated",
    "love",
    "hate",
    "cry",
    "happy",
    "upset",
    "excited"
}

resolved = []

for topic in results:

    messages = topic.get("messages", [])

    joined = " ".join(
        msg["text"]
        for msg in messages
    ).lower()

    emotional_score = 0

    for word in EMOTIONAL_WORDS:

        emotional_score += joined.count(word)

    recency_score = topic["conversation_id"]

    final_score = (
        0.7 * recency_score
        +
        0.3 * emotional_score
    )

    resolved.append({
        "conversation_id": topic["conversation_id"],
        "summary": topic["summary"],
        "score": final_score
    })

# Rank Results

resolved.sort(
    key=lambda x: x["score"],
    reverse=True
)

print("Top Ranked Chunks\n")

for item in resolved[:5]:

    print(
        f"Day {item['conversation_id']} "
        f"| Score={item['score']:.2f}"
    )

    print(item["summary"])
    print()
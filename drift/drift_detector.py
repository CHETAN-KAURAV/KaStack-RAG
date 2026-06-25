import json
from collections import Counter

# Load Data

with open("outputs/conversation_personas_clean.json", "r", encoding="utf-8") as f:
    personas = json.load(f)

with open("outputs/topic_summaries.json", "r", encoding="utf-8") as f:
    topics = json.load(f)

timeline = []

# Common meaningless keywords
STOP_TRIGGERS = {
    "hey",
    "hi",
    "hello",
    "love",
    "great",
    "good",
    "nice",
    "today",
    "day",
    "fun",
    "user",
    "thing",
    "things",
    "really",
    "awesome",
    "cool",
    "best",
    "favorite",
    "life",
    "work",
    "time",
    "people"
}

# Process Each Conversation

for persona in personas:

    conversation_id = persona["conversation_id"]

    style = persona.get("communication_style", {})

    avg_words = style.get("avg_words", 0)
    question_ratio = style.get("question_ratio", 0)
    exclamation_ratio = style.get("exclamation_ratio", 0)

    traits = persona.get("traits", [])

    trait_names = [t["trait"] for t in traits]

    # Mood Detection

    mood = "neutral"

    if "optimistic" in trait_names:
        mood = "optimistic"

    if "curious" in trait_names:
        mood = "curious"

    if "enthusiastic" in trait_names:
        mood = "enthusiastic"

    # Additional communication signals

    if question_ratio > 0.30:
        mood = "curious"

    if exclamation_ratio > 0.60:
        mood = "enthusiastic"

    # Tone Detection

    tone = "casual"

    if avg_words > 12:
        tone = "formal"

    # Trigger Detection

    trigger = "unknown"

    matching_topics = [
        topic
        for topic in topics
        if topic["conversation_id"] == conversation_id
    ]

    keyword_counter = Counter()

    for topic in matching_topics:

        for keyword in topic.get("keywords", []):

            clean_keyword = keyword.strip()

            if len(clean_keyword) < 3:
                continue

            if clean_keyword.lower() in STOP_TRIGGERS:
                continue

            keyword_counter[clean_keyword] += 1

    if len(keyword_counter) > 0:
        trigger = keyword_counter.most_common(1)[0][0]

    # Timeline Entry

    timeline.append({
        "day": conversation_id,
        "mood": mood,
        "tone": tone,
        "trigger": trigger
    })


# Save Timeline

with open("drift/drift_timeline.json", "w", encoding="utf-8") as f:
    json.dump(timeline, f, indent=2)

print(f"Generated {len(timeline)} timeline entries.")

# Preview

print("\nFirst 10 Timeline Entries:\n")

for item in timeline[:10]:
    print(item)
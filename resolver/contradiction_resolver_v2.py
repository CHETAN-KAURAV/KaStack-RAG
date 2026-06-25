import json
import re
from collections import defaultdict


TOPIC_FILE = "outputs/topic_summaries.json"


# LOAD TOPICS

with open(TOPIC_FILE, "r", encoding="utf-8") as f:
    topics = json.load(f)


# RETRIEVE RELEVANT TOPICS

def retrieve_topics(keyword):

    keyword = keyword.lower()

    results = []

    for topic in topics:

        text_blob = topic["summary"].lower()

        for msg in topic["messages"]:
            text_blob += " " + msg["text"].lower()

        if keyword in text_blob:
            results.append(topic)

    return results


# EXTRACT CLAIMS

def extract_claims(topics):

    claims = []

    patterns = [

        (
            r"i have (\w+) sister",
            "sister_count"
        ),

        (
            r"i have (\w+) sisters",
            "sister_count"
        ),

        (
            r"my sister is ([^.!,]+)",
            "sister_role"
        ),

        (
            r"my sister lives in ([^.!,]+)",
            "sister_location"
        ),

        (
            r"my sister and i are ([^.!,]+)",
            "relationship"
        )

    ]

    number_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6
    }

    for topic in topics:

        day = topic["global_topic_id"]

        for msg in topic["messages"]:

            text = msg["text"].lower()

            for pattern, claim_type in patterns:

                matches = re.findall(pattern, text)

                for match in matches:

                    value = match

                    if claim_type == "sister_count":
                        value = number_map.get(match, match)

                    claims.append({
                        "day": day,
                        "claim_type": claim_type,
                        "value": value,
                        "text": msg["text"]
                    })

    return claims


# DETECT CONTRADICTIONS

def detect_contradictions(claims):

    grouped = defaultdict(set)

    for claim in claims:

        grouped[claim["claim_type"]].add(
            str(claim["value"])
        )

    contradictions = {}

    for claim_type, values in grouped.items():

        if len(values) > 1:

            contradictions[claim_type] = list(values)

    return contradictions


# EMOTIONAL WEIGHT

def emotional_weight(text):

    score = 1

    emotional_words = [

        "love",
        "miss",
        "best friend",
        "proud",
        "late",
        "honored",
        "close",
        "important",
        "amazing",
        "special"

    ]

    text = text.lower()

    for word in emotional_words:

        if word in text:
            score += 3

    return score


# RANK CLAIMS

def rank_claims(claims):

    ranked = []

    for claim in claims:

        recency_score = claim["day"]

        emotion_score = emotional_weight(
            claim["text"]
        )

        total = recency_score + emotion_score

        ranked.append((total, claim))

    ranked.sort(reverse=True, key=lambda x: x[0])

    return ranked


# GENERATE FINAL ANSWER

def generate_answer(keyword):

    retrieved = retrieve_topics(keyword)

    print(f"\nRetrieved Topics: {len(retrieved)}")

    claims = extract_claims(retrieved)

    print(f"Claims Found: {len(claims)}")

    contradictions = detect_contradictions(claims)

    ranked = rank_claims(claims)

    print("\n" + "=" * 70)
    print("TOP EVIDENCE")
    print("=" * 70)

    for score, claim in ranked[:10]:

        print(
            f"\nDay {claim['day']} "
            f"| Score={score}"
        )

        print(claim["text"])

    print("\n" + "=" * 70)
    print("CONTRADICTIONS")
    print("=" * 70)

    if contradictions:

        for ctype, values in contradictions.items():

            print(
                f"\n{ctype}: {values}"
            )

    else:

        print("\nNo contradictions found.")

    print("\n" + "=" * 70)
    print("MERGED ANSWER")
    print("=" * 70)

    if ranked:

        best_claim = ranked[0][1]

        print(
            f"\nMost reliable evidence:"
        )

        print(best_claim["text"])

        if contradictions:

            print(
                "\n⚠ Contradictory information "
                "exists across conversations."
            )

            print(
                "The answer above is selected "
                "using recency and emotional weight."
            )

    else:

        print("\nNo information found.")


# MAIN

if __name__ == "__main__":

    query = input(
        "\nEnter entity to investigate: "
    )

    generate_answer(query)
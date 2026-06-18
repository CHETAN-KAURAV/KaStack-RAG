import json
import re
from collections import Counter


HABIT_PATTERNS = [
    r"I usually (.+)",
    r"I often (.+)",
    r"I always (.+)",
    r"I like to (.+)",
    r"I enjoy (.+)",
    r"I love (.+)"
]

FACT_PATTERNS = [
    r"I am a[n]? (.+)",
    r"I'm a[n]? (.+)",
    r"I work as a[n]? (.+)",
    r"I study (.+)",
    r"My wife (.+)",
    r"My husband (.+)",
    r"My dog (.+)",
    r"My cat (.+)"
]


def extract_habits(messages):

    habits = []

    for msg in messages:

        text = msg["text"]

        for pattern in HABIT_PATTERNS:

            matches = re.findall(
                pattern,
                text,
                re.IGNORECASE
            )

            habits.extend(matches)

    return Counter(habits)


def extract_facts(messages):

    facts = []

    for msg in messages:

        text = msg["text"]

        for pattern in FACT_PATTERNS:

            matches = re.findall(
                pattern,
                text,
                re.IGNORECASE
            )

            facts.extend(matches)

    return Counter(facts)


def communication_style(messages):

    total_words = 0
    total_msgs = len(messages)

    questions = 0
    exclamations = 0

    for msg in messages:

        text = msg["text"]

        total_words += len(
            text.split()
        )

        if "?" in text:
            questions += 1

        if "!" in text:
            exclamations += 1

    return {
        "avg_words":
            round(
                total_words /
                total_msgs,
                2
            ),

        "question_ratio":
            round(
                questions /
                total_msgs,
                2
            ),

        "exclamation_ratio":
            round(
                exclamations /
                total_msgs,
                2
            )
    }


def main():

    with open(
            "../outputs/all_messages.json",
            "r",
            encoding="utf-8"
    ) as f:

        messages = json.load(f)

    habits = extract_habits(
        messages
    )

    facts = extract_facts(
        messages
    )

    style = communication_style(
        messages
    )

    persona = {
        "habits": [
            {
                "habit": h,
                "count": c
            }
            for h, c in habits.most_common(50)
        ],

        "personal_facts": [
            {
                "fact": f,
                "count": c
            }
            for f, c in facts.most_common(50)
        ],

        "communication_style":
            style
    }

    with open(
            "../outputs/persona.json",
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            persona,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        "Persona generated."
    )


if __name__ == "__main__":
    main()
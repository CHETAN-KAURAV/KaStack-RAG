import json
import re
from tqdm import tqdm


# ---------- PATTERNS ----------

OCCUPATION_PATTERNS = [
    r"I am a[n]? (.+)",
    r"I'm a[n]? (.+)",
    r"I work as a[n]? (.+)",
    r"My job is (.+)",
]

HOBBY_PATTERNS = [
    r"I love (.+)",
    r"I enjoy (.+)",
    r"I like (.+)",
    r"My favorite hobby is (.+)",
]

TRAIT_KEYWORDS = {
    "friendly": [
        "thanks",
        "nice",
        "great",
        "wonderful"
    ],

    "enthusiastic": [
        "awesome",
        "excited",
        "amazing",
        "love"
    ],

    "curious": [
        "what",
        "why",
        "how",
        "where"
    ],

    "optimistic": [
        "hope",
        "positive",
        "looking forward"
    ]
}


# ---------- HELPERS ----------

def clean_text(text):

    text = text.strip()

    text = text.replace("!", "")
    text = text.replace("?", "")
    text = text.replace(".", "")

    return text


def extract_occupations(messages):

    occupations = []

    for msg in messages:

        text = msg["text"]

        for pattern in OCCUPATION_PATTERNS:

            matches = re.findall(
                pattern,
                text,
                re.IGNORECASE
            )

            for m in matches:

                occupation = clean_text(m)

                if len(occupation) < 60:
                    occupations.append(
                        occupation
                    )

    return list(set(occupations))


def extract_hobbies(messages):

    hobbies = []

    for msg in messages:

        text = msg["text"]

        for pattern in HOBBY_PATTERNS:

            matches = re.findall(
                pattern,
                text,
                re.IGNORECASE
            )

            for m in matches:

                hobby = clean_text(m)

                if len(hobby) < 80:
                    hobbies.append(
                        hobby
                    )

    return list(set(hobbies))


def extract_traits(messages):

    text = " ".join(
        [
            m["text"].lower()
            for m in messages
        ]
    )

    traits = []

    for trait, keywords in (
            TRAIT_KEYWORDS.items()
    ):

        score = 0

        for keyword in keywords:

            score += text.count(
                keyword
            )

        if score > 0:

            traits.append(
                {
                    "trait": trait,
                    "score": score
                }
            )

    traits.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return traits


def communication_style(messages):

    total_words = 0

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
                max(
                    len(messages),
                    1
                ),
                2
            ),

        "question_ratio":

            round(
                questions /
                max(
                    len(messages),
                    1
                ),
                2
            ),

        "exclamation_ratio":

            round(
                exclamations /
                max(
                    len(messages),
                    1
                ),
                2
            )
    }


# ---------- MAIN ----------

def main():

    with open(
            "../outputs/conversations.json",
            "r",
            encoding="utf-8"
    ) as f:

        conversations = json.load(f)

    personas = []

    for conversation in tqdm(
            conversations
    ):

        messages = (
            conversation["messages"]
        )

        occupations = (
            extract_occupations(
                messages
            )
        )

        hobbies = (
            extract_hobbies(
                messages
            )
        )

        traits = (
            extract_traits(
                messages
            )
        )

        style = (
            communication_style(
                messages
            )
        )

        personas.append(
            {

                "conversation_id":
                    conversation[
                        "conversation_id"
                    ],

                "occupation":
                    occupations[:5],

                "hobbies":
                    hobbies[:10],

                "traits":
                    traits[:5],

                "communication_style":
                    style
            }
        )

    with open(
            "../outputs/conversation_personas.json",
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            personas,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Generated "
        f"{len(personas)} personas"
    )


if __name__ == "__main__":
    main()
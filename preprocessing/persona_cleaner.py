import json
import re


STOP_WORDS = [
    " and ",
    " but ",
    " because ",
    " who ",
    " that ",
    ".",
    "!",
    "?"
]


def clean_phrase(text):

    text = text.strip()

    for stop in STOP_WORDS:

        if stop in text:

            text = text.split(stop)[0]

    return text.strip()


def main():

    with open(
            "../outputs/conversation_personas.json",
            "r",
            encoding="utf-8"
    ) as f:

        personas = json.load(f)

    for persona in personas:

        cleaned = []

        for occupation in persona["occupation"]:

            occupation = clean_phrase(
                occupation
            )

            if (
                len(occupation) > 2
                and len(occupation) < 50
            ):
                cleaned.append(
                    occupation
                )

        persona["occupation"] = (
            list(set(cleaned))
        )

    with open(
            "../outputs/conversation_personas_clean.json",
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
        "Saved cleaned personas."
    )


if __name__ == "__main__":
    main()
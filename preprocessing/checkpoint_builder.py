import json
from tqdm import tqdm
import yake


kw_extractor = yake.KeywordExtractor(
    lan="en",
    n=2,
    top=5
)


def generate_summary(text):

    keywords = kw_extractor.extract_keywords(text)

    keywords = [
        k[0]
        for k in keywords[:5]
    ]

    return (
        "Discussion about: "
        + ", ".join(keywords)
    ), keywords


def main():

    with open(
            "../outputs/all_messages.json",
            "r",
            encoding="utf-8"
    ) as f:

        messages = json.load(f)

    checkpoints = []

    checkpoint_size = 100

    checkpoint_id = 1

    for start in tqdm(
            range(
                0,
                len(messages),
                checkpoint_size
            )
    ):

        end = min(
            start + checkpoint_size,
            len(messages)
        )

        chunk = messages[start:end]

        text = " ".join(
            m["text"]
            for m in chunk
        )

        summary, keywords = (
            generate_summary(text)
        )

        checkpoints.append(
            {
                "checkpoint_id":
                    checkpoint_id,

                "start_message":
                    chunk[0]["msg_id"],

                "end_message":
                    chunk[-1]["msg_id"],

                "summary":
                    summary,

                "keywords":
                    keywords
            }
        )

        checkpoint_id += 1

    with open(
            "../outputs/checkpoints.json",
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            checkpoints,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Created "
        f"{len(checkpoints)} checkpoints"
    )


if __name__ == "__main__":
    main()
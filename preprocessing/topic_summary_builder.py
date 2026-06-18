import json
from tqdm import tqdm
import yake

from preprocessing.topic_detector import detect_topics


kw_extractor = yake.KeywordExtractor(
    lan="en",
    n=2,
    top=5
)


def summarize(messages):

    text = " ".join(
        m["text"]
        for m in messages
    )

    keywords = kw_extractor.extract_keywords(text)

    keywords = [
        k[0]
        for k in keywords[:5]
    ]

    summary = (
        "Discussion about "
        + ", ".join(keywords)
    )

    return summary, keywords


def main():

    with open(
            "../outputs/conversations.json",
            "r",
            encoding="utf-8"
    ) as f:

        conversations = json.load(f)

    topic_summaries = []

    global_topic_id = 1

    for conversation in tqdm(
            conversations
    ):

        topics = detect_topics(
            conversation["messages"]
        )

        for topic in topics:

            msgs = (
                conversation["messages"]
                [
                    topic["start_msg"]:
                    topic["end_msg"] + 1
                ]
            )

            summary, keywords = (
                summarize(msgs)
            )

            topic_summaries.append(
                {
                    "global_topic_id":
                        global_topic_id,

                    "conversation_id":
                        conversation[
                            "conversation_id"
                        ],

                    "topic_id":
                        topic["topic_id"],

                    "summary":
                        summary,

                    "keywords":
                        keywords,

                    "messages":
                        msgs
                }
            )

            global_topic_id += 1

    with open(
            "../outputs/topic_summaries.json",
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            topic_summaries,
            f,
            indent=2,
            ensure_ascii=False
        )


if __name__ == "__main__":
    main()
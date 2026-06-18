import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

WINDOW_SIZE = 3
SIMILARITY_THRESHOLD = 0.25
MIN_TOPIC_LENGTH = 4


def get_window_text(messages, start_idx, end_idx):
    texts = []

    for i in range(start_idx, end_idx):
        texts.append(messages[i]["text"])

    return " ".join(texts)


def detect_topics(messages):

    n = len(messages)

    if n <= MIN_TOPIC_LENGTH:
        return [
            {
                "topic_id": 1,
                "start_msg": 0,
                "end_msg": n - 1
            }
        ]

    boundaries = []

    for i in range(WINDOW_SIZE, n - WINDOW_SIZE):

        left_text = get_window_text(
            messages,
            i - WINDOW_SIZE,
            i
        )

        right_text = get_window_text(
            messages,
            i,
            i + WINDOW_SIZE
        )

        left_emb = model.encode(left_text)

        right_emb = model.encode(right_text)

        sim = cosine_similarity(
            [left_emb],
            [right_emb]
        )[0][0]

        if sim < SIMILARITY_THRESHOLD:
            boundaries.append(i)

    topics = []

    topic_start = 0
    topic_id = 1

    for boundary in boundaries:

        if boundary - topic_start >= MIN_TOPIC_LENGTH:

            topics.append(
                {
                    "topic_id": topic_id,
                    "start_msg": topic_start,
                    "end_msg": boundary - 1
                }
            )

            topic_id += 1
            topic_start = boundary

    topics.append(
        {
            "topic_id": topic_id,
            "start_msg": topic_start,
            "end_msg": n - 1
        }
    )

    return topics


def print_topics(conversation, topics):

    print("\n" + "=" * 70)

    print(
        f"Conversation {conversation['conversation_id']}"
    )

    print("=" * 70)

    for topic in topics:

        print(
            f"\nTopic {topic['topic_id']} "
            f"({topic['start_msg']} - {topic['end_msg']})"
        )

        print("-" * 30)

        for msg in conversation["messages"][
            topic["start_msg"]:
            topic["end_msg"] + 1
        ]:

            print(
                f"{msg['speaker']}: "
                f"{msg['text']}"
            )


def main():

    with open(
            "../outputs/conversations.json",
            "r",
            encoding="utf-8"
    ) as f:

        conversations = json.load(f)

    for conversation in conversations[:5]:

        topics = detect_topics(
            conversation["messages"]
        )

        print_topics(
            conversation,
            topics
        )

        print(
            "\nDetected Topics:",
            len(topics)
        )


if __name__ == "__main__":
    main()
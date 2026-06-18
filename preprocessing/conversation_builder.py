import pandas as pd
import re
import json
from tqdm import tqdm


def extract_messages(conversation):

    messages = []

    lines = conversation.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        match = re.match(
            r"(User\s+\d+):\s*(.*)",
            line
        )

        if match:

            messages.append({
                "speaker": match.group(1),
                "text": match.group(2)
            })

    return messages


def build_conversations():

    df = pd.read_csv(
        "../data/conversations.csv",
        header=None
    )

    conversations = []

    for conversation_id, row in enumerate(
            tqdm(df[0]),
            start=1
    ):

        conversations.append({
            "conversation_id": conversation_id,
            "messages": extract_messages(row)
        })

    return conversations


if __name__ == "__main__":

    conversations = build_conversations()

    print(
        "Total Conversations:",
        len(conversations)
    )

    print(
        "Messages in first conversation:",
        len(conversations[0]["messages"])
    )

    with open(
            "../outputs/conversations.json",
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            conversations,
            f,
            indent=2,
            ensure_ascii=False
        )
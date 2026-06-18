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

            speaker = match.group(1)
            text = match.group(2)

            messages.append({
                "speaker": speaker,
                "text": text
            })

    return messages


def build_message_stream():

    df = pd.read_csv(
        "../data/conversations.csv",
        header=None
    )

    all_messages = []

    msg_id = 1

    # conversation_id starts from 1
    for conversation_id, (_, row) in enumerate(
            tqdm(df.iterrows(), total=len(df)),
            start=1
    ):

        conversation = str(row[0])

        messages = extract_messages(conversation)

        for message in messages:

            all_messages.append({
                "msg_id": msg_id,
                "conversation_id": conversation_id,
                "speaker": message["speaker"],
                "text": message["text"]
            })

            msg_id += 1

    return all_messages


if __name__ == "__main__":

    messages = build_message_stream()

    print(
        "Total messages:",
        len(messages)
    )

    print("\nFirst 10 messages:\n")

    for msg in messages[:10]:
        print(msg)

    with open(
            "../outputs/all_messages.json",
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            messages,
            f,
            indent=2,
            ensure_ascii=False
        )
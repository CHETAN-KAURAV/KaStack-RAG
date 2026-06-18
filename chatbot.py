import json

from answer_generator import generate_answer


print("Loading chatbot...")


with open(
        "outputs/conversation_personas_clean.json",
        "r",
        encoding="utf-8"
) as f:

    personas = json.load(f)


def get_persona_docs():

    docs = []

    for persona in personas:

        docs.append(
            {
                "type": "persona",
                "text": "",

                "metadata": persona
            }
        )

    return docs


def chat():

    while True:

        query = input("\nAsk: ")

        if query.lower() in [
            "quit",
            "exit"
        ]:
            break

        docs = get_persona_docs()

        answer = generate_answer(
            query,
            docs
        )

        print("\n")
        print("=" * 60)
        print(answer)
        print("=" * 60)


if __name__ == "__main__":
    chat()
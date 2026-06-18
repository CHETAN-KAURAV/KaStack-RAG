import json
import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

documents = []


# ---------- TOPICS ----------

with open(
        "outputs/topic_summaries.json",
        "r",
        encoding="utf-8"
) as f:

    topics = json.load(f)

for topic in topics:

    text = topic["summary"]

    documents.append(
        {
            "type": "topic",
            "text": text,
            "metadata": topic
        }
    )


# ---------- CHECKPOINTS ----------

with open(
        "outputs/checkpoints.json",
        "r",
        encoding="utf-8"
) as f:

    checkpoints = json.load(f)

for checkpoint in checkpoints:

    text = checkpoint["summary"]

    documents.append(
        {
            "type": "checkpoint",
            "text": text,
            "metadata": checkpoint
        }
    )


# ---------- PERSONAS ----------

with open(
        "outputs/conversation_personas_clean.json",
        "r",
        encoding="utf-8"
) as f:

    personas = json.load(f)

for persona in personas:

    persona_text = []

    persona_text.extend(
        persona["occupation"]
    )

    persona_text.extend(
        persona["hobbies"]
    )

    for trait in persona["traits"]:

        persona_text.append(
            trait["trait"]
        )

    text = " ".join(persona_text)

    documents.append(
        {
            "type": "persona",
            "text": text,
            "metadata": persona
        }
    )


print(
    "Total Documents:",
    len(documents)
)


# ---------- EMBEDDINGS ----------

texts = [
    d["text"]
    for d in documents
]

embeddings = model.encode(
    texts,
    show_progress_bar=True
)

embeddings = np.array(
    embeddings,
    dtype=np.float32
)

# ---------- FAISS ----------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(
    embeddings
)

faiss.write_index(
    index,
    "outputs/faiss.index"
)

with open(
        "outputs/documents.pkl",
        "wb"
) as f:

    pickle.dump(
        documents,
        f
    )

print("Index saved.")
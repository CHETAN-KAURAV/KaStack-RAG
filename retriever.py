# retriever.py

import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

index = faiss.read_index(
    "outputs/faiss.index"
)

with open(
        "outputs/documents.pkl",
        "rb"
) as f:
    documents = pickle.load(f)


def retrieve(query, top_k=10):

    embedding = model.encode([query])

    embedding = np.array(
        embedding,
        dtype=np.float32
    )

    distances, indices = index.search(
        embedding,
        top_k
    )

    results = []

    for idx in indices[0]:
        results.append(
            documents[idx]
        )

    return results
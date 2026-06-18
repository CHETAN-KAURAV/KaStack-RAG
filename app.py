import streamlit as st

from retriever import retrieve
from answer_generator import generate_answer

st.title("KaStack RAG Chatbot")

query = st.text_input(
    "Ask a question"
)

if query:

    docs = retrieve(query)

    answer = generate_answer(
        query,
        docs
    )

    st.write(answer)
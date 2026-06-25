import streamlit as st
import json
import subprocess

from retriever import retrieve
from answer_generator import generate_answer

st.set_page_config(
    page_title="KaStack Adaptive Persona RAG",
    layout="wide"
)

st.title("KaStack Adaptive Persona RAG System")

feature = st.sidebar.selectbox(
    "Select Feature",
    [
        "Chatbot",
        "Persona Drift",
        "Intent Classifier",
        "Conflict Resolver"
    ]
)

# ==================================================
# CHATBOT
# ==================================================

if feature == "Chatbot":

    st.header("Conversational RAG Chatbot")

    query = st.text_input(
        "Ask a question"
    )

    if query:

        docs = retrieve(query)

        answer = generate_answer(
            query,
            docs
        )

        st.success(answer)

# ==================================================
# DRIFT
# ==================================================

elif feature == "Persona Drift":

    st.header("Adaptive Persona Timeline")

    try:

        with open(
                "drift/drift_timeline.json",
                "r",
                encoding="utf-8"
        ) as f:

            timeline = json.load(f)

        st.write(
            f"Total Days: {len(timeline)}"
        )

        for item in timeline[:100]:

            st.write(
                f"Day {item['day']} | "
                f"Mood: {item['mood']} | "
                f"Tone: {item['tone']} | "
                f"Trigger: {item['trigger']}"
            )

    except Exception as e:

        st.error(str(e))

# ==================================================
# INTENT
# ==================================================

elif feature == "Intent Classifier":

    st.header("Offline Intent Classifier")

    text = st.text_input(
        "Enter message"
    )

    if st.button(
            "Predict Intent"
    ):

        import joblib

        model = joblib.load(
            "classifier/intent_model.pkl"
        )

        pred = model.predict(
            [text]
        )[0]

        st.success(
            f"Intent: {pred}"
        )

# ==================================================
# RESOLVER
# ==================================================

elif feature == "Conflict Resolver":

    st.header(
        "Contradiction Resolver"
    )

    entity = st.text_input(
        "Entity",
        value="sister"
    )

    if st.button(
            "Run Resolver"
    ):

        try:

            output = subprocess.check_output(
                [
                    "python",
                    "resolver/contradiction_resolver_v2.py"
                ],
                text=True,
                input=f"{entity}\n"
            )

            st.text(output)

        except Exception as e:

            st.error(str(e))
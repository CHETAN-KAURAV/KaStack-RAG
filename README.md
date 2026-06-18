# KaStack Labs AI/ML Engineer Intern Assignment

## Persona-Aware Conversational RAG System

### Overview

This project implements a Retrieval-Augmented Generation (RAG) system for conversational data.

The system processes conversations chronologically, detects topic transitions, creates topic checkpoints, generates periodic summaries, extracts user personas, and answers queries using retrieved contextual information.

The goal was to build an end-to-end conversational memory system capable of:

* Detecting topic changes over time
* Creating topic-level summaries
* Creating 100-message checkpoints
* Extracting user personas
* Retrieving relevant context
* Answering user questions through a chatbot interface

---

# System Architecture

Dataset (CSV)
↓
Conversation Parsing
↓
Topic Change Detection
↓
Topic Summaries
↓
100 Message Checkpoints
↓
Persona Extraction
↓
FAISS Vector Index
↓
Retriever
↓
Chatbot
↓
Streamlit UI

---

# Dataset

Input Dataset:

* CSV file containing conversational data
* Each row represents one conversation
* Conversations are processed message-by-message in chronological order

Dataset Statistics:

* Total Conversations: 11,001
* Total Messages: 191,592
* Average Messages per Conversation: ~17

---

# Part 1: RAG System with Checkpoints

## Conversation Processing

Each conversation is parsed into individual messages while preserving chronological order.

Example:

User 1 → Message 1

User 2 → Message 2

User 1 → Message 3

User 2 → Message 4

This allows downstream modules to analyze topic transitions over time.

---

## Topic Change Detection

Instead of treating an entire conversation as a single topic, topic boundaries are detected dynamically.

### Method

1. Generate sentence embeddings for messages
2. Compare semantic similarity between message windows
3. Detect topic shifts when similarity drops below a threshold
4. Create a new topic checkpoint

This ensures that different discussion segments are stored separately.

### Example

Topic 1 → Messages 1–15

Discussion about moving to Portland

Topic 2 → Messages 16–27

Discussion about bookstores in Portland

Topic 3 → Messages 28–41

Discussion about reading habits

---

## Topic Detection Example

![Topic Detection](screenshots/02_data_pro_token_detect-a.png)
![Topic Detection](screenshots/02_data_pro_token_detect-b.png)

---

## Topic Summaries

For every detected topic segment:

* Topic ID
* Message Range
* Keywords
* Summary

are generated and stored.

Example:

Topic 1

Summary:
Discussion about moving to Portland and local recommendations.

Topic 2

Summary:
Discussion about bookstores and reading interests.

---

## Topic Summary Example

![Topic Summaries](screenshots/03_topic_summaries.png)
![Topic Summaries](screenshots/03-topic_summaries-b.png)

---

## 100 Message Checkpoints

Independent of topic segmentation, the system creates checkpoints every 100 messages.

Purpose:

* Long-term conversational memory
* Faster retrieval
* Conversation compression

Example:

Checkpoint 1

Messages 1–100

Checkpoint 2

Messages 101–200

Checkpoint 3

Messages 201–300

Each checkpoint contains a summary of its corresponding message range.

---

## Checkpoint Example

![Checkpoint Summaries](screenshots/04_checkpoints.png)

---

# Part 2: Persona Extraction

The system extracts structured persona information directly from conversation signals.

No external APIs were used.

The extracted persona includes:

### Occupation

Examples:

* Teacher
* Nurse
* Firefighter
* Librarian

### Hobbies & Interests

Examples:

* Reading
* Gardening
* Hiking
* Music
* Cooking

### Personality Traits

Examples:

* Friendly
* Curious
* Enthusiastic
* Optimistic

### Communication Style

Metrics:

* Average words per message
* Question ratio
* Exclamation ratio

---

## Persona Example

![Persona Extraction](screenshots/05_conversation_personas.png)

---

# Part 3: Retrieval-Augmented Generation (RAG)

## Index Construction

The following information sources are embedded and indexed:

### Topic Summaries

Generated topic-level checkpoints.

### Conversation Checkpoints

100-message summaries.

### Persona Records

Structured user persona information.

Embeddings are generated using:

sentence-transformers/all-MiniLM-L6-v2

and stored inside a FAISS vector index.

---

## Retrieval Workflow

User Query
↓
Query Embedding
↓
FAISS Similarity Search
↓
Retrieve Relevant Topics
↓
Retrieve Relevant Checkpoints
↓
Retrieve Relevant Personas
↓
Context Aggregation
↓
Answer Generation

---

# Part 4: Chatbot

A Streamlit-based chatbot interface was developed.

Supported Questions:

### Persona Questions

* What kind of person is this user?
* What are their habits?
* What hobbies do they have?
* How do they communicate?

### Context Questions

* Tell me about Portland
* Tell me about teachers
* Tell me about firefighters

The chatbot retrieves relevant context from the RAG pipeline and generates answers using the retrieved information.

---

## Chatbot Demo

![Chatbot Demo](screenshots/Deployment_Page.png)

---

# Technologies Used

### Core Libraries

* Python
* Pandas
* NumPy

### Embeddings

* Sentence Transformers
* all-MiniLM-L6-v2

### Vector Search

* FAISS

### NLP

* Hugging Face Transformers

### UI

* Streamlit

---

# Project Structure

KaStack-RAG/

├── app.py

├── chatbot.py

├── retriever.py

├── answer_generator.py

├── preprocessing/

│ ├── parser.py

│ ├── conversation_builder.py

│ ├── topic_detector.py

│ ├── topic_summary_builder.py

│ ├── checkpoint_builder.py

│ ├── conversation_persona_builder.py

│ └── persona_cleaner.py

├── outputs/

│ ├── conversations.json

│ ├── topic_summaries.json

│ ├── checkpoints.json

│ ├── conversation_personas_clean.json

│ ├── faiss.index

│ └── documents.pkl

├── screenshots/

├── requirements.txt

└── README.md

---

# Running Locally

## Clone Repository

git clone <repository-url>

cd KaStack-RAG

---

## Install Dependencies

pip install -r requirements.txt

---

## Run Application

streamlit run app.py

---

# Results

Successfully implemented:

✔ Topic Segmentation

✔ Topic Summaries

✔ 100-Message Checkpoints

✔ Persona Extraction

✔ FAISS-Based Retrieval

✔ Streamlit Chatbot

✔ End-to-End RAG Pipeline

---

# Deployment

Live Demo:
https://kastack-rag-gjqfpaf9dd4aleqqygfryg.streamlit.app/

---

# Notes

The dataset contains multiple independent conversational personas.

Therefore persona extraction is performed at the conversation level and then aggregated during retrieval.

This design allows the system to capture diverse persona characteristics while preserving conversational context.

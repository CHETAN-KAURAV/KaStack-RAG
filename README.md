# KaStack Labs AI/ML Engineer Intern Assignment

## Persona-Aware Conversational RAG System

### Author

Chetan Kaurav

### Live Demo

https://kastack-rag-gjqfpaf9dd4aleqqygfryg.streamlit.app/

### GitHub Repository

https://github.com/CHETAN-KAURAV/KaStack-RAG

---

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system for conversational data.

The system processes conversations chronologically, detects topic transitions, creates topic checkpoints, generates periodic summaries, extracts user personas, and answers queries using retrieved contextual information.

The goal was to build an end-to-end conversational memory system capable of:

- Detecting topic changes over time
- Creating topic-level summaries
- Creating 100-message checkpoints
- Extracting user personas
- Retrieving relevant context
- Answering user questions through a chatbot interface

---

# System Architecture
```
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
```
---

# Dataset

Input Dataset:

- CSV file containing conversational data
- Each row represents one conversation
- Conversations are processed message-by-message in chronological order

Dataset Statistics:

- Total Conversations: 11,001
- Total Messages: 191,592
- Average Messages per Conversation: ~17

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

A key requirement of the assignment was to avoid treating an entire conversation as a single topic.

The system processes every conversation chronologically, message by message.

### Method

1. Messages are grouped into semantic windows.
2. Sentence embeddings are generated using Sentence Transformers (all-MiniLM-L6-v2).
3. Semantic similarity is calculated between consecutive windows.
4. If similarity drops below a predefined threshold, a topic boundary is created.
5. A new topic checkpoint is started.
6. A summary is generated only for that topic segment.

This allows a single conversation to contain multiple topic checkpoints.

### Example

Topic 1 → Messages 1–15

Discussion about moving to Portland

Topic 2 → Messages 16–27

Discussion about bookstores in Portland

Topic 3 → Messages 28–41

Discussion about reading habits

This ensures that retrieval can operate on meaningful conversation segments rather than entire conversations.

---

## Topic Detection Example

![Topic Detection](screenshots/02_data_pro_token_detect-a.png)

![Topic Detection](screenshots/02_data_pro_token_detect-b.png)

---

## Topic Summaries

For every detected topic segment:

- Topic ID
- Message Range
- Keywords
- Summary

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

- Long-term conversational memory
- Faster retrieval
- Conversation compression

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

The system extracts structured persona information directly from conversation content.

No external APIs were used.

Persona extraction is performed at the conversation level.

### Occupation Extraction

Pattern matching is used to detect statements such as:

- I am a teacher
- I work as a nurse
- I am a firefighter
- I am a librarian

Detected occupations are stored in structured JSON format.

### Hobby Extraction

The system identifies activities and interests using conversational patterns such as:

- I like ...
- I love ...
- I enjoy ...
- My hobby is ...

Examples:

- Reading
- Gardening
- Hiking
- Cooking
- Music

### Personality Trait Extraction

Traits are inferred from observable conversation signals.

Examples:

- Friendly
- Curious
- Enthusiastic
- Optimistic

Trait scores are accumulated based on message patterns and conversational behavior.

### Communication Style Extraction

The following metrics are calculated:

- Average words per message
- Question ratio
- Exclamation ratio

These metrics provide insight into how a user communicates.

### Persona Output Format

Example:

```json
{
  "occupation": ["teacher"],
  "hobbies": ["reading", "gardening"],
  "traits": [
    {
      "trait": "friendly",
      "score": 8
    }
  ],
  "communication_style": {
    "avg_words": 10.4,
    "question_ratio": 0.28,
    "exclamation_ratio": 0.51
  }
}
```

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

Sentence Transformers (all-MiniLM-L6-v2)

and stored inside a FAISS vector index.

---

## Retrieval Workflow

The chatbot uses a Retrieval-Augmented Generation (RAG) pipeline.

### Indexed Sources

The FAISS vector database contains:

- Topic Summaries
- 100 Message Checkpoints
- Persona Records

### Retrieval Process

When a user submits a question:

1. The query is converted into an embedding.
2. FAISS performs semantic similarity search.
3. Relevant topic summaries are retrieved.
4. Relevant checkpoint summaries are retrieved.
5. Relevant persona records are retrieved.
6. Retrieved context is combined.
7. The chatbot generates an answer using the aggregated information.

Workflow:
```
User Query

↓

Query Embedding

↓

FAISS Similarity Search

↓

Retrieve Topic Summaries

↓

Retrieve Checkpoints

↓

Retrieve Persona Records

↓

Context Aggregation

↓

Answer Generation
```
This approach ensures that answers are generated using both short-term topic memory and long-term checkpoint memory.

---

# Part 4: Chatbot

A Streamlit-based chatbot interface was developed.

Supported Questions:

### Persona Questions

- What kind of person is this user?
- What are their habits?
- What hobbies do they have?
- How do they communicate?

### Context Questions

- Tell me about Portland
- Tell me about teachers
- Tell me about firefighters

The chatbot retrieves relevant context from the RAG pipeline and generates answers using the retrieved information.

---

# Round 2 Extensions

The Round 2 implementation extends the original conversational RAG system with adaptive persona modeling, offline intent classification, conflict-aware retrieval, and synchronization architecture design.

---

# Part 5: Adaptive Persona Engine

A new persona evolution module was implemented to track how user behavior changes across conversations over time.

Rather than generating a single static persona, the system maintains a timeline of personality and communication changes.

## Objective

Detect:

- Mood changes
- Tone changes
- Behavioral drift
- Triggering topics or events

---

## Persona Drift Detection

Each conversation is analyzed using:

- Extracted personality traits
- Communication style statistics
- Question frequency
- Exclamation frequency
- Average message length

From these signals the system generates:

- Mood
- Tone
- Trigger

for every conversation.

Example:

Day 1

Mood: Enthusiastic

Tone: Casual

Trigger: Powell Books

Day 4

Mood: Enthusiastic

Tone: Casual

Trigger: Everglades

Day 10

Mood: Enthusiastic

Tone: Casual

Trigger: Lasagna

---

## Drift Timeline

The output is stored in:

```
drift/drift_timeline.json
```
Example:
```
{
  "day": 10,
  "mood": "enthusiastic",
  "tone": "casual",
  "trigger": "lasagna"
}
```

## Chatbot Demo

![Chatbot Demo](screenshots/Deployment_Page.png)

---

# Technologies Used

### Core Libraries

- Python
- Pandas
- NumPy

### Embeddings

- Sentence Transformers
- all-MiniLM-L6-v2

### Vector Search

- FAISS

### NLP

- Hugging Face Transformers

### UI

- Streamlit

---

# Project Structure
```
KaStack-RAG/

├── app.py

├── chatbot.py

├── retriever.py

├── answer_generator.py

├── build_index.py

├── preprocessing/

│ ├── parser.py

│ ├── conversation_builder.py

│ ├── topic_detector.py

│ ├── topic_summary_builder.py

│ ├── checkpoint_builder.py

│ ├── conversation_persona_builder.py

│ ├── persona_extractor.py

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
```
---

# Running Locally

## Clone Repository

```bash
git clone https://github.com/CHETAN-KAURAV/KaStack-RAG.git
cd KaStack-RAG
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
streamlit run app.py
```

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
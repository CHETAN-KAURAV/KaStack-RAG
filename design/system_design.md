# System Design Document – Adaptive Persona RAG Assistant

## Overview

This document describes the synchronization architecture for an adaptive persona-aware Retrieval-Augmented Generation (RAG) assistant.

The system processes user conversations, builds topic checkpoints, extracts persona information, detects persona drift over time, and supports intelligent retrieval while maintaining a balance between privacy, synchronization efficiency, and conflict resolution.

The design follows an **offline-first architecture**, where most sensitive user data remains on the user's device while only lightweight metadata is synchronized to the cloud.

---

# Design Goals

The architecture is designed to achieve the following goals:

1. Preserve user privacy.
2. Minimize cloud storage requirements.
3. Support offline operation.
4. Synchronize important long-term memories across devices.
5. Handle conflicting memories gracefully.
6. Enable efficient retrieval and persona reasoning.

---

# High-Level Architecture

```text
+----------------------+
|      User Device     |
+----------------------+
| Raw Conversations    |
| Embedding Index      |
| Persona Cache        |
| Topic Checkpoints    |
| Drift Timeline       |
+----------+-----------+
           |
           | Sync Layer
           v
+----------------------+
|    Cloud Storage     |
+----------------------+
| Persona Metadata     |
| Topic Summaries      |
| Checkpoint Metadata  |
| Device Versions      |
+----------+-----------+
           |
           v
+----------------------+
| Retrieval Services   |
+----------------------+
| Semantic Search      |
| Conflict Resolver    |
| Persona Engine       |
+----------------------+
```

---

# On-Device Storage

The following information remains on the user's device:

## 1. Raw Conversations

Examples:

* Message history
* Chat logs
* Conversation transcripts

Reason:

Raw conversations may contain personal information and therefore should remain local whenever possible.

---

## 2. Embedding Index

Examples:

* FAISS index
* Vector embeddings
* Local retrieval database

Reason:

Embeddings can reveal information about user conversations.

Keeping them local improves privacy and enables fast offline retrieval.

---

## 3. Persona Cache

Examples:

* Personality traits
* Habits
* Communication style
* User preferences

Reason:

Persona information may contain sensitive personal characteristics.

---

## 4. Drift Timeline

Examples:

* Daily mood changes
* Tone evolution
* Trigger history

Reason:

These records describe behavioral patterns and should remain private.

---

# Cloud Storage

The following information is synchronized to the cloud.

## 1. Topic Summaries

Examples:

```text
Topic 1:
Moving to Portland

Topic 2:
Discussion about books

Topic 3:
Career plans
```

Only summaries are uploaded, not full conversations.

Benefits:

* Lower storage cost
* Faster synchronization
* Improved privacy

---

## 2. Checkpoint Metadata

Examples:

```json
{
  "checkpoint_id": 15,
  "message_range": "1500-1600",
  "created_at": "2026-06-25"
}
```

Used for synchronization and retrieval tracking.

---

## 3. Persona Metadata

Examples:

```json
{
  "occupation": "teacher",
  "traits": ["friendly", "curious"],
  "hobbies": ["reading", "gardening"]
}
```

Only high-level persona facts are synchronized.

---

## 4. Device Version Information

Examples:

```json
{
  "device_id": "laptop",
  "last_sync": "2026-06-25T14:00:00"
}
```

Used for conflict resolution.

---

# Synchronization Strategy

The system follows an incremental synchronization model.

## Step 1

User conversations are processed locally.

Outputs:

* Topic checkpoints
* Persona updates
* Drift events

---

## Step 2

Only changed summaries and metadata are uploaded.

Benefits:

* Reduces bandwidth usage
* Faster synchronization

---

## Step 3

Other devices download updated summaries and persona metadata.

This allows the user experience to remain consistent across devices.

---

# Conflict Resolution Strategy

Conflicts occur when multiple memories provide different information.

Example:

Conversation A:

```text
My sister lives in Texas.
```

Conversation B:

```text
My sister moved to California.
```

Both statements cannot simultaneously represent the latest state.

---

## Conflict Detection

The system detects contradictions by:

1. Extracting structured claims.
2. Grouping claims by entity.
3. Comparing conflicting values.

Example:

```json
{
  "entity": "sister",
  "attribute": "location",
  "values": [
    "Texas",
    "California"
  ]
}
```

---

## Conflict Ranking

Each claim receives a score:

```text
Final Score =
0.7 × Recency Score
+
0.3 × Emotional Weight
```

### Recency Score

More recent conversations receive higher priority.

---

### Emotional Weight

Claims containing emotional significance receive additional weight.

Examples:

```text
love
proud
important
close
miss
special
```

---

## Final Resolution

The highest-ranked claim becomes the primary answer.

Conflicting claims remain available as supporting evidence.

Example response:

```text
Most recent information suggests
the user's sister lives in California.

Earlier conversations mentioned Texas.

Potential contradiction detected.
```

---

# Persona Drift Detection

The system continuously monitors behavioral changes.

Metrics used:

* Personality traits
* Question frequency
* Exclamation frequency
* Message length

Example:

```text
Day 1
Mood: Curious
Tone: Formal

Day 4
Mood: Enthusiastic
Tone: Casual
```

The associated topic checkpoint is recorded as the trigger.

Example:

```text
Trigger:
Moving to Portland
```

---

# Security Considerations

The design follows privacy-first principles.

Measures:

* Offline-first processing
* Local embedding storage
* Minimal cloud synchronization
* Metadata-only uploads
* Incremental updates

This reduces exposure of sensitive user information.

---

# Scalability

The architecture scales efficiently because:

1. Retrieval uses vector search.
2. Topic checkpoints reduce retrieval scope.
3. Summaries are smaller than raw conversations.
4. Incremental synchronization minimizes bandwidth usage.

The design can support millions of conversations while maintaining efficient retrieval performance.

---

# Conclusion

This architecture combines:

* Topic-aware RAG retrieval
* Persona modeling
* Persona drift tracking
* Conflict-aware memory retrieval
* Offline-first storage
* Lightweight synchronization

The result is a scalable and privacy-preserving intelligent assistant capable of maintaining long-term conversational memory while adapting to changes in user behavior over time.

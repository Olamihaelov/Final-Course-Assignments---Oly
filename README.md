# 🎓 Final Assignments — AI Advanced

Complete course finals covering theory, embeddings, RAG, and a full AI agent with automation.

**Total Points:** 104  
**Coding Tasks:** 3 · **Theory Task:** 1

---

## 📋 Assignments Overview

| # | Assignment | Points | Description |
|---|------------|--------|-------------|
| 1 | [Theory Questions](./1%20-%20questions) | 24 | 12 conceptual questions on NLP, Vector DB, RAG, Docker, AI Agents, MCP & Agent Skills |
| 2 | [Vector Database](./2%20-%20vector%20database) | 20 | ChromaDB collection with ≥15 documents, semantic queries & analysis |
| 3 | [RAG with Word Document](./3%20-%20rag) | 20 | Full RAG pipeline: load DOCX → chunk → embed → retrieve → answer |
| 4 | [Restaurant AI Agent + n8n](./4%20-%20n8n) | 40 | Reservation chatbot + SQLite + webhook to n8n + Telegram notifications |

---

## 📁 Repository Structure

```
Finals-all/
├── 1 - questions/
│   └── questions.md / Theory_Questions.docx
├── 2 - vector database/
│   ├── vector_db.py
│   ├── requirements.txt
│   └── README.md
├── 3 - rag/
│   ├── RAG_docx.py
│   ├── rag_full_content.docx
│   ├── requirements.txt
│   ├── images/
│   └── README.md
├── 4 - n8n/
│   ├── restaurant_chatbot.py
│   ├── restaurant_db.py
│   ├── restaurant_telegram_workflow.json
│   ├── restaurant.db
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── .env.example
│   ├── images/
│   └── README.md
└── README.md
```

---

## 1️⃣ Assignment 1 — Theory Questions (24 pts)

**12 written questions** covering:

- NLP (Tokenization, Stemming vs Lemmatization, TF-IDF)
- Vector Databases & Embeddings
- Cosine Similarity
- RAG pipeline
- Docker (Image vs Container)
- AI Agents with Tools
- MCP (Model Context Protocol)
- Agent Skills

**Submission:** Written answers (DOCX / PDF / Markdown)

---

## 2️⃣ Assignment 2 — Vector Database (20 pts)

Build a local **ChromaDB** collection using the free model `all-MiniLM-L6-v2`.

**Requirements:**
- ≥ 15 documents with metadata
- 5 conceptual semantic queries
- Display similarity distances
- Short written analysis

**No API key required.**

```bash
cd "2 - vector database"
pip install -r requirements.txt
python vector_db.py
```

---

## 3️⃣ Assignment 3 — RAG with Word Document (20 pts)

Full **Retrieval-Augmented Generation** pipeline:

1. Load a `.docx` file
2. Split into chunks
3. Embed & store in ChromaDB
4. Retrieve relevant context
5. Generate LLM answers

**Requirements:**
- At least 5 relevant questions
- Show both the answer **and** the retrieved chunks

```bash
cd "3 - rag"
pip install -r requirements.txt
python RAG_docx.py
```

---

## 4️⃣ Assignment 4 — Restaurant AI Agent + n8n (40 pts)

Capstone project that combines:

- LangChain chatbot with intent classification
- Natural language reservation extraction
- SQLite storage (book / cancel)
- Webhook to **n8n**
- Telegram notifications for each event

**Architecture:**

```
Gradio UI → Chatbot → SQLite
               │
               ▼
          n8n Webhook
               │
      ┌────────┴────────┐
      ▼                 ▼
 Reservation      Cancellation
 Notification     Notification
```

```bash
cd "4 - n8n"
pip install -r requirements.txt
cp .env.example .env   # add your keys
docker-compose up -d   # start n8n
python restaurant_chatbot.py
```

---

## ✅ Submission Checklist

| Item | Status |
|------|--------|
| Theory answers (DOCX / PDF) | ✅ |
| Vector DB script + results | ✅ |
| RAG script + screenshots | ✅ |
| Restaurant chatbot + n8n workflow + screenshots | ✅ |

---

## 🛠️ Tech Stack

| Area | Tools |
|------|-------|
| Theory | Markdown / DOCX |
| Vector DB | ChromaDB, sentence-transformers |
| RAG | LangChain, ChromaDB, OpenAI, Gradio |
| Agent | LangChain, SQLite, Gradio, n8n, Telegram |

---

## 📬 Official Course Page

[Final Assignments — AI Advanced](https://pythonai200425.github.io/finals/index.html)
```
send to Email pythonai200425+finals@gmail.com

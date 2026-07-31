# 📄 RAG with Word Document

**Assignment 3 – Retrieval-Augmented Generation (20 pts)**

A complete RAG pipeline that loads a `.docx` Word document, splits it into chunks, stores embeddings in ChromaDB, and answers questions about the document’s content using an LLM.

---

## 🏗️ Pipeline Overview

```
.docx file
    │
    ▼
Docx2txtLoader
    │
    ▼
RecursiveCharacterTextSplitter  →  Chunks
    │
    ▼
OpenAI Embeddings + ChromaDB
    │
    ▼
Retriever (top-k chunks)
    │
    ▼
LLM Answer + Retrieved Context
```

---

## ✨ Features

- Load a Word (`.docx`) document
- Split text into overlapping chunks
- Create and persist embeddings in **ChromaDB**
- Ask questions about the document
- Display both the **LLM answer** and the **retrieved source chunks**
- Gradio chat interface (optional UI)

---

## 📁 Project Structure

```
3 - rag/
├── RAG_docx.py              # Main RAG application
├── rag_full_content.docx    # Source Word document
├── requirements.txt
├── images/                  # Screenshots of questions, answers & context
└── README.md
```

---

## 🚀 Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Typical packages:

```
langchain
langchain-community
langchain-openai
langchain-text-splitters
chromadb
docx2txt
python-dotenv
gradio
```

### 2. Configure environment

Create a `.env` file:

```env
OPENAI_API_KEY=sk-your-key-here
```

### 3. Run the application

```bash
python RAG_docx.py
```

---

## 🧪 How It Works

### Step 1–3: Load, Chunk & Index

1. Load the `.docx` file with `Docx2txtLoader`
2. Split the text with `RecursiveCharacterTextSplitter`
3. Create embeddings and store them in ChromaDB

### Step 4–5: Retrieve & Generate

1. Embed the user question
2. Retrieve the most relevant chunks
3. Pass the chunks + question to the LLM
4. Return the answer **together with the source context**

---

## ❓ Example Questions

The system is tested with at least 5 relevant questions, for example:

1. What is the main topic of this document?
2. Summarize the main points.
3. Who are the key people or characters mentioned?
4. What conclusions or recommendations are given?
5. What facts or examples support the main point?

For each question the output includes:
- The **LLM answer**
- The **retrieved context chunks**

---

## 📸 Screenshots

Screenshots showing the questions, answers, and retrieved context are available in the [`images/`](./images) folder.

---

## ✅ Requirements Covered

| Requirement | Status |
|-------------|--------|
| Load `.docx` document | ✅ |
| Split into chunks (with count printed) | ✅ |
| Store embeddings in ChromaDB | ✅ |
| Answer at least 5 questions with LLM | ✅ |
| Print retrieved context chunks | ✅ |
| Questions are relevant / non-trivial | ✅ |

---

## 🛠️ Tech Stack

- **LangChain**
- **OpenAI** (Embeddings + Chat)
- **ChromaDB**
- **Docx2txtLoader**
- **Gradio** (optional UI)
- **python-dotenv**
```

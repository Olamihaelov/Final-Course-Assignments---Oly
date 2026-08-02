# 📄 RAG with Word Document

**Assignment 3 – Retrieval-Augmented Generation (20 pts)**  
Official page: [https://pythonai200425.github.io/finals/03-rag-word.html](https://pythonai200425.github.io/finals/03-rag-word.html)

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
RecursiveCharacterTextSplitter
    (chunk_size=500, chunk_overlap=60)
    │
    ▼
OpenAI Embeddings + ChromaDB
    │
    ▼
Retriever (k=3)
    │
    ▼
RetrievalQA / LLM Answer + Retrieved Context
```

---

## ✨ Features

- Load a Word (`.docx`) document with `Docx2txtLoader`
- Split text with `RecursiveCharacterTextSplitter`  
  (`chunk_size=500`, `chunk_overlap=60`)
- Create and persist embeddings in **ChromaDB**
- Retrieve top **k=3** relevant chunks
- Generate answers with LLM (via `RetrievalQA` / custom chain)
- Display both the **LLM answer** and the **retrieved source chunks**
- Gradio chat interface for interactive Q&A

---

## 📁 Project Structure

```
3 - rag/
├── RAG_docx.py              # Main RAG application
├── rag_full_content.docx    # Source Word document
├── requirements.txt
├── images/                  # Screenshots
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
   - `chunk_size=500`  
   - `chunk_overlap=60`
3. Create embeddings (`OpenAIEmbeddings`) and store them in ChromaDB

### Step 4–5: Retrieve & Generate

1. Embed the user question
2. Retrieve the top **k=3** most relevant chunks
3. Pass the chunks + question to the LLM (via `RetrievalQA` or equivalent chain)
4. Return the answer **together with the source context**

---

## ❓ Example Questions

1. What is the main topic of this document?
2. Summarize the main points.
3. Who are the key people or characters mentioned?
4. What conclusions or recommendations are given?
5. What facts or examples support the main point?

For each question the output includes:
- The **LLM answer**
- The **retrieved context chunks** (top 3)

---

## 📸 Screenshots

### Gradio UI – Document Upload & Chat

![Gradio 1](https://github.com/user-attachments/assets/f6469904-35b0-432e-814a-c3dad299a9ed)

![Gradio 2](https://github.com/user-attachments/assets/145d2f2f-2b86-4efe-83ce-e1c19a63f4bf)

![Gradio 3](https://github.com/user-attachments/assets/ebf05e16-095d-4f20-925c-ab2e9730e5ef)

![Gradio 4](https://github.com/user-attachments/assets/0b996326-368b-4cc2-8b59-3462b6c21440)

![Gradio 5](https://github.com/user-attachments/assets/127f2e62-813a-4341-b25b-c77b990a2f8e)

### Evaluation – Questions, Answers & Retrieved Context

![Evaluation 1](https://github.com/user-attachments/assets/1a34e6e0-d69f-48c5-b9c8-2600128a5f15)

![Evaluation 2](https://github.com/user-attachments/assets/75ab4b7e-266d-41b3-bff8-a13a2efdc78b)

![Evaluation 3](https://github.com/user-attachments/assets/16bd6fbf-f2b2-449c-8912-c83b813d4787)

![Evaluation 4](https://github.com/user-attachments/assets/4dbbaeb5-69ae-4fa4-860a-35af16134220)

![Evaluation 5](https://github.com/user-attachments/assets/4091b60d-95b0-4d49-8da7-908525b7d34b)

![Evaluation 6](https://github.com/user-attachments/assets/334de5f1-ac5f-4ce3-b656-3c77d0baf6a4)

The screenshots show:
- Document upload in Gradio
- Multiple questions asked about the document
- LLM-generated answers
- Retrieved source chunks displayed with each answer

---

## 📊 Grading Criteria (20 pts)

| Criterion | Points | Status |
|-----------|--------|--------|
| `.docx` loaded and split into chunks (print chunk count) | 4 | ✅ |
| Embeddings stored in ChromaDB | 4 | ✅ |
| 5 questions answered with LLM | 6 | ✅ |
| Retrieved context chunks printed alongside answers | 4 | ✅ |
| Questions are relevant and non-trivial | 2 | ✅ |
| **Total** | **20** | ✅ |

---

## ✅ Requirements Covered

| Requirement | Status |
|-------------|--------|
| Load `.docx` document | ✅ |
| `chunk_size=500`, `chunk_overlap=60` | ✅ |
| Store embeddings in ChromaDB | ✅ |
| Retriever with `k=3` | ✅ |
| Answer at least 5 questions with LLM | ✅ |
| Print retrieved context chunks | ✅ |
| Questions are relevant / non-trivial | ✅ |
| Gradio UI | ✅ |

---

## 🛠️ Tech Stack

- **LangChain** (`Docx2txtLoader`, `RecursiveCharacterTextSplitter`, `RetrievalQA`)
- **OpenAI** (Embeddings + Chat)
- **ChromaDB**
- **Gradio**
- **python-dotenv**

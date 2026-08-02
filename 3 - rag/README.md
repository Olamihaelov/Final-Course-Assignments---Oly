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
- Gradio chat interface

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

### Gradio UI – Document Upload & Chat

![Evaluation 1](https://github.com/user-attachments/assets/f6469904-35b0-432e-814a-c3dad299a9ed)

![Evaluation 2](https://github.com/user-attachments/assets/145d2f2f-2b86-4efe-83ce-e1c19a63f4bf)

![Evaluation 3](https://github.com/user-attachments/assets/ebf05e16-095d-4f20-925c-ab2e9730e5ef)

![Evaluation 4](https://github.com/user-attachments/assets/0b996326-368b-4cc2-8b59-3462b6c21440)

![Evaluation 5](https://github.com/user-attachments/assets/127f2e62-813a-4341-b25b-c77b990a2f8e)

### Evaluation – Questions, Answers & Retrieved Context

![Gradio UI 1](https://github.com/user-attachments/assets/334de5f1-ac5f-4ce3-b656-3c77d0baf6a4)

![Gradio UI 2](https://github.com/user-attachments/assets/1a34e6e0-d69f-48c5-b9c8-2600128a5f15)

![Gradio UI 3](https://github.com/user-attachments/assets/75ab4b7e-266d-41b3-bff8-a13a2efdc78b)

![Gradio UI 4](https://github.com/user-attachments/assets/16bd6fbf-f2b2-449c-8912-c83b813d4787)

![Gradio UI 5](https://github.com/user-attachments/assets/4dbbaeb5-69ae-4fa4-860a-35af16134220)

![Gradio UI 6](https://github.com/user-attachments/assets/4091b60d-95b0-4d49-8da7-908525b7d34b)


The screenshots show:
- Document upload in Gradio
- Multiple questions asked about the document
- LLM-generated answers
- Retrieved source chunks displayed with each answer

---

## ✅ Requirements Covered

| Requirement | Status |
|-------------|--------|
| Load `.docx` document | ✅ |
| Split into chunks | ✅ |
| Store embeddings in ChromaDB | ✅ |
| Answer at least 5 questions with LLM | ✅ |
| Print retrieved context chunks | ✅ |
| Questions are relevant / non-trivial | ✅ |
| Gradio UI | ✅ |

---

## 🛠️ Tech Stack

- **LangChain**
- **OpenAI** (Embeddings + Chat)
- **ChromaDB**
- **Docx2txtLoader**
- **Gradio**
- **python-dotenv**

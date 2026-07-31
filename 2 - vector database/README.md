# 🗄️ Vector Database with ChromaDB

**Assignment 2 – Vector Database (20 pts)**

A local semantic search demo using **ChromaDB** and the free embedding model `all-MiniLM-L6-v2`.  
No API key is required.

---

## 🎯 Goal

Build a ChromaDB collection with domain-specific documents, run conceptual semantic queries, display similarity distances, and analyze the results.

---

## ✨ Features

- Local embedding model (`all-MiniLM-L6-v2`) – no API key needed
- At least **15 documents** with metadata
- **5 semantic queries** based on concepts (not exact keywords)
- Similarity **distances** printed for every result
- Short written **analysis** of the results

---

## 📁 Project Structure

```
2 - vector database/
├── vector_db.py         # Main script
├── requirements.txt
└── README.md
```

---

## 🚀 Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install chromadb sentence-transformers
```

### 2. Run the script

```bash
python vector_db.py
```

---

## 📦 What the Script Does

1. Creates a ChromaDB collection with a local embedding function
2. Adds **≥ 15 documents**, each with metadata (e.g. category, price, stock)
3. Runs **5 semantic queries** that rely on meaning, not exact words
4. Prints the top results with:
   - Document text
   - Metadata
   - Distance score
5. Prints a short analysis (5–8 sentences)

---

## 🔍 Example Queries (Conceptual)

Queries should use concepts rather than copying exact words from the documents, for example:

- "something fun for an indoor cat"
- "comfortable bed for an older dog"
- "food and gear for a small aquarium"
- "travel carrier for a small pet"

---

## 📊 Analysis

The script ends with a short analysis that answers:

1. Which query returned the most relevant results, and why?
2. Did any query return a surprisingly good match (conceptual match with no shared words)?
3. What distance threshold would you use to decide that a result is relevant?

---

## ✅ Requirements Covered

| Requirement | Status |
|-------------|--------|
| ≥ 15 documents with metadata | ✅ |
| Local embedding model (`all-MiniLM-L6-v2`) | ✅ |
| 5 conceptual semantic queries | ✅ |
| Distances displayed for each result | ✅ |
| Short written analysis | ✅ |

---

## 🛠️ Tech Stack

- **ChromaDB**
- **sentence-transformers** (`all-MiniLM-L6-v2`)
- **Python**

---

## 📝 Notes

- Lower distance = higher similarity (L2 distance by default)
- Distance `0.0` = perfect match
- All processing runs locally – no OpenAI key required
```

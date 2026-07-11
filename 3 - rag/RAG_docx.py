"""Chat with DOCX files using RAG — Assignment 3"""

import os
from dotenv import load_dotenv
import gradio as gr
import gradio.components.file as gradio_file
import gradio_client.utils as client_utils

from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Compatibility patch for Gradio file validation in this environment
if hasattr(gradio_file.File, "_process_single_file"):
    _orig_process_single_file = gradio_file.File._process_single_file

    def _patched_process_single_file(self, f):
        file_name = f.path
        if self.type == "filepath":
            if self.file_types:
                lower_types = [t.lower() for t in self.file_types]
                if ".docx" in lower_types or "file" in lower_types:
                    return file_name
            return _orig_process_single_file(self, f)
        return _orig_process_single_file(self, f)

    gradio_file.File._process_single_file = _patched_process_single_file


# ====================== STEP 1-3: Load, Chunk & Index ======================
def load_and_index(docx_path: str):
    """Load DOCX, chunk it, embed it, and return a retriever."""
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set. Add it to the project's .env file.")

    loader = Docx2txtLoader(docx_path)
    docs = loader.load()
    print(f"Loaded {len(docs)} document(s)")

    # Correct chunking settings (as required)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=60)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Persist vectorstore
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_docx_db"
    )
    print("Vector store created and persisted.")

    return vectorstore.as_retriever(search_kwargs={"k": 3})


class RAGChain:
    """Simple RAG chain compatible with the old RetrievalQA invoke interface."""

    def __init__(self, retriever, llm, prompt):
        self.retriever = retriever
        self.llm = llm
        self.prompt = prompt

    def invoke(self, inputs):
        question = inputs.get("query") or inputs.get("question")
        docs = self.retriever.invoke(question)
        context = "\n\n".join(doc.page_content for doc in docs)
        messages = self.prompt.format_messages(context=context, question=question)
        answer = self.llm.invoke(messages).content
        return {"result": answer, "source_documents": docs}


def build_chain(retriever):
    """Build a RAG chain."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "Answer the question based on the following context:\n\n{context}\n\nQuestion: {question}"
    )
    return RAGChain(retriever, llm, prompt)


# ====================== AUTO EVALUATION (for Assignment 3 Screenshot) ======================
def run_auto_evaluation(chain):
    """Run 5 questions and print LLM answer + full retrieved context."""
    questions = [
        "What is the main goal or purpose of this document?",
        "Who are the main people or roles mentioned and what is their purpose?",
        "What are the key recommendations or conclusions in this document?",
        "Extract 3 important facts or examples from the document.",
        "Provide a concise summary of the entire document.",
    ]

    print("\n" + "=" * 95)
    print("AUTO EVALUATION — 5 Questions with Retrieved Context (for Assignment 3)")
    print("=" * 95)

    for i, question in enumerate(questions, 1):
        result = chain.invoke({"query": question})

        print(f"\n{'=' * 95}")
        print(f"Question {i}: {question}")
        print('=' * 95)

        print(f"\nAnswer:\n{result['result']}\n")

        print("Retrieved Context (top 3 chunks):")
        if result.get("source_documents"):
            for j, src in enumerate(result["source_documents"], 1):
                print(f"\n[{j}] {src.page_content}\n")   # Full context (not truncated)
        else:
            print("No context retrieved.")

        print("-" * 95)


# Global state
chain = None


def upload_docx(docx_file):
    """Index uploaded DOCX file and run auto evaluation."""
    global chain
    if docx_file is None:
        return "No file uploaded.", []

    file_path = docx_file
    if hasattr(docx_file, "name"):
        file_path = docx_file.name
    elif hasattr(docx_file, "path"):
        file_path = docx_file.path

    if not file_path:
        return "No valid DOCX file path found.", []

    print(f"Indexing: {file_path}")
    retriever = load_and_index(file_path)
    chain = build_chain(retriever)

    # Run 5 questions + context printing (for screenshot)
    run_auto_evaluation(chain)

    return "✅ DOCX indexed successfully! You can now ask questions below.", []


def ask_question(question, history):
    """Answer a question about the uploaded DOCX."""
    global chain
    history = history or []

    if chain is None:
        return history + [
            {"role": "user", "content": question},
            {"role": "assistant", "content": "Please upload a DOCX file first."}
        ]

    result = chain.invoke({"query": question})
    answer = result.get("result", "No answer generated.")

    # Show retrieved context in chat
    if result.get("source_documents"):
        answer += "\n\n📚 Retrieved Context:"
        for i, src in enumerate(result["source_documents"], 1):
            answer += f"\n\n[{i}] {src.page_content[:350]}..."
    else:
        answer += "\n\n⚠️ No relevant information found in the document."

    return history + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer}
    ]


# ====================== GRADIO UI ======================
with gr.Blocks(title="Chat with DOCX - Assignment 3") as demo:
    gr.Markdown("## 📄 Chat with DOCX using RAG\nUpload a DOCX file and ask questions about it.")

    with gr.Row():
        docx_input = gr.File(label="Upload DOCX", file_types=[".docx"], type="filepath")
        status = gr.Textbox(label="Status", interactive=False)

    chatbot = gr.Chatbot(label="Conversation", height=450, type="messages")
    question_input = gr.Textbox(
        placeholder="Ask a question about your DOCX...",
        label="Your Question"
    )

    docx_input.change(
        fn=upload_docx,
        inputs=docx_input,
        outputs=[status, chatbot]
    )

    question_input.submit(
        fn=ask_question,
        inputs=[question_input, chatbot],
        outputs=chatbot
    )

    gr.Examples(
        examples=[
            ["What is the main topic of this document?"],
            ["Summarize the main points."],
            ["Who are the key people or characters mentioned?"],
            ["What conclusions or recommendations are given?"],
            ["What facts or examples support the main point?"],
        ],
        inputs=question_input,
    )


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)

import os
import streamlit as st

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    st.error("GOOGLE_API_KEY is missing from .env")
    st.stop()


# ==========================================
# STREAMLIT PAGE
# ==========================================

st.set_page_config(
    page_title="RAG PDF Chatbot",
    page_icon="🤖"
)

st.title("🤖 RAG PDF Chatbot")
st.write("Ask questions about the PDF.")


# ==========================================
# LOAD PDF
# ==========================================

PDF_PATH = "sample.pdf"

if not os.path.exists(PDF_PATH):
    st.error("sample.pdf not found!")
    st.stop()

loader = PyPDFLoader(PDF_PATH)

documents = loader.load()

st.success(
    f"PDF loaded successfully! Pages: {len(documents)}"
)


# ==========================================
# SPLIT TEXT
# ==========================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

st.info(
    f"Created {len(chunks)} text chunks."
)


# ==========================================
# CREATE EMBEDDINGS
# ==========================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==========================================
# CREATE VECTOR DATABASE
# ==========================================

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="day19_rag",
    persist_directory="./chroma_db"
)


# ==========================================
# RETRIEVER
# ==========================================

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# ==========================================
# GEMINI LLM
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


# ==========================================
# RAG PROMPT
# ==========================================

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful AI assistant.

Answer the question using ONLY the information
provided in the context.

If the answer is not present in the context,
say:

"I could not find the answer in the PDF."

Context:
{context}

Question:
{question}

Answer:
"""
)


# ==========================================
# USER QUESTION
# ==========================================

question = st.text_input(
    "Ask a question about your PDF:"
)

# ==========================================
# RAG PIPELINE
# ==========================================

if question:

    # Step 1: Retrieve relevant documents
    retrieved_docs = retriever.invoke(question)

    # Step 2: Combine retrieved text
    context = "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )

    # Step 3: Create the prompt
    formatted_prompt = prompt.invoke({
        "context": context,
        "question": question
    })

    # Step 4: Send prompt to Gemini
    response = llm.invoke(formatted_prompt)

    # ==========================================
    # DISPLAY ANSWER
    # ==========================================

    st.subheader("Answer")

    if isinstance(response.content, list):
        answer = "".join(
            item.get("text", "")
            for item in response.content
            if item.get("type") == "text"
        )
    else:
        answer = response.content

    st.write(answer)

    # ==========================================
    # DISPLAY RETRIEVED INFORMATION
    # ==========================================

    st.subheader("Retrieved PDF Information")

    for i, doc in enumerate(retrieved_docs, start=1):
        st.write(f"### Chunk {i}")
        st.write(doc.page_content)
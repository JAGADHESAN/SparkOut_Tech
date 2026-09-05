from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
import os


app = FastAPI(title="AI PDF Chatbot API")



UPLOAD_FOLDER = "uploads"
CHROMA_FOLDER = "chroma_db"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHROMA_FOLDER, exist_ok=True)



embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)



vectorstore = Chroma(
    collection_name="pdf_documents",
    embedding_function=embeddings,
    persist_directory=CHROMA_FOLDER
)



llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)



class QuestionRequest(BaseModel):
    question: str



@app.get("/")
def home():

    return {
        "message": "AI PDF Chatbot API is running!"
    }



@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):

        return {
            "error": "Only PDF files are allowed"
        }

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    # Read PDF
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    # Store in Chroma
    vectorstore.add_texts(chunks)

    return {
        "message": "PDF uploaded successfully!",
        "filename": file.filename,
        "pages": len(reader.pages),
        "chunks": len(chunks)
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    # Retrieve relevant documents
    documents = vectorstore.similarity_search(
        request.question,
        k=4
    )

    if not documents:

        return {
            "answer": "No relevant information found."
        }

    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    prompt = f"""
You are an AI PDF assistant.

Answer the user's question using ONLY
the information provided in the context.

If the answer is not present in the context,
say that the information is not available
in the uploaded PDF.

Context:
{context}

Question:
{request.question}

Answer clearly and concisely.
"""

    response = llm.invoke(prompt)

    return {
        "question": request.question,
        "answer": response.content,
        "sources": len(documents)
    }
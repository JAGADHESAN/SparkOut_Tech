from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI


app = FastAPI(title="AI PDF Chatbot API")



UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

VECTOR_DIR = "chroma_db"



embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)



llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)



class QuestionRequest(BaseModel):
    question: str



@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    reader = PdfReader(str(file_path))

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.create_documents([text])

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DIR
    )

    return {
        "message": "PDF uploaded successfully",
        "pages": len(reader.pages),
        "chunks": len(chunks)
    }



@app.post("/ask")
async def ask_question(request: QuestionRequest):

    vectorstore = Chroma(
        persist_directory=VECTOR_DIR,
        embedding_function=embeddings
    )

    docs = vectorstore.similarity_search(
        request.question,
        k=4
    )

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = f"""
You are an AI PDF assistant.

Answer the question using ONLY the provided context.

If the answer is not available in the context,
say that the information is not available in the document.

Context:
{context}

Question:
{request.question}
"""

    response = llm.invoke(prompt)

    answer = response.content

    if isinstance(answer, list):
        answer = "".join(
            item.get("text", "")
            for item in answer
            if isinstance(item, dict)
        )

    return {
        "question": request.question,
        "answer": answer,
        "sources": len(docs)
    }



@app.get("/")
def home():

    return {
        "message": "AI PDF Chatbot API is running"
    }
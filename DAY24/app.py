from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
import os

app = FastAPI(title="RAG PDF API")


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "RAG PDF API is running!"
    }


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    # Check file type
    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed"
        }

    # Save uploaded PDF
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

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

    return {
        "message": "PDF uploaded successfully!",
        "filename": file.filename,
        "pages": len(reader.pages),
        "characters": len(text)
    }
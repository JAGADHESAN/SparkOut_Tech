import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI


# Load environment variables
load_dotenv()


# ---------------- FASTAPI ----------------

app = FastAPI(
    title="LangChain FastAPI Chatbot",
    description="Day 23 - LangChain + FastAPI Integration",
    version="1.0"
)


# ---------------- LANGCHAIN LLM ----------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


# ---------------- REQUEST MODEL ----------------

class ChatRequest(BaseModel):
    message: str


# ---------------- HOME ENDPOINT ----------------

@app.get("/")
def home():
    return {
        "message": "LangChain + FastAPI Chatbot is running",
        "status": "success"
    }


# ---------------- CHAT ENDPOINT ----------------

@app.post("/chat")
def chat(request: ChatRequest):

    response = llm.invoke(request.message)

    if isinstance(response.content, list):

        answer = "".join(
            item.get("text", "")
            for item in response.content
            if item.get("type") == "text"
        )

    else:
        answer = response.content

    return {
        "question": request.message,
        "answer": answer
    }
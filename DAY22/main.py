from fastapi import FastAPI
from pydantic import BaseModel

# Create FastAPI application
app = FastAPI(
    title="GenAI FastAPI Demo",
    description="Day 22 - FastAPI Basics",
    version="1.0"
)


# ---------------- HOME ENDPOINT ----------------

@app.get("/")
def home():
    return {
        "message": "Welcome to GenAI FastAPI Application",
        "status": "API is running"
    }


# ---------------- GET ENDPOINT ----------------

@app.get("/hello")
def hello():
    return {
        "message": "Hello from FastAPI!"
    }


# ---------------- REQUEST MODEL ----------------

class UserRequest(BaseModel):
    name: str
    topic: str


# ---------------- POST ENDPOINT ----------------

@app.post("/generate")
def generate(request: UserRequest):

    return {
        "name": request.name,
        "topic": request.topic,
        "response": f"Hello {request.name}! You asked about {request.topic}."
    }
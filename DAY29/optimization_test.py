import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI


# ==============================
# API KEY CHECK
# ==============================

if not os.getenv("GOOGLE_API_KEY"):
    print("ERROR: GOOGLE_API_KEY is not set.")
    print("Set your Gemini API key before running the program.")
    exit()


# ==============================
# INITIALIZE LLM
# ==============================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


# ==============================
# PROMPT
# ==============================

def create_prompt(question):

    return f"""
Answer the following question clearly and briefly.

Question:
{question}

Rules:
- Use simple language.
- Give only relevant information.
- Do not invent facts.
"""


# ==============================
# AI RESPONSE FUNCTION
# ==============================

def ask_ai(question):

    if not question.strip():
        return "ERROR: Question cannot be empty."

    prompt = create_prompt(question)

    print("\n===== PROMPT =====")
    print(prompt)

    start_time = time.perf_counter()

    try:
        response = llm.invoke(prompt)

        end_time = time.perf_counter()

        latency = end_time - start_time

        print("\n===== RESPONSE =====")
        print(response.content)

        print("\n===== PERFORMANCE =====")
        print(f"Latency: {latency:.2f} seconds")

        return response.content

    except Exception as e:

        print("\n===== ERROR =====")
        print(str(e))

        return "An error occurred while processing your request."


# ==============================
# TESTING
# ==============================

print("🤖 Day 29 - AI Testing & Optimization")

question = input("\nEnter your question: ")

ask_ai(question)
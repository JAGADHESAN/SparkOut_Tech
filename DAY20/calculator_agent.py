import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent


# Load API key
load_dotenv()


# ==========================================
# CALCULATOR TOOL
# ==========================================

@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.
    """

    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)

    except Exception as e:
        return f"Error: {e}"


# ==========================================
# LLM
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


# ==========================================
# CREATE AI AGENT
# ==========================================

agent = create_agent(
    model=llm,
    tools=[calculator]
)


# ==========================================
# USER QUESTION
# ==========================================

question = input("Enter your calculation: ")


# ==========================================
# RUN AGENT
# ==========================================

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }
)


# ==========================================
# DISPLAY RESPONSE
# ==========================================

print("\n===== AI AGENT RESPONSE =====")

print(result["messages"][-1].content)
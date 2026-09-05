from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from tavily import TavilyClient
import os


app = FastAPI(title="AI Web Research Agent API")


# -----------------------------
# Gemini LLM
# -----------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


# -----------------------------
# Tavily Web Search Tool
# -----------------------------

tavily_client = TavilyClient(
    api_key=os.environ["TAVILY_API_KEY"]
)


@tool
def web_search(query: str) -> str:
    """Search the web for current information."""

    results = tavily_client.search(
        query=query,
        max_results=5
    )

    output = []

    for result in results.get("results", []):
        title = result.get("title", "")
        content = result.get("content", "")
        url = result.get("url", "")

        output.append(
            f"Title: {title}\n"
            f"Content: {content}\n"
            f"URL: {url}\n"
        )

    return "\n".join(output)


# -----------------------------
# Bind tool to Gemini
# -----------------------------

llm_with_tools = llm.bind_tools([web_search])


# -----------------------------
# Request Model
# -----------------------------

class ResearchRequest(BaseModel):
    question: str


# -----------------------------
# Home Endpoint
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "AI Web Research Agent API is running!"
    }


# -----------------------------
# Research Endpoint
# -----------------------------

@app.post("/research")
def research(request: ResearchRequest):

    prompt = f"""
You are a web research AI agent.

User question:
{request.question}

Use the web_search tool when current or online information is required.

After researching, provide:
1. A clear answer
2. Important findings
3. Sources used

Keep the response easy to understand.
"""

    response = llm_with_tools.invoke(prompt)

    # If Gemini requests a tool call
    if response.tool_calls:

        tool_results = []

        for tool_call in response.tool_calls:

            if tool_call["name"] == "web_search":

                result = web_search.invoke(
                    tool_call["args"]
                )

                tool_results.append(result)

        research_context = "\n\n".join(tool_results)

        final_prompt = f"""
Answer the user's question using the web research below.

Question:
{request.question}

Web Research:
{research_context}

Give a clear and concise answer.

Include the important sources/URLs from the research.
"""

        final_response = llm.invoke(final_prompt)

        return {
            "question": request.question,
            "answer": final_response.content,
            "web_search_used": True
        }

    # If no tool was required
    return {
        "question": request.question,
        "answer": response.content,
        "web_search_used": False
    }
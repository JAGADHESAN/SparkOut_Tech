import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple words for a beginner."
)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)

chain = prompt | llm

response = chain.invoke({
    "topic": "Machine Learning"
})

print("LLM Response:")
print(response.text)
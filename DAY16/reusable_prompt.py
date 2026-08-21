from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

prompt = PromptTemplate(
    input_variables=["topic", "level"],
    template="""
You are a helpful teacher.

Explain {topic} for a {level} student.

Use simple language and give one example.
"""
)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)

chain = prompt | llm

response = chain.invoke({
    "topic": "Machine Learning",
    "level": "beginner"
})

print("===== RESPONSE 1 =====")
print(response.text)

response2 = chain.invoke({
    "topic": "Python Functions",
    "level": "beginner"
})

print("\n===== RESPONSE 2 =====")
print(response.text)
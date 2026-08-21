from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)

explanation_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
Explain the following topic for a beginner.

Topic: {topic}

Use simple language and give a practical example.
"""
)

summary_prompt = PromptTemplate(
    input_variables=["explanation"],
    template="""
Summarize the following explanation in 3 simple points.

Explanation:
{explanation}
"""
)

keypoints_prompt = PromptTemplate(
    input_variables=["summary"],
    template="""
Based on the following summary, provide 3 important
things a student should remember.

Summary:
{summary}
"""
)

explanation_chain = explanation_prompt | llm
summary_chain = summary_prompt | llm
keypoints_chain = keypoints_prompt | llm

topic = "Machine Learning"

print("\n===== STEP 1: EXPLANATION =====")

explanation_response = explanation_chain.invoke({
    "topic": topic
})

explanation = explanation_response.text

print(explanation)


print("\n===== STEP 2: SUMMARY =====")

summary_response = summary_chain.invoke({
    "explanation": explanation
})

summary = summary_response.text

print(summary)


print("\n===== STEP 3: KEY POINTS =====")

keypoints_response = keypoints_chain.invoke({
    "summary": summary
})

keypoints = keypoints_response.text

print(keypoints)


print("\n===== PIPELINE COMPLETED =====")
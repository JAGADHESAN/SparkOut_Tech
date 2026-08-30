import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- TITLE ----------------

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and let AI analyze your skills, profile and career opportunities.")

# ---------------- PDF UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload your Resume PDF",
    type=["pdf"]
)

# ---------------- ANALYSIS ----------------

if uploaded_file is not None:

    st.success("Resume uploaded successfully!")

    # Read PDF
    reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    st.write(f"📄 Pages detected: {len(reader.pages)}")

    if not resume_text.strip():
        st.error("Could not extract text from this PDF.")
        st.stop()

    # ---------------- LLM ----------------

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash"
    )

    # ---------------- PROMPT ----------------

    prompt = f"""
You are an expert AI Resume Analyzer.

Analyze the following resume.

RESUME:
{resume_text}

Provide the analysis in the following format:

1. Resume Summary
Give a short professional summary.

2. Technical Skills
List the technical skills found in the resume.

3. Soft Skills
List the soft skills found in the resume.

4. Education
Summarize the education information.

5. Suitable Job Roles
Suggest 5 suitable entry-level job roles.

6. Strengths
Mention the strongest aspects of the resume.

7. Areas for Improvement
Give practical suggestions to improve the resume.

8. Overall Resume Rating
Give a rating out of 10 and briefly explain the rating.

Keep the answer clear and professional.
"""

    # ---------------- BUTTON ----------------

    if st.button("🤖 Analyze Resume"):

        with st.spinner("AI is analyzing your resume..."):

            response = llm.invoke(prompt)

            # Handle Gemini response
            if isinstance(response.content, list):

                answer = "".join(
                    item.get("text", "")
                    for item in response.content
                    if item.get("type") == "text"
                )

            else:
                answer = response.content

        st.success("Resume analysis completed!")

        st.markdown("## 📊 Resume Analysis")

        st.markdown(answer)
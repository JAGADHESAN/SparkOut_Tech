import streamlit as st
import requests


st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI PDF Chatbot")

st.write(
    "Upload a PDF and ask questions using Generative AI."
)


API_URL = "http://127.0.0.1:8000"



st.subheader("📄 Upload PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)


if uploaded_file is not None:

    if st.button("Upload & Process PDF"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        try:

            response = requests.post(
                f"{API_URL}/upload",
                files=files
            )

            if response.status_code == 200:

                data = response.json()

                st.success(
                    "✅ PDF processed successfully!"
                )

                st.info(
                    f"📄 Pages: {data['pages']} | "
                    f"🧩 Chunks: {data['chunks']}"
                )

            else:

                st.error(
                    f"Upload failed: {response.text}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to FastAPI."
            )



st.subheader("💬 Ask a Question")

question = st.text_input(
    "Ask something about your PDF:"
)


if st.button("Ask AI 🤖"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            response = requests.post(
                f"{API_URL}/ask",
                json={
                    "question": question
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.subheader("### Answer")

                st.write(
                    data["answer"]
                )

                st.info(
                    f"📚 Sources used: "
                    f"{data['sources']}"
                )

            else:

                st.error(
                    f"API Error: {response.text}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to FastAPI."
            )
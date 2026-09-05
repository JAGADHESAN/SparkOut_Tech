import streamlit as st
import requests

st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="🤖"
)

st.title("🤖 AI PDF Chatbot")
st.write("Ask questions about your PDF using the FastAPI backend.")

# FastAPI URL
API_URL = "http://127.0.0.1:8000/ask"

question = st.text_input(
    "Ask a question about your PDF:"
)

if st.button("Ask 🤖"):

    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            response = requests.post(
                API_URL,
                json={"question": question}
            )

            if response.status_code == 200:

                data = response.json()

                st.subheader("Answer")

                answer = data.get("answer", "")

                if isinstance(answer, list):
                    text_parts = []

                    for item in answer:
                        if isinstance(item, dict):
                            text_parts.append(
                                item.get("text", "")
                            )

                    answer = "".join(text_parts)

                st.write(answer)

                if "sources" in data:
                    st.info(
                        f"📚 Sources used: {data['sources']}"
                    )

            else:
                st.error(
                    f"API Error: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "❌ Could not connect to FastAPI. "
                "Make sure the backend is running."
            )
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma



embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


documents = [
    "Python is a popular programming language.",
    "Machine Learning allows computers to learn from data.",
    "Deep Learning uses neural networks.",
    "Natural Language Processing works with human language.",
    "Artificial Intelligence enables machines to perform intelligent tasks."
]

vector_store = Chroma.from_texts(
    texts=documents,
    embedding=embeddings,
    collection_name="day18_documents",
    persist_directory="./chroma_db"
)

print("Documents successfully converted into embeddings!")
print("Vectors successfully stored in Chroma vector database.")


query = "How do computers learn from data?"

results = vector_store.similarity_search(query, k=2)

print("\n===== SIMILAR DOCUMENTS =====")

for i, result in enumerate(results, start=1):
    print(f"{i}. {result.page_content}")
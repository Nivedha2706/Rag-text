from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM, OllamaEmbeddings

# Load embeddings (same as ingestion)
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Load vector database
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# Retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# LLM (Llama 3.2)
llm = OllamaLLM(model="llama3.2:3b")

print("RAG Chatbot Ready! Type 'exit' to stop.\n")

while True:
    query = input("Ask: ")

    if query.lower() == "exit":
        break

    # Retrieve relevant chunks
    docs = retriever.invoke(query)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
You are a helpful assistant. Answer ONLY from the document context.

Context:
{context}

Question:
{query}

Answer clearly and simply.
"""

    response = llm.invoke(prompt)

    print("\nAnswer:\n", response)
    print("\n" + "-"*50 + "\n")
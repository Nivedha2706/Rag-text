from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM, OllamaEmbeddings

# Load embeddings (same model used in ingestion)
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Load vector database
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Load LLM (Llama 3.2:3B via Ollama)
llm = OllamaLLM(model="llama3.2:3b")

# Get user query
query = input("Ask for summary: ")

# Retrieve relevant chunks
docs = retriever.invoke(query)

# Combine text
context = "\n\n".join([doc.page_content for doc in docs])

# Prompt
prompt = f"""
You are an AI assistant.

Summarize the following document in a clear, detailed and structured way.

Include:
- Main idea
- Key points
- Important details
- Final conclusion

Document:
{context}
"""

# Get response from LLM
response = llm.invoke(prompt)

print("\n===== DOCUMENT SUMMARY =====\n")
print(response)
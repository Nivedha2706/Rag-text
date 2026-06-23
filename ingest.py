import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


def load_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)

    elif ext == ".txt":
        loader = TextLoader(file_path)

    elif ext == ".csv":
        loader = CSVLoader(file_path)

    elif ext == ".docx":
        loader = UnstructuredWordDocumentLoader(file_path)

    elif ext == ".pptx":
        loader = UnstructuredPowerPointLoader(file_path)

    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return loader.load()


file_path = input("Enter document path: ")

documents = load_document(file_path)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)
print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks[:5]):  # show first 5 chunks
    print(f"\n===== Chunk {i+1} =====")
    print(chunk.page_content[:300])


embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("Document indexed successfully!")
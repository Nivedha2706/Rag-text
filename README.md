
<div align="center">

# 🤖 RAG Document Chatbot

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=28&duration=3000&pause=1000&color=00C4FF&center=true&vCenter=true&width=700&lines=Retrieval+Augmented+Generation;Llama+3.2+%7C+ChromaDB+%7C+Ollama;Document+Summarization+and+Q%26A;Built+with+LangChain+and+Streamlit" />

<br>

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-orange?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama-LLM-black?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?style=for-the-badge)

</div>

---

# 🚀 System Workflow

```text
        📄 User Document
               │
               ▼
     ┌─────────────────┐
     │ Document Loader │
     └─────────────────┘
               │
               ▼
     ┌─────────────────┐
     │ Text Splitter ✂ │
     └─────────────────┘
               │
               ▼
     ┌─────────────────┐
     │ Embeddings 🧠   │
     └─────────────────┘
               │
               ▼
     ┌─────────────────┐
     │ ChromaDB 💾     │
     └─────────────────┘
               │
               ▼
     ┌─────────────────┐
     │ Retriever 🔍    │
     └─────────────────┘
               │
               ▼
     ┌─────────────────┐
     │ Llama 3.2 🤖    │
     └─────────────────┘
               │
               ▼
        💬 Intelligent Answer
```

---

# ⚡ Features

- 📄 PDF Support
- 📝 DOCX Support
- 📊 CSV Support
- 📑 PPTX Support
- ✂️ Automatic Chunking
- 🧠 Embeddings with `nomic-embed-text`
- 💾 ChromaDB Vector Store
- 🔍 Semantic Search
- 🤖 Llama 3.2 : 3B
- 🌐 Streamlit UI
- 📚 Document Summarization
- 💬 Question Answering

---

# 🖥️ Runtime Animation

```text
[██░░░░░░░░░░░░░░░░░░] 10%
📂 Loading Document...

[██████░░░░░░░░░░░░░] 30%
✂️ Splitting Text...

[██████████░░░░░░░░░] 50%
🧠 Generating Embeddings...

[██████████████░░░░░] 70%
💾 Building Vector Database...

[██████████████████░] 90%
🔍 Retrieving Context...

[████████████████████] 100%
🤖 Ready to Answer Questions
```

---

# 📂 Project Structure

```bash
rag-document-chatbot
│
├── app.py
├── ingest.py
├── summary.py
├── chat.py
├── chroma_db/
├── requirements.txt
└── README.md
```

---

<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=22&duration=2500&pause=1000&color=36BCF7&center=true&vCenter=true&width=600&lines=Powered+by+Llama+3.2;LangChain+%2B+ChromaDB+%2B+Ollama;Happy+Coding+🚀" />

</div>

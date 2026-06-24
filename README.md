# 📄 RAG Document Chatbot

```text
╔════════════════════════════════════════════╗
║          🚀 Starting RAG Engine            ║
╚════════════════════════════════════════════╝

[█░░░░░░░░░░░░░░░░░░░░] 5%
🔍 Scanning document...

[████░░░░░░░░░░░░░░░░░] 20%
📂 Loading PDF / DOCX / TXT...

[████████░░░░░░░░░░░░] 40%
✂️ Splitting into chunks...

[████████████░░░░░░░░] 60%
🧠 Generating embeddings...

[████████████████░░░░] 80%
💾 Building ChromaDB...

[████████████████████] 100%
🤖 Connecting to Llama 3.2:3B...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ System Ready
💬 Ask Anything About Your Document
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## ⚡ Workflow

```text
             📄 User Document
                      │
                      ▼
        ┌────────────────────────┐
        │   Document Loader      │
        └────────────────────────┘
                      │
                      ▼
        ┌────────────────────────┐
        │ Recursive Splitter ✂️  │
        └────────────────────────┘
                      │
                      ▼
        ┌────────────────────────┐
        │ nomic-embed-text 🧠    │
        └────────────────────────┘
                      │
                      ▼
        ┌────────────────────────┐
        │ ChromaDB Vector Store 💾│
        └────────────────────────┘
                      │
                      ▼
        ┌────────────────────────┐
        │ Retriever 🔍           │
        └────────────────────────┘
                      │
                      ▼
        ┌────────────────────────┐
        │ Llama 3.2:3B 🤖        │
        └────────────────────────┘
                      │
                      ▼
              💬 Intelligent Answer
```

---

## 🔄 Runtime Simulation

```text
> Initializing Project...
> Loading Models...
> Loading ChromaDB...
> Creating Embeddings...
> Retrieving Context...
> Sending Prompt to Llama 3.2...
> Generating Response...
> Done ✓
```

---

## 🎯 Features

```text
✓ PDF Support
✓ DOCX Support
✓ TXT Support
✓ CSV Support
✓ PPTX Support
✓ Semantic Search
✓ ChromaDB Vector Storage
✓ Ollama Integration
✓ Llama 3.2:3B
✓ Streamlit UI
✓ Detailed Summaries
✓ Document Question Answering
```

---

## 🗂 Project Structure

```text
ragtext/
│
├── 📄 app.py
├── 📄 ingest.py
├── 📄 summary.py
├── 📄 chat.py
├── 📁 chroma_db/
├── 📄 requirements.txt
└── 📄 README.md
```

---

```text
██████╗  █████╗  ██████╗
██╔══██╗██╔══██╗██╔════╝
██████╔╝███████║██║  ███╗
██╔══██╗██╔══██║██║   ██║
██║  ██║██║  ██║╚██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝

🤖 Retrieval Augmented Generation
📚 Powered by Llama 3.2:3B + ChromaDB + Ollama
```

import os
import tempfile
import base64
import streamlit as st

from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
    UnstructuredPowerPointLoader,
)
from langchain_core.documents.base import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM, OllamaEmbeddings


# ─────────────────────────────────────────
#  SUPPORTED FILE TYPES
# ─────────────────────────────────────────
TEXT_TYPES  = ["pdf", "csv", "docx", "txt", "md", "json", "xml",
               "html", "htm", "log", "py", "js", "ts", "java", "cpp", "c"]
EXCEL_TYPES = ["xlsx", "xls"]
PPT_TYPES   = ["pptx", "ppt"]
IMAGE_TYPES = ["png", "jpg", "jpeg", "webp", "bmp", "gif", "tiff"]
ALL_TYPES   = TEXT_TYPES + EXCEL_TYPES + PPT_TYPES + IMAGE_TYPES


# ─────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(page_title="Chat With Your Files", page_icon="📄", layout="wide")
st.title("📄 Chat With Your Files")


# ─────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────
for key, default in {
    "messages": [],
    "vectorstore": None,
    "last_uploaded_file": None,
    "file_type": None,
    "image_b64": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ─────────────────────────────────────────
#  HELPER: CHECK OLLAMA IS RUNNING
# ─────────────────────────────────────────
def check_ollama():
    """Returns True if Ollama is reachable, False otherwise."""
    try:
        import httpx
        r = httpx.get("http://localhost:11434", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def load_image_as_document(file_bytes, filename):
    """
    Sends image to llava (Ollama vision model) to get a text description,
    then wraps it as a LangChain Document so it can be embedded & queried.
    Falls back gracefully if llava is not installed.
    """
    import httpx

    b64 = base64.b64encode(file_bytes).decode("utf-8")
    payload = {
        "model": "llava",
        "messages": [{
            "role": "user",
            "content": (
                "Describe everything you see in this image in full detail. "
                "Include all visible text, numbers, objects, people, colors, layout, and any data."
            ),
            "images": [b64],
        }],
        "stream": False,
    }
    try:
        r = httpx.post("http://localhost:11434/api/chat", json=payload, timeout=60)
        description = r.json()["message"]["content"]
    except Exception:
        description = (
            f"[Image file: {filename}. Auto-description failed because the 'llava' "
            "model is not installed. Run:  ollama pull llava  then re-upload.]"
        )
    return [Document(page_content=description, metadata={"source": filename, "type": "image"})]


# ─────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.header("📂 Upload Any File")

    uploaded_file = st.file_uploader(
        "PDF, Word, Excel, PowerPoint, CSV, TXT, images, code files & more",
        type=ALL_TYPES,
    )

    if st.session_state.vectorstore is not None:
        if st.button("🔄 Upload New File"):
            st.session_state.vectorstore = None
            st.session_state.messages = []
            st.session_state.last_uploaded_file = None
            st.session_state.file_type = None
            st.session_state.image_b64 = None
            st.rerun()

    st.divider()
    with st.expander("📋 Supported file types"):
        st.caption("**Documents:** PDF, DOCX, TXT, MD, HTML, XML, JSON, LOG")
        st.caption("**Spreadsheets:** XLSX, XLS, CSV")
        st.caption("**Presentations:** PPTX, PPT")
        st.caption("**Images:** PNG, JPG, JPEG, WEBP, BMP, GIF, TIFF")
        st.caption("**Code:** PY, JS, TS, JAVA, CPP, C")
    st.divider()
    st.caption("🤖 Models used")
    st.caption("• Embeddings: nomic-embed-text")
    st.caption("• LLM: llama3.2:3b")
    st.caption("• Vision (images): llava")


# ─────────────────────────────────────────
#  PROCESS UPLOADED FILE
# ─────────────────────────────────────────
if (
    uploaded_file is not None
    and uploaded_file.name != st.session_state.last_uploaded_file
):
    # ── 1. Check Ollama is running ──────────────────────────
    if not check_ollama():
        st.error(
            "❌ **Ollama is not running.**\n\n"
            "Please open a terminal and run:\n"
            "```\nollama serve\n```\n"
            "Then refresh this page."
        )
        st.stop()

    # ── 2. Detect extension & file bytes ────────────────────
    ext = uploaded_file.name.split(".")[-1].lower()
    file_bytes = bytes(uploaded_file.getbuffer())
    documents = []

    # ── 3. Load based on type ────────────────────────────────
    with st.spinner(f"📖 Reading **{uploaded_file.name}**…"):

        if ext in IMAGE_TYPES:
            # Store base64 for preview
            st.session_state.image_b64 = base64.b64encode(file_bytes).decode("utf-8")
            st.session_state.file_type = "image"
            st.info("🖼️ Image detected — using llava vision model to extract content…")
            documents = load_image_as_document(file_bytes, uploaded_file.name)

        else:
            suffix = f".{ext}"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file_bytes)
                temp_path = tmp.name

            try:
                if ext == "pdf":
                    loader = PyPDFLoader(temp_path)
                elif ext == "csv":
                    loader = CSVLoader(temp_path)
                elif ext == "docx":
                    loader = Docx2txtLoader(temp_path)
                elif ext in EXCEL_TYPES:
                    loader = UnstructuredExcelLoader(temp_path)
                elif ext in PPT_TYPES:
                    loader = UnstructuredPowerPointLoader(temp_path)
                elif ext == "json":
                    with open(temp_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    documents = [Document(page_content=content, metadata={"source": uploaded_file.name})]
                else:
                    # TXT, MD, HTML, XML, code files, LOG …
                    loader = TextLoader(temp_path, encoding="utf-8", autodetect_encoding=True)

                if not documents:
                    documents = loader.load()

                st.session_state.file_type = ext

            except Exception as e:
                st.error(f"❌ Failed to read file: {e}")
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                st.stop()

            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)

    if not documents:
        st.error("❌ No content could be extracted. The file may be empty or corrupted.")
        st.stop()

    # ── 4. Split into chunks ─────────────────────────────────
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    docs = splitter.split_documents(documents)

    if not docs:
        st.error("❌ Document splitting produced no chunks. The file may be empty.")
        st.stop()

    # ── 5. Build embeddings — with a clear error if it fails ─
    with st.spinner("🔄 Generating embeddings (this may take a moment)…"):
        try:
            embeddings = OllamaEmbeddings(model="nomic-embed-text")

            # ★ KEY FIX: test the embedding model BEFORE calling Chroma
            test_vec = embeddings.embed_query("test")
            if not test_vec:
                st.error(
                    "❌ The embedding model returned an empty vector.\n\n"
                    "Make sure `nomic-embed-text` is pulled:\n"
                    "```\nollama pull nomic-embed-text\n```"
                )
                st.stop()

        except Exception as e:
            st.error(
                f"❌ Embedding model error: {e}\n\n"
                "Run in terminal:\n"
                "```\nollama pull nomic-embed-text\n```"
            )
            st.stop()

    # ── 6. Build Chroma vectorstore ──────────────────────────
    with st.spinner("📦 Building vector store…"):
        try:
            vectorstore = Chroma.from_documents(
                documents=docs,
                embedding=embeddings,
            )
        except Exception as e:
            st.error(f"❌ Vector store creation failed: {e}")
            st.stop()

    st.session_state.vectorstore = vectorstore
    st.session_state.last_uploaded_file = uploaded_file.name
    st.session_state.messages = []
    st.success(f"✅ **{uploaded_file.name}** ready — {len(docs)} chunks indexed.")


# ─────────────────────────────────────────
#  IMAGE PREVIEW
# ─────────────────────────────────────────
if st.session_state.file_type == "image" and st.session_state.image_b64:
    with st.expander("🖼️ Uploaded Image Preview", expanded=True):
        st.image(base64.b64decode(st.session_state.image_b64), use_container_width=True)


# ─────────────────────────────────────────
#  DISPLAY CHAT HISTORY
# ─────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ─────────────────────────────────────────
#  CHAT INPUT
# ─────────────────────────────────────────
question = st.chat_input("Ask a question about your document…")

if question:

    # Save & show user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # ── Guard: no document uploaded yet ─────────────────────
    if st.session_state.vectorstore is None:
        response = "⚠️ Please upload a document first using the sidebar."

    else:
        # ── Retrieve relevant chunks ─────────────────────────
        retriever = st.session_state.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5},
        )

        try:
            retrieved_docs = retriever.invoke(question)
        except Exception as e:
            retrieved_docs = []
            st.warning(f"Retrieval error: {e}")

        context = "\n\n".join(doc.page_content for doc in retrieved_docs)

        # ── Build prompt ─────────────────────────────────────
        file_label = st.session_state.last_uploaded_file or "the uploaded file"
        prompt = f"""You are a helpful assistant. Answer the user's question using ONLY the content from "{file_label}".

RULES:
- Answer ONLY using the context provided below.
- Do NOT use outside knowledge or assumptions.
- Be direct and complete.
- If the answer is not in the context, say exactly:
  "This information is not available in the uploaded file."

Context:
{context}

Question: {question}

Answer:"""

        # ── Call LLM ─────────────────────────────────────────
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    llm = OllamaLLM(model="llama3.2:3b")
                    response = llm.invoke(prompt)
                except Exception as e:
                    response = (
                        f"❌ LLM error: {e}\n\n"
                        "Make sure `llama3.2:3b` is pulled:\n"
                        "```\nollama pull llama3.2:3b\n```"
                    )
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        # Early return since we already rendered the message above
        st.stop()

    # Fallback render (for the "no document" case)
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
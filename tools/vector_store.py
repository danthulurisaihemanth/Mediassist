# tools/vector_store.py
import os
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from .pdf_loader import load_pdf_documents

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

DATA_DIR = PROJECT_ROOT / "data"
VECTOR_DB_DIR = PROJECT_ROOT / "medical_db"
PDF_PATH = DATA_DIR / "medical_book.pdf"

_embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

_vectorstore = None

def initialize_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(VECTOR_DB_DIR, exist_ok=True)

        if not PDF_PATH.exists():
            raise FileNotFoundError(f"PDF file not found at {PDF_PATH}")

        # Load documents
        doc_splits = load_pdf_documents(str(PDF_PATH))

        if len(doc_splits) == 0:
            raise Exception("No documents after splitting. Cannot create vector DB.")

        print("Creating Chroma DB with documents:", len(doc_splits))

        _vectorstore = Chroma.from_documents(
            documents=doc_splits,
            embedding=_embeddings,
            persist_directory=str(VECTOR_DB_DIR)
        )

        print("Vector DB created successfully!")

    return _vectorstore


def get_retriever():
    if _vectorstore is None:
        initialize_vectorstore()
    return _vectorstore.as_retriever(search_kwargs={"k": 3})

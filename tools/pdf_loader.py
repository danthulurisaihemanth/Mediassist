# tools/pdf_loader.py
from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdf_documents(file_path: str):
    print("Loading PDF from:", file_path)
    
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    print("Pages loaded:", len(docs))

    if len(docs) == 0:
        raise Exception("PDF loaded 0 pages. File is scanned, encrypted, or corrupted.")

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512,
        chunk_overlap=128,
        separators=["\n\n", ". ", "\n", " "]
    )

    splits = text_splitter.split_documents(docs)
    print("Chunks created:", len(splits))

    return splits

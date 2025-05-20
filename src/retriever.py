import hashlib
import re

from pathlib import Path

from db import insert_document, insert_chunks, get_existing_hashes
from config import EMBED_MODEL_NAME
from langchain.schema import Document


def hash_file(file_path):
    return hashlib.md5(Path(file_path).read_bytes()).hexdigest()


def chunk_documents(data_dir, split_func):
    """
    Chunk documents and track metadata in SQLite, returning 
    a list of LangChain Document objects
    with embedded metadata for FAISS indexing.
    """
    docs = []
    existing_hashes = get_existing_hashes()

    for path in Path(data_dir).rglob("*"):
        if not path.is_file():
            continue

        file_hash = hash_file(path)
        if file_hash in existing_hashes:
            print(f"[SKIP] Already indexed: {path}")
            continue

        try:
            text = path.read_text(errors="ignore")
        except Exception as e:
            print(f"[ERROR] Cannot read file {path}: {e}")
            continue

        chunks = split_func(text)
        print(f"[INFO] Indexed: {path} | Chunks: {len(chunks)}")

        # Insert document metadata and chunks into SQLite
        doc_id = insert_document(
            str(path), path.stem, file_hash, path.suffix[1:], EMBED_MODEL_NAME
        )
        insert_chunks(doc_id, chunks)

        # Build LangChain Document objects with metadata for FAISS
        def is_trash(chunk: str) -> bool:
            chunk = chunk.strip()
            if len(chunk) < 10:
                return True
            total_chars = len(chunk)
            if total_chars == 0:
                return True
            alnum_chars = len(re.findall(r'\w', chunk))
            ratio = alnum_chars / total_chars
            if ratio < 0.7:
                return True
            return False

        # Usage example inside your chunking loop:
        for idx, (chunk, page_num) in enumerate(chunks):
            chunk = ' '.join(chunk.split())  # normalize spaces
            if is_trash(chunk):
                print(f"[FILTERED] Trash chunk skipped: {chunk[:50]}...")
                continue
            docs.append(Document(
                page_content=chunk,
                metadata={
                    "doc_id": doc_id,
                    "path": str(path),
                    "title": path.stem,
                    "chunk_index": idx,
                    "page": page_num
                }
            ))

    return docs

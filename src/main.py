__author__ = "https://github.com/lp-hub/localRAGSQLite.git"

import os

from langchain_huggingface import HuggingFaceEmbeddings

from config import EMBED_MODEL_NAME
from llm import run_rag, parse_args
from logger import log_exception
from retriever import chunk_documents
from store import create_vector_store, load_vector_store
from utils import split_into_chunks

# === Main Script Execution ===

def setup_retriever():
    args = parse_args()
    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    print("Embedding dimension:", len(embedding.embed_query("test")))

    if args.rebuild_db or not os.path.exists(os.path.join(args.db_dir, "index.faiss")):
        chunks = chunk_documents(args.data_dir, split_into_chunks)
        return create_vector_store(args.db_dir, chunks, embedding)
    else:
        return load_vector_store(args.db_dir, embedding)

def setup_retriever():
    args = parse_args()
    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    print("Embedding dimension:", len(embedding.embed_query("test")))

    if args.rebuild_db or not os.path.exists(os.path.join(args.db_dir, "index.faiss")):
        chunks = chunk_documents(args.data_dir, split_into_chunks)
        return create_vector_store(args.db_dir, chunks, embedding)
    else:
        return load_vector_store(args.db_dir, embedding)

def main():
    global retriever
    args = parse_args()
    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    print("Embedding dimension:", len(embedding.embed_query("test")))

    # Decide whether to rebuild or load vector store index
    if args.rebuild_db or not os.path.exists(os.path.join(args.db_dir, "index.faiss")):
        chunks = chunk_documents(args.data_dir, split_into_chunks)
        retriever = create_vector_store(args.db_dir, chunks, embedding)
    else:
        retriever = load_vector_store(args.db_dir, embedding)

    print("Interactive RAG CLI started. Type 'exit' to quit.")

    while True:
        query = input("\nYou: ")
        if query.lower() in {"exit", "quit"}:
            print("Exiting.")
            break

        try:
            sources, response = run_rag(query, retriever, args.model_path)
            print("\nSources:\n", sources)
            print("\nAssistant:\n", response)
        except Exception as e:
            log_exception("Error during RAG pipeline", e, context=query)
    return retriever

if __name__ == "__main__":
    main()
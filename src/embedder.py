from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Dict

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "pdf_rag"


def get_embedder():
    """Load the sentence transformer model."""
    print(f"Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    return model


def get_chroma_client(persist_dir: str = "data/vector_store"):
    """Create a persistent ChromaDB client."""
    client = chromadb.PersistentClient(path=persist_dir)
    return client


def build_index(chunks: List[Dict], persist_dir: str = "data/vector_store"):
    """Embed all chunks and store them in ChromaDB."""
    model = get_embedder()
    client = get_chroma_client(persist_dir)

    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)
        print("Deleted existing collection.")

    collection = client.create_collection(COLLECTION_NAME)

    # Clean: remove any chunks with empty or non-string text
    chunks = [c for c in chunks if isinstance(c["text"], str) and c["text"].strip()]
    print(f"Clean chunks to embed: {len(chunks)}")

    texts = [chunk["text"].strip() for chunk in chunks]
    ids = [chunk["chunk_id"] for chunk in chunks]
    metadatas = [{"page_num": chunk["page_num"]} for chunk in chunks]

    print(f"Embedding {len(texts)} chunks... (this may take a minute)")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32).tolist()

    batch_size = 100
    for i in range(0, len(texts), batch_size):
        collection.add(
            ids=ids[i:i+batch_size],
            documents=texts[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size]
        )
        print(f"Indexed batch {i//batch_size + 1}")

    print(f"Successfully indexed {len(texts)} chunks into ChromaDB.")
    return collection

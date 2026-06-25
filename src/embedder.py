from sentence_transformers import SentenceTransformer
from typing import List, Dict

from src.vector_store import get_connection, init_schema, clear_index, insert_chunks

MODEL_NAME = "all-MiniLM-L6-v2"


def get_embedder():
    """Load the sentence transformer model."""
    print(f"Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    return model


def build_index(chunks: List[Dict]):
    """Embed all chunks and store them in PostgreSQL with pgvector."""
    model = get_embedder()
    conn = get_connection()
    init_schema(conn)
    clear_index(conn)
    print("Cleared existing index.")

    chunks = [c for c in chunks if isinstance(c["text"], str) and c["text"].strip()]
    print(f"Clean chunks to embed: {len(chunks)}")

    texts = [chunk["text"].strip() for chunk in chunks]
    ids = [chunk["chunk_id"] for chunk in chunks]
    metadatas = [{"page_num": chunk["page_num"]} for chunk in chunks]

    print(f"Embedding {len(texts)} chunks... (this may take a minute)")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32).tolist()

    batch_size = 100
    for i in range(0, len(texts), batch_size):
        insert_chunks(
            conn,
            ids[i : i + batch_size],
            texts[i : i + batch_size],
            metadatas[i : i + batch_size],
            embeddings[i : i + batch_size],
        )
        print(f"Indexed batch {i // batch_size + 1}")

    print(f"Successfully indexed {len(texts)} chunks into PostgreSQL.")
    conn.close()
    return conn

from sentence_transformers import SentenceTransformer
from typing import List, Dict

from src.vector_store import get_connection, init_schema, count_chunks, search


def load_collection():
    """Connect to PostgreSQL and verify the vector index exists."""
    conn = get_connection()
    init_schema(conn)
    print(f"Loaded index with {count_chunks(conn)} chunks.")
    return conn


def retrieve(query: str, collection, model: SentenceTransformer, top_k: int = 5) -> List[Dict]:
    """Embed the query and retrieve the top-k most relevant chunks."""
    query_embedding = model.encode([query]).tolist()[0]
    return search(collection, query_embedding, top_k=top_k)

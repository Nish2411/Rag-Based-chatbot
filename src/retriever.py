from sentence_transformers import SentenceTransformer
import chromadb
from typing import List,Dict
from src.embedder import MODEL_NAME, COLLECTION_NAME, get_chroma_client


def load_collection(persist_dir: str = "data/vector_store"):
    """Load the existing ChromaDB collection."""
    client = get_chroma_client()
    collection = client.get_collection(COLLECTION_NAME)
    print(f"Loaded collection with {collection.count()} chunks.")
    return collection

def retrieve(query: str, collection, model: SentenceTransformer, top_k: int = 5) -> List[Dict]:
    """Embed the query and retrieve the top -k most relevant chunks."""
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "page_num": results["metadatas"][0][i]["page_num"],
            "score": round(1 - results["distances"][0][i], 4)

        })

    return chunks
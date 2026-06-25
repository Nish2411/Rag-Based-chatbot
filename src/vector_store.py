import os
from typing import List, Dict, Any

import psycopg
from psycopg import sql
from dotenv import load_dotenv
from pgvector.psycopg import register_vector

load_dotenv()

TABLE_NAME = "pdf_chunks"
EMBEDDING_DIM = 384  # all-MiniLM-L6-v2


def get_database_url() -> str:
    return os.getenv(
        "DATABASE_URL",
        "postgresql://raguser:ragpassword@localhost:5433/ragdb",
    )


def get_connection():
    """Open a PostgreSQL connection with pgvector types registered."""
    conn = psycopg.connect(get_database_url())
    register_vector(conn)
    return conn


def init_schema(conn) -> None:
    """Create the chunks table and vector index if they do not exist."""
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                chunk_id TEXT PRIMARY KEY,
                document TEXT NOT NULL,
                page_num INTEGER NOT NULL,
                embedding vector({EMBEDDING_DIM}) NOT NULL
            )
            """
        )
        cur.execute(
            sql.SQL("""
            CREATE INDEX IF NOT EXISTS pdf_chunks_embedding_idx
            ON {}
            USING hnsw (embedding vector_cosine_ops)
            """).format(sql.Identifier(TABLE_NAME))
        )
    conn.commit()


def clear_index(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(sql.SQL("TRUNCATE TABLE {}").format(sql.Identifier(TABLE_NAME)))
    conn.commit()


def insert_chunks(
    conn,
    ids: List[str],
    documents: List[str],
    metadatas: List[Dict[str, Any]],
    embeddings: List[List[float]],
    batch_size: int = 100,
) -> None:
    rows = [
        (chunk_id, doc, meta["page_num"], embedding)
        for chunk_id, doc, meta, embedding in zip(ids, documents, metadatas, embeddings)
    ]
    with conn.cursor() as cur:
        for i in range(0, len(rows), batch_size):
            batch = rows[i : i + batch_size]
            cur.executemany(
                sql.SQL("""
                INSERT INTO {} (chunk_id, document, page_num, embedding)
                VALUES (%s, %s, %s, %s)
                """).format(sql.Identifier(TABLE_NAME)),
                batch,
            )
    conn.commit()


def count_chunks(conn) -> int:
    with conn.cursor() as cur:
        cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(TABLE_NAME)))
        return cur.fetchone()[0]


def search(conn, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL("""
            SELECT document, page_num, 1 - (embedding <=> %s::vector) AS score
            FROM {}
            ORDER BY embedding <=> %s::vector
            LIMIT %s
            """).format(sql.Identifier(TABLE_NAME)),
            (query_embedding, query_embedding, top_k),
        )
        rows = cur.fetchall()

    return [
        {"text": row[0], "page_num": row[1], "score": round(float(row[2]), 4)}
        for row in rows
    ]

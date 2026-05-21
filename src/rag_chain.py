import google.generativeai as genai
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_MODEL = "gemini-2.5-flash"


def setup_gemini():
    """Configure Gemini with API key."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(GEMINI_MODEL)
    return model


def build_prompt(query: str, chunks: List[Dict]) -> str:
    """Build a RAG prompt from the query and retrieved chunks."""
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"[Chunk {i+1} | Page {chunk['page_num']}]\n{chunk['text']}\n\n"

    prompt = f"""You are a helpful and friendly AI assistant with two jobs:

1. If the question is related to the PDF document, answer using the CONTEXT below and mention the page number(s).
2. If the question is a general question not related to the document (e.g. greetings, general knowledge, math, coding), answer it using your own knowledge naturally without mentioning the document.

CONTEXT FROM DOCUMENT:
{context}

QUESTION:
{query}

INSTRUCTIONS:
- For document questions: cite the page number(s) in your answer.
- For general questions: just answer naturally and helpfully, no need to mention the document.
- Never say "I couldn't find that in the document" for general knowledge questions.
- Keep answers concise and clear.

ANSWER:"""
    return prompt


def ask(query: str, chunks: List[Dict], gemini_model) -> str:
    """Send the RAG prompt to Gemini and return the response."""
    prompt = build_prompt(query, chunks)
    response = gemini_model.generate_content(prompt)
    return response.text


def rag_answer(query: str, collection, embedder, gemini_model, top_k: int = 5) -> Dict:
    """Full RAG pipeline: retrieve chunks then generate answer."""
    from src.retriever import retrieve

    chunks = retrieve(query, collection, embedder, top_k=top_k)
    answer = ask(query, chunks, gemini_model)

    return {
        "query": query,
        "answer": answer,
        "sources": [{"page": c["page_num"], "score": c["score"]} for c in chunks]
    }

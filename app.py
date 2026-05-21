import streamlit as st
from src.pdf_loader import load_pdf, chunk_pages
from src.embedder import get_embedder, build_index
from src.retriever import load_collection
from src.rag_chain import setup_gemini, rag_answer
import os

st.set_page_config(
    page_title="Deep Learning PDF Chatbot",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Deep Learning PDF Chatbot")
st.caption("Powered by RAG + Gemini 2.5 Flash")

# ── Initialize everything once and cache it ──
@st.cache_resource
def load_resources():
    embedder = get_embedder()
    collection = load_collection()
    gemini = setup_gemini()
    return embedder, collection, gemini

with st.spinner("Loading models and index..."):
    embedder, collection, gemini = load_resources()

st.success("Ready! Ask me anything about the Deep Learning PDF.", icon="✅")
st.divider()

# ── Chat history ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            with st.expander("📄 Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- Page **{s['page']}** — relevance score: `{s['score']}`")

# ── Chat input ──
if query := st.chat_input("Ask a question about Deep Learning..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = rag_answer(query, collection, embedder, gemini)

        st.markdown(result["answer"])

        with st.expander("📄 Sources"):
            for s in result["sources"]:
                st.markdown(f"- Page **{s['page']}** — relevance score: `{s['score']}`")

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["sources"]
    })

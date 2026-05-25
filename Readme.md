# PDF-RAG-CHATBOT

A **Retrieval-Augmented Generation (RAG)** chatbot that lets users chat with the PDF *"Introduction to Deep Learning"* using local embeddings and Google's Gemini model.

## Features

- Extracts and chunks text from 'IntroToDeepLearning.pdf'
- Uses 'all-MiniLM-L6-v2' for embeddings
-Store vectors in **ChromaDB** (persistent)
- Retrieves relevant chunks for user queries
- Powered by **Gemini 2.5 Flash** for high-quality answers
- Clean **Streamlit** UI
- Returns page citations when answering from the document

## Tech Stack
Frontend: Streamlit

Embeddings: sentence-transformers (all-MiniLM-L6-v2)

Vector Store: ChromaDB

LLM: Gemini 2.5 Flash

PDF Processing: PyPDF2 / pdfminer

## How to Run

1. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```


2. **Ingest the PDF (Run once)**
    ```bash
    python ingest.py
    ```

3. **Start the chatbot**
    ```bash
    streamlit run app.py
    ```


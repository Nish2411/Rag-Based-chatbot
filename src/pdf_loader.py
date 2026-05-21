from pypdf import PdfReader
from typing import List, Dict


def load_pdf(pdf_path: str) -> List[Dict]:
    """Extract text from each page of the PDF."""
    reader = PdfReader(pdf_path)
    pages = []

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            pages.append({
                "page_num": page_num + 1,
                "text": text.strip()
            })

    print(f"Loaded {len(pages)} pages from '{pdf_path}'")
    return pages


def chunk_pages(pages: List[Dict], chunk_size: int = 500, overlap: int = 100) -> List[Dict]:
    """Split pages into overlapping chunks for better retrieval."""
    chunks = []

    for page in pages:
        text = page["text"]
        words = text.split()

        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk_text = " ".join(words[start:end])

            chunks.append({
                "text": chunk_text,
                "page_num": page["page_num"],
                "chunk_id": f"page{page['page_num']}_chunk{len(chunks)}"
            })

            start += chunk_size - overlap

    print(f"Created {len(chunks)} chunks from {len(pages)} pages")
    return chunks

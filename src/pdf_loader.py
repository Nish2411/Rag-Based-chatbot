from pypdf import PdfReader
from typing import List, Dict
import re


def clean_text(text: str) -> str:
    """Remove broken unicode surrogates and clean up text."""
    # Remove lone surrogates (broken emojis like \ud83d)
    text = text.encode('utf-16', 'surrogatepass').decode('utf-16', 'ignore')
    # Remove non-printable characters except newlines and spaces
    text = re.sub(r'[^\x20-\x7E\n\t]', ' ', text)
    # Collapse multiple spaces
    text = re.sub(r' +', ' ', text)
    return text.strip()


def load_pdf(pdf_path: str) -> List[Dict]:
    """Extract text from each page of the PDF."""
    reader = PdfReader(pdf_path)
    pages = []

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            pages.append({
                "page_num": page_num + 1,
                "text": clean_text(text)
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

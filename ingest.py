import os
from src.pdf_loader import load_pdf, chunk_pages
from src.embedder import build_index

PDF_PATH = "data/IntroToDeepLearning.pdf"

def main():
    if not os.path.exists(PDF_PATH):
        print(f"ERROR: PDF not found at '{PDF_PATH}'")
        return

    print("Step 1: Loading and chunking PDF...")
    pages = load_pdf(PDF_PATH)
    chunks = chunk_pages(pages)

    print("\nStep 2: Building ChromaDB index...")
    build_index(chunks)

    print("\nIngest complete! You can now run the chatbot with: streamlit run app.py")

if __name__ == "__main__":
    main()

from app.document_loader import load_pdf
from app.chunker import chunk_text

text = load_pdf("data/raw/NVIDIA-2025-Annual-Report.pdf")

chunks = chunk_text(text)

print("Total chunks:", len(chunks))

print(chunks[0])
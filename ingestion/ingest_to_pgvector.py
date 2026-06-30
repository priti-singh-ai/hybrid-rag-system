import sys
from pathlib import Path
sys.path.insert(0,'C:/Users/priti.kumari/Downloads/My_learning/hybrid-rag-system')
from ingestion.document_loader import load_pdf
from ingestion.chunker import chunk_text
from ingestion.embedding import get_embeddings
from database.db_connect import get_connection

print("Loading documents...")

pdf_folder = Path("data/raw")

all_chunks = []

for pdf_file in pdf_folder.glob("*.pdf"):

    print(f"Loading {pdf_file.name}")

    document = load_pdf(pdf_file)

    chunks = chunk_text(document)

    print(f"Created {len(chunks)} chunks")

    for chunk in chunks:
        all_chunks.append(
            (
                pdf_file.name,
                chunk
            )
        )

chunk_texts = [chunk for _, chunk in all_chunks]

embeddings = get_embeddings(chunk_texts)

conn = get_connection()

cursor = conn.cursor()

for (source_file, chunk), embedding in zip(all_chunks, embeddings):

    cursor.execute(
        """
        INSERT INTO nvidia_documents
        (
            source_file,
            chunk_text,
            embedding
        )
        VALUES
        (%s,%s,%s)
        """,
        (
        source_file,
        chunk,
        embedding
        )
    )

conn.commit()

cursor.close()
conn.close()

print(f"Inserted {len(chunks)} chunks")
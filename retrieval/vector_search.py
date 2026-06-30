from pathlib import Path
from pypdf import PdfReader
from ingestion.embedding import get_embeddings
from database.db_connect import get_connection


class VectorSearch:
    """
    Handles document loading and vector similarity search.
    """

    def __init__(self, data_dir="data/raw"):
        self.data_dir = Path(data_dir)

    def load_all_documents(self):
        documents = []

        for file_path in self.data_dir.rglob("*"):

            if not file_path.is_file():
                continue

            try:
                if file_path.suffix.lower() == ".pdf":

                    reader = PdfReader(file_path)

                    text = ""

                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"

                elif file_path.suffix.lower() == ".txt":

                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()

                else:
                    continue

                documents.append(
                    {
                        "source": file_path.name,
                        "path": str(file_path),
                        "text": text
                    }
                )

            except Exception as e:
                print(f"Skipping {file_path}: {e}")

        print(f"Loaded {len(documents)} documents.")
        return documents

    def generate_query_embedding(self, query: str):

        return get_embeddings([query])[0]

    def search(self, query: str, top_k: int = 5):

        query_embedding = self.generate_query_embedding(query)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                source_file,
                chunk_text,
                embedding <=> %s::vector AS distance
            FROM nvidia_documents
            ORDER BY distance
            LIMIT %s
            """,
            (query_embedding, top_k)
        )

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return [
            {
                "source": row[0],
                "text": row[1],
                "score": row[2]
            }
            for row in results
              ]


if __name__ == "__main__":

    vector_search = VectorSearch("data/raw")

    documents = vector_search.load_all_documents()

    print(f"Loaded {len(documents)} documents.\n")

    results = vector_search.search(
        "What does NVIDIA say about artificial intelligence?"
    )

    for idx, (source, chunk, distance) in enumerate(results, start=1):

        print("=" * 80)
        print(f"Rank: {idx}")
        print(f"Source: {source}")
        print(f"Distance: {distance:.4f}")
        print(chunk[:500])
        print()
# def search_documents(query, top_k=5):

#     print("Generating query embedding...")

#     query_embedding = get_embeddings([query])[0]

#     conn = get_connection()

#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         SELECT
#             source_file,
#             chunk_text,
#             embedding <=> %s::vector AS distance
#         FROM nvidia_documents
#         ORDER BY distance
#         LIMIT %s
#         """,
#         (
#             query_embedding,
#             top_k
#         )
#     )

#     results = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     return results


# if __name__ == "__main__":

#     query = "What does NVIDIA say about artificial intelligence?"

#     results = search_documents(query)

#     print("\nTop Results:\n")

#     for idx, row in enumerate(results, start=1):

#         source_file = row[0]
#         chunk_text = row[1]
#         distance = row[2]

#         print("=" * 80)

#         print(f"Rank: {idx}")
#         print(f"Source: {source_file}")
#         print(f"Distance: {distance}")

#         print("\nChunk:\n")

#         print(chunk_text[:1000])

#         print("\n")
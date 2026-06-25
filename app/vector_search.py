from app.embedding import get_embeddings
from app.db_connect import get_connection


def search_documents(query, top_k=5):

    print("Generating query embedding...")

    query_embedding = get_embeddings([query])[0]

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
        (
            query_embedding,
            top_k
        )
    )

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results


if __name__ == "__main__":

    query = "What does NVIDIA say about artificial intelligence?"

    results = search_documents(query)

    print("\nTop Results:\n")

    for idx, row in enumerate(results, start=1):

        source_file = row[0]
        chunk_text = row[1]
        distance = row[2]

        print("=" * 80)

        print(f"Rank: {idx}")
        print(f"Source: {source_file}")
        print(f"Distance: {distance}")

        print("\nChunk:\n")

        print(chunk_text[:1000])

        print("\n")
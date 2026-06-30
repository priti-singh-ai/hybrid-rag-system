import sys
sys.path.insert(0,'C:/Users/priti.kumari/Downloads/My_learning/hybrid-rag-system')
from retrieval.vector_search import search_documents

query = "What does NVIDIA say about artificial intelligence?"

results = search_documents(query, top_k=3)

for idx, row in enumerate(results):

    print("\n")
    print("=" * 80)

    print(f"Rank {idx+1}")
    print(f"Distance: {row[2]}")

    print("\nChunk Preview:\n")

    print(row[1][:1000])
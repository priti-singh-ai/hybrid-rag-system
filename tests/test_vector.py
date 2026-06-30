import sys
sys.path.insert(0,'C:/Users/priti.kumari/Downloads/My_learning/hybrid-rag-system')
from retrieval.vector_search import VectorSearch

vector = VectorSearch()

query = "What is CUDA?"

results = vector.search(query)

for i, result in enumerate(results):

    print("="*80)

    print(f"Result {i+1}")

    print(result)
import sys
sys.path.insert(0,'C:/Users/priti.kumari/Downloads/My_learning/hybrid-rag-system')

from retrieval.hybrid_retriever import HybridRetriever

hybrid = HybridRetriever()

results = hybrid.search(
    "What products does NVIDIA build?"
)

for r in results:

    print(r)
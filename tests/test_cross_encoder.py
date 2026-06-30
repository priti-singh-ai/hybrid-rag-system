from retrieval.hybrid_retriever import HybridRetriever
from reranking.reranker import Reranker

hybrid = HybridRetriever()

reranker = Reranker()

query = "What is CUDA?"

results = hybrid.search(query)

reranked = reranker.rerank(query, results)

for r in reranked:

    print("="*80)

    print(r)
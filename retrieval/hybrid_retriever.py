from retrieval.vector_search import VectorSearch
from retrieval.bm25_search import BM25Retriever


class HybridRetriever:

    def __init__(self):

        self.vector = VectorSearch()

        self.documents = self.vector.load_all_documents()
        print(f"Number of loaded documents: {len(self.documents)}")

        self.bm25 = BM25Retriever(self.documents)

    def search(self, query):
        
        vector_results = self.vector.search(query)

        bm25_results = self.bm25.search(query)

        combined = vector_results

        for doc in bm25_results:

            if doc not in combined:

                combined.append(doc)

        return combined
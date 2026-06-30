from rank_bm25 import BM25Okapi
import numpy as np


class BM25Retriever:

    def __init__(self, documents):

        self.documents = documents

        tokenized_docs = [
            doc["text"].split()
            for doc in documents
        ]

        self.bm25 = BM25Okapi(tokenized_docs)

    def search(self, query, top_k=5):

        tokenized_query = query.split()

        # Get BM25 score for every document
        scores = self.bm25.get_scores(tokenized_query)

        # Get indices of the top-k highest scores
        top_indices = np.argsort(scores)[::-1][:top_k]

        # Return the original document dictionaries
        return [
            self.documents[i]
            for i in top_indices
        ]
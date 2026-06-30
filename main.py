import time

from retrieval.metadata_filter import filter_documents
from reranking.reranker import Reranker
from retrieval.hybrid_retriever import HybridRetriever
from generation.llm import generate_answer
from app.memory import memory


hybrid = HybridRetriever()
reranker = Reranker()


def ask_question(query):

    start_time = time.time()

    # Retrieval
    results = hybrid.search(query)

    # Metadata filtering
    filtered = filter_documents(results, "2025")

    # Cross Encoder
    reranked = reranker.rerank(query, filtered)

    # Context
    context = "\n\n".join(
        doc["text"] for doc in reranked[:5]
    )

    # Memory
    history = memory.load_memory_variables({})

    # LLM
    answer = generate_answer(
        query,
        context,
        history
    )

    memory.save_context(
        {"input": query},
        {"output": answer}
    )

    latency = time.time() - start_time

    return {
        "answer": answer,
        "latency": round(latency,2)
    }
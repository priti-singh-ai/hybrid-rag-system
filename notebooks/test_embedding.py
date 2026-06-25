import sys
sys.path.insert(0,'C:/Users/priti.kumari/Downloads/My_learning/hybrid-rag-system')
from app.embedding import *
from test_ingestion import *

from sklearn.metrics.pairwise import cosine_similarity

chunks[:5]
embeddings = get_embeddings(chunks)
len(embeddings)
embeddings[0].shape

similarity = cosine_similarity(
    [embeddings[0]],
    [embeddings[1]]
)
print(type(chunks))
print(len(chunks))
print(chunks[0][:500])
print(type(embeddings))
print(embeddings.shape)
print(len(embeddings[0]))
print(similarity)
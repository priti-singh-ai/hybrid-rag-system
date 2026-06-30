import os

DB_NAME = os.getenv("POSTGRES_DB", "ragdb")
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin123")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

TOP_K = 5
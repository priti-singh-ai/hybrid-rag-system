import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="vectordb",
    user="admin",
    password="admin"
)

print("Connected to PGVector!")

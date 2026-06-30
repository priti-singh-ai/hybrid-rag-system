from db_connect import get_connection

conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
CREATE EXTENSION IF NOT EXISTS vector;
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS nvidia_documents (

    id SERIAL PRIMARY KEY,

    source_file TEXT,

    chunk_text TEXT,

    embedding VECTOR(384)

);
""")

conn.commit()

cursor.close()
conn.close()

print("Table Created Successfully")
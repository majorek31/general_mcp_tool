import sqlite3

db_path = 'src/tools/embeddings.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM embeddings")
count = cursor.fetchone()[0]
print(f'Embedding count: {count}')

cursor.execute("SELECT tool_name FROM embeddings")
tools = [row[0] for row in cursor.fetchall()]
print(f'Sample tools: {tools}')


conn.close()

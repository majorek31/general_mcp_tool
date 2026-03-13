from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

embeddings = OllamaEmbeddings(
    base_url="http://172.27.80.1:11434/",
    model="qwen3-embedding:4b",
)

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="my_docs",
    connection="postgresql+psycopg://postgres:postgres@localhost:5432/postgres",
)

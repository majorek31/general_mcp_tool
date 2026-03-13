import inspect
import json
from math import sqrt
from urllib import request
import tools as tools_module
from embedding_db import EmbeddingDatabase

class ToolDiscoveryService:
    EMBEDDING_MODEL = "qwen3-embedding:4b"
    EMBEDDING_BASE_URL = "http://172.30.144.1:11434"
    MIN_SCORE = 0.5
    
    def __init__(self, db_path: str = "embeddings.db"):
        self._entries = []
        self._db = EmbeddingDatabase(db_path)

    @staticmethod
    def _cosine_similarity(vec_a, vec_b):
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return -1.0
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        mag_a = sqrt(sum(a * a for a in vec_a))
        mag_b = sqrt(sum(b * b for b in vec_b))
        return -1.0 if mag_a == 0 or mag_b == 0 else dot_product / (mag_a * mag_b)

    def generate_embedding(self, text):
        try:
            body = json.dumps({"model": self.EMBEDDING_MODEL, "prompt": text}).encode()
            req = request.Request(
                f"{self.EMBEDDING_BASE_URL}/api/embeddings",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            response = request.urlopen(req, timeout=30)
            return json.loads(response.read()).get("embedding")
        except Exception:
            return None

    def register_tool(self, tool_func):
        embedding = self._db.load_embedding(tool_func.name)
        
        if embedding is None:
            embedding = self.generate_embedding(tool_func.name)
            if embedding:
                self._db.save_embedding(tool_func.name, embedding)
        
        self._entries.append((tool_func, embedding))

    def register_tools_from_module(self, module):
        for _, obj in inspect.getmembers(module):
            if getattr(obj, "name", None) and hasattr(obj, "invoke"):
                self.register_tool(obj)

    def find_tool(self, query):
        query_embedding = self.generate_embedding(query)
        if not query_embedding:
            return None

        best_tool = None
        best_score = -1.0
        for tool_func, embedding in self._entries:
            score = self._cosine_similarity(query_embedding, embedding)
            if score > best_score:
                best_score = score
                best_tool = tool_func

        return best_tool if best_score >= self.MIN_SCORE else None


tool_discovery_service = ToolDiscoveryService()
tool_discovery_service.register_tools_from_module(tools_module)
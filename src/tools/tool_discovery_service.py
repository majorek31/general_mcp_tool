from dataclasses import dataclass
from math import sqrt
from typing import Iterable
from langchain_core.tools import BaseTool
from langchain_ollama import OllamaEmbeddings

@dataclass
class ToolScore:
	tool: BaseTool
	score: float

class ToolDiscoveryService:
	"""Find the most relevant tools for a task using semantic similarity."""

	def __init__(self) -> None:
		self.embedding_model = "qwen3-embedding:0.6b"
		self.base_url = "http://172.30.144.1:11434"
		self.embedding_client = OllamaEmbeddings(
			model=self.embedding_model,
			base_url=self.base_url,
		)

		self._indexed_tools: list[BaseTool] = []
		self._indexed_vectors: list[list[float]] = []

	def _get_tools_module(self):
		try:
			from tools import tools as tools_module
			return tools_module
		except ImportError:
			import tools as tools_module
			return tools_module
		
	def _discover_tools(self) -> list[BaseTool]:
		tools_module = self._get_tools_module()
		discovered: list[BaseTool] = []

		for value in vars(tools_module).values():
			if isinstance(value, BaseTool):
				discovered.append(value)

		return discovered

	@staticmethod
	def _tool_to_text(tool: BaseTool) -> str:
		arg_names = ", ".join(tool.args.keys()) if tool.args else ""
		return (
			f"name: {tool.name}\n"
			f"description: {tool.description}\n"
			f"arguments: {arg_names}"
		)

	@staticmethod
	def _cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
		dot = sum(a * b for a, b in zip(vec_a, vec_b, strict=False))
		norm_a = sqrt(sum(a * a for a in vec_a))
		norm_b = sqrt(sum(b * b for b in vec_b))

		if norm_a == 0.0 or norm_b == 0.0:
			return 0.0

		return dot / (norm_a * norm_b)

	def initialize_tools(self, tools: Iterable[BaseTool] | None = None) -> None:
		all_tools = list(tools) if tools is not None else self._discover_tools()
		if not all_tools:
			self._indexed_tools = []
			self._indexed_vectors = []
			return

		tool_documents = [self._tool_to_text(tool) for tool in all_tools]
		vectors = self.embedding_client.embed_documents(tool_documents)

		self._indexed_tools = all_tools
		self._indexed_vectors = vectors

	def find_top_tools(self, task: str, limit: int = 5) -> list[tuple[BaseTool, float]]:
		if not self._indexed_tools:
			self.initialize_tools()

		if not self._indexed_tools:
			return []

		bounded_limit = max(1, min(limit, 5))
		query_vector = self.embedding_client.embed_query(task)

		scored_tools: list[ToolScore] = []
		for tool, vector in zip(self._indexed_tools, self._indexed_vectors, strict=False):
			scored_tools.append(
				ToolScore(tool=tool, score=self._cosine_similarity(query_vector, vector))
			)

		scored_tools.sort(key=lambda item: item.score, reverse=True)
		return [(item.tool, item.score) for item in scored_tools[:bounded_limit]]

	def get_all_tools(self) -> list[BaseTool]:
		if self._indexed_tools:
			return list(self._indexed_tools)

		self.initialize_tools()
		return list(self._indexed_tools)


tool_discovery_service = ToolDiscoveryService()


def find_top_tools(task: str, limit: int = 5) -> list[tuple[BaseTool, float]]:
	"""Convenience function to find top tools using the default service instance."""
	return tool_discovery_service.find_top_tools(task, limit)
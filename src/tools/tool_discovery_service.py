# tool_discovery_service.py
from langchain.tools import BaseTool
from langchain_community.tools import Tool

from database.vector_store import vector_store
from tools import tools


class ToolDiscoveryService:
    def __init__(self):
        # Stores tools as {tool_name: Tool object}
        self.tools = {}
        self._auto_register_tools()

    def _auto_register_tools(self):
        for dir_name in dir(tools):
            attr = getattr(tools, dir_name)
            if isinstance(attr, BaseTool):
                print(f"Registering tool: {attr.name}")
                self.register_tool(attr)

        # vector_store.add_documents(
        #     [
        #         Document(page_content=tool.description, metadata={"name": tool.name})
        #         for tool in self.get_all_tool_objects()
        #     ]
        # )

    def register_tool(self, tool: Tool):
        """Manually register a Tool object"""
        self.tools[tool.name] = tool

    def get_top_k_tools(self, query: str, k: int = 5) -> list[BaseTool]:
        """Retrieve top-k relevant tools based on a query using vector search"""
        results = vector_store.similarity_search(query, k=k)

        return [self.get_tool_by_name(vector.metadata["name"]) for vector in results]

    def list_tools(self):

        return [
            {"name": t.name, "description": t.description} for t in self.tools.values()
        ]

    def get_tool_by_name(self, name: str):
        return self.tools.get(name, None)

    def get_all_tool_objects(self):
        return list(self.tools.values())


# Singleton instance
tool_discovery_service = ToolDiscoveryService()

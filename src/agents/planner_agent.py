from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from schemas.step import PlannedTask


class PlannerAgent:
    def __init__(self):
        self.model = ChatOpenAI(
            model="qwen3:4b-instruct",
            temperature=0,
            base_url="http://host.docker.internal:11434/v1",
            api_key="test",  # type: ignore
        )
        self.prompt = self._load_prompt()
        self.agent = create_agent(
            self.model,
            response_format=PlannedTask,
            system_prompt=SystemMessage(content=self.prompt),
            name="planner_agent",
        )

    def _load_prompt(self):
        with open("src/prompts/planner_prompt.txt") as f:
            return f.read()

    async def plan(self, task: str) -> PlannedTask:
        result = await self.agent.ainvoke(
            {
                "messages": [
                    HumanMessage(content=task),
                ]
            }
        )
        return result["structured_response"]

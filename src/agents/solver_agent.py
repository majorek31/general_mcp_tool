from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from tools.tools import get_current_weather, save_to_file


class SolverAgent:
    def __init__(self):
        self.model = ChatOpenAI(
            model="qwen3:4b-instruct",
            temperature=0.7,
            base_url="http://172.27.80.1:11434/v1",
            max_completion_tokens=100,
            api_key="test",  # type: ignore
        )
        self.prompt = self._load_prompt()

    def _load_prompt(self):
        with open("src/prompts/solver_prompt.txt") as f:
            return f.read()

    async def solve(self, problem: str, context: str):
        agent = create_agent(
            model=self.model,
            system_prompt=SystemMessage(content=self.prompt),
            tools=[get_current_weather, save_to_file],
        )
        result = await agent.ainvoke(
            {
                "messages": [
                    SystemMessage(content=context),
                    HumanMessage(problem),
                ]
            }
        )
        last_message = result["messages"][-1]
        return last_message.content

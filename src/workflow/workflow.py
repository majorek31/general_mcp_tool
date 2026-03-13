from typing import TypedDict

from langgraph.graph import END, StateGraph

from agents.planner_agent import PlannerAgent
from agents.solver_agent import SolverAgent
from tools import tool_discovery_service


class AgentState(TypedDict):
    goal: str
    steps: list[str]
    step_index: int
    task_results: dict[int, str]
    final_result: str


def planner_node(state: AgentState):
    planner = PlannerAgent()
    print("Planning for goal:", state["goal"])
    result = planner.plan(state["goal"])
    # print("Planner result:", result.steps)
    return {
        "steps": [step.description for step in result.steps],
        "step_index": 0,
        "task_results": {},
    }


def solver_node(state: AgentState):
    steps = state["steps"]
    step_index = state["step_index"]
    step = steps[step_index]
    tools = tool_discovery_service.tool_discovery_service.get_top_k_tools(step)
    print(f"Solving step {step_index + 1}/{len(steps)}: {step} with tools: {tools}")
    solver = SolverAgent(tools=tools)
    context = "\n".join(
        [f"Step {idx}: {output}" for idx, output in state["task_results"].items()]
    )
    result = solver.solve(step, context)
    task_results = state["task_results"]

    task_results[step_index + 1] = result
    return {
        "task_results": task_results,
        "step_index": step_index + 1,
    }


def finish_node(state: AgentState):
    return {"final_result": state["task_results"][len(state["steps"])]}


def router(state: AgentState):
    if state["step_index"] < len(state["steps"]):
        return "solver"
    return "finish"


graph = StateGraph(AgentState)

graph.add_node("planner", planner_node)
graph.add_node("solver", solver_node)
graph.add_node("finish", finish_node)


graph.set_entry_point("planner")

graph.add_conditional_edges(
    "planner",
    router,
    {
        "solver": "solver",
        "finish": "finish",
    },
)

graph.add_conditional_edges(
    "solver",
    router,
    {
        "solver": "solver",
        "finish": "finish",
    },
)

graph.add_edge("finish", END)
app = graph.compile()

png = app.get_graph().draw_mermaid_png()

with open("workflow.png", "wb") as f:
    f.write(png)


def run_workflow(goal: str) -> str:
    state: AgentState = {
        "goal": goal,
        "steps": [],
        "step_index": 0,
        "task_results": {},
        "final_result": "",
    }
    result = app.invoke(state)
    return result["final_result"]

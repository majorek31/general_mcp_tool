import uvicorn
from fastmcp import FastMCP
from fastmcp.server.http import create_streamable_http_app

from tools import tool_discovery_service
from workflow.workflow import run_workflow

server = FastMCP()

#
# PRMPT -> PLANNER -> STEPS -> SOLVER (rozwiazuje, SKIP_STEP) -> REPLANNING
# REPLANNING -> PLANNER -> STEPS -> SOLVER (rozwiazuje, SKIP_STEP) -> REPLANNING
#
# print(run_workflow("Generate a random string and save it to random.md"))

print("Starting server...")
# sys.exit()

tools = tool_discovery_service.tool_discovery_service.get_all_tool_objects()


@server.tool("general_solver")
def general_solver(problem: str) -> str:
    """A general problem solver that can solve a wide range of problems by planning and executing steps."""
    return run_workflow(problem)


@server.tool("list_tools")
def list_tools() -> str:
    """List all tools that can be accessed through general_solver"""
    return "\n".join([f"{tool.name}: {tool.description}" for tool in tools])


@server.prompt("solve")
def solve(problem: str) -> str:
    """A prompt that uses the general_solver tool to solve a problem."""
    return f"Call general_solver with ({problem})"


app = create_streamable_http_app(server, "/mcp")
uvicorn.run(app, host="0.0.0.0", port=8000)

# # asyncio.run(server.run_http_async(host="0.0.0.0", transport="http"))


# async def main():
#     planner = PlannerAgent()
#     result = await planner.plan(
#         # "Collect and integrate diverse data streams: real-time stock market data, government economic reports, social media sentiment, global news, and patent filings. Normalize and validate all incoming data."
#         "Get current weather in Cieszyn and save it in a file named weather.txt"
#     )
#     # print the result in a human readable format with indexes
#     solver = SolverAgent()
#     task_results: dict[int, str] = {}
#     for i, step in enumerate(result.steps, start=1):
#         context = "\n".join(
#             [f"Step {idx}: {output}" for idx, output in task_results.items()]
#         )
#         print(f"Solving step {i}: {step.description}")
#         task_results[i] = await solver.solve(step.description, context)
#         print(f"Result for step {i}: {task_results[i]}")


# import asyncio

# asyncio.run(main())

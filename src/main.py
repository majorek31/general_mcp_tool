import uvicorn
from fastmcp import FastMCP
from fastmcp.server.http import create_streamable_http_app

from workflow.workflow import run_workflow

server = FastMCP()

#
# PRMPT -> PLANNER -> STEPS -> SOLVER (rozwiazuje, SKIP_STEP) -> REPLANNING
# REPLANNING -> PLANNER -> STEPS -> SOLVER (rozwiazuje, SKIP_STEP) -> REPLANNING
#

print("Starting server...")


@server.tool("general_solver")
def general_solver(problem: str) -> str:
    """A general problem solver that uses a planner agent to break down the problem into steps and a solver agent to solve each step."""
    return run_workflow(problem)


app = create_streamable_http_app(server, "/mcp")
uvicorn.run(app, host="0.0.0.0", port=8000)

# asyncio.run(server.run_http_async(host="0.0.0.0", transport="http"))


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

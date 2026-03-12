import asyncio

from agents.planner_agent import PlannerAgent
from agents.solver_agent import SolverAgent


async def main():
    planner = PlannerAgent()
    result = await planner.plan(
        # "Collect and integrate diverse data streams: real-time stock market data, government economic reports, social media sentiment, global news, and patent filings. Normalize and validate all incoming data."
        "Get current weather in Cieszyn and save it in a file named weather.txt"
    )
    # print the result in a human readable format with indexes
    solver = SolverAgent()
    task_results: dict[int, str] = {}
    for i, step in enumerate(result.steps, start=1):
        context = "\n".join(
            [f"Step {idx}: {output}" for idx, output in task_results.items()]
        )
        print(f"Solving step {i}: {step.description}")
        task_results[i] = await solver.solve(step.description, context)
        print(f"Result for step {i}: {task_results[i]}")


asyncio.run(main())

from src.llm.azure import AzureLLM
from src.query.planner import QueryPlanner


llm = AzureLLM()

planner = QueryPlanner(llm)

question = "Why did McLaren outperform Ferrari in 2024?"

plan = planner.plan(question)

print(plan)
print("Route:", plan.route)
print("Intent:", plan.intent)
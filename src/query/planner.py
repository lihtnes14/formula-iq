from pydantic import BaseModel
from typing import Literal
from src.llm.azure import AzureLLM
from src.llm.prompts import QUERY_PLANNER_SYSTEM_PROMPT
from pathlib import Path

class QueryPlan(BaseModel):
    route: Literal["database", "web", "hybrid"]
    intent: str

    database_required: bool
    web_required: bool
    visualization_required: bool

    reasoning: str


class QueryPlanner:
    def __init__(self, llm: AzureLLM):
        self.llm = llm

        schema_path = Path(__file__).parent.parent / "schema" / "gold_schema.txt"

        with open(schema_path, "r") as f:
            self.gold_schema = f.read()
    
    def plan(self, question:str) -> QueryPlan:

        system_prompt = QUERY_PLANNER_SYSTEM_PROMPT.format(
            schema=self.gold_schema
        )
        
        response = self.llm.generate_plan(
            system_prompt = QUERY_PLANNER_SYSTEM_PROMPT,
            question = question
        )
        return QueryPlan.model_validate_json(response)


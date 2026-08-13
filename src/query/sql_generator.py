from src.llm.azure import AzureLLM
from src.llm.prompts import SQL_SYSTEM_PROMPT
from src.schema.discover import SchemaDiscovery
from pathlib import Path

class SQLGenerator:

    def __init__(self, llm: AzureLLM):
        self.llm = llm
        schema_path = Path(__file__).parent.parent / "schema" / "gold_schema.txt"

        with open(schema_path, "r") as f:
            self.gold_schema = f.read()

    def generate_sql(self, question: str) -> str:

        schema = self.gold_schema

        system_prompt = SQL_SYSTEM_PROMPT.format(
            schema=schema
        )

        return self.llm.generate_sql(
            system_prompt=system_prompt,
            question=question,
        )
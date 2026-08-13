from src.llm.azure import AzureLLM
from src.llm.prompts import SQL_SYSTEM_PROMPT, ANSWER_SYSTEM_PROMPT
from src.schema.discover import SchemaDiscovery
from src.core.base import BaseService


schema_discovery = SchemaDiscovery()
gold_schema = schema_discovery.schema_loader()

llm = AzureLLM()

system_prompt1 = SQL_SYSTEM_PROMPT.format(
    schema=gold_schema
)

service  = BaseService()



question = "Which team won the most championship of all time?"

response1 = llm.generate_sql(
    system_prompt=system_prompt1,
    question=question,
)

result =  service.execute_query(response1)

response2 = llm.generate_answer(
    system_prompt = ANSWER_SYSTEM_PROMPT,
    question = question,
    query = response1,
    result = result
)

print("Generated SQL:")
print(response1)

print("Answer from the LLM")
print(response2)

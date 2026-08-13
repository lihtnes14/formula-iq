from openai import OpenAI
import json
from src.llm.base import BaseLLM
from src.core.config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_GPT_DEPLOYMENT,
)


class AzureLLM(BaseLLM):

    def __init__(self):
        self.client = OpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            base_url=AZURE_OPENAI_ENDPOINT,
        )

        self.model = AZURE_GPT_DEPLOYMENT

    def generate_sql(self, system_prompt: str, question: str) -> str:

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ]

        return self.invoke(messages)

    def invoke(self, messages: list) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()

    def generate_answer(
    self,
    system_prompt: str,
    question: str,
    query: str = "",
    database_result=None,
    web_result=None,
) -> str:

        if database_result is None:
            database_result = []

        if web_result is None:
            web_result = []

        messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": f"""
User Question:
{question}

Executed SQL:
{query}

Databricks Result:
{database_result}

Web Search Results:
{web_result}
""",
        },
    ]

        return self.invoke(messages)

    def generate_plan(self, question: str, system_prompt: str) -> str:

        
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ]
        return self.invoke(messages)

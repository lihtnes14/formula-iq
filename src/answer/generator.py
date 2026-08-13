import json

from src.llm.azure import AzureLLM
from src.llm.prompts import ANSWER_SYSTEM_PROMPT


class AnswerGenerator:

    def __init__(self, llm: AzureLLM):
        self.llm = llm

    def generate_answer(
        self,
        question: str,
        query: str = None,
        database_result=None,
        web_result=None,
    ):

        if database_result is not None:
            database_result = json.dumps(
                database_result,
                ensure_ascii=False,
                indent=2,
            )

        if web_result is not None:
            web_result = json.dumps(
                web_result,
                ensure_ascii=False,
                indent=2,
            )

        return self.llm.generate_answer(
            system_prompt=ANSWER_SYSTEM_PROMPT,
            question=question,
            query=query,
            database_result=database_result,
            web_result=web_result,
        )
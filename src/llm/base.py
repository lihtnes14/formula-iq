from abc import ABC, abstractmethod

class BaseLLM(ABC):

    @abstractmethod
    def generate_sql(self, system_prompt: str, query: str) -> str:
        pass
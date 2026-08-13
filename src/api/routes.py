from fastapi import APIRouter
from pydantic import BaseModel

from src.llm.azure import AzureLLM
from src.query.planner import QueryPlanner
from src.query.sql_generator import SQLGenerator
from src.query.service import QueryService
from src.answer.generator import AnswerGenerator
from src.core.databr import DatabricksService
from src.web.search import WebSearch


router = APIRouter()


# ====================================
# DEPENDENCIES
# ====================================

llm = AzureLLM()

planner = QueryPlanner(llm)
sql_generator = SQLGenerator(llm)
answer_generator = AnswerGenerator(llm)

databricks = DatabricksService()
web_search = WebSearch(max_results=5)

query_service = QueryService(
    planner=planner,
    sql_generator=sql_generator,
    answer_generator=answer_generator,
    databricks=databricks,
    web_search=web_search,
)


# ====================================
# REQUEST MODEL
# ====================================

class AskRequest(BaseModel):
    question: str


# ====================================
# RESPONSE ENDPOINT
# ====================================

@router.post("/ask")
def ask(request: AskRequest):

    response = query_service.ask(
        request.question
    )

    return response
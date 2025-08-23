from pydantic import BaseModel
from .base import BaseAgent
from prompts.templates import QUERY_AGENT_PROMPT

class QueryResponse(BaseModel):
    queries: list[str]
    thoughts: str

class QueryAgent(BaseAgent)
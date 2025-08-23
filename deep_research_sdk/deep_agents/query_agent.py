from pydantic import BaseModel
from .base import BaseAgent
from litellm import acompletion
from prompts.templates import QUERY_AGENT_PROMPT
from prompts.converter import convert_to_llm_message

class QueryResponse(BaseModel):
    queries: list[str]
    thoughts: str

class QueryAgent(BaseAgent):
    def __init__(self,
        model: str,
        query: str,
        system_prompt: str | None = QUERY_AGENT_PROMPT
    ):
        super().__init__(model, system_prompt)
        self.query = query

        if not query:
            pass
    
    async def build_queries(self) -> QueryResponse:
        messages = convert_to_llm_message(self.system_prompt, self.query)

        response = await acompletion(
        model=self.model,
        messages=messages,
        response_format=QueryResponse
      )

        return response
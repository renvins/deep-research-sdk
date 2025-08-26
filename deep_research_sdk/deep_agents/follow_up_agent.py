from pydantic import BaseModel
from litellm import acompletion
from .base import BaseAgent
from .prompts.templates import FOLLOW_UP_DECISION_PROMPT
from .prompts.converter import convert_to_llm_message

class FollowUpResponse(BaseModel):
    should_follow_up: bool
    queries: list[str]
    reasoning: str

class FollowUpAgent(BaseAgent):
    def __init__(
        self,
        model: str,
        findings: str,
        system_prompt: str | None = FOLLOW_UP_DECISION_PROMPT,
    ):
        super().__init__(model, system_prompt)
        self.findings = findings

        if not findings:
            raise ValueError("Findings cannot be empty")
            
    async def follow_up(self) -> FollowUpResponse:
        messages = convert_to_llm_message(self.system_prompt, self.findings)
        result = await acompletion(model=self.model, messages=messages, response_format=FollowUpResponse)

        import json
        content = result.choices[0].message.content
        parsed_data = json.loads(content)

        return FollowUpResponse(**parsed_data)
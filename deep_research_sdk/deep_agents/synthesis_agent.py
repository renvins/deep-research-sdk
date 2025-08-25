from litellm import acompletion
from .base import BaseAgent
from .prompts.templates import SYNTHESIS_AGENT_PROMPT
from .prompts.converter import convert_to_llm_message

class SynthesisAgent(BaseAgent):
    def __init__(self,
        model: str,
        findings: str,
        system_prompt: str | None = SYNTHESIS_AGENT_PROMPT    
    ):
        super().__init__(model, system_prompt)
        if not findings:
            pass
    
    async def synthetize(self) -> str:
        messages = convert_to_llm_message(self.system_prompt, self.findings)
        response = await acompletion(
            model=self.model,
            messages=messages
            )
        
        return response.choices[0].message.content

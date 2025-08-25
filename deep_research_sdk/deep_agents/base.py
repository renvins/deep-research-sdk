from abc import ABC, abstractmethod

class BaseAgent(ABC):

    def __init__(self, model: str, system_prompt: str | None = None) -> None:
        self.model = model
        self.system_prompt = system_prompt

        if not model:
            # raise exception
            pass
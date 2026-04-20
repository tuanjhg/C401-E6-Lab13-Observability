from __future__ import annotations

import random
import time
from dataclasses import dataclass

from .incidents import STATE


@dataclass
class FakeUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class FakeResponse:
    text: str
    usage: FakeUsage
    model: str


from .tracing import observe
from langfuse import get_client


class FakeLLM:
    def __init__(self, model: str = "claude-sonnet-4-5") -> None:
        self.model = model

    @observe(name="Generate", as_type="generation")
    def _generate_internal(self, prompt: str) -> FakeResponse:
        time.sleep(1.2)  # Simulate 1.2s generation
        input_tokens = max(20, len(prompt) // 4)
        output_tokens = random.randint(80, 180)
        if STATE["cost_spike"]:
            output_tokens *= 4
        answer = (
            "Starter answer. Teams should improve this output logic and add better quality checks. "
            "Use retrieved context and keep responses concise."
        )
        try:
            get_client().update_current_generation(
                usage_details={"input": input_tokens, "output": output_tokens},
                model=self.model
            )
        except Exception:
            pass
            
        return FakeResponse(text=answer, usage=FakeUsage(input_tokens, output_tokens), model=self.model)

    @observe(name="LLM Call")
    def generate(self, prompt: str) -> FakeResponse:
        time.sleep(0.2)  # Simulate 200ms overhead
        return self._generate_internal(prompt)

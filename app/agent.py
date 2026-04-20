from __future__ import annotations

import time
import random
from dataclasses import dataclass
from contextlib import contextmanager

from . import metrics
from .mock_llm import FakeLLM
from .mock_rag import retrieve
from .pii import hash_user_id, summarize_text
from .tracing import observe
from langfuse import get_client

try:
    from langfuse import propagate_attributes
except ImportError:
    @contextmanager
    def propagate_attributes(**_: object):
        yield


@dataclass
class AgentResult:
    answer: str
    latency_ms: int
    tokens_in: int
    tokens_out: int
    cost_usd: float
    quality_score: float


class LabAgent:
    def __init__(self, model: str = "claude-sonnet-4-5") -> None:
        self.model = model
        self.llm = FakeLLM(model=model)

    @observe(name="Input Guards")
    def _input_guards(self, message: str) -> None:
        time.sleep(0.02)  # Simulate 20ms safety check
        # Logic for PII/adversarial check could go here

    @observe(name="Agent Router")
    def _agent_router(self, message: str) -> None:
        time.sleep(0.05)  # Simulate 50ms intent classification

    @observe(name="Post-process")
    def _post_process(self, response_text: str) -> str:
        time.sleep(0.03)  # Simulate 30ms formatting
        return response_text

    @observe(name="Total Request")
    def run(self, user_id: str, feature: str, session_id: str, message: str) -> AgentResult:
        with propagate_attributes(
            user_id=hash_user_id(user_id),
            session_id=session_id,
            tags=["lab", feature, self.model],
        ):
            started = time.perf_counter()
            
            self._input_guards(message)
            self._agent_router(message)
        
            docs = retrieve(message)
            prompt = f"Feature={feature}\nDocs={docs}\nQuestion={message}"
            response = self.llm.generate(prompt)
            
            answer = self._post_process(response.text)
            quality_score = self._heuristic_quality(message, answer, docs)
            
            latency_ms = int((time.perf_counter() - started) * 1000)
            cost_usd = self._estimate_cost(response.usage.input_tokens, response.usage.output_tokens)
            
            # Mock Severity for dashboard
            severities = ["Critical", "High", "Normal", "Low"]
            weights = [0.1, 0.2, 0.5, 0.2]
            severity = random.choices(severities, weights=weights)[0]
            
            tags = ["lab", feature, self.model, f"severity:{severity}"]
            if latency_ms > 3000:
                tags.append("SLO_BREACH:latency")
            if quality_score < 0.75:
                tags.append("SLO_BREACH:quality")

            # Update trace with tags and final output
            try:
                client = get_client()
                # Update current trace level info
                client.update_current_span(
                    metadata={
                        "doc_count": len(docs), 
                        "query_preview": summarize_text(message),
                        "severity": severity
                    }
                )
                # Score the trace for quality
                client.score_current_trace(
                    name="quality_score_avg",
                    value=quality_score
                )
            except Exception:
                pass

            metrics.record_request(
                latency_ms=latency_ms,
                cost_usd=cost_usd,
                tokens_in=response.usage.input_tokens,
                tokens_out=response.usage.output_tokens,
                quality_score=quality_score,
                severity=severity
            )

            return AgentResult(
                answer=answer,
                latency_ms=latency_ms,
                tokens_in=response.usage.input_tokens,
                tokens_out=response.usage.output_tokens,
                cost_usd=cost_usd,
                quality_score=quality_score,
            )

    @observe(name="Estimate Cost")
    def _estimate_cost(self, tokens_in: int, tokens_out: int) -> float:
        input_cost = (tokens_in / 1_000_000) * 3
        output_cost = (tokens_out / 1_000_000) * 15
        return round(input_cost + output_cost, 6)

    @observe(name="Heuristic Quality")
    def _heuristic_quality(self, question: str, answer: str, docs: list[str]) -> float:
        score = 0.5
        if docs:
            score += 0.2
        if len(answer) > 40:
            score += 0.1
        if question.lower().split()[0:1] and any(token in answer.lower() for token in question.lower().split()[:3]):
            score += 0.1
        if "[REDACTED" in answer:
            score -= 0.2
        return round(max(0.0, min(1.0, score)), 2)

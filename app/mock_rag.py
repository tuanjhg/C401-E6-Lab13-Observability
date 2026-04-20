from __future__ import annotations

import time

from .incidents import STATE

CORPUS = {
    "refund": ["Refunds are available within 7 days with proof of purchase."],
    "monitoring": ["Metrics detect incidents, traces localize them, logs explain root cause."],
    "policy": ["Do not expose PII in logs. Use sanitized summaries only."],
}

from .tracing import observe


@observe(name="Embed")
def _embed(message: str) -> None:
    time.sleep(0.2)  # Simulate 200ms embedding


@observe(name="Search")
def _search(message: str) -> list[str]:
    time.sleep(0.35)  # Simulate 350ms search
    lowered = message.lower()
    for key, docs in CORPUS.items():
        if key in lowered:
            return docs
    return ["No domain document matched. Use general fallback answer."]


@observe(name="RAG Retrieve")
def retrieve(message: str) -> list[str]:
    if STATE["tool_fail"]:
        raise RuntimeError("Vector store timeout")
    if STATE["rag_slow"]:
        time.sleep(2.5)
    
    _embed(message)
    return _search(message)

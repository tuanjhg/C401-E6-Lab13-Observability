from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str = Field(..., examples=["parent_nguyen_van_a"])
    session_id: str = Field(..., examples=["s_2024_04_20"])
    campus: str = Field(default="vsc_times_city", examples=["vsc_times_city", "vsc_the_harmony", "vsc_central_park"])
    grade: str = Field(default="grade_1", examples=["grade_1", "grade_10"])
    student_id: str = Field(..., examples=["std_123456"])
    feature: str = Field(default="qa", examples=["qa", "notifications", "tuition_check"])
    message: str = Field(..., min_length=1, examples=["Lịch nghỉ lễ 30/4 của khối 1 như thế nào?"])


class ChatResponse(BaseModel):
    answer: str
    correlation_id: str
    latency_ms: int
    tokens_in: int
    tokens_out: int
    cost_usd: float
    quality_score: float


class LogRecord(BaseModel):
    ts: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    level: Literal["info", "warning", "error", "critical"]
    service: str
    event: str
    correlation_id: str
    env: str
    user_id_hash: str | None = None
    session_id: str | None = None
    feature: str | None = None
    model: str | None = None
    campus: str | None = None
    grade: str | None = None
    latency_ms: int | None = None
    tokens_in: int | None = None
    tokens_out: int | None = None
    cost_usd: float | None = None
    error_type: str | None = None
    tool_name: str | None = None
    payload: dict[str, Any] | None = None

from __future__ import annotations

import os
from typing import Any

from langfuse import observe

def tracing_enabled() -> bool:
    # Langfuse SDK automatically picks up LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, and LANGFUSE_HOST
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))

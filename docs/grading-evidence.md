# Evidence Collection Sheet

## Required screenshots
- Langfuse trace list with >= 10 traces
- One full trace waterfall
- JSON logs showing correlation_id
- Log line with PII redaction
- Dashboard with 6 panels
- Alert rules with runbook link

## Optional screenshots
- Incident before/after fix
- Cost comparison before/after optimization
- Auto-instrumentation proof

## Evidence status (current run)
- AVAILABLE: `image/step01_health_tracing_enabled.png`
- AVAILABLE: `image/step02_metrics_baseline.png.png`
- AVAILABLE: `image/step03_logs_baseline_traffic.png`
- AVAILABLE: `image/step03_logs_baseline_traffic.jsonl` (raw logs with `correlation_id`)
- AVAILABLE: `image/step04_inject_rag_slow_enabled.png`
- AVAILABLE: `image/step05_metrics_after_rag_slow.png`
- AVAILABLE: `image/step08_logs_incident_window.jsonl` (incident window logs and PII redaction markers)
- AVAILABLE: `image/step11_inject_tool_fail_enabled.png`
- AVAILABLE: `image/step12_metrics_or_logs_tool_fail_effect.png`
- AVAILABLE: `image/step13_inject_cost_spike_enabled.png`
- AVAILABLE: `image/step14_metrics_or_trace_cost_spike_effect.png`
- AVAILABLE: `image/step06_langfuse_trace_list.png`
- AVAILABLE: `image/step07_langfuse_trace_waterfall_rag_slow.png`
- AVAILABLE: `image/step15_dashboard_6_panels_overview.png`
- PENDING: `image/step16_alert_rules_and_runbook_link.png`

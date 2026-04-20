# Incident RCA - Huy (Load Test & Incident)

## Scenario
- Name: `rag_slow`
- Trigger command: `python scripts/inject_incident.py --scenario rag_slow`
- Recovery command: `python scripts/inject_incident.py --scenario rag_slow --disable`

## Symptoms Observed
- Batch run status: `26/26` requests returned `200` (no hard errors).
- User-facing latency increased significantly during incident window.
- Metrics showed a large jump in tail latency.

## Evidence
- Metrics (baseline, before incident):
  - `traffic=26`
  - `latency_p50=154ms`
  - `latency_p95=155ms`
- Metrics (during `rag_slow`):
  - `traffic=52`
  - `latency_p50=155ms`
  - `latency_p95=2660ms`
  - `latency_p99=2660ms`
- Logs (`data/logs.jsonl`) during incident:
  - Multiple `response_sent` events recorded with `latency_ms` around `2653-2660ms`.
  - Example correlation IDs seen in slow responses:
    - `req-c493b105`
    - `req-00fc526b`
    - `req-5f34153d`
- Trace evidence (Langfuse):
  - Trace list screenshot in incident window: `<fill_trace_list_screenshot_path>`
  - Waterfall screenshot showing slow retrieval span: `<fill_trace_waterfall_screenshot_path>`
  - Trace ID from waterfall: `<fill_trace_id_from_langfuse>`

## Root Cause
- `rag_slow` incident injects artificial delay in retrieval:
  - Source: `app/mock_rag.py`
  - Behavior: when `STATE["rag_slow"] == True`, `retrieve()` executes `time.sleep(2.5)`.
- This delay propagates to `/chat` end-to-end response latency, causing P95/P99 breach.

## Fix Action
- Disable incident toggle (`rag_slow`) after verification.
- Confirm health state returns incidents to `false`.

## Preventive Measure
- Add alert rule for latency tail breach (P95 threshold).
- Add runbook step: inspect retrieval span first when latency spikes.
- Consider fallback retrieval or timeout budget for retrieval stage.

## Suggested Section 4 Mapping (Blueprint)
- `[SCENARIO_NAME]`: `rag_slow`
- `[SYMPTOMS_OBSERVED]`: P95 latency rose from ~155ms to ~2660ms during incident run.
- `[ROOT_CAUSE_PROVED_BY]`: metrics snapshot + slow `response_sent` logs + Langfuse trace waterfall.
- `[FIX_ACTION]`: disabled `rag_slow` and verified incident state reset.
- `[PREVENTIVE_MEASURE]`: latency alert + retrieval-focused runbook + fallback strategy.

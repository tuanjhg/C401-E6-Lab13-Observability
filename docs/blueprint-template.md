# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: C401-E6
- [REPO_URL]: https://github.com/tuanjhg/C401-E6-Lab13-Observability
- [MEMBERS]:
  - Member 1: Hồ Hải Thuận | Role: Logging Core
  - Member 2: Khổng Mạnh Tuấn | Role: PII & Security
  - Member 3: Quách Ngọc Quang | Role: Tracing & Enrichment
  - Member 4: Nguyễn Hoàng Long | Role: SLO & Alerts
  - Member 5: Lâm Hoàng Hải | Role: Dashboard & Metrics
  - Member 6: Trần Thái Huy | Role: Load Test & Incident
  - Member 7: Nguyễn Mạnh Dũng | Role: Demo Lead & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]:321
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: `image/step03_logs_baseline_traffic.png` (backup raw log: `image/step03_logs_baseline_traffic.jsonl`)
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: `image/step08_logs_incident_window.jsonl` (contains `[REDACTED_PHONE_VN]` and `[REDACTED_EMAIL]`)
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: `image/step07_langfuse_trace_waterfall_rag_slow.png`
- [TRACE_WATERFALL_EXPLANATION]: Trace list (`image/step06_langfuse_trace_list.png`) and waterfall (`image/step07_langfuse_trace_waterfall_rag_slow.png`) show request timeline where retrieval-related work dominates total latency in `rag_slow`; this matches the `latency_p95=2660` spike and slow `response_sent` logs.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: `image/step15_dashboard_6_panels_overview.png`
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 2660ms (during `rag_slow`) |
| Error Rate | < 2% | 28d | 100% in incident batch (`tool_fail`, 26/26 failed) |
| Cost Budget | < $2.5/day | 1d | avg_cost_usd 0.0042 after `cost_spike` batch |
| Quality Score | > 0.75 | 28d | 0.85 (pre-incident baseline) |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: `C401-E6:image/step16_alert_rules_and_runbook_link.png`
- [SAMPLE_RUNBOOK_LINK]: `docs/alerts.md#1-high-latency-p95`

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: `rag_slow`
- [SYMPTOMS_OBSERVED]: - Batch run status: `26/26` requests returned `200` (no hard errors). User-facing latency increased significantly during incident window. Metrics showed a large jump in tail latency.
- [ROOT_CAUSE_PROVED_BY]: - `rag_slow` incident injects artificial delay in retrieval: source `app/mock_rag.py`; Behavior: when `STATE["rag_slow"] == True`, `retrieve()` executes `time.sleep(2.5)`. This delay propagates to `/chat` end-to-end response latency, causing P95/P99 breach.
- [FIX_ACTION]: Disable incident toggle (`rag_slow`) after verification. Confirm health state returns incidents to `false`.
- [PREVENTIVE_MEASURE]: Add alert rule for latency tail breach (P95 threshold). Add runbook step: inspect retrieval span first when latency spikes. Consider fallback retrieval or timeout budget for retrieval stage.

---

## 5. Individual Contributions & Evidence

### [Hồ Hải Thuận]
- [TASKS_COMPLETED]:
1. **Building the Tracking Mechanism (middleware.py)**: Initialize and synchronize correlation_id (x-request-id) for all requests, handle context leaks, and integrate response time measurement.
2.**Enriching Log Data (main.py)**: Integrate important contextual information (user, session, feature, etc.) into the structlog system to ensure complete metadata for the Observability Dashboard. 
- [EVIDENCE_LINK]:
https://github.com/VinUni-AI20k/Lab13-Observability/pull/78#issue-4295874060

### [Khổng Mạnh Tuấn]
- [TASKS_COMPLETED]: 
1. **Mock Data Engineering**: Designed and enhanced realistic parent query scenarios
2. **Schema Design**: Extended ChatRequest schema with campus, grade, and student_id fields
3. **Dashboard Architecture**: Created system design template for observability dashboard
4. **Data Quality & Consistency**: Fixed and refined sample queries, expected answers, and incident scenarios
- [EVIDENCE_LINK]: 
https://github.com/VinUni-AI20k/Lab13-Observability/commit/6d913c89329b52b9e9488bf112220dca33b80bac

### [Quách Ngọc Quang]
- [TASKS_COMPLETED]: 
1. **Tracing Infrastructure (tracing.py)**: Configure and initialize the Langfuse V4 SDK, establishing a secure connection to the cloud and ensuring the @observe decorator is functional across the system.
2. **Agent Instrumentation (agent.py)**: Implement deep tracing within the agent's core workflow (Retrieve, Generate, Rank), using get_client().update_current_span to record detailed metadata such as model type, token usage, and cost estimates.
3. **Trace Lifecycle & Span Management**: Manage the full lifecycle of traces by capturing a comprehensive waterfall of spans, enabling granular visibility into each step of the agentic process from retrieval to generation.
- [EVIDENCE_LINK]: 
https://github.com/tuanjhg/C401-E6-Lab13-Observability/pull/2

### [Nguyễn Hoàng Long]
- [TASKS_COMPLETED]: 
1. **SLO Configuration (slo.yaml)**: Defined Service Level Objectives for Latency (P95 < 3000ms), Error Rate (< 2%), and daily Cost Budget ($2.5) to establish system reliability targets.
2. **Alert Rule Implementation (alert_rules.yaml)**: Configured 3+ critical alert rules for latency breaches, error rate spikes, and cost overruns using a standardized YAML schema.
3. **Incident Runbook Design (docs/alerts.md)**: Authored a comprehensive runbook providing step-by-step diagnostic and mitigation instructions for each alert type.
4. **Alert Validation**: Verified alert triggers by simulating the `rag_slow` incident, ensuring the observability pipeline correctly captures and signals threshold violations.
- [EVIDENCE_LINK]: 
https://github.com/tuanjhg/C401-E6-Lab13-Observability/pull/1

### [Lâm Hoàng Hải]
- [TASKS_COMPLETED]:
**Metrics Designing**: Design metrics displayed in dashboard layers whicu are: severity levels, input output token, error rate, budget, notification traffic, quality score, latency
**Dashboard Implementation**: Design and implement the Dashboard with 3 layers where 1st layer displays overview, 2nd layer shows graph view of metrics and 3rd layer intergrate with langfuse to log traces and errors 
- [EVIDENCE_LINK]: 
https://github.com/tuanjhg/C401-E6-Lab13-Observability/pull/3

### [Trần Thái Huy]
- [TASKS_COMPLETED]:
Environment & Tracing Setup: Configured runtime environment and Langfuse keys to enable observability pipeline.
Result: Application health check and tracing status are active for testing flows.
Incident Execution & Analysis: Ran baseline and injected rag_slow, tool_fail, and cost_spike scenarios to validate system behavior under failure conditions.
Result: Collected clear evidence for latency spike, error spike, and cost/token spike.
Incident Reporting: Consolidated observations into structured RCA format following Metrics -> Logs -> Traces flow.
Result: Incident section is ready with scenario, symptoms, root cause, fix action, and preventive actions.
Batch Query UI MVP: Built a simple UI to import JSONL queries, run batch requests, monitor progress, and export results.
Result: Team can execute query batches without CLI and reuse outputs for demo/reporting.
- [EVIDENCE_LINK]: 
https://github.com/tuanjhg/C401-E6-Lab13-Observability/pull/5
https://github.com/tuanjhg/C401-E6-Lab13-Observability/pull/4

### [Nguyễn Mạnh Dũng]
- [TASKS_COMPLETED]:
1. **Demo Leadership & Scripting**: Designed the end-to-end live demo flow, focusing on the "Incident -> Alert -> Trace -> Log" debugging lifecycle. Ensure schemas and request form unified with chosen topic.
2. **Report Consolidation**: Orchestrated the completion of the `blueprint-template.md`, ensuring technical evidence from all members is accurately represented.
3. **Q&A Preparation**: Prepared the team for oral defense by mapping potential instructor questions to specific technical leads.
- [EVIDENCE_LINK]: 
https://github.com/tuanjhg/C401-E6-Lab13-Observability/commit/bcc3a58ac7ca3c0dc05cf0fc7f729225870b28e6
---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)

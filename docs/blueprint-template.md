# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: 
- [REPO_URL]: 
- [MEMBERS]:
  - Member A: [Name] | Role: Logging & PII
  - Member B: [Name] | Role: Tracing & Enrichment
  - Member C: [Name] | Role: SLO & Alerts
  - Member D: [Name] | Role: Load Test & Dashboard
  - Member E: [Name] | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: /100
- [TOTAL_TRACES_COUNT]: 
- [PII_LEAKS_FOUND]: 

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

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: `PENDING_TEAM:image/step16_alert_rules_and_runbook_link.png`
- [SAMPLE_RUNBOOK_LINK]: `docs/alerts.md#1-high-latency-p95`

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: `rag_slow`
- [SYMPTOMS_OBSERVED]: Baseline latency was around `~151-155ms`, but when `rag_slow` was enabled, request latency jumped to around `~2653-2660ms` while status codes remained `200`.
- [ROOT_CAUSE_PROVED_BY]: Metrics snapshot in `image/step05_metrics_after_rag_slow.png` shows `latency_p95=2660`; logs in `image/step08_logs_incident_window.jsonl` show multiple `response_sent` with `latency_ms` around `2655-2660` and correlation IDs such as `req-a5965399`, `req-02aa1b85`, `req-16b8d2a5`; control log contains `incident_enabled` for `rag_slow`.
- [FIX_ACTION]: Disabled incident toggle after capture using `python scripts/inject_incident.py --scenario rag_slow --disable` and confirmed healthy state before continuing the next scenarios.
- [PREVENTIVE_MEASURE]: Add/keep latency P95 alerting, inspect retrieval stage first in runbook, and add fallback retrieval/timeout guard to reduce tail latency impact.

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: (Link to specific commit or PR)

### [MEMBER_B_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### [MEMBER_C_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### [MEMBER_D_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### [MEMBER_E_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)

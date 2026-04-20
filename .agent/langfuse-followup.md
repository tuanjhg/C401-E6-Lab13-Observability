# Langfuse Follow-up Notes (Deferred)

## Context
- Date: 2026-04-20
- Owner: Huy
- Reason deferred: Complete non-Langfuse evidence first, then return to traces/screenshots.

## Pending Langfuse Evidence
- `image/step06_langfuse_trace_list.png`
- `image/step07_langfuse_trace_waterfall_rag_slow.png`
- (Optional for cost spike) trace screenshot showing high token usage

## Pending Metadata to capture
- `trace_id` for one representative `rag_slow` trace
- short explanation of slow span from waterfall (for blueprint section 3.1 / RCA proof)

## How to resume later
1. Open `https://cloud.langfuse.com`
2. Select correct org/project (matching keys in `.env`)
3. Filter traces by time window when `rag_slow` was enabled
4. Capture list screenshot and one waterfall screenshot
5. Copy trace ID into report placeholders

## Report placeholders waiting for Langfuse
- File: `docs/huy-incident-rca.md`
- Placeholders:
  - `<fill_trace_list_screenshot_path>`
  - `<fill_trace_waterfall_screenshot_path>`
  - `<fill_trace_id_from_langfuse>`

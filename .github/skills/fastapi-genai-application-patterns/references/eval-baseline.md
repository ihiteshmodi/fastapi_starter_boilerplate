# Evaluation Baseline

Track at minimum:

- quality: task success, factuality checks, citation validity when required
- latency: p50/p95/p99 by route and model
- cost: tokens and provider cost by request class
- safety: policy violations, prompt injection detection outcomes

Release rule:

- no GenAI feature is promoted without baseline eval and regression checks.
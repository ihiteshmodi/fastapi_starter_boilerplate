---
name: fastapi-genai-application-patterns
description: Design FastAPI-based GenAI applications with robust model orchestration, tool-calling safety, prompt/context controls, and reliability boundaries. Use when users ask to build AI apps, LLM APIs, or agentic workflows on FastAPI.
argument-hint: [genai-goal] [model-stack] [constraints]
---

# FastAPI GenAI Application Patterns

## Scope

This skill extends the core FastAPI skills for GenAI service architecture.

The architecture model used here is a hybrid:

1. Four virtual layers for decoupling and testability.
2. Production AI slices for reliability and operational maturity.

## Workflow

1. Define the four virtual layers: domain, application, infrastructure, interfaces.
2. Keep domain and application decoupled from serving interfaces and infra providers.
3. Define production slices: prompts, agents, services, security, evaluation, observability.
4. Define prompt/context management policy and token budget strategy.
5. Define tool-calling permissions, allowlists, and timeout boundaries.
6. Define fallback strategy (model fallback, cache fallback, degraded response).
7. Define evaluation baseline (quality, latency, cost, safety).
8. Define tracing schema for prompts, tools, and model outputs.

## Guardrails

1. Keep prompts and model outputs out of logs unless explicitly redacted and policy-approved.
2. Keep model routing decisions deterministic where possible.
3. Keep tool execution bounded by timeout and allowlist.
4. Routes and serving adapters must not contain provider-specific orchestration logic.
5. Keep layer labels pragmatic; strict purity can be relaxed when simplicity materially improves delivery.

## Trigger Examples

Should trigger:

- "Design a FastAPI RAG architecture with prompt registry and eval loops."
- "Build an agentic API with tool-calling safety and fallback routing."

Paraphrased should trigger:

- "How should I structure LLM app layers and runtime slices in FastAPI?"

Should not trigger:

- "Implement basic CRUD endpoint status codes only."
- "Prepare deployment pre-flight checklist for go-live."

## Additional Resources

- Single canonical structure doc: [references/architecture-and-domain-genai.md](references/architecture-and-domain-genai.md)
- GenAI layering: [references/genai-layering.md](references/genai-layering.md)
- Hybrid architecture decision guide: [references/hybrid-architecture.md](references/hybrid-architecture.md)
- Production AI slices: [references/production-ai-slices.md](references/production-ai-slices.md)
- Agentic patterns playbook (6 patterns): [references/agentic-design-patterns-playbook.md](references/agentic-design-patterns-playbook.md)
- External tool and agent runtime safety: [references/external-tool-agent-runtime-safety.md](references/external-tool-agent-runtime-safety.md)
- Prompt and tool safety: [references/prompt-tool-safety.md](references/prompt-tool-safety.md)
- Eval baseline: [references/eval-baseline.md](references/eval-baseline.md)

## Validation Expectations

1. Architecture output includes virtual layers plus production slices with clear ownership boundaries.
2. Tool-calling policy includes allowlists, timeout limits, and fallback behavior.
3. Output format must include orchestration flow, safety controls, and eval baseline checkpoints.
4. Edge-case behavior for model outage, tool failure, and prompt budget overrun is documented.
5. Recovery guidance explains degraded-mode response strategy and re-entry to normal operation.
# GenAI Layering

Recommended virtual layers:

- domain layer: entities, prompts, reasoning policy, invariants
- application layer: orchestration, planning, routing, workflow state
- infrastructure layer: models, tools, memory, loaders, storage adapters
- interfaces layer: FastAPI endpoints, MCP servers, CLI commands

Rules:

- routes call application orchestration, not provider SDKs directly
- provider-specific logic stays in infrastructure adapters
- domain and application remain decoupled from interface and provider details
- token and latency budgets are enforced at application boundary

Production AI slices to apply across layers:

- services: rag pipeline, semantic cache, memory, query rewrite, routing
- prompts: versioned, typed, and registered
- agents: grading, decomposition, adaptive routing
- security: input guard, content guard, output guard
- evaluation: golden dataset, offline eval, online monitoring
- observability: per-stage tracing, feedback linkage, cost tracking
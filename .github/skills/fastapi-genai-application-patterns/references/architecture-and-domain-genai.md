# Architecture And Domain For FastAPI GenAI Apps

This is the single canonical structure reference for FastAPI plus GenAI projects.

## Design Model

Use a hybrid model:

1. Virtual layers for dependency control.
2. Production AI slices for runtime completeness.

Virtual layers:

- Domain: entities, prompt intent, reasoning policy, domain rules.
- Application: orchestration, planning, workflow routing, transaction boundaries.
- Infrastructure: model providers, vector stores, memory stores, loaders, external tools.
- Interfaces: FastAPI routes, MCP servers, CLI commands, background workers.

Production AI slices:

- Services: RAG pipeline, semantic cache, memory manager, query rewriter, query router.
- Prompts: versioned templates, typed prompt contracts, prompt registry.
- Agents: decomposition, grading, adaptive routing.
- Security: input guard, content guard, output guard.
- Evaluation: golden dataset, offline eval, online monitoring.
- Observability: per-stage tracing, feedback capture, cost tracking.

## Canonical Folder Shape

Use this structure as the default blueprint. Keep names stable unless existing repo conventions require adaptation.

```text
project/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── schemas.py
│   ├── components/
│   │   ├── hybrid_retriever.py
│   │   └── reranker.py
│   ├── services/
│   │   ├── rag_pipeline.py
│   │   ├── semantic_cache.py
│   │   ├── memory_service.py
│   │   ├── query_rewriter.py
│   │   └── query_router.py
│   ├── prompts/
│   │   ├── templates.py
│   │   └── registry.py
│   ├── agents/
│   │   ├── document_grader.py
│   │   ├── query_decomposer.py
│   │   └── adaptive_router.py
│   ├── tools/
│   │   ├── vector_search.py
│   │   ├── web_search.py
│   │   └── code_search.py
│   ├── security/
│   │   ├── input_guard.py
│   │   ├── content_filter.py
│   │   └── output_filter.py
│   ├── evaluation/
│   │   ├── golden_dataset.json
│   │   ├── offline_eval.py
│   │   └── online_monitor.py
│   └── observability/
│       ├── tracer.py
│       ├── feedback.py
│       └── cost_tracker.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── index_config/
├── scripts/
│   ├── seed.py
│   ├── migrate.py
│   └── healthcheck.py
├── tests/
│   ├── test_retrieval.py
│   ├── test_cache.py
│   ├── test_routing.py
│   └── test_security_filters.py
├── docs/
│   ├── architecture.md
│   ├── api-reference.md
│   └── deployment.md
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Dependency Direction

Allowed direction:

- Interfaces -> Application -> Domain
- Infrastructure implements contracts used by Application

Avoid:

- Domain importing FastAPI or provider SDKs
- Route handlers directly calling provider SDKs
- Prompt strings hardcoded in route files

## FastAPI Integration Rule

Route handlers should:

1. Validate transport contracts.
2. Call application service methods.
3. Translate domain and application errors to API error contracts.

Route handlers should not perform model orchestration directly.

## Prompt Management Rule

- Prompts are versioned and typed.
- Prompt selection happens in application layer.
- Prompt templates are loaded from prompt registry, not inline literals in business code.

## Security Rule

Apply all three guards for model-facing paths:

1. Input guard before orchestration.
2. Content guard on retrieved or generated intermediate content.
3. Output guard before response emission.

## Evaluation Rule

No major GenAI feature ships without:

1. Golden dataset coverage.
2. Offline benchmark pass.
3. Online monitor with latency, quality, and failure indicators.

## Observability Rule

Track at least:

- request and trace IDs
- stage-level latency
- tool and model call metadata
- cost per request class
- user feedback linkage to trace IDs

## Pragmatism Rule

Layer boundaries are guidance for evolvability, not rigid ceremony. Small exceptions are acceptable when they reduce complexity without creating long-term coupling debt.
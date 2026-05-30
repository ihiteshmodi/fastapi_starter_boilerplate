# Agentic Design Patterns Playbook (6 Patterns)

Source inspiration was mapped from Nilay Parikh's agentic pattern series and runnable repos:

- Part 1 repo: https://github.com/nilayparikh/tuts-agentic-ai-examples/tree/main/agents/mono/agent-design-patterns-1
- Part 2 repo: https://github.com/nilayparikh/tuts-agentic-ai-examples/tree/main/agents/mono/agent-design-patterns-2

Use this as an implementation bridge for FastAPI GenAI apps.

## 01. Single Agent

When to use:

- one bounded problem domain
- low orchestration complexity

FastAPI shape:

- one route -> one application service -> one agent runtime
- tool calls stay local and bounded by timeout/allowlist

Exit criteria to upgrade:

- tool list keeps growing
- prompts become overloaded with routing logic

## 02. Sequential Agents

When to use:

- deterministic multi-step pipeline
- each step enriches context for next step

FastAPI shape:

- orchestrator service executes step order explicitly
- each step emits a typed payload consumed by next step

Guardrails:

- enforce per-step timeout and circuit-breaker/fallback
- persist step-level trace data for replay

## 03. Parallel Agents

When to use:

- independent subtasks that can run concurrently
- latency target is dominated by slowest branch

FastAPI shape:

- one orchestrator launches bounded concurrent calls
- fan-in synthesizer combines branch outputs into final response

Guardrails:

- cap concurrency and payload size
- define partial-failure policy (best effort vs strict fail)

## 04. Coordinator Routing

When to use:

- user intents vary and best specialist is dynamic
- hardcoded pipeline causes low relevance

FastAPI shape:

- coordinator classifies intent then routes to specialist service
- specialists expose a stable contract so routing can evolve safely

Guardrails:

- maintain deterministic fallback route when confidence is low
- log route decision and reason code for auditability

## 05. Agent-as-Tool

When to use:

- primary agent should retain control while specialists act as functions
- need composability without handing over full dialogue state

FastAPI shape:

- primary runtime exposes tool schema mapped to specialist adapters
- adapter calls specialist agent endpoints and returns structured tool output

Guardrails:

- tool argument validation before execution
- strict allowlist of callable specialist tools

## 06. Loop And Critique

When to use:

- quality is more important than single-pass latency
- output needs iterative refinement and explicit quality gates

FastAPI shape:

- orchestrator runs generate -> critique loop with max-iteration bound
- stop on PASS; otherwise inject critique into next generation turn

Guardrails:

- hard max iterations and request deadline
- return best-known output with status when budget is exhausted

## Pattern Selection Heuristic

- start with Single Agent
- move to Sequential when order matters
- move to Parallel when branches are independent
- add Coordinator when intent routing is dynamic
- use Agent-as-Tool when one primary planner should stay in control
- add Loop And Critique when quality gates are mandatory

## FastAPI Integration Checklist

- attach request ID and trace context at middleware layer
- keep orchestration in application services, not route handlers
- define typed request/response contracts between agents
- enforce timeout, retry budget, and fallback per agent call
- emit structured logs for each orchestration step and final decision

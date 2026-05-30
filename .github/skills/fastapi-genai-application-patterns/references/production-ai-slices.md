# Production AI Slices

This section defines mandatory AI slices that run through the layer model.

## Services Slice

Core runtime units:

- rag pipeline
- semantic cache
- conversation memory
- query rewriter
- query router

## Prompts Slice

Prompt assets must be:

- versioned
- typed by use-case
- centrally registered

## Agents Slice

Agent behaviors should include:

- document grading
- query decomposition
- adaptive source or tool routing

## Security Slice

Three guards are required:

- input guard
- content guard
- output guard

## Evaluation Slice

Evaluation stack should include:

- golden dataset
- offline batch evals
- online monitors and drift checks

## Observability Slice

Track per stage:

- traces and spans
- user or operator feedback linked to traces
- latency and cost per request class
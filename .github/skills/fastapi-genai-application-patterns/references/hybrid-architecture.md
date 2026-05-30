# Hybrid Architecture Decision Guide

Use a hybrid structure for GenAI FastAPI systems:

1. Virtual layers to keep dependencies healthy.
2. Production slices to ensure operational completeness.

Why this works:

- Virtual layers prevent dependency sprawl and improve refactor safety.
- Production slices ensure teams do not skip critical AI runtime concerns like evaluation and observability.

Pragmatic rule:

- Layering is a thinking tool, not strict dogma.
- Allow tactical exceptions for simplicity, but keep coupling intentional and visible.

Decision checks:

- Can models or tools be swapped without changing route handlers?
- Can orchestration evolve without changing serving contracts?
- Can evaluation and observability be run independently of interface layer changes?
- Can security guards be upgraded without rewriting business flows?
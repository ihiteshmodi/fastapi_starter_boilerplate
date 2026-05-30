# Test Pyramid Policy

- Unit tests: many, fast, cheap.
- Integration tests: moderate amount for cross-component behavior.
- End-to-end tests: few, focused on critical user flows.

LLM agent policy:

- For every important function, generate at least one meaningful unit or integration test.
- Full TDD cycle is preferred but optional for token efficiency.
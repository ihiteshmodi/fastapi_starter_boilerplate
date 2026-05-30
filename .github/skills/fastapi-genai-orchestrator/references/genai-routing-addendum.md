# GenAI Routing Addendum

Use fastapi-genai-application-patterns when prompts contain:

- "build AI app"
- "add LLM workflow"
- "agentic endpoint"
- "RAG service"
- "tool calling"
- "AI architecture layers"
- "agent project structure"
- "evaluation and observability for LLM app"

For full builds, use this order:

1. fastapi-foundation-contracts
2. fastapi-auth-security
3. fastapi-data-crud-patterns
4. fastapi-integration-reliability
5. fastapi-genai-application-patterns
6. fastapi-testing-quality
7. fastapi-observability-operations
8. fastapi-release-gates

Structure policy for GenAI builds:

1. Apply virtual layers: domain, application, infrastructure, interfaces.
2. Apply production slices: services, prompts, agents, security, evaluation, observability.
3. Keep route handlers in interface layer thin and provider-agnostic.
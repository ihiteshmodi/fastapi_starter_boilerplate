# Routing Matrix

Use this matrix to select side skills.

- Full backend build request -> foundation, auth, data, integration, testing, observability, release
- "Scaffold first, harden auth later" -> foundation plus auth-placeholder mode, then data/integration/genai/testing/observability, then release review
- "Set up auth" -> fastapi-auth-security
- "Design CRUD" -> fastapi-data-crud-patterns
- "Harden API calls" -> fastapi-integration-reliability
- "Design async long-task APIs (202 + task status)" -> fastapi-integration-reliability
- "Build LLM/RAG/agentic APIs" -> fastapi-genai-application-patterns
- "Write tests" -> fastapi-testing-quality
- "Add logs/metrics/traces" -> fastapi-observability-operations
- "Prepare deployment" -> fastapi-release-gates

If request spans multiple domains, route sequentially by stage order.
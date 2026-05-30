# Prompt and Tool Safety

Prompt policy:

- separate system policy from user input
- sanitize and bound context windows
- include provenance metadata for retrieved context

Tool policy:

- allowlist tool catalog by route or user role
- enforce per-tool timeout and retry policy
- validate tool outputs before returning to model or client
- never execute unrestricted shell/database actions from model output without policy checks
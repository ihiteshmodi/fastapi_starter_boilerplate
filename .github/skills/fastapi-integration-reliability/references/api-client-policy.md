# API Client Policy

- Always set timeout values.
- Always validate response status.
- Always handle network exceptions explicitly.
- Keep client-specific exceptions mapped to stable API error codes.
- Use context-managed or lifespan-managed clients for proper cleanup.
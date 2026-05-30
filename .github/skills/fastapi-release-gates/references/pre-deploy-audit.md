# Pre-Deploy Audit

Code review:

- endpoints work locally
- status/error handling is consistent
- no debug print leftovers

Security:

- passwords hashed
- API keys and secrets from environment
- CORS policy reviewed
- no sensitive data in repository history

Database:

- migrations committed and reviewed
- no test data in production schema
- pooling and backup posture documented
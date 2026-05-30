# JWT Baseline

Required endpoints:

1. POST /auth/register
2. POST /auth/login
3. GET /users/me
4. PATCH /users/me

Policy:

- Passwords hashed with bcrypt or equivalent strong hash.
- Access tokens include exp claim.
- Signing secret is strong and environment-provided.
- Protected endpoints require auth dependency chain.
- Use identical error message for invalid credentials scenarios.
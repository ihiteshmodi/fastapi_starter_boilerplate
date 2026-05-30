# Status Contract

- 200 for successful reads and standard success responses.
- 201 for successful creates.
- 202 for accepted long-running tasks that continue asynchronously (return task_id).
- 204 for successful no-body operations, especially delete by default.
- 400 for validation/request-shape failures.
- 401 for unauthenticated requests.
- 403 for authenticated but unauthorized requests.
- 404 for missing resources.
- 409 for optimistic locking and conflict cases.
- 500 for unexpected server-side failures.

Use the most specific code for each failure path.
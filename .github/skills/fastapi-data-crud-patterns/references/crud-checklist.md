# CRUD Checklist

- Create returns 201 and created resource payload.
- Update semantics distinguish PUT vs PATCH.
- PATCH only applies provided fields.
- Delete uses 204 by default.
- Soft delete policy documented where applicable.
- Error semantics are consistent across CRUD endpoints.
- Validation schemas cover input boundaries.
# Soft Delete And Audit Semantics

Use soft delete by default for business records unless hard delete is explicitly required.

## Contract

- soft delete sets is_deleted flag and deleted_at timestamp
- delete endpoint behavior remains consistent with API status contract
- default queries exclude deleted rows unless explicitly requested

## Audit Fields

Track at minimum:

- created_at, created_by
- updated_at, updated_by
- deleted_at, deleted_by
- optional delete_reason

## Restoration Policy

- define restore endpoint or service operation if business requires recovery
- restore clears deletion markers and writes restore audit event
- restoration permissions should be stricter than standard update permissions

## Filtering Defaults

- list and get operations default to active records only
- admin/audit views may include deleted records via explicit filter

## Guardrails

- do not physically delete records in standard flow
- keep referential integrity behavior clear for deleted parents/children
- never mix hard and soft delete semantics in same endpoint contract
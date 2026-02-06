API JSON contracts

This folder contains API-level JSON contracts and conventions used across Project Chimera.

Files:

- `error_model.schema.json`: canonical error response schema (see below).

Conventions:

- Successful responses return objects defined in the per-endpoint schemas under `specs/schemas/`.
- Errors return HTTP status codes and a body conforming to `error_model.schema.json`.
- Validation failures should use `400` with `error` = "validation_error" and `details` containing field-level messages.
- Authentication/authorization errors should use `401`/`403` with `error` values of "unauthorized" or "forbidden".

Example error body:

```json
{
  "error": "validation_error",
  "error_description": "One or more fields are invalid",
  "code": 400,
  "details": {"title": "must not be empty"}
}
```

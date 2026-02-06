Initial migrations for Project Chimera

This folder contains baseline SQL migration files useful for bootstrapping a Postgres-compatible database.

Guidance:
- These files are plain SQL and intended as a starting point. We recommend using a migration tool such as `alembic` (for SQLAlchemy) or a simple numbered migrations runner in CI.
- To apply (Postgres example):

```bash
psql $DATABASE_URL -f specs/migrations/001_create_schema.sql
```

- To roll back: write a corresponding `002_drop_schema.sql` that drops objects in reverse order, or use a migration tool that supports transactional rollbacks.
- Keep migration files immutable once applied to a production database; create new numbered migration files for subsequent changes.

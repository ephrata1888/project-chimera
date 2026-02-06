# Data Lifecycle — Project Chimera

Purpose: describe how data moves through the system, retention, ownership, and governance checkpoints.

Stages:

- Ingest
  - Source: trend fetchers, agent outputs, human uploads, integrations.
  - Raw data stored in `raw` bucket/table with source metadata and immutable audit fields.
  - Retention: raw data retained for 90 days by default.

- Normalization
  - Transform raw inputs into canonical `content` records (see `content` table schema).
  - Metadata normalization includes language, inferred audience, and content tags.

- Drafting (Agent-generated)
  - Agents write `content` records in `draft` state with `agent_id` provenance.
  - Human-in-the-loop or automated checks mark entries for validation.

- Validation
  - `validation` records store checker name, issues, and status (pending/approved/rejected).
  - Validation can be manual (human reviewer) or automated (toxicity, copyright, brand-safety).

- Approval
  - `content.status` moves to `approved` when all required checks pass.
  - Approval events are recorded in `publish_log` with scheduled or immediate publishing metadata.

- Publishing
  - `publish_log` tracks each publish attempt and the external response payload.
  - Retries follow exponential backoff; failures mark `publish_log.status` = `failed` and generate an incident record.

- Archival & Deletion
  - Published content archived after 1 year; archived copies stored in cold storage with read-only access.
  - Deletion requests follow policy: soft-delete (mark as deleted) retained for 30 days before permanent purge.

Governance & Audit

- All state transitions must be auditable: include actor (`agent_id` or user id), timestamp, and reason.
- Access control: role-based access to read/write/approve/publish operations; agents have scoped credentials.
- Privacy: PII discovered during validation must be redacted and flagged; retention for PII follows compliance rules.

Assumptions

- Default retention durations are configurable per-environment.
- External channel responses can contain arbitrary JSON; store them in `publish_log.response` as JSONB.

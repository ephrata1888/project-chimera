# Project Chimera — OpenClaw Integration Specification

## Purpose

Define how Chimera agents broadcast **availability and operational status** to external agent ecosystems such as OpenClaw.

---

## Agent Status States

* AVAILABLE
* BUSY
* PAUSED
* HUMAN_REVIEW

---
## Overview

This document describes a robust, auditable, and privacy-preserving plan for publishing agent availability and operational status from Project Chimera into the OpenClaw network. The goal is to enable coarse-grained ecosystem coordination while preserving internal governance, preventing leakage of sensitive data, and providing operational observability.

Key decisions at a glance:

- Transport: HTTPS POST to an OpenClaw ingestion endpoint (or local OpenClaw proxy) with authenticated requests.
- Message schema: compact JSON with strict allowed fields and a versioned schema.
- Cadence: periodic heartbeats plus event-driven updates on state changes.
- Security: mutual authentication via mTLS or bearer tokens, optional message signing (JWS) for non-repudiation.
- Safety: redact any internal-only fields; publish only informational metadata.

---

## Message Schema (v1)

All messages MUST conform to the following JSON Schema (versioned). Fields not in the schema MUST be rejected by the publisher.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Chimera Agent Status v1",
  "type": "object",
  "properties": {
    "schema_version": { "type": "string", "const": "openclaw-status.v1" },
    "message_id": { "type": "string" },
    "agent_id": { "type": "string" },
    "status": { "type": "string", "enum": ["AVAILABLE","BUSY","PAUSED","HUMAN_REVIEW"] },
    "capabilities": { "type": "array", "items": { "type": "string" } },
    "last_updated": { "type": "string", "format": "date-time" },
    "uptime_s": { "type": "number" },
    "notes": { "type": "string" }
  },
  "required": ["schema_version","message_id","agent_id","status","last_updated"],
  "additionalProperties": false
}
```

Field notes:

- `message_id`: UUIDv4 for idempotency and traceability.
- `uptime_s`: optional integer indicating agent uptime.
- `notes`: optional human-readable short message (no internal decision data allowed).

---

## Transport & Endpoint

- Primary: POST JSON to `https://openclaw.example.org/ingest/chimera-status` (or an operator-controlled OpenClaw proxy).
- Alternate (local): publish to a local MCP/OpenClaw proxy running on loopback; useful for development and private networks.
- Request content-type: `application/json`; responses expected: 2xx on success; non-2xx with JSON error on failure.

Example POST (curl):

```bash
curl -X POST https://openclaw.example.org/ingest/chimera-status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENCLAW_TOKEN" \
  -d '{"schema_version":"openclaw-status.v1","message_id":"...","agent_id":"chimera_planner_01","status":"AVAILABLE","capabilities":["trend_analysis"],"last_updated":"2026-02-06T12:00:00Z"}'
```

---

## Authentication & Message Integrity

Support for one of the following operator-configured methods (choose one per deployment):

1. Mutual TLS (mTLS): preferred for strong mutual authentication in production. Certificates managed by ops.
2. Bearer token (short-lived): token provided by OpenClaw; rotate via secret manager.
3. JWS signing: sign the payload with a private key and include `X-Signature` header (useful for additional non-repudiation).

Implementation guidance:

- Do not include credentials or secrets in the payload.
- Validate the server certificate and reject connections to unknown hosts.
- Rotate keys and tokens using the org's secret management workflow; do not store plaintext tokens in repo.

---

## Cadence & Rate Limits

- Heartbeat cadence (default): publish a heartbeat every 60 seconds while `AVAILABLE` or `BUSY`.
- State-change events: publish immediately when the agent transitions between states (e.g., AVAILABLE -> HUMAN_REVIEW).
- Backoff: on transient network errors, retry with exponential backoff (initial 1s, multiplier 2x, max 5 retries). After max retries, mark status locally as `PAUSED` and emit an internal alert.
- Rate limits: do not exceed 60 messages/minute per agent; aggregate multiple rapid state changes into a single update if they occur within 5 seconds.

---

## Idempotency & Ordering

- Each message MUST include `message_id` (UUID) and `last_updated` timestamp.
- Receivers should use `message_id` to deduplicate and `last_updated` to order messages from the same `agent_id`.

---

## Safety & Privacy

- Prohibited fields: internal decision rationale, task inputs/outputs, credentials, unpublished content, PII.
- `notes` must be short (<= 256 chars) and must not contain URLs to internal resources.
- Any attempt to send additional properties will be rejected by validation.

---

## Error Handling & Observability

Publishing layer must record the following local telemetry:

- `status_publish_attempts_total` (counter)
- `status_publish_success_total` (counter)
- `status_publish_failures_total` (counter) with `reason` label
- Last successful publish timestamp per `agent_id`

Logs:

- Structured logs for each publish attempt including `message_id`, `agent_id`, `status`, `http_status`, and `error` if any.

Alerts:

- Alert if an agent records 3 consecutive publish failures or if the local publish queue grows beyond a configured threshold.

---

## Testing & Validation

Unit / Integration tests to include:

- JSON Schema validation tests for example messages (valid and invalid payloads).
- Transport tests: send to a local OpenClaw test harness that simulates 2xx, 4xx, 5xx responses and validates retries and backoff.
- Security tests: verify mTLS and bearer token flows in staging.
- Fuzz tests: ensure additional properties are rejected.

Acceptance criteria:

- Heartbeat messages appear on the OpenClaw ingestion endpoint within 60 ± 5 seconds while agent is AVAILABLE.
- State-change messages are delivered within 5 seconds in normal network conditions.
- No rejected messages due to schema violations under normal operation.

---

## Rollout Plan

1. Development: run a local OpenClaw proxy; publish to loopback; run schema tests.
2. Staging: enable authenticated publishing (bearer token or mTLS) to a staging OpenClaw endpoint; run integration and security tests.
3. Canary: enable publishing for a small subset of agents (10%) in production; monitor errors and telemetry for 48 hours.
4. Full rollout: enable publishing for all agents once canary is stable and no critical issues found.

Rollback criteria:

- Repeated authentication failures, schema rejections, or spikes in publish failures beyond predefined thresholds.

---

## Developer Checklist (pre-deploy)

- [ ] Implement message serialization that enforces the schema (reject unknown fields).
- [ ] Integrate chosen auth method and verify token/key rotation works.
- [ ] Implement exponential backoff with jitter and maximum retry caps.
- [ ] Emit structured telemetry and ensure integration with operator dashboards.
- [ ] Provide a toggle to disable external publishing for maintenance/testing.

---

## Example Minimal Payload

```json
{
  "schema_version": "openclaw-status.v1",
  "message_id": "b6f9e3f8-2d3a-4e6a-9f12-0d3a1b2c3d4e",
  "agent_id": "chimera_planner_01",
  "status": "AVAILABLE",
  "capabilities": ["trend_analysis","campaign_planning"],
  "last_updated": "2026-02-06T12:00:00Z",
  "uptime_s": 3600
}
```

---

## Open Questions / [NEEDS CLARIFICATION]

- Q1: Which authentication method should be the default for production (mTLS or bearer tokens)?
  - A: mTLS provides stronger mutual auth; bearer tokens are easier for short-term testing.

Limit clarifications to the most impactful items; if you prefer, I can open a separate `/speckit.clarify` flow to gather answers from stakeholders.


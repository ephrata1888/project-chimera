# Project Chimera — Functional Specification

## Specification Style

All requirements are written as **agent‑centric user stories** describing WHAT the agent must achieve and the observable outcomes. Acceptance criteria are explicit and testable.

---

## Trend Analysis (Planner Agent)

- As a **Planner Agent**, I fetch trends from configured sources so that the system proposes timely topics.
	- Acceptance: `fetch_trends(source)` returns a list of trends with `name` and `score` and `source` metadata.
- As a **Planner Agent**, I filter and rank trends by persona relevance and publisher constraints.
	- Acceptance: ranking includes `relevance_score` and respects persona blocklists.

---

## Content Generation (Worker Agent)

- As a **Worker Agent**, I generate caption and script drafts for an approved trend and persona.
	- Acceptance: `generate_content(trend, persona)` returns `caption`, `script`, `confidence_score`, and `flags`.
- As a **Worker Agent**, I attach metadata (trend source, timestamps, content_id).
	- Acceptance: every draft includes `content_id` and `metadata.trend.source`.

---

## Validation & Safety (Judge Agent)

- As a **Judge Agent**, I validate generated drafts for policy and persona alignment before publishing.
	- Acceptance: `validate_content(content)` returns `ok: bool`, `issues: []`, and `score`.
- As a **Judge Agent**, I escalate content with high-risk flags to human review.
	- Acceptance: content with `sensitivity` or `low_confidence` produces an audit entry and a human review ticket.

---

## Publishing (Publisher Agent / Worker Agent)

- As a **Publisher Agent**, I schedule and push approved content to platform APIs under the configured persona accounts.
	- Acceptance: publish returns `platform_response`, `published_at`, and `publish_id` and records `publish_log`.
- As a **Planner Agent**, I may cancel or re-schedule pending publishes.
	- Acceptance: cancellations update the `publish_log` and surface the result to observability.

---

## Observability & Auditing (Operator)

- As a **Human Operator**, I must see the plan, inputs, validation results, and final publish artifacts for every published item.
	- Acceptance: UI or API exposes `content_id -> audit trail` with timestamps and actor IDs.
- As an **Operator**, I receive alerts on failed validations, publish errors, or suspicious activity.
	- Acceptance: alerting contains context and a link to the audit record.

---

## Example End-to-End User Story

- As a **Planner Agent**, I fetch top trends, rank them for `persona: brandX`, propose the top 3 to the Worker Agent. Worker generates drafts; Judge validates; one draft passes and Publisher posts it. The entire plan and verdicts are stored in the audit log.


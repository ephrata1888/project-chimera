# Rule Creation Intent — Project Chimera

Purpose: define how users or operators create governance rules that agents use for content filtering, validation, and publication decisions.

Actors

- Policy Author: human who drafts and approves rules.
- Validator Agent: automated checks that execute rules.
- Reviewer: human who reviews rule effects and exceptions.

Rule Model

- `rule_id`: stable identifier
- `name`: short descriptive name
- `description`: human-readable rationale
- `trigger`: event that causes rule evaluation (e.g., "on_content_create", "on_publish_attempt")
- `conditions`: structured predicates (field, operator, value) evaluated against `content` and `metadata`
- `actions`: one or more actions (e.g., `block`, `flag`, `add_issue`, `require_human_review`, `auto_approve`)
- `priority`: integer to resolve conflicts
- `owner`: `agent_id` or user id who owns the rule
- `enabled`: boolean

Creation Workflow

1. Draft: Policy Author creates a rule via UI or JSON payload. Draft saved but not active.
2. Test: Author runs rule against sample content (sandbox) to see matched examples and potential false positives.
3. Review: Reviewer inspects test results and either approves or requests changes.
4. Publish: On approval, rule `enabled=true` and becomes active for matching triggers.
5. Monitor: System logs matches and provides an audit trail; owners notified of high-match rates.

Validation & Safety

- Rules must be syntactically validated before saving; condition operators are limited to a safe subset (`==`, `!=`, `contains`, `in`, `regex`, numeric comparisons).
- Reject rules that reference non-existent fields or use unsafe constructs (no arbitrary code execution).

Rule Examples

- Block profanity:

```json
{
  "name": "block-profanity",
  "trigger": "on_content_create",
  "conditions": [{"field":"body","operator":"regex","value":"(badword1|badword2)"}],
  "actions": ["block","add_issue"],
  "priority": 100
}
```

- Require human review for political content:

```json
{
  "name": "political-review",
  "trigger": "on_content_create",
  "conditions": [{"field":"metadata.topics","operator":"contains","value":"politics"}],
  "actions": ["require_human_review"],
  "priority": 80
}
```

Audit & Traceability

- Every rule evaluation produces a `rule_match` event stored with `content_id`, `rule_id`, `timestamp`, `result`, and `details`.
- Changes to rules are versioned with author, timestamp, and change summary.

Success Criteria

- Authors can create and test rules without editing code.
- No rule can execute arbitrary code; only declarative conditions/actions allowed.
- Rule test coverage reports show example matches and false-positive/false-negative indicators.

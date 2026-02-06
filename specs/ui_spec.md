# UI Specification — Project Chimera

Purpose: provide a concise, stakeholder-focused UI spec for the minimal web dashboard used by human reviewers and operators.

Audience: content managers, human validators, system operators.

Pages / Views

- Dashboard (Home)
  - Purpose: quick operational snapshot.
  - Components: agents summary (count by state), content pipeline counters (draft/pending/approved/published), recent publish_log entries, system alerts.
  - Actions: open validation queue, open content editor, view agent details.

- Content Editor
  - Purpose: view and edit agent-generated drafts, run validations, request human review.
  - Components: title, rich-text editor for `body`, metadata editor (tags, audience), preview pane (rendered output), validation panel (list of checks and issues), save button, request-review button.
  - Data: binds to `content` schema fields (`id`, `title`, `body`, `metadata`, `status`, `agent_id`).

- Validation Queue
  - Purpose: list items awaiting validation/approval.
  - Components: filter by check type, list with status badges, quick actions (approve, reject, add-issue, escalate), pagination.
  - UX: clicking an item opens the Content Editor focused on validation panel.

- Publish Scheduler
  - Purpose: schedule publishing to channels and view publish history.
  - Components: channel selector, schedule datetime picker, immediate publish toggle, publish history list (from `publish_log`).

- Agent Monitor
  - Purpose: inspect agent status and recent activity.
  - Components: agent list with state, last_heartbeat, uptime; click to open agent detail with metrics chart and recent actions.

Design & Interaction Notes

- Accessibility: follow standard keyboard navigation and ARIA roles for lists, dialogs, and forms.
- Security: role-based UI controls — only users with `publisher` role see publish actions; reviewers see validate actions.
- Autosave: content editor autosaves drafts every 10s.

Acceptance Criteria (UI-level)

- Users can see pipeline counts on Dashboard within 2s of page load for small test dataset.
- Reviewer can approve or reject a validation item and cause `validation` and `content.status` to update.
- Schedule publish persists an entry in `publish_log` with correct `scheduled_at`.

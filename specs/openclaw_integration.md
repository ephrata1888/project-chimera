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

## Status Payload Format

```json
{
  "agent_id": "chimera_planner_01",
  "status": "AVAILABLE",
  "capabilities": ["trend_analysis", "campaign_planning"],
  "last_updated": "ISO‑8601"
}
```

---

## Safety Constraints

* No internal decision logic may be shared
* No credentials or unpublished content may be exposed
* Status updates are informational only

---

## Design Intent

This integration enables **ecosystem‑level coordination** without sacrificing Chimera’s internal governance or safety guarantees.

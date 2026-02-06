# Project Chimera — Meta Specification

## Vision

Project Chimera is an Autonomous Influencer System that transforms topical signals into short-form social content through governed automation. The system balances creativity and safety by requiring explicit, auditable plans, human review for sensitive decisions, and verifiable traces of every agent action.

## Core Principles

- Specs are authoritative: the `specs/` directory is the single source of truth for agent behavior.
- Traceability: every non-trivial action must be accompanied by a short plan and provenance metadata.
- Safety-by-design: safety checks and policy validation run before any publish action.
- Least privilege: agents run with minimum required permissions and access to secrets is controlled by the operator.
- Human oversight by exception: humans intervene when confidence is low or when content touches sensitive domains.

## Hard Constraints (Non-Negotiable)

- Agents MUST NOT generate or publish code without an approved spec.
- Agents MUST NOT publish content without passing the `validation` checks specified in `specs/`.
- Agents MUST only operate within declared scopes (accounts, personas, platforms).
- All actions that change repository or published state require an explicit plan logged in the audit trail.

## Non-Goals

- This project does not aim to build fully autonomous, unsupervised agents.
- It is not a general-purpose conversational assistant or chatbot platform.
- It will not make legal or medical decisions without human review.

## Success Definition

Project success is measured by the following outcomes:

- Accuracy: 95% of published content passes post-publish audits for persona alignment and policy compliance.
- Safety: 0 critical safety incidents caused by autonomous publishing in production.
- Traceability: every published item includes a verifiable audit record linking the agent plan, inputs, validations, and final artifact.
- Velocity: the system reduces time-to-publish for validated content by at least 40% compared to manual workflows.

## Stakeholders

- Product / Content Strategists — define personas and editorial rules.
- Engineers — implement agents and CI.
- Safety / Policy — author validation rules.
- Operations — manage credentials and deployment.

## Compliance & Privacy Notes

- Credentials and tokens must be stored in a secrets manager; never checked into source control.
- Personal data must be handled according to applicable privacy regulations; redact or obtain consent before publishing.


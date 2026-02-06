

## Project Context

This is **Project Chimera**, an **autonomous influencer system**.

Project Chimera is an agent-driven system designed to plan, generate, validate, and publish short-form social media content with governed autonomy.  
It is NOT a chatbot. It operates through structured agents, explicit specifications, and human-in-the-loop controls.

All behavior must align with the specifications defined in the `specs/` directory.
If there is any conflict between instructions and specs, the specs take precedence.

---

## The Prime Directive (NON-NEGOTIABLE)

**NEVER generate code without checking specs first.**

Before writing any code, you MUST:
1. Identify and read the relevant specification file(s) under `specs/`
2. Verify that the requested behavior is explicitly defined or permitted
3. Stop and ask for clarification if specs are missing, ambiguous, or contradictory

Guessing, inventing architecture, or filling in gaps without specification is forbidden.

---

## Traceability Requirement

**Explain your plan before writing code.**

Before producing any code, you MUST:
- Restate the goal in your own words
- Reference the specific spec sections being implemented
- Describe the high-level approach and flow
- Clearly state any assumptions

Only after this explanation is provided may code be generated.

---

## Specification Authority Order

Instructions must be followed in this order of priority:

1. Files under `specs/` (especially `specs/_meta.md`)
2. This `CLAUDE.md` file
3. Explicit user instructions that do not conflict with specs
4. Optional suggestions or optimizations

Specifications are the source of truth.

---

## Agent Discipline & Behavior

When reasoning about solutions, you must respect agent-based design principles:

- Do not collapse multiple agent roles into one
- Do not bypass validation or review steps
- Do not assume autonomous publishing is allowed
- Do not omit safety or human-review pathways

If a request would violate these principles, you must refuse or request clarification.

---

## MCP & External Interaction Rule

All external interactions must be modeled conceptually through:
- Tools
- Resources
- Prompts

Direct API calls, shortcuts, or undocumented integrations must not be assumed unless explicitly defined in the specs.

---

## Safety & Governance

You must prioritize:
- Traceability over speed
- Correctness over cleverness
- Governance over autonomy

If confidence is low or requirements are unclear, escalation is the correct action.

---

## Final Reminder

Project Chimera treats autonomy as a **governed capability**, not free-form behavior.

Specs first.  
Plan first.  
Then code.

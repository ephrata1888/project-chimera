# Chimera Agent Skills

This directory contains declarative skill definitions for the Chimera Agent. A "Skill" is a self-contained capability package that exposes a clear Input/Output contract so it can be composed safely by higher-level planners.

Each skill listed below includes: name, purpose, inputs, outputs, side effects, preconditions, and error conditions. Implementations should strictly follow these contracts.

---

## skill_fetch_content

- Purpose: Retrieve content from external sources (web pages, social posts, YouTube links, RSS feeds) and normalize it for downstream processing.
- Inputs:
  - `source_type` (string) — one of `"web" | "youtube" | "rss" | "social"`
  - `source_id` (string) — URL or provider-specific identifier
  - `options` (object, optional) — e.g., `{ "max_bytes": 500000, "format": "text|html|json" }`
- Outputs (success):
  - `ok: true`
  - `content` (string | object) — normalized text or structured JSON depending on `options.format`
  - `metadata` (object) — `{ "source_type", "source_id", "fetched_at", "content_type", "size_bytes" }`
- Error outputs:
  - `ok: false`, `error` (string), optional `http_status` (int)
- Side effects: none (should not write to disk by default). Implementations may cache results when configured; cache location and TTL must be configurable.
- Preconditions: network access; if a provider requires auth, credentials must be supplied via environment/secret store and declared in the plan.

---

## skill_transcribe_audio

- Purpose: Convert audio (local file or remote URL) into time-aligned text transcripts for downstream summarization and captioning.
- Inputs:
  - `audio_source` (string) — local path or URL
  - `language` (string, optional) — ISO language code, default `auto`
  - `options` (object, optional) — e.g., `{ "timestamps": true, "words": true, "max_duration_s": 1800 }`
- Outputs (success):
  - `ok: true`
  - `transcript` (string) — full transcript text
  - `segments` (array, optional) — list of `{ start_s, end_s, text }` if timestamps requested
  - `confidence` (float, 0..1, optional)
- Error outputs:
  - `ok: false`, `error` (string), optional `code` (string)
- Side effects: may upload audio to external transcription provider when required; caller must declare consent and credentials in the plan.
- Preconditions: audio must be accessible and within allowed duration; external API keys must be available if using cloud services.

---

## skill_git_operations

- Purpose: Perform scoped git operations on the repository (status, diff, add, commit, rev-parse). This skill is the programmatic abstraction over the `git-mcp` service.
- Inputs:
  - `op` (string) — one of `"status" | "diff" | "add" | "commit" | "rev-parse"`
  - `path` (string, optional) — repository-relative path for operation (default repository root)
  - `args` (object, optional) — operation-specific arguments, e.g. `{ "files": ["f1","f2"], "message": "..." }`
- Outputs (success):
  - `ok: true`
  - `result` (object) — raw command output, e.g. status lines, diff text, commit SHA
  - `metadata` (object) — `{ "returncode": 0, "command": "git commit -m ..." }`
- Error outputs:
  - `ok: false`, `error` (string), optional `returncode` (int)
- Side effects: may modify repository state (`git add`, `git commit`); callers must include an explicit plan and approval step before invoking write operations (see Prime Directive in CLAUDE.md).
- Preconditions: running on a git repository; caller must ensure the working tree state is acceptable and that any credentials for remote pushes are configured separately.

---

Notes:
- Implementation guidance: each skill should expose a thin HTTP or RPC shim that strictly validates inputs and returns only the declared outputs.
- Testing: tests should include contract tests validating both success and error outputs for representative inputs.
- Security: any skill that touches external networks or secrets must document required environment variables and validation steps in its own subdirectory README before implementation.

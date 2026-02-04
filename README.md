# Project Chimera

**Role:** Forward Deployed Engineer (FDE) Trainee
**Mission:** Build the foundation for an Autonomous AI Influencer

## Overview

Project Chimera is a spec-driven, agent-ready Python environment designed for AI agents to operate autonomously. It integrates **Tenx MCP Sense** for activity logging and uses **uv** for reproducible dependency management. The repository is structured to support **specs, agent skills, tests, and CI/CD**, providing a robust, future-proof development environment.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/ephrata1888/project-chimera.git
cd project-chimera
```

2. Install dependencies and create a virtual environment:

```bash
pip install uv
uv venv
.venv\Scripts\activate   # Windows
```

3. Initialize project:

```bash
uv init
uv add fastapi uvicorn   # optional
```

4. Configure Tenx MCP:

* `.vscode/mcp.json` contains server settings
* Start MCP server in VS Code and authenticate via GitHub

## Structure

* `specs/` — project specifications
* `skills/` — agent skills definitions
* `tests/` — failing tests for TDD
* `pyproject.toml` & `uv.lock` — environment config
* `Dockerfile` & `Makefile` — containerization and automation

## Notes

* Commit early and often
* Activate `.venv` before running Python commands
* MCP logs provide traceability for all work

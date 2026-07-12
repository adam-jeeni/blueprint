# blueprint

**Convention-over-configuration methodology for AI-human software development.**

Blueprint gives you a fixed project structure, a set of documents, and a defined
lifecycle — so every AI agent that opens your project knows exactly what to do
without being told. No CLI, no build step, no package installation. Just open the
project and start building.

## Quick start

1. Open a fresh directory with your AI agent.
2. Load the project initialization agent: `agents/prompts/project-init.md`
3. The agent will assess your project state and scaffold the full Blueprint
   convention structure, including backend and frontend scaffolding.
4. Start a **fresh session** in the same directory. `AGENTS.md` will detect the
   convention and route your agent into the standard feature lifecycle.

## What's inside

| File / directory | Purpose |
|---|---|
| `AGENTS.md` | Lifecycle engine — the first file every agent reads |
| `METHODOLOGY.md` | Agent reference — what goes in every template section |
| `agents/prompts/` | Role prompts — orchestrator, schema, backend, frontend, etc. |
| `docs/` | Standing documents — architecture, data dictionary, user guide |
| `specs/` | Feature specs — problem statement through shipped code |
| `backend/` | Python FastAPI service with Alembic migrations |
| `frontend/` | TypeScript React service with Playwright E2E tests |
| `docker/` | Per-service Dockerfiles for containerized development |

## Agent-agnostic

Built to work with any AI coding agent. No tool-specific syntax in the prompts.
The convention is encoded in the folder structure, not in configuration files.

## Documentation

- **`blueprint-methodology-v4.md`** — Full human-readable guide: how it works, why it works, getting started, worked example.
- **`METHODOLOGY.md`** — Agent reference: what goes in every template section. For AI agents, not humans.
- **`AGENTS.md`** — Lifecycle engine. The first file every agent reads.

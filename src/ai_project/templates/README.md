# blueprint

**Convention-over-configuration methodology for AI-human software development.**

AI coding agents fail from underspecified prompts. Blueprint gives you a fixed project structure,
a set of documents, and a defined lifecycle — so every agent that opens your project knows
exactly what to do without being told.

## Quick start

```bash
git clone https://github.com/YOUR_USERNAME/blueprint.git
cd blueprint
python -m venv .venv && source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -e .

# Scaffold a new project
blueprint init my-project --name "My App" --stack "python-3.12,fastapi" --context "B2B SaaS"

# Or onboard an existing project
cd my-existing-project
blueprint onboard
```

Open the project with any AI agent — `AGENTS.md` routes it into the feature lifecycle.

## What's inside

| Command | Purpose |
|---|---|
| `blueprint init` | Scaffold a greenfield project |
| `blueprint onboard` | Scaffold convention around existing code |
| `blueprint new-feature <name>` | Start a new feature from template |
| `blueprint verify` | Check structure integrity and doc-code drift |

## Documentation

- **[blueprint-methodology-v4.md](blueprint-methodology-v4.md)** — The full guide: how it works, why it works, getting started, worked example, where it still fails. Read this first.
- **[METHODOLOGY.md](METHODOLOGY.md)** — Agent reference: what goes in every template section. For AI agents, not humans.
- **[AGENTS.md](AGENTS.md)** — Lifecycle engine. The first file every agent reads.

## Agent-agnostic

Built to work with any AI coding agent. No tool-specific syntax in the prompts. The convention is
encoded in the folder structure, not in configuration files.

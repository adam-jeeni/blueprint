---
id: 003
status: draft
date: 2026-07-12
author: Adam Davies
---

# Problem statement

## Statement

**Problem:** Blueprint claims to be an AI-native methodology for AI-human software
development, but its own bootstrap contradicts this: a human must run a Python CLI tool
(`blueprint init`) that reads external template files to scaffold a project. An AI agent
cannot initialize a Blueprint project — the methodology's own creation story requires a
human with a script. This is the methodology's central contradiction: it exists to enable
AI-driven development, but cannot itself be started by an AI.

**Success criteria:**
1. A single, self-contained agent prompt file contains all knowledge needed to scaffold a
   complete Blueprint-convention project — no external template files, no CLI tool.
2. **Greenfield:** Given an empty directory, the agent produces a full convention tree with
   every file containing complete, usable content (not blank placeholders).
3. **Brownfield without Blueprint structure:** The agent detects the project state, presents
   the three-option prompt (full refactor / docs+specs only / custom), and executes the
   human's choice without touching existing source files unless explicitly asked.
4. **Brownfield with Blueprint structure:** The agent detects existing convention, offers to
   scaffold a new feature spec folder, and creates it with populated outline documents when
   given a slug.
5. The `src/ai_project/` directory, the `blueprint` CLI, its package templates, and the
   `pyproject.toml` build configuration are removed — the project contains zero executable
   code.
6. The converted project can bootstrap itself: a human loads the project-init agent as a
   standalone session, scaffolds a project, then starts a fresh session where `AGENTS.md`
   routes into the standard feature lifecycle — all without any CLI tool or prior setup.

**Non-functional Requirements:**
- The project-init agent is a single self-contained Markdown file with no external
  dependencies — all structural knowledge and file content is embedded in the prompt.
- All existing feature specs (001, 002, 003) are preserved.
- The methodology documents (`AGENTS.md`, `METHODOLOGY.md`, agent prompts, standing docs)
  continue to function as they do today for projects initialized under the new approach.
- No build step, package manager, or runtime is required to use the project — it is a pure
  specification repository consumable by any AI agent.

---
status: active
last_updated: 2026-07-10
---

# User guide

## Who uses this system
- **Developer starting a new project** — wants a convention-compliant scaffold without reading
  a methodology document.
- **Developer with an existing project** — wants to adopt the convention structure without
  manually creating 20+ files.
- **Developer mid-feature** — wants to start a new feature with the template chain.
- **CI pipeline** — wants to verify that standing docs haven't drifted from the code.

## Current flows

### Init a new project (greenfield)
- Trigger: `blueprint init my-project --name "My Project" --stack "python-3.12" --context "B2B SaaS"`
- Steps: creates full directory tree, populates every .md file with headings + explanations,
  seeds project-overview.md with provided values, creates pyproject.toml
- Outcome: a fully scaffolded project directory. Open it with any AI agent — `AGENTS.md` routes
  it into the normal feature lifecycle.

### Onboard an existing project (brownfield)
- Trigger: `blueprint onboard` (run from existing project root)
- Steps: detects the project has code but no convention, creates `AGENTS.md`, `METHODOLOGY.md`,
  `agents/`, `docs/` (skeletons), `specs/_template/`, and `specs/README.md` — without touching
  existing source files
- Outcome: convention skeleton around existing code. Open with an AI agent — `AGENTS.md` detects
  scenario 2 and reverse-engineers standing docs.

### Start a new feature
- Trigger: `blueprint new-feature add-export`
- Steps: reads `specs/README.md` for next feature number, copies `specs/_template/` into
  `specs/NNN-add-export/`, updates the feature index
- Outcome: a numbered feature folder with all four template files ready to fill in

### Verify project health
- Trigger: `blueprint verify`
- Steps: checks required files and directories exist, checks known-callers register against
  actual imports, checks data dictionary against schema
- Outcome: pass (exit 0) or a drift report (exit 1) listing every mismatch

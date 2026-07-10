---
id: 001
status: draft
date: 2026-07-10
links_to_problem_statement: 001
inputs_consulted:
  architecture_version: 2026-07-10
  data_dictionary_version: 2026-07-10
  user_guide_version: 2026-07-10
  project_overview_version: 2026-07-10
---

# Solution design

## Layers required
CLI layer, core layer. No data layer — file system only. No frontend layer — CLI only.

## Interface contracts

### blueprint init

**Command:** `blueprint init <project-dir> --name <name> --stack <stack> --context <context>`

**Arguments:**
| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `project-dir` | Positional string | Yes | Must not be an existing non-empty directory | Path to create the new project at |
| `--name` | string | Yes | Non-empty | Human-readable project name |
| `--stack` | string | Yes | Non-empty | Tech stack description, e.g. "python-3.12,fastapi" |
| `--context` | string | Yes | Non-empty | One-paragraph business context |

**Output (success):** Directory created at `project-dir` with full convention structure. Exit code 0.

**Output (error):**
| Condition | Exit code | Message |
|---|---|---|
| `project-dir` exists and is non-empty | 1 | "Error: <path> already exists and is not empty" |
| Missing required argument | 2 | argparse default usage |

### blueprint onboard

**Command:** `blueprint onboard` (run from project root directory)

**Output (success):** Convention skeleton created. Existing source files untouched. Exit code 0.

**Output (error):**
| Condition | Exit code | Message |
|---|---|---|
| No source files detected (`.py`, `.js`, `.ts`, `.go`, `.rs`) | 1 | "Error: no source files detected. Use 'init' for new projects." |
| `AGENTS.md` already exists | 1 | "Error: AGENTS.md already exists. Project may already be onboarded." |

### blueprint new-feature

**Command:** `blueprint new-feature <feature-name>`

**Arguments:**
| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `feature-name` | Positional string | Yes | Alphanumeric + hyphens, non-empty | Slug for the feature folder |

**Output (success):** `specs/NNN-feature-name/` created with all template files. `specs/README.md`
updated with new row. Exit code 0.

**Output (error):**
| Condition | Exit code | Message |
|---|---|---|
| `specs/_template/` not found | 1 | "Error: specs/_template/ not found. Is this a convention project?" |
| Feature already exists | 1 | "Error: feature '<name>' already exists as <NNN>" |

### blueprint verify

**Command:** `blueprint verify` (run from project root directory)

**Output (success):** All checks pass. Exit code 0.

**Output (error):** Drift report printed to stdout. Exit code 1 if any drift found; 2 if structure
is invalid (missing required files).

## Impact / change specifications

### CLI layer change specification

**Created:** `src/ai_project/cli.py` — entry point. Imports `scaffold` and `verify` modules.
Parses subcommands via argparse subparsers. Dispatches to the appropriate function.

**Changed:** None — this is a new project.

**Removed:** None.

**Behaviour existing callers can still rely on:** N/A — no existing callers.

**Acceptance criteria:** Running `python -m ai_project.cli` or `python src/ai_project/cli.py`
shows usage. Each subcommand is reachable.

### Core layer change specification

**Created:**
- `src/ai_project/__init__.py` — package init, version string
- `src/ai_project/scaffold.py` — `init_project()`, `onboard_project()`, `new_feature()`,
  `_copy_template_dir()`, `_render_template()` (placeholder replacement)
- `src/ai_project/verify.py` — `verify_structure()`, `verify_docs()`, `_read_yaml_frontmatter()`
- `src/ai_project/templates/` — the canonical templates shipped as package data. Directory
  structure mirrors the project root: `AGENTS.md`, `METHODOLOGY.md`, `agents/` (10 prompt files
  including the new `architecture-advisor.md`), `docs/`, `specs/_template/`.

**Changed:** None.

**Removed:** None.

**Behaviour existing callers can still rely on:** N/A — no existing callers.

**Acceptance criteria:** Each function callable independently for testing. `_copy_template_dir()`
handles nested directories. `_render_template()` replaces `{{NAME}}`, `{{STACK}}`, `{{CONTEXT}}`
placeholders.

## Failure modes

| Component | Failure | User sees | Logged at | Recovery path |
|---|---|---|---|---|
| `init` | Target directory creation fails (permissions) | "Error: cannot create <path>: <OS error>" | stderr | Fix permissions, re-run |
| `init` | Template directory missing from package | "Error: template data not found. Reinstall blueprint." | stderr | Reinstall the package |
| `onboard` | Cannot create files (permissions) | "Error: cannot write to <path>: <OS error>" | stderr | Fix permissions, re-run |
| `new-feature` | `specs/README.md` parse failure | "Error: cannot parse specs/README.md" | stderr | Fix or recreate README.md |
| `verify` | `docs/architecture.md` missing known-callers table | "drift: docs/architecture.md — known-callers section missing" | stdout | Add known-callers section |

## Observability

| What | Level | Metric / log message | Alert threshold |
|---|---|---|---|
| Command invocation | INFO | `blueprint <subcommand> <args>` to stderr in verbose mode | N/A |
| Verification drift found | stdout | Per-mismatch line: `drift: <file> — <detail>` | Exit code non-zero |
| File creation | INFO | `created <path>` to stderr in verbose mode | N/A |

## Rollback plan
No rollback needed. All operations are additive (create files/directories) or read-only (verify).
The tool never deletes or modifies existing files except `specs/README.md` (new-feature), which
it appends to — a failed append can be reverted via git.

## Prioritised functions

| Function | Layer | Priority | Ordering driver | Acceptance criteria |
|---|---|---|---|---|
| `init_project()` | Core | 1 | Business value — greenfield is the primary use case | Creates full project directory; all .md files have content |
| `_copy_template_dir()` | Core | 1 | Technical dependency — used by init, onboard, new-feature | Recursively copies; placeholders replaced |
| `main()` with subcommand dispatch | CLI | 1 | Technical dependency — nothing else is reachable | All four subcommands dispatch correctly |
| `onboard_project()` | Core | 2 | Business value — brownfield adoption | Creates skeleton without modifying existing files |
| `new_feature()` | Core | 2 | Business value — feature lifecycle support | Copies templates; updates README |
| `verify_structure()` | Core | 3 | Business value — CI integration | Detects missing required files/dirs |
| `verify_docs()` | Core | 3 | Business value — drift prevention | Compares known-callers register against code |

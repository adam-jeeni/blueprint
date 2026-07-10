---
status: active
last_updated: 2026-07-10
---

# Data dictionary

This project has no database. It operates on the file system. The "entities" below describe
the structural elements the tool reads and writes.

## Project directory (the entity the tool operates on)
| Field | Type | Description |
|---|---|---|
| `root_path` | Path | Absolute or relative path to the project root |
| `has_agents_md` | bool | Whether `AGENTS.md` exists at root |
| `has_docs_dir` | bool | Whether `docs/` exists and contains populated files |
| `has_code` | bool | Whether the directory contains source files (`.py`, `.js`, etc.) |
| `scenario` | enum: 1\|2\|3 | Detected entry scenario based on combination of above |

## Feature (per-folder metadata)
| Field | Type | Description |
|---|---|---|
| `id` | int | Feature number, e.g. 001 |
| `name` | string | Feature folder name, e.g. `cli-tool` |
| `status` | enum: draft\|approved\|in-progress\|shipped | Current lifecycle status |
| `problem_statement_path` | Path | `specs/NNN-name/1-problem-statement.md` |
| `solution_design_path` | Path | `specs/NNN-name/2-solution-design.md` |

## Doc verification result
| Field | Type | Description |
|---|---|---|
| `doc_path` | Path | The standing doc that was verified |
| `status` | enum: pass\|drift | Whether the doc matches the code |
| `mismatches` | list[dict] | For drift: what the doc claims vs. what the code actually has |

## Known-callers register entry
| Field | Type | Description |
|---|---|---|
| `component` | string | The shared component identifier (e.g. `crm.py: log_interaction()`) |
| `doc_callers` | list[string] | Callers listed in `docs/architecture.md` |
| `code_callers` | list[string] | Callers found by static analysis of the actual code |
| `mismatch` | bool | True if the two lists differ |

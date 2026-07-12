---
id: 003
status: draft
links_to_solution_design: 003
links_to_problem_statement: 003
---

# Test specification

## Acceptance criteria trace

| Success criterion (from problem statement) | Test case(s) |
|---|---|
| SC1: Self-contained agent prompt with all knowledge | UNIT-1: Manifest completeness; UNIT-2: No external dependencies |
| SC2: Greenfield — full convention tree with usable content | INT-1: Greenfield scaffold; UNIT-3: File content verification |
| SC3: Brownfield without Blueprint — three-option prompt | INT-2: Brownfield-no-structure detection; INT-3: Option 1 (refactor); INT-4: Option 2 (docs+specs); INT-5: Option 3 (custom) |
| SC4: Brownfield with Blueprint — feature spec scaffold | INT-6: Blueprint-structure detection; INT-7: Feature spec creation |
| SC5: CLI and code removed — zero executable code | UNIT-4: Code removal verification |
| SC6: Project can bootstrap itself | INT-8: End-to-end bootstrap |

## Unit tests

### Assessment logic

| Test case | Test data / setup | Expected result |
|---|---|---|
| UNIT-ASSESS-1: Greenfield detection | Empty directory (no files) | Agent identifies as greenfield |
| UNIT-ASSESS-2: Greenfield with .git only | Directory containing only `.git/` | Agent identifies as greenfield |
| UNIT-ASSESS-3: Brownfield-no-structure detection | Directory with `.py` files but no `AGENTS.md` | Agent identifies as brownfield (no Blueprint structure) |
| UNIT-ASSESS-4: Blueprint-structure detection | Directory with `AGENTS.md` and `docs/` containing populated files | Agent identifies as brownfield (Blueprint structure) |
| UNIT-ASSESS-5: Partial onboard | Directory with `AGENTS.md` but no other convention files | Agent reports "mixed state" and asks for guidance |
| UNIT-ASSESS-6: Ambiguous directory | Directory with `AGENTS.md` and source files but no docs/ | Agent reports assessment reasoning; human can override |

### Conversation flow

| Test case | Test data / setup | Expected result |
|---|---|---|
| UNIT-CONV-1: Greenfield prompt | Greenfield scenario detected | Agent presents the greenfield scaffold prompt listing files to create |
| UNIT-CONV-2: Brownfield-no-structure prompt | Brownfield-no-structure detected | Agent presents three-option prompt [1] [2] [3] |
| UNIT-CONV-3: Blueprint-structure prompt | Blueprint-structure detected | Agent presents feature-spec prompt |
| UNIT-CONV-4: Consent responses | Human says "yes", "y", "go", "proceed" | Agent executes the proposed action |
| UNIT-CONV-5: Denial responses | Human says "no", "n", "stop", "cancel" | Agent halts and asks what the human wants |
| UNIT-CONV-6: Scenario choice by number | Human says "1", "2", or "3" | Agent routes to the corresponding flow |
| UNIT-CONV-7: Scenario choice by phrase | Human says "just add docs and specs" | Agent routes to option 2 |
| UNIT-CONV-8: Feature slug input | Human provides "add-export" | Agent scaffolds `specs/NNN-add-export/` |
| UNIT-CONV-9: Plan approval | Human says "approved" or "go ahead" | Agent executes the plan |
| UNIT-CONV-10: Plan revision | Human requests specific changes | Agent revises `init-plan.md` and re-presents |

### Plan gate

| Test case | Test data / setup | Expected result |
|---|---|---|
| UNIT-PLAN-1: Plan generation | Option 1 (refactor) selected in brownfield-no-structure | Agent writes `init-plan.md` with every file operation listed |
| UNIT-PLAN-2: Plan approval gate | `init-plan.md` presented | Agent waits for human approval before any file changes |
| UNIT-PLAN-3: Plan approval | Human approves the plan | Agent executes all operations in the plan |
| UNIT-PLAN-4: Plan revision cycle | Human requests changes to the plan | Agent revises `init-plan.md` and re-waits for approval |

### File manifest

| Test case | Test data / setup | Expected result |
|---|---|---|
| UNIT-MAN-1: Manifest completeness | Inspect `project-init.md` | Contains entries for all files in the canonical tree (root, agents, docs, specs, backend, frontend, docker) |
| UNIT-MAN-2: No external dependencies | Search prompt for file-read or template-load instructions | No references to external files or templates; all content is inline |
| UNIT-MAN-3: File content quality | Inspect each manifest entry | Every file entry contains complete, usable content — no "TODO" or "fill this in" placeholders |

### Idempotency

| Test case | Test data / setup | Expected result |
|---|---|---|
| UNIT-IDEM-1: Existing file conflict | Scaffold greenfield; re-run on same directory | Agent reports conflict for each existing file; asks skip or overwrite |
| UNIT-IDEM-2: Skip existing | Human chooses "skip" for a conflict | Agent skips that file; continues with remaining files |
| UNIT-IDEM-3: Overwrite existing | Human chooses "overwrite" for a conflict | Agent overwrites that file; continues with remaining files |

### Code removal

| Test case | Test data / setup | Expected result |
|---|---|---|
| UNIT-RM-1: CLI directory removed | After implementation, check `src/ai_project/` | Directory does not exist |
| UNIT-RM-2: Package metadata removed | After implementation, check `src/blueprint.egg-info/` | Directory does not exist |
| UNIT-RM-3: Build config removed | After implementation, check `pyproject.toml` | File does not exist |
| UNIT-RM-4: Test suite removed | After implementation, check `tests/` | Directory does not exist |

## Integration tests

| Test case | Components exercised | Setup | Expected result |
|---|---|---|---|
| INT-1: Greenfield scaffold | Assessment + conversation flow + manifest | Empty directory; load agent; confirm scaffold | Full canonical tree created; all files have content |
| INT-2: Brownfield-no-structure detection | Assessment + conversation flow | Directory with `.py` files, no `AGENTS.md`; load agent | Agent detects brownfield; presents three-option prompt |
| INT-3: Brownfield option 1 (refactor) | Assessment + plan gate + file operations | Brownfield directory; select option 1 | Agent produces `init-plan.md`; waits for approval; executes on approval |
| INT-4: Brownfield option 2 (docs+specs) | Assessment + manifest (docs+specs subset) | Brownfield directory; select option 2 | `docs/` and `specs/` created; existing source files untouched |
| INT-5: Brownfield option 3 (custom) | Assessment + conversation flow | Brownfield directory; select option 3 with custom instruction | Agent follows the custom instruction |
| INT-6: Blueprint-structure detection | Assessment + conversation flow | Directory with `AGENTS.md` and populated `docs/`; load agent | Agent detects Blueprint structure; offers feature spec option |
| INT-7: Feature spec creation | Assessment + manifest (spec subset) | Blueprint-structure directory; provide slug "test-feature" | `specs/NNN-test-feature/` created with populated outline documents; `specs/README.md` updated |
| INT-8: End-to-end bootstrap | Full workflow | After all implementation changes, start fresh session | `AGENTS.md` scenario 1 directs human to load project-init agent; agent can scaffold a new project |

## Edge cases and boundary tests

| Test case | Edge condition | Expected result |
|---|---|---|
| EDGE-1: Empty directory | Zero files, not even `.git` | Detected as greenfield |
| EDGE-2: Git-only directory | Only `.git/` directory present | Detected as greenfield |
| EDGE-3: Permission denied on write | Target directory is read-only | Agent reports "Cannot write to `<path>` — permission denied"; human can fix and retry |
| EDGE-4: Very long feature slug | Slug > 100 characters | Agent accepts or validates; does not crash |
| EDGE-5: Slug with special characters | Slug contains spaces, slashes, or unicode | Agent validates and rejects invalid slugs |
| EDGE-6: Ambiguous human input | Human says "maybe" or "I'm not sure" | Agent asks a clarifying question rather than guessing |
| EDGE-7: Mid-operation interruption | Agent is stopped mid-scaffold | On resume, agent reports progress and offers to continue or restart |
| EDGE-8: Nested directories | Scaffold into `a/b/c/` where parent doesn't exist | Agent creates parent directories as needed |
| EDGE-9: Git submodule directory | Directory contains `.gitmodules` or submodule refs | Agent reports assessment reasoning; does not silently misbehave |
| EDGE-10: Feature spec with existing number | Slug matches an already-used feature number | Agent detects conflict and assigns the next available number |

## Regression tests

| Test case | Existing behaviour preserved | Caller(s) affected |
|---|---|---|
| REG-1: Orchestrator prompt unchanged | `orchestrator.md` content and behaviour identical | All projects using the orchestrator |
| REG-2: Schema agent prompt unchanged | `schema-agent.md` content and behaviour identical | Schema agent callers |
| REG-3: Backend agent prompt unchanged | `backend-agent.md` content and behaviour identical | Backend agent callers |
| REG-4: Frontend agent prompt unchanged | `frontend-agent.md` content and behaviour identical | Frontend agent callers |
| REG-5: Architecture advisor prompt unchanged | `architecture-advisor.md` content and behaviour identical | Human-invoked advisor sessions |
| REG-6: Spec agent prompt unchanged | `spec-agent.md` content and behaviour identical | Spec agent callers |
| REG-7: Review agent prompt unchanged | `review-agent.md` content and behaviour identical | Review agent callers |
| REG-8: Refactor agent prompt unchanged | `refactor-agent.md` content and behaviour identical | Refactor agent callers |
| REG-9: AGENTS.md scenario 2 and 3 | Detection of scenarios 2 and 3 still works correctly | All agents entering an existing project |
| REG-10: Feature specs preserved | `specs/001-cli-tool/` and `specs/002-pdf-v4/` and `specs/003-convert-to-ai/` unchanged | Human reviewers; historical record |
| REG-11: Standing docs format unchanged | All 5 standing docs maintain their YAML frontmatter and section structure | All agents reading standing docs |
| REG-12: METHODOLOGY.md unchanged | Agent reference content and conventions preserved | All agents referencing the methodology |

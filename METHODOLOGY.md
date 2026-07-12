# METHODOLOGY.md — Agent Reference

The authoritative reference for AI agents working within the blueprint methodology. Read this
when you need to understand what goes into each document, what makes it good, and what
conventions govern it. The template files in `specs/_template/` contain headings and field
names only — this document explains what to write under each heading.

## The Feature Lifecycle

| Step | Document | Purpose |
|---|---|---|
| 0 | — | **Architecture Advisor** helps the human scope and design (optional, human-invoked) |
| 1 | `1-problem-statement.md` | What needs to change and why |
| → | Human approval gate | Human says "go" or "revise" |
| 2 | `2-solution-design.md` | How it will be built — contracts, impact, failure modes |
| 3 | `3-backlog.md` | Sequenced implementation tasks with parallelisation map |
| 4 | `4-test-spec.md` | Test cases traced to success criteria |
| 5 | — | Implementation agents execute the backlog |
| 6 | — | Review agent: full test suite, contract verification, doc gate |
| 7 | — | Spec agent updates standing docs |

Steps 3 and 4 are parallel — both depend only on step 2. Check `SKIP-RUBRIC.md` before
producing them.

---

## 1. Problem Statement (`1-problem-statement.md`)

### Purpose
Describe the problem, not the solution. What needs to change, who needs it, and why now.
Be specific about scope — what is in and what is explicitly out.

### Section: Statement

Duplicate the statement block if the feature addresses more than one distinct problem.

**Problem:** What is wrong or missing? Describe the current state and why it falls short.
Focus on the gap, not the fix.

**Success criteria:** Concrete, testable outcomes. "Done" means these are true. Each criterion
must map to at least one test case in `4-test-spec.md`. Use EARS-style phrasing: "The system
shall..." or "The user can..."

**Non-functional Requirements:** What constraints does this feature operate under? Covers
explicit scope boundaries, platform limitations, performance requirements, security constraints,
and anything the feature will NOT do. Prevents scope creep and gives the agent clear boundaries.
The best entries are tempting inclusions that the human actively decided against.

---

## 2. Solution Design (`2-solution-design.md`)

### Purpose
Translate the problem statement into a concrete technical plan. This is the contract that
implementation agents work from — be precise about interfaces, data shapes, and behaviour.

### Section: Layers Required

Which layers does this feature touch? Options: data (schema / migrations / repositories),
backend (API / services / agents), frontend (UI / client). List them explicitly. This
determines which implementation agents are deployed.

### Section: Functional Overview

What does the proposed solution do, at a high level? Describe the core functionality —
the main capabilities, the key workflows, and how the pieces fit together. This is the
"what" before the "how" of the interface contracts. Keep it to a few paragraphs; save
the detail for the contracts and impact specs below.

### Section: UI Outline

If the feature has a user-facing surface, describe what the user sees and does — screens,
controls, flows, commands. Not wireframes; prose that an agent can reason about. If there
is no UI surface, state that explicitly.

### Section: Interface Contracts

Full request/response schemas for every new or changed API endpoint. Include: HTTP method,
path, request body shape (field names, types, required/optional, validation rules), response
body shape, error response shapes with status codes, authz requirements, and idempotency
semantics.

For each endpoint, create a subsection with the endpoint name and these sub-sections:
- **Method + path** — e.g. `PUT /api/v1/admin/tenants/{id}/channel-config`
- **Request table** — Field, Type, Required, Validation, Description columns
- **Response (success)** — Field, Type, Description columns
- **Response (error)** — Status, Body shape, When columns. Cover at minimum: validation
  failure (422/400), auth failure (401/403), not found (404), server error (500).
- **Authz** — what permissions/roles are required
- **Idempotency** — is repeated submission safe? If not, what mechanism prevents duplicates?

### Section: Impact / Change Specifications

One subsection per layer. For each component in that layer, specify:

**Changed:** What existing components are modified. List file paths and describe the change.

**Created:** What new components are introduced. List file paths and describe responsibility.

**Removed:** What is deleted. List file paths and confirm no remaining callers exist (check
the known-callers register in `docs/architecture.md`).

**Behaviour existing callers can still rely on:** Only needed if this touches a shared/coupled
component listed in `docs/architecture.md`'s known-callers register. State what behaviour is
preserved so dependent code doesn't break silently. This is the single most important field for
preventing silent breakage.

**Acceptance criteria:** Concrete, testable outcomes for this layer.

### Section: Failure Modes

Per-endpoint or per-component: what happens when something fails. Production software is
defined by how it degrades, not just how it succeeds. Table columns:

| Component | Failure | User sees | Logged at | Recovery path |

Cover at minimum: external dependency unavailable, database unavailable, invalid input,
timeout, partial failure (write succeeded but side-effect failed).

### Section: Observability

| What | Level | Metric / log message | Alert threshold |

What gets logged, at what level (DEBUG/INFO/WARN/ERROR), and what metric or alert threshold
applies. Every endpoint should log at least: request received (DEBUG), response sent with
status (INFO), and any error (ERROR).

### Section: Rollback Plan

If this feature touches the data layer or shared state, how is it reversed? "No rollback
needed" is acceptable if the change is purely additive with no schema impact. For migrations:
describe the down migration. For config changes: describe the revert procedure.

### Section: Prioritised Functions

Table: Function, Layer, Priority, Ordering driver, Acceptance criteria.

State whether ordering is driven by business value or technical dependency. Priority 1
functions unblock everything else — they should be the minimum viable slice that delivers
value.

---

## 3. Backlog (`3-backlog.md`)

### Purpose
Sequenced implementation tasks derived from the solution design. Each task is a unit of work
that one agent can complete independently. Tasks that share no dependencies run in parallel.

### Section: Tasks

Table: Task ID, Description, Layer, Depends on, Can run parallel with.

Task IDs use the pattern `NNN-M` where NNN is the feature number and M is sequential.
The description should name the specific function or file the agent will create or modify.

### Section: Parallelisation Map

Group tasks into waves. Wave 1 has no dependencies and runs first. Wave 2 depends on wave 1
outputs. Within a wave, tasks run concurrently in separate worktrees.

Critical rule: tasks that touch the same file must NOT run in parallel — they will
merge-conflict. If two tasks both modify `admin.py`, they cannot be in the same wave. State
worktree assignments explicitly: `[Worktree A] Tasks: 001-1, 001-3`.

---

## 4. Test Specification (`4-test-spec.md`)

### Purpose
Test cases traced to the problem statement's success criteria and the solution design's
acceptance criteria. Covers unit, integration, edge-case, and regression tests.

### Section: Acceptance Criteria Trace

Every success criterion from `1-problem-statement.md` must map to at least one test case.
Table: Success criterion, Test case(s).

### Section: Unit Tests

One table per function under test. Table: Test case, Test data / setup, Expected result.
Unit tests exercise a single function in isolation with mocked dependencies.

### Section: Integration Tests

Tests that exercise multiple components together. Table: Test case, Components exercised,
Setup, Expected result. Integration tests use real (or test-container) databases and services
where practical, not mocks.

### Section: Edge Cases and Boundary Tests

Empty input, maximum values, concurrent access, missing dependencies, timeouts, null fields,
duplicate submissions. Table: Test case, Edge condition, Expected result.

### Section: Regression Tests

Existing behaviour that must not break. Reference the known-callers register to identify
callers of changed shared components. Table: Test case, Existing behaviour preserved,
Caller(s) affected.

---

## Skip Rubric

A feature can skip producing `3-backlog.md` and `4-test-spec.md` when ALL five conditions
are true:

1. The change touches a single file (not counting test files).
2. The change does not touch any shared component listed in the known-callers register.
3. The change does not alter the data model — no new fields, no schema changes, no migration.
4. The acceptance criteria are fully specified in the problem statement's success criteria.
5. Test cases are obvious from the acceptance criteria — one test case per criterion, no
   edge cases requiring separate test design.

If any condition is uncertain, produce the full artifact. A skipped artifact that should have
existed is a gap; an extra artifact is cheap.

---

## Standing Documents

### `docs/architecture.md`
Components, layers, integration points, shared components and their known callers, and
architectural decisions. Updated by the spec agent after every merge. The known-callers
register is the single most important field — it makes brownfield impact analysis possible.

### `docs/data-dictionary.md`
Entities, fields, types, relationships, and ownership. Updated when a feature changes the
data model.

### `docs/user-guide.md`
Current user-facing behaviour described from the user's perspective. Updated when a feature
changes what the user sees or does.

### `docs/project-overview.md`
Business context, stakeholders, tech stack. Rarely changed.

### `docs/production-feedback.md`
Incident log. Each row: Date, Feature, Layer, Severity, Root cause, What changed, Prevention.
The "Prevention" column describes what systemic change prevents recurrence. The "Layer" field
enables filtering — only read incidents relevant to the layers the current feature touches.

---

## Amendment Path

When implementation reveals a contract was wrong, the spec is updated before the code drifts.
The amendment flows back through `2-solution-design.md`; the orchestrator re-checks downstream
impacts before sub-agents continue. Never silently overwrite a spec to match the code —
update the spec, then the code follows.

---

## Document Verification Gate

After every merge, the review agent verifies that standing documents match the code. The
known-callers register is checked against actual imports in the codebase. The data dictionary
is checked against the actual schema. A mismatch blocks the merge.

---

## Agent Hierarchy

- **Architecture Advisor** — human-invoked. Design thinking partner during specification.
  Helps scope, design, and gap-check. Reads only the standing docs relevant to the work.
- **Orchestrator** — defines interface contracts, coordinates sub-agents, runs the lifecycle.
- **Schema Agent** — datastore migrations, repository functions.
- **Backend Agent** — API endpoints, services, agent logic.
- **Frontend Agent** — UI components, client calls.
- **Spec Agent** — updates standing docs after a feature ships.
- **Review Agent** — merge gate: full test suite, contract verification, doc verification.
- **Refactor Agent** — structural consolidation between feature batches.

## Conventions

- `specs/` folder numbers match git branch names (`feature/NNN-...`).
- `test-spec.md` specifies tests; `tests/` holds the generated test code — distinct artifacts.
- Standing docs are updated after every merge, but only the ones the feature touched.
- All agent prompts use agent-agnostic language — no tool-specific syntax.

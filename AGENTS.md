# AGENTS.md

The first file any AI agent reads in this project. It is the lifecycle engine —
detect where you are, then route to the right prompt. Do not skip the detection step.

## Entry-Point Detection

On first read, determine which scenario applies by checking in this order:

1. **If `AGENTS.md` exists AND `docs/` contains populated standing docs**
   → Scenario 3 — normal feature lifecycle. Read the standing docs, then follow
   `agents/prompts/orchestrator.md` for the feature lifecycle.

2. **If code exists (`.py`, `.js`, `.ts`, `.go`, `.rs`, etc.) but `docs/` or `AGENTS.md` is absent**
   → Scenario 2 — brownfield project without Blueprint convention. The human should
   load `agents/prompts/project-init.md` explicitly to onboard the project.

3. **If no significant code and no `AGENTS.md` exist**
   → Scenario 1 — new project. The human should load `agents/prompts/project-init.md`
   explicitly to scaffold the project. The project-init agent is a standalone pre-step;
   after initialization, start a fresh session here and `AGENTS.md` will route into
   the standard lifecycle.

## Project Structure

```
project-root/
├── AGENTS.md                      # Lifecycle engine & coordinator context
├── METHODOLOGY.md                 # Human-readable guide to this AI-first setup
├── docker-compose.yml
│
├── agents/                        # Operational prompts per role + scenario
│   ├── README.md                  # Role index
│   └── prompts/
│       ├── project-init.md        # Standalone pre-step — scaffold or refactor
│       ├── orchestrator.md        # Scenario 3 — normal feature lifecycle
│       ├── schema-agent.md
│       ├── backend-agent.md
│       ├── frontend-agent.md
│       ├── architecture-advisor.md  # Human-facing — design thinking partner
│       ├── spec-agent.md
│       ├── review-agent.md
│       └── refactor-agent.md
│
├── docs/                          # Standing documents — global, always current
│   ├── architecture.md            # Components, layers, integration points
│   ├── data-dictionary.md         # Entities, fields, ownership
│   ├── user-guide.md              # Current user-facing behaviour
│   ├── project-overview.md        # Business context, stakeholders, tech stack
│   └── production-feedback.md     # Incident log + systemic prevention
│
├── specs/                         # Per-feature specification chain
│   ├── README.md                  # Index of every feature and its status
│   └── _template/                 # Base template for starting a new feature
│       ├── SKIP-RUBRIC.md
│       ├── 1-problem-statement.md
│       ├── 2-solution-design.md
│       ├── 3-backlog.md
│       └── 4-test-spec.md
│
├── backend/                       # Python Back-End Service
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   ├── src/
│   │   └── app/
│   │       ├── __init__.py
│   │       ├── main.py
│   │       ├── api/
│   │       │   ├── v1/
│   │       │   └── dependencies.py
│   │       ├── core/
│   │       │   ├── config.py
│   │       │   └── database.py
│   │       ├── models/
│   │       ├── schemas/
│   │       └── services/
│   └── tests/
│       ├── conftest.py
│       ├── api/
│       ├── models/
│       └── services/
│
├── frontend/                      # TypeScript Front-End Service
│   ├── package.json
│   ├── tsconfig.json
│   ├── playwright.config.ts
│   ├── src/
│   │   ├── components/
│   │   ├── utils/
│   │   └── main.tsx
│   ├── e2e/
│   └── public/
│
└── docker/                        # Isolated build environments
    ├── backend.Dockerfile
    └── frontend.Dockerfile
```

## The Feature Lifecycle (Scenario 3)

| Step | Inputs | Output | Agent |
|---|---|---|---|
| 0. Design thinking | Human's rough idea | Clarified requirements, scoped design | **Architecture Advisor** (human invokes `agents/prompts/architecture-advisor.md`) |
| 1. Problem statement | Human requirements | `1-problem-statement.md` | Orchestrator |
| → Human approval gate | — | "Go" or "Revise" | Human |
| 2. Solution design | Problem statement + all standing docs | `2-solution-design.md` | Orchestrator |
| 3. Backlog | Solution design + standing docs | `3-backlog.md` | Orchestrator |
| 4. Test spec | Solution design + problem statement | `4-test-spec.md` | Orchestrator |
| 5. Implementation | Backlog + test spec | Merged code, per-agent works | Schema / Backend / Frontend agents |
| 6. Review & QA | Full repo test suite + solution design | Merge approval, regression report | Review agent |
| 7. Doc update | Shipped code | Updated standing docs (scoped) | Spec agent |
| → Doc verification gate | Standing docs vs. code | Pass / drift report | Review agent |

Steps 3 and 4 are parallel — both depend only on step 2. Check `SKIP-RUBRIC.md` before
producing them; some small features don't need a full backlog or test spec.

## Amendment Path

When implementation reveals a contract was wrong, the spec is updated before the code drifts.
The amendment flows back through `2-solution-design.md`; the orchestrator re-checks downstream
impacts before sub-agents continue. Never silently overwrite a spec to match the code —
update the spec, then the code follows.

## Conventions

- `docs/` documents are feature-independent — every feature's step 2 reads them.
- `specs/` folder numbers match git branch names (`feature/NNN-...`).
- `test-spec.md` specifies tests; `tests/` holds the generated test code. They are distinct.
- Standing docs must be updated after every feature merge — only the ones the feature touched.
- The known-callers register in `docs/architecture.md` must be updated when any shared
  component changes its interface.
- All agent prompts use agent-agnostic language — no tool-specific syntax.

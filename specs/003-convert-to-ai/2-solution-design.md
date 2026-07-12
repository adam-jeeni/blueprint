---
id: 003
status: draft
date: 2026-07-12
links_to_problem_statement: 003
inputs_consulted:
  architecture_version:
  data_dictionary_version:
  project_overview_version:
---

# Solution design

## Layers required

**Methodology layer** — this feature creates, modifies, and removes agent prompt files
within `agents/prompts/`. It removes the existing code layer (`src/ai_project/`).

No data layer, no backend layer, no frontend layer. The output is a self-contained agent
prompt file plus updates to routing documents.

## Functional Overview

The feature replaces the `blueprint` CLI with a single AI agent prompt —
`agents/prompts/project-init.md`. This prompt contains a complete file
manifest: every file the agent can generate, its exact path, and its full content. When
an AI agent loads this prompt, it can scaffold a Blueprint project through conversation
alone — no external files, no script, no package installation.

The agent operates in three modes, detected by inspecting the current directory:

1. **Greenfield** (empty or nearly-empty directory): the agent scaffolds the full convention
   tree. Every file is written with complete content from the embedded manifest.

2. **Brownfield — no Blueprint structure** (existing code, no `AGENTS.md`): the agent
   presents a three-option prompt. The human chooses, and the agent executes — either
   refactoring into the convention tree, adding only `docs/` and `specs/`, or following
   custom instructions. For refactoring, the agent produces an `init-plan.md` for human
   review before making changes.

3. **Brownfield — Blueprint structure** (existing `AGENTS.md`): the agent detects the
   convention, offers to scaffold a new feature spec, and creates the numbered folder with
   populated outline documents from the manifest.

The project-init agent is **not** routed through `AGENTS.md`. Because its prompt is large
(containing full file contents for the entire convention tree), it is designed to be loaded
as a standalone session — the human explicitly invokes it by opening the prompt file or
instructing their AI agent to load it. Once initialization is complete, the human starts a
**fresh session with a clean context window**. In that new session, `AGENTS.md` is present
in the project root and routes the agent into the standard feature lifecycle. The
project-init agent's job is done; the orchestrator, spec, and implementation agents take
over with a clean context.

## UI outline

### Startup and assessment

When explicitly loaded by the human (outside of `AGENTS.md` auto-routing), the agent
introduces itself and assesses the project state:

- Checks for `AGENTS.md` to determine if Blueprint convention exists.
- Checks for source files (`.py`, `.js`, `.ts`, `.go`, `.rs`, etc.) to determine if this
  is a greenfield or brownfield project.
- Reports its assessment to the human.
- Makes clear that this is a one-time initialization session and that the human should
  start a fresh session after completion.

### Greenfield flow

```
This appears to be a new project. I'll scaffold a complete Blueprint
convention project structure. This includes:

- AGENTS.md (lifecycle engine)
- METHODOLOGY.md (agent reference)
- 8 agent prompts (orchestrator, schema, backend, frontend, etc.)
- 5 standing documents (architecture, data dictionary, user guide, etc.)
- Spec templates and README
- .gitignore

Shall I proceed? [yes/no]
```

On confirmation, the agent writes all files. Reports progress as it goes. When complete,
confirms the tree and advises the human: "Initialization complete. Start a new session in
this directory — `AGENTS.md` will take over from here."

### Brownfield — no Blueprint structure

```
This is a brownfield project that does not follow Blueprint convention.
What would you like me to do?

[1] Refactor into full Blueprint structure
[2] Add only docs/ and specs/ folders
[3] Something else (describe what you need)
```

- **Option 1:** Agent produces `init-plan.md` showing the proposed refactor. Human reviews
  and approves before any files are moved or created.
- **Option 2:** Agent creates `docs/` and `specs/` alongside existing code. No existing
  files are touched.
- **Option 3:** Agent follows custom instructions.

### Brownfield — Blueprint structure

```
This project already follows Blueprint convention.

[1] Create a new feature spec? (provide the feature slug)
[2] Something else?
```

- **Option 1:** Agent scaffolds `specs/NNN-slug/` with populated outline documents and
  updates `specs/README.md`.

### Plan gate for complex work

For any multi-step operation (full refactor, option 1), the agent writes an `init-plan.md`
listing every file operation (create, move, delete) and waits for human approval before
executing. The plan gate prevents the agent from running ahead with irreversible changes.

## Conversation contract

The agent's interface is conversational, not programmatic. The contract is defined by
states and transitions.

### Agent → Human messages

| Message | Trigger | Contains |
|---|---|---|
| Assessment report | On load | Detected scenario, evidence (AGENTS.md found? source files found?) |
| Scenario prompt | After assessment | The appropriate multi-option prompt for the detected scenario |
| Plan for review | Before complex work (`init-plan.md`) | Every file operation, grouped by type (create/move/delete) |
| Progress updates | During execution | Each file as it's written |
| Completion summary | When done | Count of files created, next steps |

### Human → Agent responses

| Response type | Valid inputs | Agent action |
|---|---|---|
| Consent | `yes`, `y`, `go`, `proceed` | Execute the proposed action |
| Denial | `no`, `n`, `stop`, `cancel` | Halt and ask what the human wants instead |
| Scenario choice | `1`, `2`, `3` or descriptive phrase | Route to the corresponding flow |
| Feature slug | A name (e.g. `add-export`) | Scaffold `specs/NNN-slug/` |
| Plan approval | `approved`, `looks good`, `go ahead` | Execute the plan |
| Plan revision | Specific changes requested | Revise `init-plan.md` and re-present |

### Idempotency

The agent checks for existing files before writing. If a file already exists, it reports
the conflict and asks whether to skip or overwrite. The agent never silently overwrites
existing work.

## Impact / change specifications

### Methodology layer — created

**`agents/prompts/project-init.md`**

A self-contained agent prompt with the following structure:

1. **Role and purpose:** The agent's identity and job description.
2. **Assessment logic:** How to detect the three scenarios from directory contents.
3. **Conversation flows:** The prompts for each scenario, as specified in the UI outline
   above.
4. **Plan gate rule:** When to produce `init-plan.md` and wait for approval.
 5. **File manifest:** For every file in the scaffolded project tree, a structured entry
    containing: file name, full relative path, and complete file content. Each entry
    contains usable content — not placeholders. The canonical project tree is:

    ```
    app_name/
    ├── .gitignore
    ├── README.md
    ├── AGENTS.md
    ├── METHODOLOGY.md
    ├── docker-compose.yml
    ├── pyproject.toml                 # Root workspace dependencies
    │
    ├── agents/
    │   ├── README.md
    │   └── prompts/
    │       ├── orchestrator.md
    │       ├── schema-agent.md
    │       ├── backend-agent.md
    │       ├── frontend-agent.md
    │       ├── architecture-advisor.md
    │       ├── spec-agent.md
    │       ├── review-agent.md
    │       └── refactor-agent.md
    │
    ├── docs/
    │   ├── architecture.md
    │   ├── data-dictionary.md
    │   ├── user-guide.md
    │   ├── project-overview.md
    │   └── production-feedback.md
    │
    ├── specs/
    │   ├── README.md
    │   └── _template/
    │       ├── SKIP-RUBRIC.md
    │       ├── 1-problem-statement.md
    │       ├── 2-solution-design.md
    │       ├── 3-backlog.md
    │       └── 4-test-spec.md
    │
    ├── backend/
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
    ├── frontend/
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
    └── docker/
        ├── backend.Dockerfile
        └── frontend.Dockerfile
    ```

    The `agents/prompts/` list is the standard lifecycle set — the `greenfield-setup`
    and `brownfield-onboarding` prompts from the current project are deprecated; their
    function is subsumed by the project-init agent itself. The `specs/` directory
    contains only the template — no example feature folder is generated. Feature specs
    are created later by the orchestrator during the standard lifecycle.

 6. **File specifications:** What each file in the manifest contains.

    ### Root files

    **`.gitignore`**
    - Standard Python + Node gitignore. Ignores `__pycache__/`, `.venv/`, `node_modules/`,
      `.env`, `dist/`, `.DS_Store`, IDE directories.

    **`README.md`**
    - Project name, one-paragraph description, quick-start instructions. Includes the
      AI-driven workflow: load the project in any AI agent — `AGENTS.md` routes it.

    **`AGENTS.md`**
    - Lifecycle engine. Three-scenario entry-point detection. Routes to the standard
      lifecycle prompts. Includes a compact convention-only project tree (not the full
      backend/frontend detail — that lives in the init agent). Includes the feature
      lifecycle table, amendment path, and conventions.

    **`METHODOLOGY.md`**
    - Agent reference. Explains every template section, the lifecycle, standing docs,
      skip rubric, amendment path, and agent hierarchy. This is the document agents read
      to understand *how* to fill in the templates.

    **`docker-compose.yml`**
    - Defines `backend` and `frontend` services with build contexts pointing to
      `docker/backend.Dockerfile` and `docker/frontend.Dockerfile`. Includes a `db`
      service (PostgreSQL) for local development. Ports: backend 8000, frontend 5173,
      db 5432. Named volume for database persistence.

    **`pyproject.toml`** (root)
    - Workspace-level tool configuration. Defines the root package name, Python version
      constraint (≥3.12), and dev dependencies shared across services (linting, formatting).

    ### `agents/`

    **`agents/README.md`**
    - Role index. One-line description of each agent prompt and when it is invoked.
      Lists the 8 standard lifecycle prompts plus the project-init agent as a standalone
      pre-step.

    **`agents/prompts/orchestrator.md`**
    - Runs the feature lifecycle (scenario 3). Reads standing docs, coordinates
      sub-agents, produces spec files. Contains the full lifecycle table and step
      sequencing rules.

    **`agents/prompts/schema-agent.md`**
    - Manages data models and migrations. Reads `docs/data-dictionary.md` and
      `docs/architecture.md`. Produces Alembic migrations, SQLAlchemy models, and
      Pydantic schemas.

    **`agents/prompts/backend-agent.md`**
    - Builds API endpoints and services. Reads solution design interface contracts.
      Produces FastAPI route handlers, service-layer logic, and dependency wiring.

    **`agents/prompts/frontend-agent.md`**
    - Builds UI components. Reads solution design UI outline and user guide. Produces
      React/TypeScript components, hooks, and API client calls.

    **`agents/prompts/architecture-advisor.md`**
    - Human-invoked design thinking partner. Operates at step 0 — before the
      orchestrator. Helps scope, spot gaps, and develop half-formed ideas. Reads only
      the standing docs relevant to the feature's layers.

    **`agents/prompts/spec-agent.md`**
    - Updates standing docs after a feature ships. Reads the merged implementation
      and diff. Updates `docs/architecture.md` (known-callers register), `docs/data-
      dictionary.md`, and `docs/user-guide.md`.

    **`agents/prompts/review-agent.md`**
    - Merge gate. Runs the full test suite, verifies interface contracts against the
      solution design, runs the doc verification gate. Produces a pass/fail report.

    **`agents/prompts/refactor-agent.md`**
    - Post-init structural consolidation. Runs between feature batches. Improves
      codebase structure without changing behaviour. The full test suite must pass
      identically before and after.

    ### `docs/`

    **`docs/architecture.md`**
    - System overview, layers, components table (name, layer, responsibility, module
      path), integration points, shared components with known-callers register, and
      architectural decisions. Populated with placeholder sections — filled in by
      the spec agent as features ship.

    **`docs/data-dictionary.md`**
    - Entities, fields, types, relationships, and ownership. Populated with
      placeholder sections — filled in by the schema agent and spec agent.

    **`docs/user-guide.md`**
    - Current user-facing behaviour described from the user's perspective. Populated
      with placeholder sections — filled in by the spec agent.

    **`docs/project-overview.md`**
    - Business context, stakeholders, tech stack. Populated during init with the
      project name, stack, and context provided by the human. Updated rarely.

    **`docs/production-feedback.md`**
    - Incident log with columns: Date, Feature, Layer, Severity, Root cause, What
      changed, Prevention. Starts empty — populated as incidents occur.

    ### `specs/`

    **`specs/README.md`**
    - Feature index table with columns: ID, Name, Status, Problem statement link,
      Solution design link. Starts with only the header row and status legend comment.

    **`specs/_template/SKIP-RUBRIC.md`**
    - Five checkable criteria for skipping backlog and test spec. Includes usage
      instructions and revisit policy.

    **`specs/_template/1-problem-statement.md`**
    - Template with YAML frontmatter (id, status, date, author) and three sections:
      Problem, Success criteria, Non-functional Requirements.

    **`specs/_template/2-solution-design.md`**
    - Template with YAML frontmatter and sections: Layers required, Functional
      Overview, UI outline, Interface contracts, Impact/change specifications,
      Failure modes, Observability, Rollback plan, Prioritised functions.

    **`specs/_template/3-backlog.md`**
    - Template with tasks table and parallelisation map (wave-based worktree
      assignments).

    **`specs/_template/4-test-spec.md`**
    - Template with acceptance criteria trace, unit tests, integration tests,
      edge cases, and regression tests tables.

    ### `backend/`

    **`backend/pyproject.toml`**
    - Python backend service configuration. Dependencies: FastAPI, Pydantic v2,
      SQLAlchemy 2.0, Alembic, uvicorn, pytest, httpx. Python ≥3.12. Entry point
      for the backend service.

    **`backend/alembic.ini`**
    - Alembic configuration pointing to `backend/src/app/core/database.py` for
      the SQLAlchemy engine. Migration directory: `backend/alembic/versions/`.

    **`backend/alembic/env.py`**
    - Alembic environment setup. Imports SQLAlchemy metadata from the app's models.
      Configured for async migrations if the stack uses async SQLAlchemy.

    **`backend/alembic/versions/`**
    - Empty directory. Migration files are created by the schema agent.

    **`backend/src/app/__init__.py`**
    - Package init. Empty or contains version string.

    **`backend/src/app/main.py`**
    - FastAPI application factory. Creates the app, includes the v1 API router,
      configures CORS, and wires dependencies. Returns the app object for uvicorn.

    **`backend/src/app/api/__init__.py`**
    - Package init. Empty.

    **`backend/src/app/api/v1/__init__.py`**
    - Package init. Imports and includes all v1 route modules.

    **`backend/src/app/api/dependencies.py`**
    - Shared FastAPI dependencies: database session, current user, configuration.
      Used across route modules.

    **`backend/src/app/core/config.py`**
    - Pydantic Settings class. Reads from environment variables with sensible
      defaults for local development. Fields: DATABASE_URL, SECRET_KEY, DEBUG,
      CORS_ORIGINS.

    **`backend/src/app/core/database.py`**
    - SQLAlchemy async engine and session factory. Provides a `get_db` async
      generator dependency. Creates the engine from `config.DATABASE_URL`.

    **`backend/src/app/models/`**
    - Empty directory. SQLAlchemy ORM models are created by the schema agent.

    **`backend/src/app/schemas/`**
    - Empty directory. Pydantic request/response schemas are created by the
      schema agent.

    **`backend/src/app/services/`**
    - Empty directory. Business logic services are created by the backend agent.

    **`backend/tests/conftest.py`**
    - Pytest fixtures: test database, async test client, auth headers. Configures
      a test database that is created and torn down per session.

    **`backend/tests/api/`**
    - Empty directory. API integration tests are created alongside feature
      implementation.

    **`backend/tests/models/`**
    - Empty directory. Model unit tests are created alongside feature
      implementation.

    **`backend/tests/services/`**
    - Empty directory. Service unit tests are created alongside feature
      implementation.

    ### `frontend/`

    **`frontend/package.json`**
    - Node project configuration. Dependencies: React 18+, Vite, Tailwind CSS,
      TypeScript. Dev dependencies: Playwright, Vitest, ESLint, Prettier.
      Scripts: `dev`, `build`, `preview`, `test`, `lint`, `e2e`.

    **`frontend/tsconfig.json`**
    - TypeScript configuration. Strict mode enabled. Paths aliased (`@/` →
      `src/`). JSX: react-jsx. Target: ES2022. Module: ESNext.

    **`frontend/playwright.config.ts`**
    - Playwright E2E test configuration. Web server pointing to the Vite dev
      server. Test directory: `e2e/`. Browsers: Chromium, Firefox, WebKit.

    **`frontend/src/main.tsx`**
    - Application entry point. Renders the root App component into the DOM.
      Imports global CSS (Tailwind directives).

    **`frontend/src/components/`**
    - Empty directory. UI components are created by the frontend agent.

    **`frontend/src/utils/`**
    - Empty directory. Utility functions and API client code are created by
      the frontend agent.

    **`frontend/e2e/`**
    - Empty directory. Playwright E2E test files are created alongside feature
      implementation.

    **`frontend/public/`**
    - Empty directory. Static assets (favicon, robots.txt) — populated by the
      human or frontend agent as needed.

    ### `docker/`

    **`docker/backend.Dockerfile`**
    - Multi-stage Python Dockerfile. Build stage installs dependencies from
      `backend/pyproject.toml`. Runtime stage copies the app and runs uvicorn.
      Python 3.12-slim base image. Non-root user.

    **`docker/frontend.Dockerfile`**
    - Multi-stage Node Dockerfile. Build stage runs `npm ci && npm run build`.
      Runtime stage serves static files via nginx:alpine. Node 20-alpine base
      image for build.

 7. **Idempotency and conflict handling:** Rules for existing files.

### Methodology layer — changed

**`README.md`**

Updated to describe the AI-driven initialization workflow. The quick-start section
documents how to explicitly load `agents/prompts/project-init.md` for
project initialization, and that a fresh session with `AGENTS.md` should follow.

**`AGENTS.md`**

Entry-point detection for scenario 1 updated to instruct the human to load the
project-init agent explicitly, rather than running `greenfield-setup.md` or the CLI.
The project-init agent is not auto-loaded through `AGENTS.md` — it is a standalone
pre-step.

### Methodology layer — removed

| Path | Reason |
|---|---|
| `agents/prompts/greenfield-setup.md` | Scenario 1 (greenfield scaffolding) — replaced by the project-init agent |
| `agents/prompts/brownfield-onboarding.md` | Scenario 2 (brownfield onboarding) — replaced by the project-init agent |

The `refactor-agent.md` prompt is retained — it operates post-init between feature
batches and is unrelated to project initialization.

### Code layer — removed

| Path | Reason |
|---|---|
| `src/ai_project/` | CLI tool, scaffold, verify — replaced by the project-init agent |
| `src/blueprint.egg-info/` | Package metadata — no longer a package |
| `pyproject.toml` | Build configuration — no longer a Python package |
| `tests/` | CLI test suite — no code to test |

The `blueprint-methodology-v4.md` PDF document remains at the project root.

### Behaviour existing callers can still rely on

- The 8 standard lifecycle agent prompts in `agents/prompts/` continue to function
  identically for projects initialized under the new approach. Their content is unchanged.
  The `greenfield-setup` and `brownfield-onboarding` prompts are deprecated — their
  function is handled by the project-init agent.
- The standing docs format is unchanged — they are populated with the same template content
  as before.
- `AGENTS.md` continues to perform entry-point detection. Scenario 1 now directs the
  human to load the project-init agent explicitly, rather than auto-routing to a prompt.
- Feature specs (001, 002, 003) are preserved verbatim.

## Failure modes

| Component | Failure | Human sees | Recovery path |
|---|---|---|---|
| Assessment | Directory contains both `AGENTS.md` and no other convention files (partial onboard) | Agent reports "mixed state" and asks for guidance | Human clarifies intent; agent follows instructions |
| Assessment | Directory is a git repo with submodules or unusual layout | Agent may misdetect scenario | Agent reports its assessment reasoning; human can override |
| File write | Permission denied on target directory | "Cannot write to `<path>` — permission denied" | Human fixes permissions; agent retries |
| File write | File already exists (idempotency conflict) | "`<path>` already exists. Skip or overwrite?" | Human chooses; agent proceeds |
| Plan review | Human provides ambiguous feedback on `init-plan.md` | Agent asks clarifying question | Human clarifies; agent revises |
| Large manifest | Prompt is too large for some AI models | N/A — design constraint; the prompt targets models with ≥128K context windows | Document minimum context requirement in README |

## Observability

The agent's observability is the conversation itself — every action is reported to the
human as it happens. No separate logging or metrics. After completion, the agent provides
a summary: files created, files skipped, and next steps.

If the agent fails mid-operation, it reports what was completed and what remains. The
human can ask it to resume or start over.

## Rollback plan

All operations are additive (create files/directories) or read-only (assessment). The
agent never deletes files except when explicitly asked during a refactoring operation,
which requires plan approval first. Rollback is:

- **During greenfield scaffold:** Delete the created directory — no existing files were
  touched.
- **During docs+specs only:** Delete `docs/` and `specs/` — no existing files were touched.
- **During full refactor:** Revert via git (`git checkout .`) since the plan gate ensures
  the human reviewed the changes before execution.

## Prioritised functions

| Function | Priority | Ordering driver | Acceptance criteria |
|---|---|---|---|
| Assessment logic | 1 | Technical dependency — must detect scenario before any action | Correctly identifies greenfield, brownfield-no-structure, and brownfield-with-structure |
| Greenfield scaffold (full tree) | 1 | Business value — primary use case | Writes complete convention tree; every file has usable content |
| File manifest (all file contents) | 1 | Technical dependency — all scaffold operations depend on it | Contains every convention file with correct path and complete content |
| Conversation flow — prompts and responses | 2 | Business value — the human interface | Each scenario prompt is clear; the agent responds correctly to all valid inputs |
| Brownfield detection + prompt | 2 | Business value — brownfield adoption | Detects missing convention; presents the three-option prompt |
| Brownfield docs+specs (option 2) | 2 | Business value — lightweight adoption path | Creates docs/ and specs/ without touching existing files |
| Plan gate (`init-plan.md`) | 3 | Safety — prevents irreversible changes | Produces readable plan file; waits for human approval |
| Brownfield refactor (option 1) | 3 | Business value — full adoption | Executes plan only after approval; existing source files preserved or moved as specified |
| Feature spec scaffold (blueprint-structure) | 3 | Business value — feature lifecycle entry | Creates NNN-slug/ with populated outlines; updates README |
| AGENTS.md scenario 1 update | 4 | Integration — points humans to the init agent | Scenario 1 instructs the human to explicitly load the project-init agent |
| README.md update | 4 | Documentation | Quick-start describes AI-driven initialization |
| Code removal (`src/`, `pyproject.toml`, `tests/`) | 5 | Cleanup — removes the old approach | No executable code remains; project still self-bootstraps |

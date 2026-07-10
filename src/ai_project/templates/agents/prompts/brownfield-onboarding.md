# brownfield-onboarding — Scenario 2 Prompt

## Role
You are onboarding an existing codebase into the convention-over-configuration methodology.
The project has working code but no `AGENTS.md`, no `docs/`, and no `specs/` folder. Your
job is to reverse-engineer standing documents from the existing code, present them for human
approval, and scaffold the convention skeleton around the code.

## Inputs
- The existing project directory — read the codebase thoroughly before populating any document.
- The `AGENTS.md` and `METHODOLOGY.md` templates (read them to understand the target structure).

## Process

1. **Survey the codebase.** Read the directory tree, identify the language(s), framework,
   entry points, and test structure. Determine what already exists vs. what the convention
   structure needs.

2. **Reverse-engineer standing docs.** Read the code and produce populated versions of:
   - `docs/architecture.md` — components, layers, integration points. Identify shared
     components and build the known-callers register from actual import/call patterns.
   - `docs/data-dictionary.md` — entities, fields, relationships. Extract from ORM models,
     schema files, or type definitions.
   - `docs/user-guide.md` — current user-facing behaviour. Describe flows from the user's
     perspective, inferred from routes, handlers, and UI code.
   - `docs/project-overview.md` — business context (infer from project name, README, comments),
     stakeholders (ask the human), tech stack (detected from the codebase).

3. **Present for human review.** Show the populated standing docs to the human. Ask them to
   correct errors, fill gaps, and confirm the reverse-engineered understanding. Do not proceed
   until you have explicit approval.

4. **Propose a restructuring plan.** If the existing code has a non-standard layout, propose
   moving files into the `src/` and `tests/` convention directories. Show the human a
   before/after. Do not move files without explicit approval.

5. **Create AGENTS.md** — the lifecycle engine. The detection logic will route into scenario 3
   on subsequent sessions.

6. **Create METHODOLOGY.md** — the human-readable guide.

7. **Create agents/README.md and agents/prompts/** — all nine prompt files.

8. **Create specs/README.md** — an empty feature index.

9. **Create specs/_template/** — all five template files.

10. **Create docs/production-feedback.md** — empty incident log ready for future entries.

## Output
The existing codebase, now convention-compliant. `AGENTS.md` exists. `docs/` contains
human-verified standing docs. The folder structure has `agents/`, `specs/`, and all template
files. The project is ready for scenario 3 (normal feature lifecycle).

## Stopping condition
You are done when the human confirms the standing docs are accurate and the convention
skeleton is in place.

## Verification
- Read `AGENTS.md` and confirm it would route into scenario 3 on next session.
- Confirm every standing doc section is populated — no blanks or "TODO" markers.
- Confirm the known-callers register in `docs/architecture.md` matches actual imports in the
  codebase (at least one spot-check per shared component).

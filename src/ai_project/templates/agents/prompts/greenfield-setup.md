# greenfield-setup — Scenario 1 Prompt

## Role
You are scaffolding a brand-new project that will use the convention-over-configuration
methodology for AI-human collaborative development. Your job is to create the full folder
structure and populate every .md file with headings and explanatory text.

## Inputs
- Human-provided: project name, tech stack, business context
- The `AGENTS.md` and `METHODOLOGY.md` templates (read them to understand the structure)

## Process

1. **Ask the human** for: project name, preferred tech stack (language, framework, database),
   and a one-paragraph business context. Do not proceed without these.

2. **Create the directory structure:**
   ```
   project-root/
   ├── agents/prompts/
   ├── docs/
   ├── specs/_template/
   ├── src/
   └── tests/
   ```

3. **Create AGENTS.md** — the lifecycle engine. Use the template; update the "Known Constraints"
   section with the project's stack.

4. **Create METHODOLOGY.md** — the human-readable guide. Use the template as-is; it is
   project-agnostic.

5. **Create agents/README.md** — the role index. Use the template as-is.

6. **Copy all prompt files into agents/prompts/** — greenfield-setup.md, brownfield-onboarding.md,
   orchestrator.md, schema-agent.md, backend-agent.md, frontend-agent.md, spec-agent.md,
   review-agent.md, refactor-agent.md. These are identical across all projects.

7. **Create docs/** standing documents — architecture.md, data-dictionary.md, user-guide.md,
   project-overview.md, production-feedback.md. Each must have every section heading populated
   with an explanation of what goes in that section. Seed project-overview.md with the
   human-provided business context, tech stack, and project name.

8. **Create specs/README.md** — an empty feature index with the status key comment.

9. **Create specs/_template/** — SKIP-RUBRIC.md, 1-problem-statement.md, 2-solution-design.md,
   3-backlog.md, 4-test-spec.md. These are the canonical feature templates.

10. **Create pyproject.toml** — a minimal project metadata file with the project name and
    Python version. No dependencies except what the human specified.

## Output
A fully scaffolded project directory. Every .md file has headings and explanatory text in
every section — no blanks, no "TODO" markers. The human can immediately open this with any
AI agent and the agent will follow `AGENTS.md` into the normal feature lifecycle.

## Stopping condition
You are done when all files exist, all sections are populated with explanatory text, and
`AGENTS.md` routes correctly into scenario 3 (normal lifecycle).

## Verification
- Run `ls -R` and confirm the folder structure matches the specification.
- Read `AGENTS.md` and confirm the entry-point detection logic is present.
- Read one standing doc and confirm every section heading has explanatory text.

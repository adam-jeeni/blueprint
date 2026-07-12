---
id: 003
status: draft
links_to_solution_design: 003
---

# Backlog

## Tasks

| Task ID | Description | Layer | Depends on | Can run parallel with |
|---|---|---|---|---|
| 003-1 | Write `agents/prompts/project-init.md` — the complete agent prompt containing role, assessment logic, conversation flows, plan gate rules, file manifest (all ~46 files with complete content), and idempotency rules | Methodology | — | — |
| 003-2 | Update `AGENTS.md` — change scenario 1 to instruct the human to load the project-init agent explicitly; update project structure tree (remove `src/`, `tests/`, `pyproject.toml`; add `backend/`, `frontend/`, `docker/`); remove Non-Negotiables and Known Constraints referencing the CLI | Methodology | 003-1 | 003-3, 003-4, 003-5 |
| 003-3 | Update `README.md` — replace CLI quick-start (`pip install`, `blueprint init`) with AI-driven workflow instructions (load project-init agent → scaffold → fresh session with AGENTS.md) | Methodology | 003-1 | 003-2, 003-4, 003-5 |
| 003-4 | Remove deprecated prompts: `agents/prompts/greenfield-setup.md` and `agents/prompts/brownfield-onboarding.md` | Methodology | — | 003-1, 003-5 |
| 003-5 | Remove code layer: delete `src/ai_project/`, `src/blueprint.egg-info/`, `pyproject.toml`, and `tests/` | Code | — | 003-1, 003-4 |

## Parallelisation map

### Wave 1 (no dependencies)
- **[Worktree A]** Task 003-1 — Write project-init.md
- **[Worktree B]** Task 003-4 — Remove deprecated prompts
- **[Worktree C]** Task 003-5 — Remove code layer

Wave 1 runs three independent workstreams in parallel. Task 003-1 is the largest —
the prompt contains all assessment logic, conversation flows, and the full file
manifest with complete content for every file in the canonical tree. Tasks 003-4
and 003-5 are simple deletions.

### Wave 2 (depends on wave 1)
- **[Worktree D]** Task 003-2 — Update AGENTS.md
- **[Worktree E]** Task 003-3 — Update README.md

Both depend on 003-1 completing — they need to reference the new prompt filename
and describe the workflow correctly. They touch different files and can run in
parallel within the wave.

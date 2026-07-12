---
id: NNN
status: draft
links_to_solution_design: NNN
---

# Backlog
[Sequenced implementation tasks derived from the solution design. Each task is a unit of work one agent can complete independently. Tasks sharing no dependencies run in parallel in separate worktrees.]

## Tasks
[One row per task. Task IDs use the pattern NNN-M. The description should name the specific function or file the agent will create or modify.]

| Task ID | Description | Layer | Depends on | Can run parallel with |
|---|---|---|---|---|
| NNN-1 | [What to build] | [data / backend / frontend] | [Task IDs that must finish first] | [Task IDs that can run concurrently] |

## Parallelisation map
[Group tasks into waves. Wave 1 has no dependencies. Tasks in the same wave run concurrently. Tasks touching the same file must NOT be in the same wave.]

### Wave 1 (no dependencies)
- [Worktree A] Tasks: [NNN-1, NNN-2]

### Wave 2 (depends on wave 1)
- [Worktree B] Tasks: [NNN-3]

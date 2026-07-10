---
id: 001
status: draft
links_to_solution_design: 001
---

# Backlog

## Tasks

| Task ID | Description | Layer | Depends on | Can run parallel with |
|---|---|---|---|---|
| 001-1 | Create `src/ai_project/__init__.py` with version string | Core | none | 001-2 |
| 001-2 | Package template files into `src/ai_project/templates/` | Core | none | 001-1 |
| 001-3 | Implement `_copy_template_dir()` and `_render_template()` | Core | 001-2 | — |
| 001-4 | Implement `init_project()` using `_copy_template_dir()` | Core | 001-3 | — |
| 001-5 | Implement `onboard_project()` | Core | 001-3 | 001-4 |
| 001-6 | Implement `new_feature()` | Core | 001-3 | 001-4, 001-5 |
| 001-7 | Implement `verify_structure()` and `verify_docs()` | Core | none | 001-4, 001-5, 001-6 |
| 001-8 | Implement `main()` with argparse subcommand dispatch | CLI | 001-4, 001-5, 001-6, 001-7 | — |
| 001-9 | Create `pyproject.toml` with entry point | CLI | none | all |
| 001-10 | Write tests for all core functions | Tests | 001-4, 001-5, 001-6, 001-7 | 001-8 |

## Parallelisation map

### Wave 1 (no dependencies)
- [Worktree A] Tasks: 001-1, 001-2, 001-7, 001-9 — all independent of each other

### Wave 2 (depends on wave 1)
- [Worktree B] Tasks: 001-3 (depends on 001-2 for template path)
- [Worktree C] Tasks: 001-4, 001-5, 001-6 (all depend on 001-3 for shared helper)

### Wave 3 (depends on wave 2)
- [Worktree D] Tasks: 001-8 (depends on all core functions being available)
- [Worktree E] Tasks: 001-10 (depends on all core functions being available)

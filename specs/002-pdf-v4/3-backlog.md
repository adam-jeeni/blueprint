---
id: 002
status: draft
links_to_solution_design: 002
---

# Backlog

## Tasks

| Task ID | Description | Layer | Depends on | Can run parallel with |
|---|---|---|---|---|
| 002-1 | Write executive summary and problem statement sections (§1-2) | Document | none | — |
| 002-2 | Write `blueprint` CLI section (§3) | Document | none | 002-1 |
| 002-3 | Write Architecture Advisor + hierarchy section (§4) | Document | none | 002-2 |
| 002-4 | Write folder structure + conventions section (§5) | Document | none | 002-2, 002-3 |
| 002-5 | Write entry-point scenarios section (§6) | Document | none | 002-4 |
| 002-6 | Write token-efficiency section (§7) | Document | none | 002-4, 002-5 |
| 002-7 | Write worked example section (§8) | Document | none | 002-6 |
| 002-8 | Write failure modes section (§9) | Document | none | 002-7 |
| 002-9 | Write two-document model section (§10) | Document | none | 002-8 |
| 002-10 | Write appendix (§A) | Document | 002-4, 002-5, 002-6 | 002-7, 002-8, 002-9 |
| 002-11 | Create diagrams (lifecycle, hierarchy, folder structure, entry points) | Document | 002-4, 002-5 | 002-7, 002-8, 002-9 |
| 002-12 | Compose PDF, cross-check against AGENTS.md and METHODOLOGY.md | Document | 002-1 through 002-11 | — |
| 002-13 | Archive old v3 PDF, place v4 at workspace root | Document | 002-12 | — |

## Parallelisation map

### Wave 1 (no dependencies)
- [Worktree A] Tasks: 002-1, 002-2, 002-3 — introductory sections, independent of each other
- [Worktree B] Tasks: 002-4, 002-5 — structure and scenarios

### Wave 2 (depends on wave 1)
- [Worktree C] Tasks: 002-6, 002-7 — token efficiency + worked example (both depend on structure being defined)
- [Worktree D] Tasks: 002-8, 002-9 — failure modes + two-document model

### Wave 3 (depends on wave 2)
- [Worktree E] Tasks: 002-10, 002-11 — appendix + diagrams (need all content to be final)
- [Worktree F] Tasks: 002-12 — compose final PDF

### Wave 4
- [Worktree G] Tasks: 002-13 — archive old, place new

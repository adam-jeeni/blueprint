---
id: 002
status: draft
date: 2026-07-10
links_to_problem_statement: 002
inputs_consulted:
  architecture_version: 2026-07-10
  data_dictionary_version: 2026-07-10
  user_guide_version: 2026-07-10
  project_overview_version: 2026-07-10
---

# Solution design

## Layers required
No software layers — this is a document production feature. Produces a single PDF file.

## Interface contracts
No APIs. The PDF is a standalone file produced by an AI agent (or human) and placed at the
workspace root as `blueprint-methodology-v4.pdf`.

## Impact / change specifications

### Document layer change specification

**Created:** `blueprint-methodology-v4.pdf` — a 12-16 page PDF at the workspace root. Replaces
`specifying-software-for-ai-development-extended-v3.pdf` which can be archived or deleted.

**Changed:** None.

**Removed:** None.

**Behaviour existing callers can still rely on:** N/A — standalone document, no callers.

**Acceptance criteria:**
- Contains all sections listed in Prioritised Functions below.
- Contains at least 4 diagrams (lifecycle, agent hierarchy, folder structure, entry points).
- Contains the Country Collection worked example, updated for the `blueprint` workflow.
- Contains an honest failure-modes section.
- Is a valid PDF file, readable in any PDF viewer.
- References `blueprint` as the CLI command throughout.

## Failure modes

| Component | Failure | User sees | Logged at | Recovery path |
|---|---|---|---|---|
| PDF generation | Diagram rendering fails | Placeholder or text fallback in PDF | N/A (document) | Regenerate PDF with fixed diagram |
| PDF generation | Content references outdated feature names | Reader confused | N/A | Cross-check against AGENTS.md and METHODOLOGY.md before finalising |
| PDF consumption | Reader skips to the end without reading the argument | Low adoption | N/A | Executive summary on page 1; "what this is" in the first paragraph |

## Observability
N/A — no runtime component.

## Rollback plan
Keep the v3 PDF until v4 is approved. Delete or archive the old version after the human confirms
the new one is accurate. If v4 contains errors, revert to v3 as a reference while correcting v4.

## Prioritised functions

| Function | Layer | Priority | Ordering driver | Acceptance criteria |
|---|---|---|---|---|
| Executive summary + problem statement | Document §1-2 | 1 | Opening argument — nothing else matters if this doesn't land | Reader can state the three failure modes and why the methodology closes them |
| `blueprint` CLI as the central metaphor | Document §3 | 1 | The big change from v3 — the methodology is now a product | Reader understands `blueprint init`, `onboard`, `new-feature`, `verify` |
| Architecture Advisor + agent hierarchy | Document §4 | 1 | New role that didn't exist in v3 | Reader understands the 10 roles, the advisor's place, and the human's workflow |
| Folder structure + conventions | Document §5 | 2 | Visual reference | Reader can describe the project layout and naming conventions |
| Three entry-point scenarios | Document §6 | 2 | Practical — how do I actually start? | Reader can identify which scenario applies to their situation |
| Token-efficiency design | Document §7 | 2 | Answers the cost objection | Reader understands the comment-stripping, scoped reads, and layer filtering |
| Country Collection worked example | Document §8 | 3 | Persuasive — a real feature, really shipped | Reader can trace the workflow from idea to shipped code |
| Where it still fails | Document §9 | 3 | Honesty — credibility depends on it | Reader can name at least two limitations of the methodology |
| Two-document model (PDF + METHODOLOGY.md) | Document §10 | 3 | Explains the split | Reader understands which document to read for which purpose |
| Appendix: quick reference | Document §A | 4 | Reference value | Reader can find the agent hierarchy, CLI commands, and folder structure in one place |

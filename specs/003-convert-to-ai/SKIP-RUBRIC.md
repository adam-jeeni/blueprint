---
id: 003
status: draft
---

# SKIP-RUBRIC — when to skip the backlog and test spec

A feature qualifies to skip steps 3 (`3-backlog.md`) and 4 (`4-test-spec.md`) when ALL of
the following are true. If any condition is not met, produce the full backlog and test spec.

## Checkable criteria

- [ ] The change touches **a single file** (not counting test files).
- [ ] The change does **not touch any shared component** listed in `docs/architecture.md`'s
      known-callers register.
- [ ] The change does **not alter the data model** — no new fields, no schema changes,
      no migration required.
- [ ] The acceptance criteria are **fully specified** in `1-problem-statement.md`'s success
      criteria section — no additional design decisions are needed.
- [ ] The test cases are **obvious from the acceptance criteria** — a single test case per
      criterion, no edge cases requiring separate test design.

## How to use this

Before producing `3-backlog.md` and `4-test-spec.md`, the orchestrator checks each criterion
against the feature. If all five are checked true, skip steps 3 and 4. The acceptance criteria
in the problem statement serve as the backlog; the obvious test cases serve as the test spec.

If the orchestrator is unsure about any criterion, default to producing the full artifact.
A skipped artifact that should have existed is a gap. An artifact that exists but is minimal
is cheap.

## When to revisit

If a feature that skipped 3 and 4 subsequently causes a regression or a production incident,
revisit this rubric — the criteria may need tightening. Log the incident in
`docs/production-feedback.md` with the cause category "skip-rubric gap."

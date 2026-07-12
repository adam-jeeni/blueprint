---
status: active
last_updated: 2026-07-10
---

# Production feedback

Incident-driven log. Each entry describes a problem found in production (or during development
that could have become a production problem), what caused it, and what systemic change prevents
it from recurring.

## How to use this

1. When a bug, regression, or surprise is found, add a row.
2. Classify the root cause. Common categories: spec gap, standing-doc error, test gap,
   unknown dependency, config drift, skip-rubric gap, contract violation.
3. The "Prevention" column is the most important — what changed in the methodology, templates,
   prompts, or tooling so the next feature catches this earlier.
4. Over time, the prevention column should trend toward "none needed — already covered" because
   the methodology absorbed the lesson.

## Incidents
[Add a row for each incident. Fill in every column — the "Prevention" column drives systemic improvement.]

| Date | Feature | Layer | Severity | Root cause | What changed | Prevention |
|---|---|---|---|---|---|---|
| [YYYY-MM-DD] | [Feature name] | [data / backend / frontend / docs] | [critical / major / minor] | [spec gap / standing-doc error / test gap / unknown dependency / config drift / contract violation] | [What was fixed in this specific case] | [What systemic change prevents this class of problem from recurring] |

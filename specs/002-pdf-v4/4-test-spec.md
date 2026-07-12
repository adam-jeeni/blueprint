
---
id: 002
status: draft
links_to_solution_design: 002
links_to_problem_statement: 002
---

# Test specification

## Acceptance criteria trace

| Success criterion (from problem statement) | Test case(s) |
|---|---|
| Reader can explain what the methodology does and how to start | TC-1 |
| Document accurately describes all v4 additions | TC-2 |
| Worked example reflects `blueprint` workflow | TC-3 |
| Document includes failure modes section | TC-4 |
| Document replaces v3 PDF | TC-5 |

## Unit tests
N/A — document production has no unit-testable functions.

## Integration tests

| Test case | Components exercised | Setup | Expected result |
|---|---|---|---|
| TC-1 | Human reader | Hand PDF to someone unfamiliar with the methodology; ask them to explain it back after 20 minutes | They correctly describe: three failure modes, `blueprint init`, Architecture Advisor, folder structure, three entry points |
| TC-2 | Cross-reference check | Compare PDF against AGENTS.md, METHODOLOGY.md, agents/README.md, and agents/prompts/*.md | No feature, role, or convention described in the PDF contradicts the actual artifacts |
| TC-3 | Worked example check | Read §8 (Country Collection) and trace the described workflow against the actual process | Every step described in the worked example is achievable with the current `blueprint` CLI and agent prompts |
| TC-4 | Failure modes check | Read §9 and compare against the "Open items" in the original handoff.md | All known limitations are addressed; new ones discovered since v3 are included |
| TC-5 | File replacement | Check that `blueprint-methodology-v4.pdf` exists at workspace root and `specifying-software-for-ai-development-extended-v3.pdf` is archived or absent | New PDF exists, old PDF does not |

## Edge cases and boundary tests

| Test case | Edge condition | Expected result |
|---|---|---|
| TC-EDGE-1 | Reader opens PDF on a mobile device | Diagrams are legible; text reflows correctly |
| TC-EDGE-2 | Reader prints the PDF in black and white | Diagrams are still interpretable without colour |
| TC-EDGE-3 | Reader searches PDF for "blueprint" | All instances are found; no references to "ai-project" remain |
| TC-EDGE-4 | Reader who used the v3 methodology reads v4 | Can identify what changed; doesn't encounter contradictions with their prior knowledge |

## Regression tests

| Test case | Existing behaviour preserved | Caller(s) affected |
|---|---|---|
| TC-REG-1 | The five-step process description is still present (updated for `blueprint`) | Existing readers who learned the v3 process |
| TC-REG-2 | The amendment path is still documented | Implementation agents that follow the amendment flow |
| TC-REG-3 | The doc verification gate is still described | Review agents that run the gate |

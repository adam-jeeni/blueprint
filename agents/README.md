# Agent Prompts

Role index for the operational prompts in `prompts/`. Each file is a template — the
orchestrator fills in feature-specific details before handing it to a sub-agent.

## Entry-point prompts (scenario detection)

| Prompt file | When to use | Who runs it |
|---|---|---|
| `prompts/greenfield-setup.md` | Scenario 1 — empty folder, new project | Orchestrator (or human with `blueprint init`) |
| `prompts/brownfield-onboarding.md` | Scenario 2 — existing code, no convention | Agent, routed by `AGENTS.md` detection |
| `prompts/orchestrator.md` | Scenario 3 — convention in place, normal lifecycle | Orchestrator agent |

## Role prompts (feature lifecycle)

| Prompt file | Role | When deployed |
|---|---|---|
| `prompts/schema-agent.md` | Datastore / migrations | During implementation (step 5), if the feature touches the data layer |
| `prompts/backend-agent.md` | API / services | During implementation (step 5), if the feature touches the backend layer |
| `prompts/frontend-agent.md` | UI / client | During implementation (step 5), if the feature touches the frontend layer |
| `prompts/spec-agent.md` | Document update | After merge (step 7), updates only the standing docs the feature touched |
| `prompts/review-agent.md` | Merge gate | Before merge (step 6), runs full test suite and doc verification |
| `prompts/refactor-agent.md` | Consolidation | Between feature batches, improves structure without changing behaviour |

## Human-facing prompts (specification phase)

| Prompt file | Role | When deployed |
|---|---|---|
| `prompts/architecture-advisor.md` | Design thinking partner | During steps 1–4 (specification). Used by the human — not deployed by the orchestrator. Helps scope ideas, design solutions, spot gaps, and prepare for handoff to the orchestrator. |

## How to use a prompt

1. Read the prompt file to understand the agent's responsibilities and constraints.
2. Fill in the feature-specific details: which files are affected, what the contracts are,
   what the acceptance criteria are.
3. Hand it to the agent as its operating context.
4. Verify the agent's output against the contracts before merging.

## Conventions for prompt files

- Use agent-agnostic language — no tool-specific syntax.
- Specify inputs (what the agent reads) and outputs (what it produces).
- Include stopping conditions: when is the agent done?
- Include verification instructions: how does the orchestrator check the result?

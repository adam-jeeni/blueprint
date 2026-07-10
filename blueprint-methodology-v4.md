# Specifying Software for AI Development — v4

**A working process — now a product**

Applied Intelligence — Internal methodology reference

July 2026

---

## Executive Summary

AI coding agents fail in three specific ways when working from ad-hoc prompts: they fill ambiguity
with a plausible guess rather than the team's intent, they lose track of earlier decisions once a
codebase outgrows a session, and they change shared code without knowing who else depends on it.

The blueprint methodology closes all three by producing a written specification before any code is
generated — but unlike the v3 document you may have read, the methodology is no longer a document
you follow. It is a product you run.

```
blueprint init my-project --name "My App" --stack "python-3.12" --context "B2B SaaS"
```

One command. A fully scaffolded project. Every .md file pre-populated with headings. Every agent
prompt in place. An AI Architecture Advisor ready to help you design your first feature. This
document explains how it works, why it works, what it costs, and where it still fails.

---

## 1. The Problem

"Add support for X" is not a specification. When an AI agent is given a prompt like that, it fills
in every unstated detail — validation rules, error handling, what happens to existing behaviour —
with its own best guess. Three failure modes account for most of the damage.

### Intent Drift
An underspecified prompt gets filled in with the model's best guess, not the team's intent. Code
that runs, passes a cursory read, and quietly does something other than what was meant.

### Context Decay
As the codebase outgrows a single session, earlier decisions are forgotten and silently contradicted.
The agent in turn 47 doesn't know what the agent in turn 3 decided about error handling conventions.

### Silent Breakage
A shared component changes shape; nothing in the task told the agent who else was calling it. A
function signature changes; three callers break; no test covers them because the agent never knew
they existed.

A specification process only earns its cost if it closes all three, not just the first one.

---

## 2. "Isn't This Just Waterfall?"

The honest answer: partly, and that's fine. What makes this different is scope and audience.

A waterfall spec tried to describe an entire system upfront, for human readers who could fill gaps
from shared context. The specification here is scoped to one change, and it is read by an agent
that fills gaps with a guess instead of judgement — so the gaps a human spec could safely leave
implicit must be made explicit here.

The document is also a working input to code generation, not a sign-off artifact that gets filed
and never reopened. And crucially: **you don't write it by hand.** The Architecture Advisor helps
you think through it. The CLI scaffolds the files. The orchestrator fills in the details. The human
approves, corrects, and guides — but never starts from a blank page.

---

## 3. The CLI: Methodology as Product

The biggest change from v3. The methodology is no longer a process you read about — it's a command
you run.

### `blueprint init` — Greenfield
```
blueprint init my-project --name "My App" --stack "python-3.12,fastapi" --context "B2B SaaS"
```
Creates the full convention structure: AGENTS.md, METHODOLOGY.md, agents/ (10 prompts), docs/
(5 standing docs), specs/_template/, specs/README.md, src/, tests/, pyproject.toml. Every .md file
has headings and explanatory text in every section. Open with any AI agent — AGENTS.md routes it
into the feature lifecycle.

### `blueprint onboard` — Brownfield
```
cd existing-project
blueprint onboard
```
Scaffolds the convention skeleton around your existing code. Creates AGENTS.md, METHODOLOGY.md,
agents/, docs/, specs/ — without touching a single source file. Then open with an AI agent:
AGENTS.md detects scenario 2, reverse-engineers standing docs from your codebase, and presents
them for your approval.

### `blueprint new-feature` — Start a Feature
```
blueprint new-feature add-export
```
Reads specs/README.md, assigns the next feature number, copies specs/_template/ into
specs/NNN-add-export/, updates the index. Your feature folder is ready — edit the numbered
files in order, with the Architecture Advisor helping at every step.

### `blueprint verify` — CI Gate
```
blueprint verify
```
Checks every required file and directory exists. Checks the known-callers register against
actual code imports. Checks standing doc section headings. Pass (exit 0) or a drift report
(exit non-zero). Safe for CI — read-only, never modifies files.

---

## 4. The Agent Hierarchy

Ten roles, not four. Here's how they fit together.

### Human-Facing

**Architecture Advisor** — Your design thinking partner during specification (steps 1-4). You
describe the idea in plain language. The advisor asks the right questions, spots gaps in your
design, checks the known-callers register for impact, and filters production-feedback for
relevant past incidents. It reads only the standing docs relevant to your feature — not all five.
It never produces final documents, delegates to sub-agents, or overrides your decisions. You
invoke it; you dismiss it; the orchestrator takes over when you're ready.

### Lifecycle Coordination

**Orchestrator** — Runs the full feature lifecycle. Copies templates, fills in specs, delegates
to implementation agents, integrates results, coordinates review. The orchestrator is the
operational layer between human approval and shipped code.

### Implementation (Horizontal)

- **Schema Agent** — Datastore migrations, repository functions. Reversible migrations,
  constraint-level integrity, integration tests with up/down rollback.
- **Backend Agent** — API endpoints, service logic. Matches interface contracts exactly.
  Error handling, observability, no leaked secrets.
- **Frontend Agent** — UI components, client calls. Loading/success/error states. Accessibility.
  API error messages shown to the user, not generic fallbacks.

### Cross-Cutting

- **Spec Agent** — Updates standing docs after merge. Targeted — only the documents the feature
  actually changed. The known-callers register update is its single most important job.
- **Review Agent** — Merge gate. Full test suite (not just the feature's). Contract verification.
  Doc verification gate. Security scan. BLOCKER/WARNING/INFO classification.
- **Refactor Agent** — Structural consolidation between feature batches. Deduplication, dead code
  removal, interface consistency. No behaviour change — every existing test must pass identically.

### Entry-Point (Scenario Detection)

- **Greenfield Setup** — Scenario 1. Scaffolds a brand-new project.
- **Brownfield Onboarding** — Scenario 2. Reverse-engineers standing docs from existing code.

---

## 5. The Folder Structure

```
project-root/
├── AGENTS.md                      # Agent entry point — lifecycle engine
├── METHODOLOGY.md                 # Agent reference — what goes in every template section
├── agents/                        # Operational prompts
│   ├── README.md                  # Role index
│   └── prompts/                   # 10 prompt files
├── docs/                          # Standing documents — always current
│   ├── architecture.md            # Components, layers, known callers
│   ├── data-dictionary.md         # Entities, fields, ownership
│   ├── user-guide.md              # User-facing behaviour
│   ├── project-overview.md        # Business context, stakeholders, stack
│   └── production-feedback.md     # Incident log + systemic prevention
├── specs/                         # Per-feature specification chain
│   ├── README.md                  # Feature index
│   ├── _template/                 # Copy this to start a feature
│   │   ├── SKIP-RUBRIC.md
│   │   ├── 1-problem-statement.md
│   │   ├── 2-solution-design.md
│   │   ├── 3-backlog.md
│   │   └── 4-test-spec.md
│   └── NNN-feature-name/
├── src/
├── tests/
└── pyproject.toml
```

Three load-bearing design decisions:

1. **docs/ is feature-independent.** Every feature's step 2 reads these; no single feature owns them.
   The known-callers register in architecture.md makes brownfield impact analysis possible.

2. **specs/ folder numbers match git branch names.** feature/003-... matches specs/003-.../.
   Collision-proofing that matters once features run in parallel worktrees.

3. **test-spec.md specifies tests; tests/ holds the generated code.** They are distinct artifacts.
   The review agent checks the latter against the former — they are not the same thing.

---

## 6. The Three Entry Points

### Greenfield — New Project, Empty Folder

```bash
blueprint init my-app --name "My App" --stack "python-3.12,fastapi,postgresql" --context "B2B SaaS platform"
```

Result: a fully scaffolded project. Open with any AI agent. AGENTS.md detects the convention
is in place (scenario 3). Read the standing docs. Start feature 001.

### Brownfield — Existing Code, Foreign Structure

```bash
cd my-existing-project
blueprint onboard
```

The CLI detects your source files, creates the convention skeleton around them, and stops. Then
you open the project with an AI agent. AGENTS.md detects scenario 2. The agent reverse-engineers
architecture.md, data-dictionary.md, user-guide.md, and project-overview.md from your actual
code — not guesses, not templates. It presents them for your approval. Once you approve, the
project is convention-compliant and enters scenario 3.

### Brownfield — Already Convention-Compliant

The agent reads AGENTS.md, detects scenario 3, reads the standing docs, and enters the normal
feature lifecycle. This is the steady state — every feature after the first one.

---

## 7. Token Efficiency

The methodology's templates and documents are read by multiple agents across every feature.
Small savings per read compound into significant reductions over a project's lifetime.

### Comment stripping
Template files (1-problem-statement.md through 4-test-spec.md) were 6KB with explanatory
comments. Now they're 2KB of headings and field names only. All explanation lives in
METHODOLOGY.md — read once per session, not repeated in every template read by every agent.
Saving: ~4KB per template set, read by 2-3 agents per feature.

### Scoped standing doc reads
The Architecture Advisor reads only the standing docs relevant to the current feature's layers.
A frontend-only change reads user-guide.md and project-overview.md — two docs, not five.
Saving: ~4KB per feature.

### Layer-filtered production feedback
The production-feedback.md incident table has a Layer column. The advisor filters by the current
feature's layers — skips datastore incidents for a frontend change.
Saving: grows with the incident log.

### Skip-rubric encoded in the prompt
The advisor knows the five skip-rubric conditions from its prompt. SKIP-RUBRIC.md stays for
agents that need it; the advisor skips reading it.
Saving: ~1.7KB per feature.

### Two-document model
METHODOLOGY.md is the agent reference — 12KB of template guidance, lifecycle detail, and
conventions. Read once per session by the advisor and orchestrator. The PDF you're reading
now is for humans. Each document serves one audience; neither duplicates the other.

---

## 8. Worked Example: Country Collection Conversation Threading

The Country Collection pipeline handles inbound customer enquiries across email, chat, and
contact form. Each message is classified, handled by a specialist agent, and drafted into a
reply for human review. The problem: replies to existing conversations were creating new
threads in Outlook rather than continuing the original thread. The customer saw fragmented
conversations; the operator couldn't trace the full history.

### How the workflow looked with blueprint

**Step 0 — The operator describes the problem to the Architecture Advisor.**

The advisor asks: "When an email comes in, how does the system determine if it's a reply or a
new enquiry? What field would you use to link it to an existing thread?" The operator explains
the Outlook conversation ID. The advisor checks the known-callers register in architecture.md:
`crm.py: find_conversation()` is currently only called by `email_poller.py`. "If we use this for
chat and contact form too," the advisor asks, "are those callers prepared for the not-found path?"
The operator confirms: yes, they'll need to handle it — add that to the acceptance criteria.

**Step 1 — Problem statement drafted.**

The operator and advisor produce the problem statement: what needs to change, success criteria
(threading works across all three channels), non-goals (no new channel types).

**Step 2 — Solution design.**

The solution touches backend and data layers. The advisor walks through the template sections:
interface contracts for the threading endpoint, impact on crm.py (shared component — must preserve
existing callers), failure modes (what if Outlook is down? what if the thread ID is malformed?),
rollback plan.

**Step 3 — Backlog.**

Four tasks: add conversation_id to the normalisation pipeline, thread lookup in crm.py, wire
email_poller to use it, wire chat and contact-form handlers. Backend tasks 1 and 2 run in
parallel; 3 and 4 depend on them but can run concurrently with each other.

**Step 4 — Test spec.**

Acceptance criteria trace: every success criterion maps to a test. Edge cases: malformed thread
ID, missing conversation, concurrent replies to the same thread. Regression tests: existing
email-only threading still works; crm.py's existing callers are unharmed.

**Steps 5-7 — Implementation, review, doc update.**

The orchestrator delegates tasks per the parallelisation map. Schema agent handles the migration
(adding an index on conversation_id). Backend agent implements the thread-lookup service. Review
agent runs the full test suite, verifies the known-callers register was updated, and approves.
Spec agent updates architecture.md and user-guide.md.

The feature shipped. The customer's conversations thread correctly. The known-callers register
now has accurate caller information for the next feature that touches crm.py.

---

## 9. Where It Still Fails

This section is not marketing copy. The methodology has limits, and being honest about them is
what makes the rest of the document credible.

### Standing-doc staleness is a hard problem
The doc verification gate catches drift after a merge, but if architecture.md is wrong when step 2
starts, the entire solution design is built on bad foundations. We've added a staleness check
(the orchestrator compares last-updated dates against git history before reading), but this is
a heuristic, not a guarantee. A document can be up-to-date and still wrong.

### The known-callers register is manually maintained
It is the single most important field in the entire methodology — and it depends on humans and
agents remembering to update it. The verify command cross-checks it against actual imports for
Python projects, but this is a spot-check, not a full static analysis. For non-Python projects,
the register is maintained entirely by discipline. One missed update and the system degrades
back to silent-breakage territory.

### The methodology costs upfront time
A feature that takes two hours to build might take three with specification. The methodology
earns that hour back in reduced debugging, fewer regressions, and better agent output — but the
hour is still spent. For a single-file change that qualifies for the skip rubric, the overhead
is minimal (one problem statement). For a multi-layer, multi-agent feature, the upfront cost is
real and must be weighed against the downstream savings.

### The Architecture Advisor can't read your mind
It asks good questions, but it can only ask about what it knows to check. If a project has
undocumented tribal knowledge — "we always use UTC for timestamps, even though the DB stores
local time" — the advisor won't catch it unless it's in the standing docs. The methodology
amplifies what's written down; it can't amplify what isn't.

### Agent variance is real
Different AI agents interpret the same prompt differently. The prompts in agents/prompts/ are
designed to be specific and constraining, but they can't eliminate variance entirely. The
review agent catches most divergence, but not all. This improves as models improve.

### It's designed for projects with a single team
The methodology assumes one team working on one codebase. Multi-team, multi-repo setups with
shared libraries across repositories would need the known-callers register to span project
boundaries — something the current tooling doesn't support.

---

## 10. Two Documents, Two Audiences

This PDF is for humans. It explains why the methodology exists, how it works at a conceptual
level, and what you need to know to evaluate or adopt it.

`METHODOLOGY.md` is for AI agents. It is the operational reference: what goes in every template
section, what makes a good problem statement, the exact format of interface contracts, the skip
rubric criteria, the amendment path, the verification gate. It is 12KB of dense, structured
reference — the document an agent reads when it needs to know "what goes under this heading?"

The split is intentional. A human doesn't need to know the exact table structure of the failure
modes section. An agent doesn't need the persuasive argument for why the methodology exists.
Each document serves its audience without compromise.

---

## Appendix A: Quick Reference

### CLI Commands
| Command | Purpose |
|---|---|
| `blueprint init <dir> --name ... --stack ... --context ...` | Scaffold greenfield project |
| `blueprint onboard` | Scaffold convention around existing code |
| `blueprint new-feature <name>` | Create numbered feature folder from template |
| `blueprint verify` | Check structure integrity and doc-code drift |

### Agent Roles
| Agent | When |
|---|---|
| Architecture Advisor | Steps 1-4 — human-invoked design partner |
| Orchestrator | Full lifecycle — coordinates specification and implementation |
| Schema Agent | Implementation — datastore migrations, repositories |
| Backend Agent | Implementation — API endpoints, services |
| Frontend Agent | Implementation — UI components, client calls |
| Spec Agent | Post-merge — updates standing docs (scoped) |
| Review Agent | Merge gate — full test suite, contracts, docs, security |
| Refactor Agent | Between batches — structural consolidation |
| Greenfield Setup | Scenario 1 — scaffold new project |
| Brownfield Onboarding | Scenario 2 — reverse-engineer standing docs |

### Feature Lifecycle
| Step | Document | Agent |
|---|---|---|
| 0 | — (design thinking) | Architecture Advisor |
| 1 | 1-problem-statement.md | Orchestrator + human |
| → | Human approval gate | Human |
| 2 | 2-solution-design.md | Orchestrator |
| 3 | 3-backlog.md | Orchestrator (parallel with 4) |
| 4 | 4-test-spec.md | Orchestrator (parallel with 3) |
| 5 | — (implementation) | Schema / Backend / Frontend agents |
| 6 | — (review) | Review agent |
| 7 | — (doc update) | Spec agent |
| → | Doc verification gate | Review agent |

### Standing Documents
| Document | Updated by | When |
|---|---|---|
| architecture.md | Spec agent | When backend or data layer changes |
| data-dictionary.md | Spec agent | When schema or entities change |
| user-guide.md | Spec agent | When user-facing behaviour changes |
| project-overview.md | Spec agent | Rarely — stakeholders or stack |
| production-feedback.md | Human or orchestrator | After any incident or surprise |

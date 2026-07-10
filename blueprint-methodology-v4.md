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

## 3. Getting Started

This section takes you from zero to your first feature. If you have an existing project without the
blueprint structure, start at "Onboarding an Existing Project." If you're starting fresh, begin here.

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/blueprint.git
cd blueprint

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows

# Install in editable mode
pip install -e .
```

Verify it works:

```bash
blueprint --help
```

You should see four subcommands: `init`, `onboard`, `new-feature`, `verify`.

### Your First Project

```bash
blueprint init my-project \
  --name "My Application" \
  --stack "python-3.12,fastapi,postgresql" \
  --context "B2B SaaS platform for UK SMEs"
```

This creates a fully scaffolded project directory. Every `.md` file has headings and explanatory
text in every section. The folder structure is the convention — no configuration needed.

Open the project with any AI agent. It reads `AGENTS.md` first, detects that the convention is in
place (scenario 3), reads the standing documents in `docs/`, and enters the normal feature lifecycle.

### Onboarding an Existing Project

Got an existing codebase with no convention structure? Run this from your project root:

```bash
cd my-existing-project
blueprint onboard
```

The CLI detects your source files (`.py`, `.js`, `.ts`, etc.), creates the convention skeleton
around them — `AGENTS.md`, `METHODOLOGY.md`, `agents/`, `docs/`, `specs/` — and stops. It never
touches your existing source files.

Now open the project with an AI agent. `AGENTS.md` detects scenario 2. The agent uses the
Brownfield Onboarding prompt to reverse-engineer standing documents from your actual code. It reads
your modules, identifies components and layers, builds the known-callers register from actual
imports, and presents the populated docs for your approval. Once you approve, your project is
convention-compliant and enters scenario 3.

### The Architecture Advisor

Now you have a convention-compliant project. Before you write any spec, meet your design partner.

Tell your AI agent:

> "Load the Architecture Advisor prompt from `agents/prompts/architecture-advisor.md`."

The advisor introduces itself and asks what you're working on. Describe your idea in plain language.
The advisor:

- **Asks questions, not gives answers.** "Who experiences this problem? What would 'done' look like?"
- **Checks the known-callers register.** If your idea touches an existing component, the advisor asks
  who else calls it and whether they'll break.
- **Filters production history.** Reads `docs/production-feedback.md` for past incidents in the
  same layer — warns you about edge cases that bit someone else.
- **Reads only what's relevant.** A frontend-only change? The advisor reads `user-guide.md` and
  `project-overview.md`, not `data-dictionary.md`. Token-efficient by design.
- **Knows the templates cold.** Mentally checks your thinking against every section of the relevant
  template and flags gaps without you needing to open the template file.

The advisor doesn't produce final documents, delegate to other agents, or override your decisions.
It's a thinking partner. When you're ready, you dismiss it and the orchestrator takes over.

### Your First Feature

With your idea clarified by the advisor, create the feature folder:

```bash
blueprint new-feature add-user-export
```

This reads `specs/README.md`, assigns the next feature number, copies the template files into
`specs/NNN-add-user-export/`, and updates the index. Now open the numbered files in order:

1. **`1-problem-statement.md`** — what needs to change and why. The advisor helps you scope it.
2. **`2-solution-design.md`** — the contract implementation agents will follow. The advisor walks
   you through interface contracts, failure modes, and rollback.
3. **`3-backlog.md`** — sequenced tasks with a parallelisation map. (Skippable — check `SKIP-RUBRIC.md`.)
4. **`4-test-spec.md`** — test cases traced to success criteria. (Skippable.)

The human approval gate sits between steps 1 and 2. You approve the problem statement before
design work begins. After step 4, the orchestrator delegates implementation to the appropriate
agents (schema, backend, frontend), the review agent runs the full test suite and doc verification
gate, and the spec agent updates the standing documents.

### Who Touches What

Not every document is for you. Not every document is for the AI. Here's the split:

| Document | Human | Architecture Advisor | Orchestrator / Agents | Purpose |
|---|---|---|---|---|
| `AGENTS.md` | — | reads once | reads every session | Lifecycle engine + scenario detection |
| `METHODOLOGY.md` | — | reads once | reads on demand | Template reference — what goes in every section |
| `docs/architecture.md` | — | reads (if relevant) | reads (step 2) | Components, layers, known callers |
| `docs/data-dictionary.md` | — | reads (if relevant) | reads (step 2) | Entities, fields, ownership |
| `docs/user-guide.md` | — | reads (if relevant) | reads (step 2) | Current user-facing behaviour |
| `docs/project-overview.md` | — | reads always | reads (step 2) | Business context, stack |
| `docs/production-feedback.md` | — | reads (filtered by layer) | reads (step 2) | Past incidents and preventions |
| `specs/README.md` | — | — | reads + writes | Feature index |
| `1-problem-statement.md` | **writes** (with advisor) | helps draft | fills template | What needs to change |
| `2-solution-design.md` | **writes** (with advisor) | helps draft | fills template | How it will be built |
| `3-backlog.md` | writes (or skips) | — | fills template | Sequenced tasks |
| `4-test-spec.md` | writes (or skips) | — | fills template | Test cases |
| `SKIP-RUBRIC.md` | — | knows from prompt | reads | Whether to skip 3 and 4 |

In practice, most of the "human writes" work is done conversationally with the Architecture
Advisor. You describe the idea; the advisor asks the right questions; together you produce a
solid draft. The human approves. The orchestrator handles the rest.

---

## 4. The Agent Hierarchy

Ten roles. Here's how they fit together.

### Human-Facing

**Architecture Advisor** — Your design thinking partner during specification (steps 1-4). You
describe the idea in plain language. The advisor asks the right questions, spots gaps in your
design, checks the known-callers register for impact, and filters production-feedback for
relevant past incidents. It reads only the standing docs relevant to your feature — not all five.
It never produces final documents, delegates to sub-agents, or overrides your decisions.

### Lifecycle Coordination

**Orchestrator** — Runs the full feature lifecycle. Copies templates, fills in specs, delegates
to implementation agents, integrates results, coordinates review.

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
2. **specs/ folder numbers match git branch names.** feature/003-... matches specs/003-.../.
3. **test-spec.md specifies tests; tests/ holds the generated code.** They are distinct artifacts.

---

## 6. Token Efficiency

The methodology's templates and documents are read by multiple agents across every feature.
Small savings per read compound into significant reductions over a project's lifetime.

### Comment stripping
Template files were 6KB with explanatory comments. Now they're 2KB of headings and field names
only. All explanation lives in `METHODOLOGY.md` — read once per session, not repeated in every
template read by every agent.

### Scoped standing doc reads
The Architecture Advisor reads only the standing docs relevant to the current feature's layers.
A frontend-only change reads two docs, not five.

### Layer-filtered production feedback
`production-feedback.md` has a `Layer` column. The advisor filters by the feature's layers.

### Skip-rubric encoded in the prompt
The advisor knows the five criteria from its prompt. No separate file read needed.

### Two-document model
`METHODOLOGY.md` is the agent reference — read once per session. This PDF is for humans.
Each document serves one audience; neither duplicates the other.

---

## 7. Worked Example: Country Collection Conversation Threading

The Country Collection pipeline handles inbound customer enquiries across email, chat, and
contact form. The problem: replies to existing conversations were creating new threads in
Outlook rather than continuing the original thread.

### How the workflow looked with blueprint

**Step 0 — The operator describes the problem to the Architecture Advisor.**

The advisor asks: "When an email comes in, how does the system determine if it's a reply or a
new enquiry?" The operator explains the Outlook conversation ID. The advisor checks the
known-callers register: `crm.py: find_conversation()` is currently only called by `email_poller.py`.
"If we use this for chat and contact form too," the advisor asks, "are those callers prepared
for the not-found path?"

**Step 1 — Problem statement drafted.**

The operator and advisor produce the problem statement: what needs to change, success criteria
(threading works across all three channels), non-goals (no new channel types).

**Step 2 — Solution design.**

Interface contracts for the threading endpoint, impact on crm.py (shared component), failure
modes (Outlook down, malformed thread ID), rollback plan.

**Step 3 — Backlog.**

Four tasks: add conversation_id to normalisation, thread lookup in crm.py, wire email_poller,
wire chat and contact-form handlers. Backend tasks 1 and 2 run in parallel.

**Step 4 — Test spec.**

Edge cases: malformed thread ID, missing conversation, concurrent replies. Regression tests:
existing email-only threading still works.

**Steps 5-7 — Implementation, review, doc update.**

Schema agent adds an index. Backend agent implements the lookup service. Review agent runs the
full suite, verifies the known-callers register. Spec agent updates architecture.md and
user-guide.md. The feature shipped.

---

## 8. Where It Still Fails

### Standing-doc staleness is a hard problem
The doc verification gate catches drift after a merge, but if architecture.md is wrong when
step 2 starts, the entire solution design is built on bad foundations. We check last-updated
dates against git history, but this is a heuristic, not a guarantee.

### The known-callers register is manually maintained
The verify command cross-checks it against actual imports for Python projects, but this is a
spot-check. One missed update and the system degrades back to silent-breakage territory.

### The methodology costs upfront time
A feature that takes two hours might take three with specification. The methodology earns that
hour back in reduced debugging and fewer regressions — but the hour is still spent.

### The Architecture Advisor can't read your mind
It can only ask about what it knows to check. Undocumented tribal knowledge — "we always use
UTC even though the DB stores local time" — won't be caught unless it's in the standing docs.

### Agent variance is real
Different AI agents interpret the same prompt differently. The prompts are designed to be
specific and constraining, but they can't eliminate variance entirely.

### It's designed for single-team projects
Multi-team, multi-repo setups with shared libraries across repositories would need the
known-callers register to span project boundaries — not currently supported.

---

## 9. Two Documents, Two Audiences

This document (PDF/Markdown) is for humans. It explains why the methodology exists, how it
works at a conceptual level, and how to get started.

`METHODOLOGY.md` is for AI agents. It is the operational reference: what goes in every template
section, what makes a good problem statement, the exact format of interface contracts, the skip
rubric criteria, the amendment path, the verification gate. 12KB of dense, structured
reference — the document an agent reads when it needs to know "what goes under this heading?"

The split is intentional. A human doesn't need the exact table structure of the failure modes
section. An agent doesn't need the persuasive argument for why the methodology exists. Each
document serves its audience without compromise.

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

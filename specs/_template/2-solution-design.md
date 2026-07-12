---
id: NNN
status: draft
date: YYYY-MM-DD
links_to_problem_statement: NNN
inputs_consulted:
  architecture_version:
  data_dictionary_version:
  user_guide_version:
  project_overview_version:
---

# Solution design
[Translate the problem statement into a concrete technical plan. This is the contract that implementation agents work from — be precise.]

## Layers required
[Which layers does this feature touch? Data (schema / migrations), backend (API / services), frontend (UI / client). List them explicitly — this determines which implementation agents are deployed.]

## Functional Overview
[What does the proposed solution do, at a high level? Describe the core functionality, key workflows, and how the pieces fit together. A few paragraphs — save detail for the contracts below.]

## UI outline
[If the feature has a user-facing surface, describe what the user sees and does — screens, controls, flows. Not wireframes; prose that an agent can reason about. State explicitly if there is no UI.]

## Interface contracts
[Full request/response schemas for every new or changed endpoint. One subsection per endpoint.]

### [Endpoint name]

**Method + path:**
[GET /api/v1/resource]

**Request:**
[Request body shape or query parameters.]

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| [field_name] | [string / int / bool / etc.] | [yes / no] | [rules] | [What this field means] |

**Response (success):**
[Response body shape on success. Include status code.]

| Field | Type | Description |
|---|---|---|
| [field_name] | [type] | [What this field means] |

**Response (error):**
[Error response shapes. Cover at minimum: validation failure (422/400), auth failure (401/403), not found (404), server error (500).]

| Status | Body shape | When |
|---|---|---|
| [HTTP status] | [Response body] | [Condition that triggers this error] |

**Authz:**
[What permissions or roles are required to call this endpoint?]

**Idempotency:**
[Is repeated submission safe? If not, what mechanism prevents duplicates?]

## Impact / change specifications
[One subsection per layer. For each component in that layer, specify what changes.]

### [Layer] change specification

**Changed:**
[Existing components being modified. List file paths and describe the change.]

**Created:**
[New components being introduced. List file paths and describe responsibility.]

**Removed:**
[Components being deleted. Confirm no remaining callers exist (check the known-callers register).]

**Behaviour existing callers can still rely on:**
[Only needed if this touches a shared component. State what behaviour is preserved.]

**Acceptance criteria:**
[Concrete, testable outcomes for this layer.]

## Failure modes
[Per-component: what happens when something fails. Production software is defined by how it degrades.]

| Component | Failure | User sees | Logged at | Recovery path |
|---|---|---|---|---|
| [Component name] | [What fails] | [What the user experiences] | [Log level and message] | [How to recover] |

## Observability
[What gets logged and monitored.]

| What | Level | Metric / log message | Alert threshold |
|---|---|---|---|
| [Event] | [DEBUG / INFO / WARN / ERROR] | [Log message format] | [When to alert] |

## Rollback plan
[How is this feature reversed if deployment fails? "No rollback needed" is acceptable for purely additive changes with no schema impact. For migrations: describe the down migration. For config: describe the revert procedure.]

## Prioritised functions
[Implementation order. Priority 1 functions unblock everything else. State whether ordering is driven by business value or technical dependency.]

| Function | Layer | Priority | Ordering driver | Acceptance criteria |
|---|---|---|---|---|
| [Function name] | [data / backend / frontend] | [1 / 2 / 3] | [business value / technical dependency] | [How to verify it's done] |

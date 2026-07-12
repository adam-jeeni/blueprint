---
status: active
last_updated: 2026-07-10
---

# Architecture

## System overview
[Describe the system at a high level — what it does, who it serves, what stack it runs on.]

## Layers
[Describe each layer of the system: data, backend, frontend. What responsibility does each have? How do they communicate?]

## Components
[Each component in the system. Add a row for every significant module, class, or service.]

| Component | Layer | Responsibility | Module path |
|---|---|---|---|
| [Component name] | [data / backend / frontend] | [What it does] | [File path] |

## Integration points
[How do components communicate? REST, gRPC, message queue, direct function calls? What external services does the system depend on? List each dependency and how it's accessed.]

## Shared components and known callers
[Components used by multiple other components. When changing a shared component, every caller listed here must be checked for breakage. Update this register after every feature merge.]

| Shared component | Callers | Behaviour callers can rely on |
|---|---|---|
| [component path] | [caller 1, caller 2] | [contract / guarantees] |

## Decisions
[Architectural decisions made during development. Record the decision, why it was made, and the date. Revisit when circumstances change.]

| Decision | Rationale | Date |
|---|---|---|
| [What was chosen] | [Why] | YYYY-MM-DD |

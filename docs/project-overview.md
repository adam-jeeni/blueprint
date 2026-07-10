---
status: active
last_updated: 2026-07-10
---

# Project overview

## Business context
`blueprint` is the reference implementation of the convention-over-configuration methodology
for AI-human collaborative software development. It exists to make the methodology instantly
usable: instead of reading a 15-page PDF and manually creating 25+ files, a developer runs one
command and gets a fully scaffolded project.

The tool is to the methodology what `mvn archetype:generate` is to Maven — a single command
that produces a working, convention-compliant starting point.

## Stakeholders
| Name / role | Interest |
|---|---|
| Adam Davies (Applied Intelligence) | Primary author; uses the methodology on Applied Intelligence projects |
| AI agent users | Developers who use AI coding agents and want a spec-first workflow |
| Brownfield project teams | Teams adopting the methodology on existing codebases |

## Tech stack
Python 3.12+ · stdlib only (`argparse`, `pathlib`, `shutil`, `os`, `importlib.resources`)

## Related documents
- [Architecture](./architecture.md)
- [Data dictionary](./data-dictionary.md)
- [User guide](./user-guide.md)
- [Production feedback](./production-feedback.md)

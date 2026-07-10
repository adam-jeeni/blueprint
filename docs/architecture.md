---
status: active
last_updated: 2026-07-10
---

# Architecture

## System overview
`blueprint` is a CLI tool that scaffolds and verifies projects using the convention-over-configuration
methodology for AI-human collaborative development. It is a Python package with no external CLI
dependencies — it uses only stdlib `argparse`, `pathlib`, `shutil`, and `os`.

## Layers
### CLI layer
`src/ai_project/cli.py` — entry point. Parses subcommands (`init`, `onboard`, `new-feature`, `verify`),
validates arguments, and delegates to the appropriate module.

### Core layer
`src/ai_project/` — modules for each operation:
- `scaffold.py` — file system operations: create directory trees, copy template files, populate
  variable placeholders in templates
- `verify.py` — structure integrity checks and doc-code drift detection

## Components
| Component | Layer | Responsibility | Module path |
|---|---|---|---|
| `main()` | CLI | Entry point, subcommand dispatch | `src/ai_project/cli.py` |
| `scaffold_init()` | Core | Greenfield scaffolding — full directory tree + all .md files | `src/ai_project/scaffold.py` |
| `scaffold_onboard()` | Core | Brownfield skeleton — convention files around existing code | `src/ai_project/scaffold.py` |
| `scaffold_new_feature()` | Core | Copy _template/ into numbered spec folder, update README | `src/ai_project/scaffold.py` |
| `verify_structure()` | Core | Check required files/dirs exist | `src/ai_project/verify.py` |
| `verify_docs()` | Core | Doc-code drift detection — known-callers register vs. imports | `src/ai_project/verify.py` |

## Integration points
- **Template source:** The `specs/_template/`, `agents/prompts/`, and root template files are
  stored in a `templates/` directory inside the package, shipped as package data.
- **No external services.** The CLI operates entirely on the local file system.

## Shared components and known callers
| Shared component | Callers | Behaviour callers can rely on |
|---|---|---|
| `scaffold._copy_template_dir()` | `scaffold_init()`, `scaffold_onboard()`, `scaffold_new_feature()` | Recursively copies a directory, replaces `{{PLACEHOLDER}}` variables from a provided dict |
| `verify._read_yaml_frontmatter()` | `verify_structure()`, `verify_docs()` | Returns a dict of frontmatter fields; returns empty dict for files with no frontmatter |

## Decisions
- **Stdlib only for CLI dependencies.** The tool must be copy-paste installable with no `pip install`
  step. `argparse` over `click` or `typer` — one less dependency, one less thing to break.
- **Templates shipped as package data.** Using `importlib.resources` (Python 3.9+) to locate
  template files regardless of install method.
- **Verify is read-only.** The `verify` command never modifies files — it reports drift and exits
  non-zero. This makes it safe for CI.

---
id: 001
status: draft
links_to_solution_design: 001
links_to_problem_statement: 001
---

# Test specification

## Acceptance criteria trace

| Success criterion (from problem statement) | Test case(s) |
|---|---|
| `init` creates complete project with all .md files populated | TC-1, TC-2 |
| `onboard` creates skeleton without modifying existing source files | TC-3, TC-4 |
| `new-feature` copies templates and updates README | TC-5, TC-6 |
| `verify` exits 0 on valid project; non-zero on drift | TC-7, TC-8 |
| Tool is installable by copying `src/ai_project/` onto PYTHONPATH | TC-9 |

## Unit tests

### `_copy_template_dir()`

| Test case | Test data / setup | Expected result |
|---|---|---|
| TC-UT-1 | Source dir with two files, one subdir; dest dir empty; no placeholders | Dest dir has identical structure and content |
| TC-UT-2 | Source file with `{{NAME}}` placeholder; vars dict has `NAME: "Test"` | Output file has "Test" where `{{NAME}}` was |

### `_render_template()`

| Test case | Test data / setup | Expected result |
|---|---|---|
| TC-UT-3 | Content: "Hello {{NAME}}"; vars: `{"NAME": "World"}` | Returns "Hello World" |
| TC-UT-4 | Content: "No placeholders here"; vars: `{}` | Returns unchanged content |
| TC-UT-5 | Content: "{{UNKNOWN}}"; vars: `{}` | Raises KeyError or returns "{{UNKNOWN}}" (design choice) |

### `_read_yaml_frontmatter()`

| Test case | Test data / setup | Expected result |
|---|---|---|
| TC-UT-6 | File with valid YAML frontmatter between `---` markers | Returns dict of frontmatter fields |
| TC-UT-7 | File with no frontmatter (no opening `---`) | Returns empty dict |
| TC-UT-8 | File with malformed YAML in frontmatter | Returns empty dict + logs warning |

## Integration tests

### `init_project()`

| Test case | Components exercised | Setup | Expected result |
|---|---|---|---|
| TC-1 | `init_project`, `_copy_template_dir`, `_render_template` | tmpdir, valid args | Full directory tree created; every .md file has content in every section |
| TC-2 | `init_project` | Non-empty tmpdir | Exits with error, directory unchanged |

### `onboard_project()`

| Test case | Components exercised | Setup | Expected result |
|---|---|---|---|
| TC-3 | `onboard_project` | tmpdir with a `.py` file, no convention files | Convention skeleton created; `.py` file untouched |
| TC-4 | `onboard_project` | Empty tmpdir | Exits with error "no source files detected" |

### `new_feature()`

| Test case | Components exercised | Setup | Expected result |
|---|---|---|---|
| TC-5 | `new_feature` | Valid convention project with empty specs/README.md | `specs/001-test-feature/` created; README updated with new row |
| TC-6 | `new_feature` | Same project, same feature name | Exits with error "feature already exists" |

### `verify()`

| Test case | Components exercised | Setup | Expected result |
|---|---|---|---|
| TC-7 | `verify_structure`, `verify_docs` | Valid convention project | Exit 0, no output (or "all checks passed") |
| TC-8 | `verify_structure` | Project missing `docs/architecture.md` | Exit 1, reports missing file |

### Installability

| Test case | Components exercised | Setup | Expected result |
|---|---|---|---|
| TC-9 | CLI entry point | `PYTHONPATH=src python -m ai_project.cli --help` | Shows usage with all four subcommands |

## Edge cases and boundary tests

| Test case | Edge condition | Expected result |
|---|---|---|
| TC-EDGE-1 | `init` with project name containing spaces | Creates directory with spaces in name; placeholder replacement handles it |
| TC-EDGE-2 | `init` with very long --context string (>1000 chars) | Works or fails gracefully with clear message |
| TC-EDGE-3 | `new-feature` when specs/README.md has no features yet (NNN=001) | Correctly assigns 001 |
| TC-EDGE-4 | `new-feature` when specs/README.md already has features up to 999 | Correctly assigns 1000 |
| TC-EDGE-5 | `onboard` in directory with AGENTS.md but no docs/ | Exits with error; does not overwrite AGENTS.md |
| TC-EDGE-6 | `verify` on directory with no specs/README.md | Reports missing file, not crash |

## Regression tests
N/A — this is the first feature. No existing behaviour to preserve.

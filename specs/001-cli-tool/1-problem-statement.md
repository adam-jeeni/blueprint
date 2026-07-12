---
id: 001
status: draft
date: 2026-07-10
author: Adam Davies
---

# Problem statement

## Statement

**Problem:** The convention-over-configuration methodology requires a developer to manually create
20+ files with specific content to set up a project. This is error-prone, slow, and creates variance
between projects. Without a tool, adoption requires reading a 15-page PDF and copying files by hand.

**Success criteria:**
1. `blueprint init my-project --name "Test" --stack "python-3.12" --context "test"` creates a
   complete project directory with every .md file containing headings + explanatory text (no blanks).
2. `blueprint onboard` run in a directory with existing `.py` files creates the convention skeleton
   without modifying any existing source files.
3. `blueprint new-feature add-export` creates `specs/001-add-export/` (or next number), copies all
   template files, and updates `specs/README.md`.
4. `blueprint verify` run on a valid project exits 0; run on a project with drift exits non-zero
   and prints the mismatches.
5. The tool is installable by copying `src/ai_project/` onto PYTHONPATH — no `pip install` required.

**Non-functional Requirements:** No web UI. No file watching or daemon mode. No database. No external API integrations.
No automatic code generation — the tool scaffolds documents, not implementation. The `verify` command
checks known-callers register against actual imports only for Python projects (language detection
is deferred to a future feature).

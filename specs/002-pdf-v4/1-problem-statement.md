---
id: 002
status: draft
date: 2026-07-10
author: Adam Davies
---

# Problem statement

## Statement

**Problem:** The existing methodology PDF (`specifying-software-for-ai-development-extended-v3.pdf`)
describes a process that no longer matches the product. The methodology has evolved from a
document-centric process into a CLI-driven convention-over-configuration system with 10 agent roles,
a token-efficiency design, and a human-facing Architecture Advisor. The PDF is v3; the methodology
is effectively v4. Anyone reading the PDF to understand the methodology will learn a version that
no longer exists.

**Who has it / context:** Two audiences:
1. A skeptical senior architect or engineering lead evaluating whether to adopt the methodology.
   They need the persuasive case: what problem it solves, how it works, what it costs, where it fails.
2. A developer about to use `blueprint init` for the first time. They need the orientation:
   what the folder structure means, what agents exist, what the lifecycle looks like.

**Why now:** Every other artifact has been updated — templates stripped, METHODOLOGY.md rewritten,
Architecture Advisor prompt created, `blueprint` CLI built and verified. The PDF is the last
artifact from v3. Leaving it stale undermines the methodology's credibility: if the methodology's
own documentation is out of date, why would anyone trust it for their project?

**UI outline:** A PDF document, 12-16 pages. Infographic-heavy — diagrams for the lifecycle, agent
hierarchy, folder structure, and three entry-point scenarios. Prose sections for the persuasive
argument, the worked example, and the honest assessment of where the methodology still fails.
Designed to be read in 20 minutes, then kept as a reference.

**Data outline:** No data changes. The PDF is a standalone document, not part of the convention
structure (it sits alongside it, like the v3 PDF currently does in the workspace root).

**Success criteria:**
1. A reader who has never seen the methodology can explain what it does, why it exists, and how to
   start using it — after reading the document.
2. The document accurately describes: the `blueprint` CLI, the Architecture Advisor role, the 10-agent
   hierarchy, the token-efficiency design decisions, the two-document split (METHODOLOGY.md for AI,
   PDF for humans), and the three entry-point scenarios.
3. The document includes the Country Collection worked example, updated to reflect the `blueprint`
   workflow rather than the old manual process.
4. The document includes an honest "where it still fails" section — not marketing copy.
5. The document replaces `specifying-software-for-ai-development-extended-v3.pdf` in the workspace.

**Non-goals:** No update to the templates, prompts, CLI, or METHODOLOGY.md. No new features in the
methodology itself. No translation to other formats (web, slides) — PDF only. The content does not
replace METHODOLOGY.md — it complements it for a different audience.

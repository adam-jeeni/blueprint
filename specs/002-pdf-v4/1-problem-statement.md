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

**Non-functional Requirements:** No update to the templates, prompts, CLI, or METHODOLOGY.md. No new features in the
methodology itself. No translation to other formats (web, slides) — PDF only. The content does not
replace METHODOLOGY.md — it complements it for a different audience.

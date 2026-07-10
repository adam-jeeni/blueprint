"""verify.py — structure integrity and doc-code drift checks for blueprint."""

import os
import re
from pathlib import Path


def _read_yaml_frontmatter(filepath: Path) -> dict[str, str]:
    """Read YAML frontmatter from a Markdown file.

    Args:
        filepath: Path to the .md file.

    Returns:
        Dict of frontmatter fields, or empty dict if no frontmatter found.
    """
    try:
        content = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {}

    # Frontmatter must start with --- on the first line
    if not content.startswith("---"):
        return {}

    # Find the closing ---
    end_idx = content.find("---", 3)
    if end_idx == -1:
        return {}

    frontmatter_text = content[3:end_idx].strip()
    if not frontmatter_text:
        return {}

    # Simple YAML parser for flat key: value pairs
    result: dict[str, str] = {}
    for line in frontmatter_text.splitlines():
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def verify_structure(*, verbose: bool = False) -> list[str]:
    """Check that the convention directory structure is intact.

    Args:
        verbose: If True, print progress to stderr.

    Returns:
        List of drift messages. Empty list means all checks passed.
    """
    cwd = Path.cwd()
    issues: list[str] = []

    required_files = [
        "AGENTS.md",
        "METHODOLOGY.md",
        "agents/README.md",
        "docs/architecture.md",
        "docs/data-dictionary.md",
        "docs/user-guide.md",
        "docs/project-overview.md",
        "docs/production-feedback.md",
        "specs/README.md",
        "specs/_template/SKIP-RUBRIC.md",
        "specs/_template/1-problem-statement.md",
        "specs/_template/2-solution-design.md",
        "specs/_template/3-backlog.md",
        "specs/_template/4-test-spec.md",
    ]

    for rel_path in required_files:
        full_path = cwd / rel_path
        if not full_path.exists():
            issues.append(f"missing: {rel_path}")

    # Check agent prompt files exist
    prompt_dir = cwd / "agents" / "prompts"
    required_prompts = [
        "greenfield-setup.md",
        "brownfield-onboarding.md",
        "orchestrator.md",
        "architecture-advisor.md",
        "schema-agent.md",
        "backend-agent.md",
        "frontend-agent.md",
        "spec-agent.md",
        "review-agent.md",
        "refactor-agent.md",
    ]
    if prompt_dir.is_dir():
        for prompt_name in required_prompts:
            if not (prompt_dir / prompt_name).exists():
                issues.append(f"missing: agents/prompts/{prompt_name}")
    else:
        issues.append("missing: agents/prompts/")

    if verbose and not issues:
        print("Structure check: all required files present.", file=os.sys.stderr)

    return issues


def verify_docs(*, verbose: bool = False) -> list[str]:
    """Check standing docs against the actual codebase for drift.

    Currently checks:
    - Known-callers register in docs/architecture.md has the expected sections.
    - Architecture docs have the expected section headings.

    Full import-graph analysis for the known-callers register is deferred
    to a future feature (language-specific static analysis).

    Args:
        verbose: If True, print progress to stderr.

    Returns:
        List of drift messages. Empty list means all checks passed.
    """
    cwd = Path.cwd()
    issues: list[str] = []

    # Check architecture.md has key sections
    arch_path = cwd / "docs" / "architecture.md"
    if arch_path.exists():
        arch_content = arch_path.read_text(encoding="utf-8")
        required_sections = [
            "## System overview",
            "## Components",
            "## Shared components and known callers",
            "## Decisions",
        ]
        for section in required_sections:
            if section not in arch_content:
                issues.append(
                    f"drift: docs/architecture.md — missing section '{section}'"
                )

        # Check known-callers register has at least a table header
        if "| Shared component | Callers" not in arch_content:
            issues.append(
                "drift: docs/architecture.md — known-callers register table missing or malformed"
            )

    # Check data-dictionary.md has key sections
    dd_path = cwd / "docs" / "data-dictionary.md"
    if dd_path.exists():
        dd_content = dd_path.read_text(encoding="utf-8")
        if "## Entities" not in dd_content and "## " not in dd_content:
            issues.append(
                "drift: docs/data-dictionary.md — no entity sections found"
            )

    # Check user-guide.md has flows
    ug_path = cwd / "docs" / "user-guide.md"
    if ug_path.exists():
        ug_content = ug_path.read_text(encoding="utf-8")
        if "## Current flows" not in ug_content:
            issues.append(
                "drift: docs/user-guide.md — missing 'Current flows' section"
            )

    # Check production-feedback.md has incidents table
    pf_path = cwd / "docs" / "production-feedback.md"
    if pf_path.exists():
        pf_content = pf_path.read_text(encoding="utf-8")
        if "## Incidents" not in pf_content:
            issues.append(
                "drift: docs/production-feedback.md — missing 'Incidents' section"
            )

    if verbose and not issues:
        print("Doc verification: no drift detected.", file=os.sys.stderr)

    return issues


def run_verify(*, verbose: bool = False) -> int:
    """Run all verification checks and return exit code.

    Args:
        verbose: If True, print progress to stderr.

    Returns:
        0 if all checks pass, 1 if drift found, 2 if structure is invalid.
    """
    structure_issues = verify_structure(verbose=verbose)
    doc_issues = verify_docs(verbose=verbose)

    all_issues = structure_issues + doc_issues

    if not all_issues:
        print("All checks passed.")
        return 0

    for issue in all_issues:
        print(issue)

    # Exit 2 if any structure issues (missing required files)
    if structure_issues:
        return 2

    return 1

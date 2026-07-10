"""scaffold.py — file system operations for blueprint.

Creates directory trees, copies template files, and renders placeholder variables.
"""

import os
import shutil
from pathlib import Path


def _render_template(content: str, vars: dict[str, str]) -> str:
    """Replace {{PLACEHOLDER}} variables in content with values from vars dict.

    Unknown placeholders are left unchanged.
    """
    result = content
    for key, value in vars.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result


def _copy_template_dir(
    src: Path,
    dst: Path,
    vars: dict[str, str] | None = None,
    *,
    verbose: bool = False,
) -> None:
    """Recursively copy a template directory, rendering placeholders in files.

    Args:
        src: Source template directory.
        dst: Destination directory.
        vars: Optional dict of placeholder replacements.
        verbose: If True, print each created file to stderr.
    """
    if vars is None:
        vars = {}

    dst.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        dst_item = dst / item.name
        if item.is_dir():
            _copy_template_dir(item, dst_item, vars, verbose=verbose)
        else:
            content = item.read_text(encoding="utf-8")
            if vars:
                content = _render_template(content, vars)
            dst_item.write_text(content, encoding="utf-8")
            if verbose:
                print(f"created {dst_item}", file=os.sys.stderr)


def _get_templates_dir() -> Path:
    """Return the path to the templates directory shipped with the package.

    Checks multiple locations: package data, development layout, and
    the project root (when running from source).
    """
    # Check relative to this file (development layout)
    package_dir = Path(__file__).resolve().parent
    templates_src = package_dir / "templates"
    if templates_src.is_dir():
        return templates_src

    # Check relative to cwd (running from project root)
    cwd_templates = Path.cwd() / "src" / "ai_project" / "templates"
    if cwd_templates.is_dir():
        return cwd_templates

    raise FileNotFoundError(
        "Template directory not found. Reinstall blueprint or run from the project root."
    )


def init_project(
    project_dir: str | Path,
    name: str,
    stack: str,
    context: str,
    *,
    verbose: bool = False,
) -> None:
    """Scaffold a new greenfield project with the full convention structure.

    Args:
        project_dir: Path to create the new project at.
        name: Human-readable project name.
        stack: Tech stack description (e.g. "python-3.12,fastapi").
        context: One-paragraph business context.
        verbose: If True, print progress to stderr.

    Raises:
        FileExistsError: If project_dir exists and is non-empty.
        FileNotFoundError: If the templates directory cannot be found.
    """
    project_path = Path(project_dir).resolve()

    if project_path.exists() and any(project_path.iterdir()):
        raise FileExistsError(
            f"Error: {project_path} already exists and is not empty."
        )

    templates_dir = _get_templates_dir()
    vars = {"NAME": name, "STACK": stack, "CONTEXT": context}

    if verbose:
        print(f"Scaffolding {name} at {project_path}...", file=os.sys.stderr)

    _copy_template_dir(templates_dir, project_path, vars, verbose=verbose)

    if verbose:
        print(f"Done. Open {project_path} with any AI agent.", file=os.sys.stderr)


def onboard_project(*, verbose: bool = False) -> None:
    """Scaffold the convention skeleton around an existing codebase.

    Creates AGENTS.md, METHODOLOGY.md, agents/, docs/, specs/_template/, and
    specs/README.md without modifying any existing source files.

    Args:
        verbose: If True, print progress to stderr.

    Raises:
        FileExistsError: If AGENTS.md already exists.
        RuntimeError: If no source files are detected in the current directory.
    """
    cwd = Path.cwd()

    # Check for existing AGENTS.md
    if (cwd / "AGENTS.md").exists():
        raise FileExistsError(
            "Error: AGENTS.md already exists. Project may already be onboarded."
        )

    # Check for source files
    source_extensions = {".py", ".js", ".ts", ".go", ".rs", ".java", ".rb"}
    has_source = False
    for ext in source_extensions:
        if list(cwd.rglob(f"*{ext}")):
            has_source = True
            break

    if not has_source:
        raise RuntimeError(
            "Error: no source files detected. Use 'init' for new projects."
        )

    templates_dir = _get_templates_dir()

    if verbose:
        print("Onboarding existing project...", file=os.sys.stderr)

    # Copy only convention files — never touch src/, tests/, or existing files.
    # The templates directory contains the full structure including src/ and tests/,
    # so we selectively copy specific paths.
    convention_items = [
        "AGENTS.md",
        "METHODOLOGY.md",
        "agents",
        "docs",
        "specs",
        "pyproject.toml",
    ]

    for item_name in convention_items:
        src_item = templates_dir / item_name
        dst_item = cwd / item_name

        if not src_item.exists():
            continue

        if dst_item.exists():
            if verbose:
                print(f"skipping existing {item_name}", file=os.sys.stderr)
            continue

        if src_item.is_dir():
            _copy_template_dir(src_item, dst_item, verbose=verbose)
        else:
            shutil.copy2(src_item, dst_item)
            if verbose:
                print(f"created {dst_item}", file=os.sys.stderr)

    if verbose:
        print(
            "Done. Open this directory with any AI agent — AGENTS.md will detect scenario 2.",
            file=os.sys.stderr,
        )


def new_feature(feature_name: str, *, verbose: bool = False) -> None:
    """Copy _template/ into a numbered spec folder and update the feature index.

    Args:
        feature_name: Slug for the feature folder (alphanumeric + hyphens).
        verbose: If True, print progress to stderr.

    Raises:
        FileNotFoundError: If specs/_template/ doesn't exist.
        FileExistsError: If a feature with this name already exists.
    """
    cwd = Path.cwd()
    template_dir = cwd / "specs" / "_template"
    specs_readme = cwd / "specs" / "README.md"

    if not template_dir.is_dir():
        raise FileNotFoundError(
            "Error: specs/_template/ not found. Is this a convention project?"
        )

    # Validate feature name
    if not feature_name.replace("-", "").isalnum() or not feature_name:
        raise ValueError(
            "Error: feature name must be alphanumeric with hyphens only."
        )

    # Read specs/README.md to find the next feature number
    if not specs_readme.exists():
        raise FileNotFoundError(
            "Error: specs/README.md not found. Is this a convention project?"
        )

    content = specs_readme.read_text(encoding="utf-8")
    lines = content.splitlines()

    # Find existing feature IDs to determine next number
    max_id = 0
    for line in lines:
        # Match table rows: | 001 | name | status | ...
        if line.startswith("|") and "|" in line[1:]:
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if parts and parts[0].isdigit():
                max_id = max(max_id, int(parts[0]))

    next_id = max_id + 1
    feature_folder = cwd / "specs" / f"{next_id:03d}-{feature_name}"

    if feature_folder.exists():
        raise FileExistsError(
            f"Error: feature '{feature_name}' already exists as {next_id:03d}"
        )

    # Copy template files
    _copy_template_dir(template_dir, feature_folder, verbose=verbose)

    # Update specs/README.md
    new_row = f"| {next_id:03d} | {feature_name} | draft | [1-problem-statement.md](./{next_id:03d}-{feature_name}/1-problem-statement.md) | [2-solution-design.md](./{next_id:03d}-{feature_name}/2-solution-design.md) |"
    specs_readme.write_text(content.rstrip() + "\n" + new_row + "\n", encoding="utf-8")

    if verbose:
        print(
            f"Created {feature_folder}. Edit the numbered files in order.",
            file=os.sys.stderr,
        )

"""cli.py — entry point for the blueprint CLI tool."""

import argparse
import sys

from ai_project.scaffold import init_project, onboard_project, new_feature
from ai_project.verify import run_verify


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="blueprint",
        description="CLI tool for the convention-over-configuration methodology.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # init
    init_parser = subparsers.add_parser(
        "init", help="Scaffold a new greenfield project"
    )
    init_parser.add_argument(
        "project_dir", help="Path to create the new project at"
    )
    init_parser.add_argument(
        "--name", required=True, help="Human-readable project name"
    )
    init_parser.add_argument(
        "--stack",
        required=True,
        help='Tech stack description, e.g. "python-3.12,fastapi"',
    )
    init_parser.add_argument(
        "--context", required=True, help="One-paragraph business context"
    )
    init_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print progress messages"
    )

    # onboard
    onboard_parser = subparsers.add_parser(
        "onboard", help="Scaffold convention skeleton around existing code"
    )
    onboard_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print progress messages"
    )

    # new-feature
    new_feature_parser = subparsers.add_parser(
        "new-feature", help="Create a new numbered feature folder from template"
    )
    new_feature_parser.add_argument(
        "feature_name", help="Slug for the feature folder (alphanumeric + hyphens)"
    )
    new_feature_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print progress messages"
    )

    # verify
    verify_parser = subparsers.add_parser(
        "verify", help="Check structure integrity and doc-code drift"
    )
    verify_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print progress messages"
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    try:
        if args.command == "init":
            init_project(
                args.project_dir,
                args.name,
                args.stack,
                args.context,
                verbose=args.verbose,
            )
        elif args.command == "onboard":
            onboard_project(verbose=args.verbose)
        elif args.command == "new-feature":
            new_feature(args.feature_name, verbose=args.verbose)
        elif args.command == "verify":
            exit_code = run_verify(verbose=args.verbose)
            sys.exit(exit_code)
    except (FileExistsError, FileNotFoundError, RuntimeError, ValueError) as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()

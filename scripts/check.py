#!/usr/bin/env python3

"""Run all project quality checks."""

import subprocess
import sys

COMMANDS: list[list[str]] = [
    ["ruff", "check", "."],
    ["mypy", "astralis"],
    ["pytest", "-v"],
]


def main() -> None:
    """Run all quality checks."""

    for command in COMMANDS:
        print(
            f"\n▶ Running: {' '.join(command)}",
        )

        result = subprocess.run(
            command,
            check=False,
        )

        if result.returncode != 0:
            print(
                "\n❌ Quality checks failed.",
            )
            sys.exit(
                result.returncode,
            )

    print(
        "\n✅ All quality checks passed!",
    )


if __name__ == "__main__":
    main()

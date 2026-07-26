#!/usr/bin/env python3

import subprocess
import sys

"""Run all project quality checks."""

COMMANDS = [
    ["ruff", "check", "."],
    ["mypy", "astralis"],
    ["pytest", "-v"],
]

for command in COMMANDS:
    print(f"\n▶ Running: {' '.join(command)}")

    result = subprocess.run(
        command,
        check=False,
    )

    if result.returncode != 0:
        print("\n❌ Quality checks failed.")
        sys.exit(result.returncode)

print("\n✅ All quality checks passed!")
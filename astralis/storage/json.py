import json
from pathlib import Path
from typing import Any

from astralis.storage.base import Storage


class JsonStorage(Storage):
    """Stores data in JSON files."""

    def __init__(
        self,
        file_path: Path,
    ) -> None:
        self.file_path = file_path

        self.file_path.parent.mkdir(
            exist_ok=True,
        )

        if not self.file_path.exists():
            self.file_path.write_text(
                "[]",
                encoding="utf-8",
            )

    def load(
        self,
    ) -> Any:
        """Load data."""

        with open(
            self.file_path,
            encoding="utf-8",
        ) as file:
            return json.load(
                file,
            )

    def save(
        self,
        data: Any,
    ) -> None:
        """Save data."""

        with open(
            self.file_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
            )

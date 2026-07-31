import json
from pathlib import Path
from typing import TypeVar

from astralis.storage.base import Storage

T = TypeVar("T")


class JsonStorage(Storage[T]):
    """Stores data in JSON files."""

    def __init__(
        self,
        file_path: Path,
    ) -> None:
        self.file_path = file_path

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.file_path.exists():
            self.file_path.write_text(
                "[]",
                encoding="utf-8",
            )

    def load(
        self,
    ) -> T:
        """Load data."""

        with self.file_path.open(
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def save(
        self,
        data: T,
    ) -> None:
        """Save data."""

        with self.file_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
            )

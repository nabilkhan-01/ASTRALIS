from typing import Any

from astralis.storage.base import Storage


class PostgresStorage(Storage):
    """Stores data in PostgreSQL."""

    def load(
        self,
    ) -> Any:
        raise NotImplementedError()

    def save(
        self,
        data: Any,
    ) -> None:
        raise NotImplementedError()

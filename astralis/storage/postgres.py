from typing import Generic, TypeVar

from astralis.storage.base import Storage

T = TypeVar("T")


class PostgresStorage(
    Storage[T],
    Generic[T],
):
    """Stores data in PostgreSQL."""

    def __init__(
        self,
        connection_string: str,
    ) -> None:
        self.connection_string = connection_string

    def load(
        self,
    ) -> T:
        """Load data."""

        raise NotImplementedError(
            "PostgresStorage is not implemented yet.",
        )

    def save(
        self,
        data: T,
    ) -> None:
        """Save data."""

        raise NotImplementedError(
            "PostgresStorage is not implemented yet.",
        )

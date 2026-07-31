from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Storage(
    ABC,
    Generic[T],
):
    """Defines a storage backend."""

    @abstractmethod
    def load(
        self,
    ) -> T:
        """Load data."""

    @abstractmethod
    def save(
        self,
        data: T,
    ) -> None:
        """Save data."""

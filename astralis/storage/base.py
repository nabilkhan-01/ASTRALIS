from abc import ABC, abstractmethod
from typing import Any


class Storage(ABC):
    """Defines a storage backend."""

    @abstractmethod
    def load(
        self,
    ) -> Any:
        """Load data."""

    @abstractmethod
    def save(
        self,
        data: Any,
    ) -> None:
        """Save data."""

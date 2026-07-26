from abc import ABC
from dataclasses import asdict
from typing import Any, ClassVar, Generic, TypeVar, cast

from astralis.storage import Storage

T = TypeVar("T")


class BaseMemory(
    ABC,
    Generic[T],
):
    """Base class for memory components."""

    MODEL: ClassVar[type[T]]

    def __init__(
        self,
        storage: Storage,
    ) -> None:
        self.storage = storage

    def _load_models(
        self,
    ) -> list[T]:
        """Load models from storage."""

        data = self.storage.load()

        return [self.MODEL(**item) for item in data]

    def _save_models(
        self,
        models: list[T],
    ) -> None:
        """Save models to storage."""

        self.storage.save(
            [
                asdict(
                    cast(Any, model),
                )
                for model in models
            ],
        )

    def clear(
        self,
    ) -> None:
        """Remove all stored models."""

        self.storage.save([])

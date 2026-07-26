from typing import Any


class ModuleRegistry:
    """
    Keeps track of all registered ASTRALIS modules.

    The registry provides a centralized place to register,
    retrieve, list, and remove application modules.
    """

    def __init__(self) -> None:
        self._modules: dict[str, Any] = {}

    def register(self, name: str, module: Any) -> None:
        """
        Register a module with the registry.

        Raises:
            ValueError: If a module with the same name is already registered.
        """
        if name in self._modules:
            raise ValueError(f"Module '{name}' is already registered.")

        self._modules[name] = module

    def get(self, name: str) -> Any | None:
        """
        Return a registered module.

        Returns:
            The registered module if found, otherwise None.
        """
        return self._modules.get(name)

    def unregister(self, name: str) -> None:
        """
        Remove a registered module.

        If the module does not exist, no action is taken.
        """
        self._modules.pop(name, None)

    def list_modules(self) -> list[str]:
        """
        Return the names of all registered modules.
        """
        return list(self._modules.keys())

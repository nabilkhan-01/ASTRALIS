class ModuleRegistry:
    """Keeps track of all registered ASTRALIS modules."""

    def __init__(
        self,
    ) -> None:
        self._modules: dict[str, object] = {}

    def register(
        self,
        name: str,
        module: object,
    ) -> None:
        """Register a module."""

        if name in self._modules:
            raise ValueError(
                f"Module '{name}' is already registered.",
            )

        self._modules[name] = module

    def get(
        self,
        name: str,
    ) -> object | None:
        """Return a registered module."""

        return self._modules.get(
            name,
        )

    def unregister(
        self,
        name: str,
    ) -> None:
        """Remove a registered module."""

        self._modules.pop(
            name,
            None,
        )

    def list_modules(
        self,
    ) -> list[str]:
        """Return all registered module names."""

        return sorted(
            self._modules,
        )

from dataclasses import FrozenInstanceError

import pytest

from astralis.core.project_identity import (
    CANONICAL_PROJECT_IDENTITY,
    ProjectIdentity,
)


class TestProjectIdentity:
    """Tests for the canonical ASTRALIS ProjectIdentity."""

    def test_canonical_identity_values(
        self,
    ) -> None:
        """Verify the canonical official ASTRALIS project identity values."""
        assert CANONICAL_PROJECT_IDENTITY.name == "ASTRALIS"
        assert CANONICAL_PROJECT_IDENTITY.founder == "Nabil Ahmad Khan"
        assert CANONICAL_PROJECT_IDENTITY.creator == "Nabil Ahmad Khan"

    def test_identity_is_immutable(
        self,
    ) -> None:
        """Verify that ProjectIdentity instances are frozen and reject mutation."""
        identity = ProjectIdentity()

        with pytest.raises(FrozenInstanceError):
            identity.name = "DifferentName"  # type: ignore[misc]

        with pytest.raises(FrozenInstanceError):
            identity.founder = "DifferentFounder"  # type: ignore[misc]

    def test_no_mutation_methods_exist(
        self,
    ) -> None:
        """Verify that ProjectIdentity exposes no setter, update, or delete methods."""
        forbidden_methods = [
            "set_name",
            "set_founder",
            "set_creator",
            "update",
            "delete",
            "mutate",
        ]
        for method_name in forbidden_methods:
            assert not hasattr(CANONICAL_PROJECT_IDENTITY, method_name)

    def test_environment_variables_do_not_override_canonical_identity(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Canonical project identity is fixed and unaffected by environment variables."""
        monkeypatch.setenv("ASTRALIS_FOUNDER", "Someone Else")
        monkeypatch.setenv("ASTRALIS_CREATOR", "Someone Else")
        monkeypatch.setenv("USER", "DifferentUser")
        monkeypatch.setenv("USERNAME", "DifferentUser")

        # The canonical singleton remains immutable and unaffected
        assert CANONICAL_PROJECT_IDENTITY.founder == "Nabil Ahmad Khan"
        assert CANONICAL_PROJECT_IDENTITY.creator == "Nabil Ahmad Khan"
        assert CANONICAL_PROJECT_IDENTITY.name == "ASTRALIS"

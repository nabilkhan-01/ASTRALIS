from astralis.api.email import EmailApi
from astralis.capability.email import EmailCapability
from tests.helpers.conversation_factory import (
    create_conversation,
)
from tests.helpers.interpretation_factory import (
    create_interpretation,
)
from tests.helpers.request_factory import (
    create_request,
)


class TestEmailCapability:
    """Tests for EmailCapability."""

    @staticmethod
    def _create_capability() -> EmailCapability:
        """Create an email capability."""

        return EmailCapability(
            EmailApi(),
        )

    def test_help(
        self,
    ) -> None:
        """Display available email commands."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "email",
            ),
            create_conversation(),
            create_interpretation(
                entities=["email"],
            ),
        )

        assert response.success is True
        assert "Available commands" in response.text

    def test_create_draft(
        self,
    ) -> None:
        """Create an email draft."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "draft email john@example.com Meeting",
            ),
            create_conversation(),
            create_interpretation(
                entities=["email"],
            ),
        )

        assert response.success is True
        assert (
            response.text
            == "Email draft created for 'Meeting' to john@example.com."
        )

    def test_send_not_supported(
        self,
    ) -> None:
        """Sending emails is not yet supported."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "send email john@example.com Meeting",
            ),
            create_conversation(),
            create_interpretation(
                entities=["email"],
            ),
        )

        assert response.success is False
        assert response.text == "Sending emails is not yet supported."

    def test_unknown_command(
        self,
    ) -> None:
        """Reject an unknown email command."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "email everything",
            ),
            create_conversation(),
            create_interpretation(
                entities=["email"],
            ),
        )

        assert response.success is False
        assert response.text == "Unknown email command."

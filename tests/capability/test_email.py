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

    def setup_method(
        self,
    ) -> None:
        self.capability = EmailCapability()

    def test_help(
        self,
    ) -> None:
        response = self.capability.execute(
            create_request("email"),
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
        response = self.capability.execute(
            create_request(
                "draft email john@example.com Meeting",
            ),
            create_conversation(),
            create_interpretation(
                entities=["email"],
            ),
        )

        assert response.success is True
        assert response.text == "Draft created for john@example.com."

    def test_send_not_supported(
        self,
    ) -> None:
        response = self.capability.execute(
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
        response = self.capability.execute(
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

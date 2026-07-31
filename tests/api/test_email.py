import pytest

from astralis.api.email import EmailApi


class TestEmailApi:
    """Tests for EmailApi."""

    def test_create_draft(
        self,
    ) -> None:
        """Create an email draft."""

        api = EmailApi()

        result = api.create_draft(
            recipient="john@example.com",
            subject="Hello",
            body="Hi!",
        )

        assert (
            result
            == "Email draft created for 'Hello' to john@example.com."
        )

    def test_send_not_supported(
        self,
    ) -> None:
        """Sending emails is not yet implemented."""

        api = EmailApi()

        with pytest.raises(
            NotImplementedError,
        ):
            api.send_email(
                recipient="john@example.com",
                subject="Hello",
                body="Hi!",
            )
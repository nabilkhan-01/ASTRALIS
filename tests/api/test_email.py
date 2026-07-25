from astralis.api.email import EmailApi

import pytest


class TestEmailApi:
    """Tests for EmailApi."""

    def setup_method(
        self,
    ) -> None:
        self.api = EmailApi()

    def test_create_draft(
        self,
    ) -> None:
        result = self.api.create_draft(
            recipient="john@example.com",
            subject="Hello",
            body="Hi!",
        )

        assert result == "Draft created for john@example.com."

    def test_send_not_supported(
        self,
    ) -> None:
        with pytest.raises(
            NotImplementedError,
        ):
            self.api.send_email(
                recipient="john@example.com",
                subject="Hello",
                body="Hi!",
            )
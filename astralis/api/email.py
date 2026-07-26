class EmailApi:
    """Provides email functionality."""

    def create_draft(
        self,
        recipient: str,
        subject: str,
        body: str,
    ) -> str:
        """Create an email draft."""

        return f"Draft created for {recipient}."

    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
    ) -> str:
        """Send an email."""

        raise NotImplementedError(
            "Sending emails is not yet supported.",
        )

from astralis.brain.message import Message
from astralis.brain.role import Role


class Conversation:
    """Represents an active conversation."""

    def __init__(self) -> None:
        self._messages: list[Message] = []

    def add(
        self,
        role: Role,
        content: str,
    ) -> None:
        """Add a message to the conversation."""

        self._messages.append(
            Message(
                role=role,
                content=content,
            )
        )

    @property
    def messages(
        self,
    ) -> list[Message]:
        """Return the conversation history."""

        return self._messages
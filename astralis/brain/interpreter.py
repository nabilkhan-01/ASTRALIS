from typing import ClassVar

from astralis.brain.intent import Intent
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request


class Interpreter:
    """Interprets incoming user requests."""

    GREETINGS: ClassVar[set[str]] = {
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
    }

    QUESTION_PREFIXES: ClassVar[tuple[str, ...]] = (
        "what",
        "why",
        "how",
        "when",
        "where",
        "who",
        "which",
        "can",
        "could",
        "would",
        "is",
        "are",
        "do",
        "does",
    )

    MEMORY_PREFIXES: ClassVar[tuple[str, ...]] = (
        "remember",
        "don't forget",
        "my name is",
        "i am",
    )

    EXPLICIT_COMMANDS: ClassVar[dict[str, tuple[str, ...]]] = {
        "search": (
            "search",
            "find",
            "lookup",
        ),
        "notes": (
            "note ",
            "notes",
            "delete note",
        ),
        "browser": ("open",),
    }

    ENTITY_KEYWORDS: ClassVar[dict[str, tuple[str, ...]]] = {
        "time": (
            "time",
            "clock",
        ),
        "date": (
            "date",
            "day",
            "today",
        ),
        "calculator": ("calculate",),
        "weather": (
            "weather",
            "forecast",
            "temperature",
        ),
        "file_system": (
            "pwd",
            "list files",
            "list folders",
            "read",
        ),
        "calendar": (
            "calendar",
            "event",
            "today",
            "add event",
            "delete event",
        ),
        "alarm": (
            "alarm",
            "alarms",
            "enable alarm",
            "disable alarm",
            "delete alarm",
        ),
        "email": (
            "email",
            "draft email",
            "send email",
        ),
    }

    def interpret(
        self,
        request: Request,
    ) -> Interpretation:
        """Interpret an incoming request."""

        text = self._normalize(
            request.text,
        )

        intent = self._detect_intent(
            text,
        )

        explicit_entity = self._detect_explicit_command(
            text,
        )

        if explicit_entity is not None:
            return Interpretation(
                intent=intent,
                entities=[
                    explicit_entity,
                ],
            )

        return Interpretation(
            intent=intent,
            entities=self._extract_entities(
                text,
            ),
        )

    def _normalize(
        self,
        text: str,
    ) -> str:
        """Normalize user input."""

        return text.strip().lower()

    def _detect_intent(
        self,
        text: str,
    ) -> Intent:
        """Determine the user's intent."""

        if text in self.GREETINGS:
            return Intent.GREETING

        if text.startswith(
            self.MEMORY_PREFIXES,
        ):
            return Intent.MEMORY

        if text.endswith("?") or text.startswith(
            self.QUESTION_PREFIXES,
        ):
            return Intent.QUESTION

        return Intent.CONVERSATION

    def _detect_explicit_command(
        self,
        text: str,
    ) -> str | None:
        """Detect commands that map directly to a capability."""

        for entity, commands in self.EXPLICIT_COMMANDS.items():
            if entity == "notes":
                if text == "notes" or text.startswith(commands):
                    return entity

            elif text.startswith(commands):
                return entity

        return None

    def _extract_entities(
        self,
        text: str,
    ) -> list[str]:
        """Extract entities from user input."""

        entities: list[str] = []

        for entity, keywords in self.ENTITY_KEYWORDS.items():
            if entity == "file_system":
                matched = any(text.startswith(keyword) for keyword in keywords)
            else:
                matched = any(keyword in text for keyword in keywords)

            if matched:
                entities.append(
                    entity,
                )

        if self._detect_intent(text) is Intent.MEMORY:
            entities.append(
                "memory",
            )

        return entities

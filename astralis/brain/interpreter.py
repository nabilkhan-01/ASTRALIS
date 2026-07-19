from astralis.brain.intent import Intent
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request


class Interpreter:
    """Interprets incoming user requests."""

    GREETINGS = {
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
    }

    QUESTION_PREFIXES = (
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

    MEMORY_PREFIXES = (
        "remember",
        "don't forget",
        "my name is",
        "i am",
    )

    TOOL_KEYWORDS = (
        "weather",
        "calculate",
        "search",
        "open",
    )

    def interpret(
        self,
        request: Request,
    ) -> Interpretation:
        """Interpret an incoming request."""

        text = request.text.strip().lower()

        if text in self.GREETINGS:
            return Interpretation(
                intent=Intent.GREETING,
            )

        if (
            text.endswith("?")
            or text.startswith(self.QUESTION_PREFIXES)
        ):
            return Interpretation(
                intent=Intent.QUESTION,
            )

        if text.startswith(self.MEMORY_PREFIXES):
            return Interpretation(
                intent=Intent.MEMORY,
            )

        if any(
            keyword in text
            for keyword in self.TOOL_KEYWORDS
        ):
            return Interpretation(
                intent=Intent.TOOL,
            )

        return Interpretation(
            intent=Intent.CONVERSATION,
        )
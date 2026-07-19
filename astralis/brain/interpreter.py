from astralis.brain.intent import Intent
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request


class Interpreter:
    """Interprets incoming user requests."""

    def interpret(
        self,
        request: Request,
    ) -> Interpretation:
        """Interpret a request."""

        text = request.text.strip().lower()

        greetings = {
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
        }

        if text in greetings:
            return Interpretation(
                intent=Intent.GREETING,
            )

        if text.endswith("?"):
            return Interpretation(
                intent=Intent.QUESTION,
            )

        return Interpretation(
            intent=Intent.GENERAL,
        )
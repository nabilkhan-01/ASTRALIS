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

    TIME_KEYWORDS = (
        "time",
        "clock",
    )

    DATE_KEYWORDS = (
        "date",
        "day",
        "today",
    )

    CALCULATION_KEYWORDS = (
        "calculate",
    )

    WEATHER_KEYWORDS = (
        "weather",
        "forecast",
        "temperature",
    )

    SEARCH_COMMANDS = (
        "search",
        "find",
        "lookup",
    )

    NOTES_COMMANDS = (
        "note ",
        "notes",
        "delete note",
    )

    BROWSER_COMMANDS = (
        "open",
    )

    FILE_SYSTEM_COMMANDS = (
        "pwd",
        "list files",
        "list folders",
        "read",
    )

    def interpret(
        self,
        request: Request,
    ) -> Interpretation:
        """Interpret an incoming request."""

        text = request.text.strip().lower()

        intent = Intent.CONVERSATION
        entities: list[str] = []

        # Greeting
        if text in self.GREETINGS:
            intent = Intent.GREETING

        # Memory
        elif text.startswith(self.MEMORY_PREFIXES):
            intent = Intent.MEMORY
            entities.append("memory")

        # Explicit search command
        elif text.startswith(self.SEARCH_COMMANDS):
            entities.append("search")

            return Interpretation(
                intent=intent,
                entities=entities,
            )

        # Explicit notes command
        elif text == "notes" or text.startswith(
            self.NOTES_COMMANDS,
        ):
            entities.append("notes")

            return Interpretation(
                intent=intent,
                entities=entities,
            )

        elif text.startswith(self.BROWSER_COMMANDS,):
            entities.append("browser")

            return Interpretation(
                intent=intent,
                entities=entities,
            )
        
        # Question
        elif (
            text.endswith("?")
            or text.startswith(self.QUESTION_PREFIXES)
        ):
            intent = Intent.QUESTION

        # Entity extraction

        if any(
            keyword in text
            for keyword in self.TIME_KEYWORDS
        ):
            entities.append("time")

        if any(
            keyword in text
            for keyword in self.DATE_KEYWORDS
        ):
            entities.append("date")

        if any(
            keyword in text
            for keyword in self.CALCULATION_KEYWORDS
        ):
            entities.append("calculator")

        if any(
            keyword in text
            for keyword in self.WEATHER_KEYWORDS
        ):
            entities.append("weather")

        if any(
            text.startswith(keyword)
            for keyword in self.FILE_SYSTEM_COMMANDS
        ):
            entities.append("file_system",)

        return Interpretation(
            intent=intent,
            entities=entities,
        )
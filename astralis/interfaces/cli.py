from astralis.brain.brain import Brain
from astralis.brain.request import Request
from astralis.brain.source import RequestSource

_EXIT_COMMANDS = {"exit", "quit"}


class CommandLineInterface:
    """Provides a command-line interface for ASTRALIS."""

    def __init__(
        self,
        brain: Brain,
    ) -> None:
        self.brain = brain

    def run(self) -> None:
        """Start the interactive command-line session."""

        print()
        print("Welcome to ASTRALIS.")
        print("Type 'exit' or 'quit' to quit.")
        print()

        while True:
            text = input("> ").strip()

            if not text:
                continue

            if text.lower() in _EXIT_COMMANDS:
                print()
                print("Thank you for using ASTRALIS.\n Goodbye.")
                break

            request = Request(
                text=text,
                source=RequestSource.CLI,
            )

            response = self.brain.process(request)

            print()
            print(f"ASTRALIS: {response.text}")
            print()

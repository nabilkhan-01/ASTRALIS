from astralis.brain.request import Request
from astralis.brain.source import RequestSource
from astralis.pipeline.request_pipeline import RequestPipeline

_EXIT_COMMANDS = {"exit", "quit"}


class CommandLineInterface:
    """Provides a command-line interface for ASTRALIS."""

    def __init__(
        self,
        pipeline: RequestPipeline,
    ) -> None:
        self.pipeline = pipeline

    def run(
        self,
    ) -> None:
        """Start the interactive command-line session."""

        self._print_welcome()

        while True:
            try:
                text = input("> ").strip()

            except (
                KeyboardInterrupt,
                EOFError,
            ):
                print()
                print("Thank you for using ASTRALIS.")
                break

            if not text:
                continue

            if text.lower() in _EXIT_COMMANDS:
                print()
                print("Thank you for using ASTRALIS.")
                break

            request = Request(
                text=text,
                source=RequestSource.CLI,
            )

            response = self.pipeline.process(
                request,
            )

            print()
            print(
                f"ASTRALIS: {response.text}",
            )
            print()

    def _print_welcome(
        self,
    ) -> None:
        """Display the startup banner."""

        print()
        print("Welcome to ASTRALIS.")
        print("Type 'exit' or 'quit' to quit.")
        print()

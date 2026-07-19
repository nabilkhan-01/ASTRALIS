from astralis.core.engine import Engine


def main() -> None:
    """Application entry point."""

    engine = Engine()
    engine.start()
    engine.run()


if __name__ == "__main__":
    main()
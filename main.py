from astralis.bootstrap.bootstrap import Bootstrap


def main() -> None:
    """Application entry point."""

    bootstrap = Bootstrap()
    engine = bootstrap.build()
    engine.start()
    engine.run()


if __name__ == "__main__":
    main()

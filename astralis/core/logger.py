import logging


class AstralisLogger:
    """Provides a centralized logger for ASTRALIS."""

    def __init__(
        self,
    ) -> None:
        self._logger = logging.getLogger(
            "ASTRALIS",
        )

        self._logger.setLevel(
            logging.INFO,
        )

        self._logger.propagate = False

        if not self._logger.handlers:
            console_handler = logging.StreamHandler()

            console_handler.setLevel(
                logging.INFO,
            )

            formatter = logging.Formatter(
                "[%(levelname)s] %(message)s",
            )

            console_handler.setFormatter(
                formatter,
            )

            self._logger.addHandler(
                console_handler,
            )

    @property
    def logger(
        self,
    ) -> logging.Logger:
        """Return the configured logger instance."""

        return self._logger

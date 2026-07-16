import logging


class AstralisLogger:
    """Provides a centralized logger for ASTRALIS."""

    def __init__(self):
        self._logger = logging.getLogger("ASTRALIS")
        self._logger.setLevel(logging.INFO)

        if not self._logger.handlers:
            console_handler = logging.StreamHandler()

            log_format = "[%(levelname)s] %(message)s"

            formatter = logging.Formatter(log_format)   

            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)

    @property
    def logger(self):
        """Return the configured logger instance."""
        return self._logger
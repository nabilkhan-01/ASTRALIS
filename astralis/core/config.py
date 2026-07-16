"""
ASTRALIS Configuration

Central configuration for the ASTRALIS application.

Philosophy:
Assist. Don't Control.
"""


class Config:
    """
    Stores application-wide configuration for ASTRALIS.

    This class contains settings that define how the application
    behaves. User-specific preferences are managed separately.
    """

    def __init__(self):
        self.project_name = "ASTRALIS"
        self.version = "0.0.1"
        self.codename = "Genesis"
        self.tagline = "Assist. Don't Control."

        self.language = "en"
        self.debug = True
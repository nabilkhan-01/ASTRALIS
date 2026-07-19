"""
ASTRALIS Configuration

Central configuration for the ASTRALIS application.

Philosophy:
Assist. Don't Control.
"""

from dataclasses import dataclass


@dataclass
class Config:
    """
    Stores application-wide configuration for ASTRALIS.

    This class contains settings that define how the application
    behaves. User-specific preferences are managed separately.
    """

    project_name: str = "ASTRALIS"
    version: str = "0.1.0"
    codename: str = "Foundation"
    tagline: str = "Assist. Don't Control."

    language: str = "en"
    debug: bool = True

    # AI Provider Configuration
    provider: str = "mock"
    model: str = "gpt-5"
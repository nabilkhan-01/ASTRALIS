from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Stores application-wide configuration."""

    # Application Information
    project_name: str = "ASTRALIS"
    version: str = "0.1.0"
    codename: str = "Foundation"
    tagline: str = "Assist. Don't Control."

    # Runtime Settings
    language: str = "en"
    debug: bool = True

    # AI Provider Configuration
    provider: str = "openai"
    model: str = os.getenv(
        "OPENAI_MODEL",
        "gpt-5",
    )

    openai_api_key: str = os.getenv(
        "OPENAI_API_KEY",
        "",
    )
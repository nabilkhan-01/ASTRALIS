from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Stores application-wide configuration."""

    # Application Information
    project_name: str = "ASTRALIS"
    version: str = "0.2.0"
    codename: str = "Brain Architecture"
    tagline: str = "Assist. Don't Control."

    # Runtime Settings
    language: str = "en"
    debug: bool = True

    # Active AI Provider
    provider: str = os.getenv(
        "DEFAULT_PROVIDER",
        "gemini",
    )

    # Gemini Configuration
    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        "",
    )

    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-flash-latest",
    )

    # OpenAI Configuration
    openai_api_key: str = os.getenv(
        "OPENAI_API_KEY",
        "",
    )

    openai_model: str = os.getenv(
        "OPENAI_MODEL",
        "gpt-5",
    )
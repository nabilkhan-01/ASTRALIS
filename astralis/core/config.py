import os
from dataclasses import dataclass
from typing import ClassVar

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Stores application-wide configuration."""

    # Application Information
    project_name: str = "ASTRALIS"
    version: str = "0.3.1"
    codename: str = "Engineering Stability"
    tagline: str = "Assist. Don't Control."

    # Runtime Settings
    language: str = "en"

    # Monitoring Settings
    monitoring_enabled: bool = False

    debug: bool = (
        os.getenv(
            "DEBUG",
            "false",
        ).lower()
        == "true"
    )

    # Default AI Provider
    DEFAULT_PROVIDER: ClassVar[str] = "gemini"

    # Active AI Provider
    provider: str = os.getenv(
        "DEFAULT_PROVIDER",
        DEFAULT_PROVIDER,
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

    # Ollama / Local Model Configuration
    ollama_host: str = os.getenv(
        "OLLAMA_HOST",
        "http://localhost:11434",
    )

    ollama_model: str = os.getenv(
        "OLLAMA_MODEL",
        "",
    )

    # Tavily Configuration
    tavily_api_key: str = os.getenv(
        "TAVILY_API_KEY",
        "",
    )

    # HTTP Configuration
    api_timeout: int = int(
        os.getenv(
            "API_TIMEOUT",
            "5",
        )
    )

    user_agent: str = f"ASTRALIS/{version}"

    # Voice Settings
    voice_enabled: bool = False
    wake_word: str = "Astralis"

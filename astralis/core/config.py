import os
from dataclasses import dataclass, field
from typing import ClassVar

from dotenv import load_dotenv

from astralis.providers.reasoning import ReasoningMode

load_dotenv()


def _get_default_reasoning_mode() -> ReasoningMode:
    return ReasoningMode.from_string(
        os.getenv(
            "OLLAMA_REASONING_MODE",
            "auto",
        ),
    )



@dataclass
class Config:
    """Stores application-wide configuration."""

    # Application Information
    project_name: str = "ASTRALIS"
    version: str = "0.4.0"
    codename: str = "Context Foundation"
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

    ollama_timeout: int = int(
        os.getenv(
            "OLLAMA_TIMEOUT",
            "60",
        )
    )

    ollama_reasoning_mode: ReasoningMode = field(
        default_factory=_get_default_reasoning_mode,
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

    def __post_init__(self) -> None:
        if isinstance(
            self.ollama_reasoning_mode,
            str,
        ):
            self.ollama_reasoning_mode = (
                ReasoningMode.from_string(
                    self.ollama_reasoning_mode,
                )
            )

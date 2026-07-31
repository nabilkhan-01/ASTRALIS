from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class SearchResult:
    """Represents a search result."""

    title: str
    url: str
    content: str

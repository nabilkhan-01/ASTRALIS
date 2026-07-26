from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherData:
    """Represents current weather conditions."""

    city: str
    temperature: float
    windspeed: float

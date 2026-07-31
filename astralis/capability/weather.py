import requests

from astralis.api.weather import WeatherApi
from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability


class WeatherCapability(Capability):
    """Provides current weather information."""

    def __init__(
        self,
        api: WeatherApi,
    ) -> None:
        self.api = api

    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Return the current weather."""

        _ = conversation, interpretation

        try:
            city = self._extract_city(
                request.text,
            )

            weather = self.api.get_current_weather(
                city,
            )

            return Response(
                text=(
                    f"The current temperature in "
                    f"{weather.city} is "
                    f"{weather.temperature}°C "
                    f"with a wind speed of "
                    f"{weather.wind_speed} km/h."
                ),
            )

        except (
            ValueError,
            requests.RequestException,
        ) as error:
            return Response(
                text=str(error),
                success=False,
            )

    def _extract_city(
        self,
        text: str,
    ) -> str:
        """Extract the requested city."""

        lower = text.lower()

        if " in " not in lower:
            raise ValueError(
                "Please specify a city.",
            )

        index = lower.index(
            " in ",
        )

        city = text[index + 4 :].strip()

        if not city:
            raise ValueError(
                "Please specify a city.",
            )

        return city

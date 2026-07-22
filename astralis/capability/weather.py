import requests

from astralis.api.weather import WeatherApi
from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability


class WeatherCapability(Capability):
    """Provides current weather information."""

    def __init__(self) -> None:
        self.api = WeatherApi()

    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Return the current weather."""

        city = self._extract_city(
            request.text,
        )

        try:
            weather = self.api.get_current_weather(
                city,
            )

            return Response(
                text=(
                    f"The current temperature in "
                    f"{weather.city} is "
                    f"{weather.temperature}°C "
                    f"with a wind speed of "
                    f"{weather.windspeed} km/h."
                ),
                success=True,
            )

        except Exception as error:
            return Response(
                text=str(error),
                success=False,
            )

        except requests.RequestException:
            return Response(
                text="Unable to retrieve weather information right now.",
                success=False,
            )

    def _extract_city(
        self,
        text: str,
    ) -> str:
        """Extract the requested city."""

        text = text.lower()

        if " in " not in text:
            raise ValueError(
                "Please specify a city."
            )

        city = text.split(
            " in ",
            maxsplit=1,
        )[1].strip()

        return city
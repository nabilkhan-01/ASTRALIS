from unittest.mock import Mock

from astralis.api.weather import WeatherApi
from astralis.capability.weather import WeatherCapability
from astralis.models.weather_data import WeatherData
from tests.helpers.conversation_factory import (
    create_conversation,
)
from tests.helpers.interpretation_factory import (
    create_interpretation,
)
from tests.helpers.request_factory import (
    create_request,
)


class TestWeatherCapability:
    """Tests for the WeatherCapability."""

    @staticmethod
    def _create_capability() -> tuple[WeatherCapability, Mock]:
        """Create a weather capability with a mocked API."""

        api = Mock(
            spec=WeatherApi,
        )

        capability = WeatherCapability(
            api,
        )

        return capability, api

    def test_weather(
        self,
    ) -> None:
        """Return the current weather."""

        capability, api = self._create_capability()

        api.get_current_weather.return_value = WeatherData(
            city="Delhi",
            temperature=31.2,
            wind_speed=7.5,
        )

        response = capability.execute(
            create_request(
                "weather in delhi",
            ),
            create_conversation(),
            create_interpretation(
                entities=["weather"],
            ),
        )

        api.get_current_weather.assert_called_once_with(
            "delhi",
        )

        assert response.success is True
        assert (
            response.text == "The current temperature in Delhi is 31.2°C "
            "with a wind speed of 7.5 km/h."
        )

    def test_unknown_city(
        self,
    ) -> None:
        """Handle an unknown city."""

        capability, api = self._create_capability()

        api.get_current_weather.side_effect = ValueError(
            "Unknown city.",
        )

        response = capability.execute(
            create_request(
                "weather in nowhere",
            ),
            create_conversation(),
            create_interpretation(
                entities=["weather"],
            ),
        )

        api.get_current_weather.assert_called_once_with(
            "nowhere",
        )

        assert response.success is False
        assert response.text == "Unknown city."

    def test_missing_city(
        self,
    ) -> None:
        """Handle a missing city."""

        capability, _ = self._create_capability()

        response = capability.execute(
            create_request(
                "weather",
            ),
            create_conversation(),
            create_interpretation(
                entities=["weather"],
            ),
        )

        assert response.success is False
        assert response.text == "Please specify a city."

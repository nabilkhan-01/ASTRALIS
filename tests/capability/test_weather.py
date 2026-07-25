from unittest.mock import Mock

from astralis.models.weather_data import WeatherData
from astralis.capability.weather import WeatherCapability

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

    def setup_method(self) -> None:
        """Create a weather capability."""

        self.capability = WeatherCapability()

        self.capability.api = Mock()

    def test_weather(self) -> None:
        """Return the current weather."""

        self.capability.api.get_current_weather.return_value = (
            WeatherData(
                city="Delhi",
                temperature=31.2,
                windspeed=7.5,
            )
        )

        response = self.capability.execute(
            create_request(
                "weather in delhi",
            ),
            create_conversation(),
            create_interpretation(
                entities=["weather"],
            ),
        )

        assert response.success is True

        assert (
            response.text
            == "The current temperature in Delhi is 31.2°C with a wind speed of 7.5 km/h."
        )

    def test_unknown_city(self) -> None:
        """Handle an unknown city."""

        self.capability.api.get_current_weather.side_effect = (
            ValueError(
                "Unknown city.",
            )
        )

        response = self.capability.execute(
            create_request(
                "weather in nowhere",
            ),
            create_conversation(),
            create_interpretation(
                entities=["weather"],
            ),
        )

        assert response.success is False
        assert response.text == "Unknown city."

    def test_missing_city(self) -> None:
        """Handle a missing city."""

        response = self.capability.execute(
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
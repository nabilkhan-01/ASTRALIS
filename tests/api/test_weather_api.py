from unittest.mock import Mock, patch

from astralis.api.weather import WeatherApi
from astralis.core.config import Config


class TestWeatherApi:
    """Tests for the WeatherApi."""

    @patch("requests.Session.get")
    def test_get_current_weather(
        self,
        mock_get: Mock,
    ) -> None:
        """Retrieve the current weather."""

        geocoding_response = Mock()

        geocoding_response.json.return_value = {
            "results": [
                {
                    "name": "Delhi",
                    "latitude": 28.61,
                    "longitude": 77.21,
                },
            ],
        }

        geocoding_response.raise_for_status.return_value = None

        weather_response = Mock()

        weather_response.json.return_value = {
            "current_weather": {
                "temperature": 30.5,
                "wind_speed": 8.2,
            },
        }

        weather_response.raise_for_status.return_value = None

        mock_get.side_effect = [
            geocoding_response,
            weather_response,
        ]

        config = Config()

        api = WeatherApi(
            config,
        )

        weather = api.get_current_weather(
            "Delhi",
        )

        assert mock_get.call_count == 2

        first_call = mock_get.call_args_list[0]
        second_call = mock_get.call_args_list[1]

        assert first_call.kwargs["params"] == {
            "name": "Delhi",
            "count": 10,
        }

        assert second_call.kwargs["params"] == {
            "latitude": 28.61,
            "longitude": 77.21,
            "current_weather": True,
        }

        assert weather.city == "Delhi"
        assert weather.temperature == 30.5
        assert weather.wind_speed == 8.2
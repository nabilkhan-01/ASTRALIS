from unittest.mock import Mock, patch

from astralis.api.weather import WeatherApi


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
                }
            ]
        }

        geocoding_response.raise_for_status.return_value = None

        weather_response = Mock()

        weather_response.json.return_value = {
            "current_weather": {
                "temperature": 30.5,
                "windspeed": 8.2,
            }
        }

        weather_response.raise_for_status.return_value = None

        mock_get.side_effect = [
            geocoding_response,
            weather_response,
        ]

        api = WeatherApi()

        weather = api.get_current_weather(
            "Delhi",
        )

        assert weather.city == "Delhi"
        assert weather.temperature == 30.5
        assert weather.windspeed == 8.2

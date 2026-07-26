from astralis.api.client import ApiClient
from astralis.models.weather_data import WeatherData


class WeatherApi(ApiClient):
    """Client for retrieving weather data."""

    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    def get_current_weather(
        self,
        city: str,
    ) -> WeatherData:
        """Return the current weather for a city."""

        location = self._get_location(
            city,
        )

        current = self._get_weather(
            latitude=location["latitude"],
            longitude=location["longitude"],
        )

        return WeatherData(
            city=location["name"],
            temperature=current["temperature"],
            windspeed=current["windspeed"],
        )

    def _get_location(
        self,
        city: str,
    ) -> dict:
        """Resolve a city into coordinates."""

        search_name = city

        country = None

        if "," in city:
            search_name, country = city.split(
                ",",
                maxsplit=1,
            )

            search_name = search_name.strip()
            country = country.strip().lower()

        data = self.get(
            self.GEOCODING_URL,
            params={
                "name": search_name,
                "count": 10,
            },
        )

        results = data.get(
            "results",
        )

        if not results:
            raise ValueError(
                f"Unknown city '{city}'.",
            )

        if country is not None:
            for result in results:
                if (
                    result.get(
                        "country",
                        "",
                    ).lower()
                    == country
                ):
                    return result

        return results[0]

    def _get_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:
        """Retrieve current weather."""

        data = self.get(
            self.WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": True,
            },
        )

        return data["current_weather"]

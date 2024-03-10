import unittest
from unittest.mock import MagicMock

import requests
from sdk_classes.class_sdk_weather import OpenWeatherMap
from config.config  import API_KEY


class TestWeatherAPI(unittest.TestCase):
    """Test errors status code"""
    def setUp(self):
        """
                        Set up test data and create an instance of the OpenWeatherMap API client.
                        """
        self.api_key = API_KEY
        self.mode = "on_demand"
        self.weather = OpenWeatherMap(api_key=self.api_key, mode=self.mode)
        self.city = "London"

    def tearDown(self):
        """
                      Clean up after each test by deleting the instance.
                      """
        self.weather.delete_instance()

    def test__get_weather_on_demand_401(self):
        """Test handling HTTPError with status code 401."""
        with self.assertRaises(requests.exceptions.HTTPError):
            mock_response = MagicMock()
            mock_response.status_code = 401
            self.weather._get_weather_on_demand = MagicMock(side_effect=requests.exceptions.HTTPError(response=mock_response))
            self.weather._get_weather_on_demand(city=self.city, key=self.api_key)

    def test__get_weather_on_demand_404(self):
        """Test handling HTTPError with status code 404."""
        with self.assertRaises(requests.exceptions.HTTPError):
            mock_response = MagicMock()
            mock_response.status_code = 404
            self.weather._get_weather_on_demand = MagicMock(side_effect=requests.exceptions.HTTPError(response=mock_response))
            self.weather._get_weather_on_demand(city=self.city, key=self.api_key)

    def test__get_weather_on_demand_429(self):
        """Test handling HTTPError with status code 429."""
        with self.assertRaises(requests.exceptions.HTTPError):
            mock_response = MagicMock()
            mock_response.status_code = 429
            self.weather._get_weather_on_demand = MagicMock(side_effect=requests.exceptions.HTTPError(response=mock_response))
            self.weather._get_weather_on_demand(city=self.city, key=self.api_key)

    def test__get_weather_on_demand_500(self):
        """Test handling HTTPError with status code 500."""
        with self.assertRaises(requests.exceptions.HTTPError):
            mock_response = MagicMock()
            mock_response.status_code = 500
            self.weather._get_weather_on_demand = MagicMock(side_effect=requests.exceptions.HTTPError(response=mock_response))
            self.weather._get_weather_on_demand(city=self.city, key=self.api_key)

    def test__get_weather_on_demand_502(self):
        """Test handling HTTPError with status code 502."""
        with self.assertRaises(requests.exceptions.HTTPError):
            mock_response = MagicMock()
            mock_response.status_code = 502
            self.weather._get_weather_on_demand = MagicMock(side_effect=requests.exceptions.HTTPError(response=mock_response))
            self.weather._get_weather_on_demand(city=self.city, key=self.api_key)

    def test__get_weather_on_demand_503(self):
        """Test handling HTTPError with status code 503."""
        with self.assertRaises(requests.exceptions.HTTPError):
            mock_response = MagicMock()
            mock_response.status_code = 503
            self.weather._get_weather_on_demand = MagicMock(side_effect=requests.exceptions.HTTPError(response=mock_response))
            self.weather._get_weather_on_demand(city=self.city, key=self.api_key)

    def test__get_weather_on_demand_504(self):
        """Test handling HTTPError with status code 504."""
        with self.assertRaises(requests.exceptions.HTTPError):
            mock_response = MagicMock()
            mock_response.status_code = 504
            self.weather._get_weather_on_demand = MagicMock(side_effect=requests.exceptions.HTTPError(response=mock_response))
            self.weather._get_weather_on_demand(city=self.city, key=self.api_key)

    def test__get_weather_on_demand_RequestException(self):
        """Test handling RequestException."""
        with self.assertRaises(requests.exceptions.RequestException):
            self.weather._get_weather_on_demand = MagicMock(side_effect=requests.exceptions.RequestException)
            self.weather._get_weather_on_demand(city=self.city, key=self.api_key)

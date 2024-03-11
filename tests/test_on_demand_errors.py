import unittest
from unittest.mock import patch

import requests

from conf import API_KEY
from sdk_classes.class_sdk_weather import OpenWeatherMap


class TestOpenWeatherMap(unittest.TestCase):
    """
    Test cases for the OpenWeatherMap class errors.
    """

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

    @patch("sdk_classes.class_sdk_weather.requests.get")
    def test_get_weather_on_demand_success(self, mock_get):
        """
        Test successful weather data retrieval.

        Mocks a successful API response and verifies that weather data is retrieved correctly.

        """

        mock_response = {
            "weather": [{"main": "Clouds", "description": "broken clouds"}],
            "main": {"temp": 20, "feels_like": 18},
            "visibility": 10000,
            "wind": {"speed": 3.5},
            "dt": 1646890800,
            "sys": {"sunrise": 1646851977, "sunset": 1646894477},
            "timezone": -18000,
            "name": "New York",
        }
        mock_get.return_value.json.return_value = mock_response

        weather_data = self.weather._get_weather_on_demand(self.city, self.api_key)

        self.assertIsNotNone(weather_data)
        self.assertEqual(weather_data["weather"]["main"], "Clouds")

    @patch("sdk_classes.class_sdk_weather.requests.get")
    def test_get_weather_on_demand_error_401_handling(self, mock_get):
        """
        Test handling of HTTP 401 error.

        Mocks an HTTP 401 error response and verifies that it is handled correctly.

        """
        key = "test-key"
        mock_response = requests.Response()
        mock_response.status_code = 401
        mock_get.side_effect = requests.exceptions.HTTPError(response=mock_response)

        weather_data = self.weather._get_weather_on_demand(self.city, key)

        self.assertIsNone(weather_data)
        self.assertTrue(mock_get.called)

    @patch("sdk_classes.class_sdk_weather.requests.get")
    def test_get_weather_on_demand_error_404_handling(self, mock_get):
        """
        Test handling of HTTP 404 error.

        Mocks an HTTP 404 error response and verifies that it is handled correctly.

        """

        city = "Nonexistent City"
        mock_response = requests.Response()
        mock_response.status_code = 404
        mock_get.side_effect = requests.exceptions.HTTPError(response=mock_response)

        weather_data = self.weather._get_weather_on_demand(city, self.api_key)

        self.assertIsNone(weather_data)
        self.assertTrue(mock_get.called)

    @patch("sdk_classes.class_sdk_weather.requests.get")
    def test_get_weather_on_demand_error_429_handling(self, mock_get):
        """
        Test handling of HTTP 429 error.

        Mocks an HTTP 429 error response and verifies that it is handled correctly.

        """
        mock_response = requests.Response()
        mock_response.status_code = 429
        mock_get.side_effect = requests.exceptions.HTTPError(response=mock_response)

        weather_data = self.weather._get_weather_on_demand(self.city, self.api_key)

        self.assertIsNone(weather_data)
        self.assertTrue(mock_get.called)

    @patch("sdk_classes.class_sdk_weather.requests.get")
    def test_get_weather_on_demand_error_500_handling(self, mock_get):
        """
        Test handling of HTTP 500 error.

        Mocks an HTTP 500 error response and verifies that it is handled correctly.

        """
        mock_response = requests.Response()
        mock_response.status_code = 500
        mock_get.side_effect = requests.exceptions.HTTPError(response=mock_response)

        # Act
        weather_data = self.weather._get_weather_on_demand(self.city, self.api_key)

        # Assert
        self.assertIsNone(weather_data)
        self.assertTrue(mock_get.called)

    @patch("sdk_classes.class_sdk_weather.requests.get")
    def test_get_weather_on_demand_error_410_handling(self, mock_get):
        """
        Test handling of  any HTTP error.

        Mocks an HTTP 410 error response and verifies that it is handled correctly.

        """
        mock_response = requests.Response()
        mock_response.status_code = 410
        mock_get.side_effect = requests.exceptions.HTTPError(response=mock_response)

        # Act
        weather_data = self.weather._get_weather_on_demand(self.city, self.api_key)

        # Assert
        self.assertIsNone(weather_data)
        self.assertTrue(mock_get.called)

    @patch("sdk_classes.class_sdk_weather.requests.get")
    def test_get_weather_on_demand_error_handling(self, mock_get):
        """
        Test handling of general request error.

        Mocks a general request error and verifies that it is handled correctly.

        """
        mock_response = requests.Response()
        mock_get.side_effect = requests.exceptions.RequestException(
            response=mock_response
        )

        weather_data = self.weather._get_weather_on_demand(self.city, self.api_key)

        self.assertIsNone(weather_data)
        self.assertTrue(mock_get.called)

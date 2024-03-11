import os
import unittest
from conf import API_KEY
from sdk_classes.class_sdk_weather import OpenWeatherMap
from sdk_classes.metaclass import DuplicateClassError

class TestOpenWeatherMap(unittest.TestCase):
    """
       Test cases for the OpenWeatherMap class.
       """

    def setUp(self):
        """
                Set up test data and create an instance of the OpenWeatherMap API client.
                """
        self.api_key = API_KEY
        self.mode = "on_demand"
        self.weather = OpenWeatherMap(api_key=self.api_key, mode=self.mode)
        self.city = "Vilnius"
        self.url = f'https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}'
        self.cities = [
            "New York",
            "London",
            "Tokyo",
            "Paris",
            "Moscow",
            "Beijing",
            "Berlin",
            "Istanbul",
            "Rio de Janeiro",
            "Vilnius"
        ]

    def tearDown(self):
        """
               Clean up after each test by deleting the instance.
               """
        if os.path.exists(self.weather.file_name):
            os.remove(self.weather.file_name)
        self.weather.delete_instance()

    def test_get_weather(self):
        """
                Test getting weather data for various cities.
                """
        for city in self.cities:
            weather_data = self.weather.get_weather(city)
            self.assertIsNotNone(weather_data)


    def test_get_url(self):
        """
                Test generating the URL for API requests.
                """
        url = self.weather.get_url(self.city, self.api_key)
        self.assertIsNotNone(url)
        self.assertEqual(url, self.url)

    def test__get_weather_on_demand(self):
        """
               Test retrieving weather data in on-demand mode.
               """
        for city in self.cities:
            weather_data = self.weather._get_weather_on_demand(city=city, key=self.api_key)
            self.assertIsNotNone(weather_data)

    def test_delete_instance(self):
        """
                Test deleting the instance.
                """
        self.assertIn(self.api_key, OpenWeatherMap._instances)
        self.weather.delete_instance()
        self.assertNotIn(self.api_key, OpenWeatherMap._instances)

    def test_get_weather_invalid_mode(self):
        """
                Test initializing OpenWeatherMap with an invalid mode.
                """
        self.weather.delete_instance()
        mode = "test_mode"
        with self.assertRaises(ValueError):
            weather = OpenWeatherMap(api_key=self.api_key, mode=mode)

    def test_duplicate_copies(self):
        with self.assertRaises(DuplicateClassError):
            weather = OpenWeatherMap(api_key=self.api_key, mode=self.mode)







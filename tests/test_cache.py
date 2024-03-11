from conf import API_KEY
from sdk_classes.class_sdk_weather import OpenWeatherMap
import unittest

import json

import os


class TestSaveCache(unittest.TestCase):
    """
    Test cases for saving and loading cache data.
    """

    def setUp(self):
        """
        Set up test data and create an instance of the OpenWeatherMap API client.
        """
        self.cache_data = {
            "New York": {
                "time": "2024-03-09T19:44:09.584723",
                "data": {
                    "weather": {"main": "Haze", "description": "haze"},
                    "temperature": {"temp": 278.65, "feels_like": 274.06},
                    "visibility": 8047,
                    "wind": {"speed": 7.72},
                    "datetime": 1710005627,
                    "sys": {"sunrise": 1709983007, "sunset": 1710024977},
                    "timezone": -18000,
                    "name": "New York",
                },
            }
        }
        self.api_key = API_KEY
        self.mode = "on_demand"

        self.weather_instance = OpenWeatherMap(api_key=self.api_key, mode=self.mode)
        with open(self.weather_instance.file_name, "w") as file:
            json.dump(self.cache_data, file)

    def tearDown(self):
        """
        Clean up after each test by removing the cache file and deleting the instance.
        """
        os.remove(self.weather_instance.file_name)
        self.weather_instance.delete_instance()

    def test_load_cache_existing_file(self):
        """
        Test loading cache data from an existing file.
        """
        loaded_cache_data = self.weather_instance._load_cache()
        expected_time = self.cache_data["New York"]["time"]
        actual_time = loaded_cache_data["New York"]["time"].strftime(
            "%Y-%m-%dT%H:%M:%S.%f"
        )
        self.assertEqual(actual_time, expected_time)
        expected_data = self.cache_data["New York"]["data"]
        actual_data = loaded_cache_data["New York"]["data"]
        self.assertEqual(expected_data, actual_data)

    def test_load_cache_corrupted_file(self):
        """
        Test loading cache data from a corrupted file.
        """
        with open(self.weather_instance.file_name, "w") as file:
            file.write("corrupted_test_data")
        loaded_cache_data = self.weather_instance._load_cache()
        self.assertEqual(loaded_cache_data, {})

    def test_save_cache(self):
        """
        Test saving cache data to a file.
        """
        self.weather_instance._save_cache(self.cache_data)
        self.assertTrue(os.path.exists(self.weather_instance.file_name))
        with open(self.weather_instance.file_name, "r") as file:
            saved_cache_data = json.load(file)
        self.assertEqual(saved_cache_data, self.cache_data)

    def test_cache_overflow(self):
        cities = [
            "Minsk",
            "London",
            "Tokyo",
            "Paris",
            "Moscow",
            "Beijing",
            "Berlin",
            "Istanbul",
            "Rio de Janeiro",
            "Vilnius",
            "Rome",
        ]
        self.assertEqual(len(self.weather_instance._cache), 0)
        for city in cities:
            self.weather_instance.get_weather(city)
        self.assertEqual(
            len(self.weather_instance._cache), self.weather_instance.cache_limit
        )

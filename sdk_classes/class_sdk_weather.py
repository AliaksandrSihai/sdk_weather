import json
import logging

import time
from datetime import datetime, timedelta
import concurrent.futures
import requests

from sdk_classes.metaclass import SingletonMeta


class OpenWeatherMap(metaclass=SingletonMeta):
    __ON_DEMAND = "on_demand"
    __POLLING = "polling"

    def __init__(self, api_key: str, mode: str) -> None:
        """
        Initializes an instance of the OpenWeather API client.

        Instructions on how to obtain an API key can be found here: https://openweathermap.org/appid

        Args:
            api_key (str): Your OpenWeather application programming interface (API) key.
            mode (str): The mode of operation for the API client. Should be one of 'polling' or 'on_demand'.

        Attributes:
            api_key (str): Your OpenWeather API key.
            file_name (str): The filename to store cache data.
            _cache (dict): A dictionary to store cached weather data.
            cache_limit (int): The maximum number of cached entries.
            mode (str): The mode of operation for the API client. Either 'polling' or 'on_demand'.

        Raises:
            ValueError: If the `mode` is not 'polling' or 'on_demand'.
        """
        self.api_key = api_key
        self.file_name = "weather_cache.json"
        self._cache = self._load_cache()
        self.cache_limit = 10

        # Ensure only one mode is active (concise error message)
        if mode not in [self.__ON_DEMAND, self.__POLLING]:
            logging.error(
                f"Mode must be one of {self.__ON_DEMAND} or {self.__POLLING}."
            )
            raise ValueError(
                f"Mode must be one of {self.__ON_DEMAND} or {self.__POLLING}."
            )

        self.mode = mode
        if self.mode == self.__POLLING:
            self.update_weather_thread()

        logging.info(
            f"Initialized OpenWeatherMap API with key {api_key} (mode: {self.mode})"
        )

    def delete_instance(self) -> None:
        """
        Deletes the instance from the class-level dictionary of instances.

        Returns:
            None
        """
        if self.api_key in self.__class__._instances:
            del self.__class__._instances[self.api_key]

    def _load_cache(self) -> dict:
        """
        Loads cache data from a file.
        Returns:
            dict: A dictionary containing cache data loaded from the file.
        """

        try:
            with open(self.file_name, "r") as file:
                cache_data = json.load(file)
                for city, data in cache_data.items():
                    data["time"] = datetime.fromisoformat(data["time"])
                return cache_data
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return dict()

    def _save_cache(self, cache_data: dict) -> None:
        """
        Saves cache data to a file.
        Args:
            cache_data (dict): A dictionary containing cache data to be saved.

        Returns:
            None
        """

        for city, data in cache_data.items():
            if isinstance(data["time"], str):
                data["time"] = datetime.fromisoformat(data["time"])
            data["time"] = data["time"].isoformat()
        with open(self.file_name, "w") as file:
            json.dump(cache_data, file)

    def get_weather(self, city: str) -> dict:
        """
        Retrieves weather data for the specified city.

        Args:
            city (str): The name of the city for which to get weather data.

        Returns:
            dict or None: A dictionary containing weather data on success, or None on error.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the API request.
            ValueError: If the mode is unknown.
        """

        now = datetime.now()

        if city in self._cache:
            cached_time = (
                self._cache[city]["time"]
                if isinstance(self._cache[city]["time"], datetime)
                else datetime.fromisoformat(self._cache[city]["time"])
            )
            if now - cached_time < timedelta(minutes=10):
                logging.debug(f"Using cached weather data for {city}")
                return self._cache[city]["data"]

        elif city not in self._cache:
            if len(self._cache) >= self.cache_limit:

                oldest_city = min(self._cache, key=lambda k: self._cache[k]["time"])
                del self._cache[oldest_city]

            self._cache[city] = {"time": datetime.now(), "data": {}}
            self._save_cache(self._cache)

        if self.mode == self.__ON_DEMAND:
            weather_data = self._get_weather_on_demand(city, key=self.api_key)
            self._cache[city] = {"time": datetime.now(), "data": weather_data}
            self._save_cache(self._cache)
            logging.info(f"Retrieved weather data for {city}")

            return weather_data

    def update_weather_thread(self) -> None:
        """
        Continuously updates weather data for cities in the cache using concurrent threads.

        Uses a ThreadPoolExecutor to asynchronously update weather data for each city in the cache.
        The weather data is retrieved using the _get_weather_on_demand method.
        The cache is updated with the latest weather data for each city.
        The updated cache is saved to the file.

        The method runs indefinitely and updates the weather data every 10 minutes (600 seconds).

        Returns:
            None
        """

        with concurrent.futures.ThreadPoolExecutor() as executor:
            while True:
                futures = [
                    executor.submit(
                        lambda c: self._get_weather_on_demand(c, self.api_key), city
                    )
                    for city in self._cache.keys()
                ]
                for future in concurrent.futures.as_completed(futures):

                    result = future.result()
                    city = result["name"]

                    self._cache[city] = {"time": datetime.now(), "data": result}
                    self._save_cache(self._cache)

                time.sleep(60 * 10)

    @classmethod
    def get_url(cls, city: str, key: str) -> str:
        """
        Constructs the URL for making API requests to OpenWeather.

        Args:
            city (str): The name of the city for which to get weather data.
            key (str): Your OpenWeather API key.

        Returns:
            str: The URL for making API requests.

        """

        """Getting ulr for api requests"""
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}"
        return url

    @classmethod
    def _get_weather_on_demand(cls, city: str, key: str) -> dict or None:
        """
        Retrieves weather data for the specified city using on-demand mode.

        Args:
            city (str): The name of the city for which to get weather data.
            key (str): Your OpenWeather API key.

        Returns:
            dict or None: A dictionary containing weather data on success, or None on error.

        """

        try:

            url = cls.get_url(city=city, key=key)
            weather_request = requests.get(url)
            weather_request.raise_for_status()
            current_weather = weather_request.json()

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logging.error("Error 401: Unauthorized API request")
            elif e.response.status_code == 404:
                logging.error(
                    "Error 404: City not found or incorrect API request format"
                )
            elif e.response.status_code == 429:
                logging.error(
                    "Error 429: Too many requests, consider upgrading your subscription or reducing API calls"
                )
            elif e.response.status_code in [500, 502, 503, 504]:
                logging.error(
                    f"Error {e.response.status_code}: Server error, please contact support"
                )
            else:
                logging.error(f"Unhandled HTTP error: {e}")

            return None

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching weather data for {city}: {e}")
            return None

        weather_data = {
            "weather": {
                "main": current_weather["weather"][0]["main"],
                "description": current_weather["weather"][0]["description"],
            },
            "temperature": {
                "temp": current_weather["main"]["temp"],
                "feels_like": current_weather["main"]["feels_like"],
            },
            "visibility": current_weather["visibility"],
            "wind": {
                "speed": current_weather["wind"]["speed"],
            },
            "datetime": current_weather["dt"],
            "sys": {
                "sunrise": current_weather["sys"]["sunrise"],
                "sunset": current_weather["sys"]["sunset"],
            },
            "timezone": current_weather["timezone"],
            "name": current_weather["name"],
        }
        return weather_data

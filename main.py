from sdk_classes.class_sdk_weather import OpenWeatherMap
from conf import API_KEY

if __name__ == "__main__":
    # mode = 'polling'
    mode = "on_demand"
    city = "Vilnius"
    weather = OpenWeatherMap(api_key=API_KEY, mode=mode)
    print(weather.get_weather(city=city))

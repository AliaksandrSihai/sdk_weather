# Weather API SDK
___
**Introduction**
- **This SDK provides easy access to the OpenWeatherMap API for retrieving weather data for a given location, test coverage = 95 %, flake8 = 100%**
____
**Contents**
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Example](#usage-example)
___
<br>**Supported Language**
   - Python
---
## <a name="installation"></a>Installation:
- `git clone https://github.com/AliaksandrSihai/sdk_weather.git`
- next need to create a .env file, add your api key to this file  (required configurations in .env_sample).
- `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
---
## <a name="configuration"></a>Configuration:
- create .env file(example of all the environment variables in the file .env_sample)
- register in https://openweathermap.org and add your api key to the .env file.
---
## <a name="usage-example"></a>Usage Example:
- SDK can work with different keys, while creating two copies of an object with the same key is not possible.
- in on-demand mode the SDK updates the weather information only on customer requests, If you initialize the client in 'polling' mode, SDK requests new
  weather information for all stored locations.
- The SDK store weather information about the requested cities(in 'on-demand' mode ) and if it is relevant, return the
stored value (Weather is considered if less than 10 minutes have passed after last request).
- The SDK can store information for no more than 10 cities at a time.
```
from sdk_classes.class_sdk_weather import OpenWeatherMap
from conf import API_KEY

    mode = "on_demand"
    city = "Vilnius"
    weather = OpenWeatherMap(api_key=API_KEY, mode=mode)
    result = weather.get_weather(city=city)
    print(result) -> {'weather': {'main': 'Clear', 'description': 'clear sky'}, 'temperature': {'temp': 278.64, 'feels_like': 274.4}, 'visibility': 10000, 'wind': {'speed': 6.69}, 'datetime': 1710168349, 'sys': {'sunrise': 1710132202, 'sunset': 1710173670}, 'timezone': 7200, 'name': 'Vilnius'}
    weather.delete_object()   
```
___
**Documentation:**
- Initialization Parameters:
    - api_key: API key for OpenWeatherMap
    - mode: Mode of the SDK ("on-demand" or "polling")
- Methods:
    - get_weather(city_name): Retrieves weather data for the specified city.
    - delete_object(): Deletes the object.
- Unit Tests:
   - Unit tests for SDK methods are available in the tests directory.
- Error Handling:
    - The SDK throws exceptions with a description of the reason in case of failure
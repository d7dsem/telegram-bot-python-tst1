import auxilary as aux
import requests
from typing import Tuple, Dict, List, Union



weather_api_token = None

def init_token():
    global weather_api_token
    weather_api_token = aux.get_token('OPENWEATHER_API_KEY') 

def get_weather_info_from_OpenWeather_response_mk0(data: dict) -> str:
    main_data = data.get('main', {})
    weather_data = data.get('weather', [{}])[0]
    wind_data = data.get('wind', {})

    temperature = main_data.get('temp', "N/A")
    pressure = main_data.get('pressure', "N/A")
    humidity = main_data.get('humidity', "N/A")
    weather_description = weather_data.get('description', "N/A")
    wind_speed = wind_data.get('speed', "N/A")

    return (f"The weather in {data.get('name', 'Unknown city')} is currently {weather_description} with a temperature of {temperature} degrees Celsius. "
            f"The pressure is {pressure} hPa, the humidity is {humidity}% and the wind speed is {wind_speed} m/s.")

def get_weather_info_from_OpenWeather_response(data: dict) -> str:
    info = []
    
    if 'name' in data:
        info.append(f"City {data['name']}:")

    main_data = data.get('main', {})
    if 'temp' in main_data:
        info.append(f"Temperature: {main_data['temp']} degrees Celsius")
    if 'pressure' in main_data:
        info.append(f"Pressure: {main_data['pressure']} hPa")
    if 'humidity' in main_data:
        info.append(f"Humidity: {main_data['humidity']}%")

    weather_data = data.get('weather', [{}])[0]
    if 'description' in weather_data:
        info.append(f"Condition: {weather_data['description']}")

    wind_data = data.get('wind', {})
    if 'speed' in wind_data:
        info.append(f"Wind speed: {wind_data['speed']} m/s")

    return "\n".join(info) if info else "Unexpected response format"

def get_weather_now(city):
    global weather_api_token
    if weather_api_token is None:
        raise ValueError("The variable 'waether_api_token' is not initialized.")
    
    weather_citi_req = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_token}&units=metric"
    resp = requests.get(weather_citi_req)
    try:
        resp.raise_for_status()
        return get_weather_info_from_OpenWeather_response(resp.json())        
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err} in {aux.get_current_function_name()}"
    except requests.exceptions.ConnectionError as conn_err:
        return f"Error connecting: {conn_err} in {aux.get_current_function_name()}"
    except requests.exceptions.Timeout as timeout_err:
        return f"Timeout error: {timeout_err} in {aux.get_current_function_name()}"
    except requests.exceptions.RequestException as req_err:
        return f"An unexpected error occurred during the request: {req_err} in {aux.get_current_function_name()}"

def get_coordinates(city: str) -> Tuple[float, float]:
    global weather_api_token
    if weather_api_token is None:
        raise ValueError("The variable 'weather_api_token' is not initialized.")
    
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={weather_api_token}"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    if not data:
        raise ValueError(f"No data found for city: {city}")

    return data[0]['lat'], data[0]['lon']

def get_forecasts(lat: float, lon: float) -> Dict:
    global weather_api_token
    if weather_api_token is None:
        raise ValueError("The variable 'weather_api_token' is not initialized.")
    
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&units=metric&appid={weather_api_token}"
    response = requests.get(url)
    response.raise_for_status()

    return response.json()
 
def get_forecast_types() -> List[str]:
    return ['current', 'daily', 'hourly']

def get_forecast(data: Dict, forecast_type: str) -> Union[str, List[str]]:
    if forecast_type not in get_forecast_types():
        raise ValueError(f"Invalid forecast type. Available types are: {get_forecast_types()}")

    if forecast_type == 'current':
        return get_weather_info_from_OpenWeather_response(data['current'])
    elif forecast_type in ['daily', 'hourly']:
        return [get_weather_info_from_OpenWeather_response(f) for f in data[forecast_type]]

    raise ValueError(f"Invalid forecast type. Available types are: {get_forecast_types()}")

def show_city_weather(city: str):
    weather = get_weather_now(city)
    print(weather)
    coord = get_coordinates(city) 
    print(f"Coord: {coord}")
    print()
    try:
        forecasts = get_forecasts(*coord)
    # except requests.exceptions.HTTPError as http_err:
    #     print(f"{aux.COLOR_ERROR}HTTPError Error{aux.RESET}: {e}") 
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 401:
            print("Unauthorized: The API key is invalid or missing.")
        else:
            print(f"HTTPError: {http_err}")
        return 
    except Exception as e:
        print(f"{aux.COLOR_ERROR}HTTPError{aux.RESET}: {e}") 
        return
    
    for forecast in get_forecast_types:
        info = get_forecast(forecasts,forecast)
        print(f"{forecast}")
        print(info)
        print()
 
         
if __name__ == "__main__":
    try:  
        aux.init_virt_terminal()
       
        
        
        city = "Київ"
        show_city_weather(city)

    except Exception as e:
        print(f"{aux.COLOR_ERROR}Error{aux.RESET}: {e}")     
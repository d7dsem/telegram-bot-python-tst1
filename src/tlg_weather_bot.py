import auxilary as aux
import telebot
from telebot import types
import requests
import webbrowser




waether_api_token = None

def get_weather(city):
    global waether_api_token
    if waether_api_token is None:
        raise ValueError("The variable 'waether_api_token' is not initialized.")
# https://api.openweathermap.org/data/2.5/weather?q={Kyiv}&appid={10d00cbbb36f98f939d22782f02f9b5d}&units=metric
    weather_citi_req = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={waether_api_token}&units=metric"
    resp = requests.get(weather_citi_req)
    try:
        resp.raise_for_status()
        data = resp.json()

        if 'main' in data and 'temp' in data['main']:
            temperature = data['main']['temp']
            return f"The temperature in {city} is {temperature} degrees Celsius."
        else:
            return "Unexpected response format"
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err} in {aux.get_current_function_name()}"
    except requests.exceptions.ConnectionError as conn_err:
        return f"Error connecting: {conn_err} in {aux.get_current_function_name()}"
    except requests.exceptions.Timeout as timeout_err:
        return f"Timeout error: {timeout_err} in {aux.get_current_function_name()}"
    except requests.exceptions.RequestException as req_err:
        return f"An unexpected error occurred during the request: {req_err} in {aux.get_current_function_name()}"
      

bot = telebot.TeleBot(aux.get_token('TLG_WEATHER_BOT_TOKEN'))

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Kyiv', callback_data='Kyiv')
    btn2 = types.InlineKeyboardButton('Konotop', callback_data='Konotop')

    markup.row(btn2,btn1)

    bot.send_message(message.chat.id,"Hello there! Choose city!",reply_markup=markup)

@bot.callback_query_handler(func=lambda callback:True)
def on_button_press(callback):   
    city = callback.data.strip()
    bot.send_message(callback.message.chat.id,get_weather(city))
        
@bot.message_handler()
def handler_input(message):
    city = message.text.strip()
    bot.send_message(message.chat.id,get_weather(city))


if __name__ == "__main__":
    try:  
        aux.init_virt_terminal()
        waether_api_token = aux.get_token('OPENWEATHER_API_KEY')
        aux.print_start_bot("weather")     
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"{aux.COLOR_ERROR}Error{aux.RESET}: {e}")     
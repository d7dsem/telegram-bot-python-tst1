import auxilary as aux
import ctypes
import telebot
from telebot import types
import requests
import webbrowser



kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

waether_api_token = aux.get_token('OPENWEATHER_API_KEY')

def get_weather(city):
# https://api.openweathermap.org/data/2.5/weather?q={Kyiv}&appid={10d00cbbb36f98f939d22782f02f9b5d}&units=metric
    weather_citi_req = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={waether_api_token}&units=metric"
    resp = requests.get(weather_citi_req)
    return f"Weathere in {city}:\n{resp}"

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
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"{aux.COLOR_ERROR}Error{aux.RESET}: {e}")     
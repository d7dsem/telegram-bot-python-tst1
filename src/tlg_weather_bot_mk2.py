import logging
import telebot
from telebot import types
import auxilary as aux
import openweather_interaction as owi




logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

owi.init_token()
bot = telebot.TeleBot(aux.get_token('TLG_WEATHER_BOT_TOKEN'))  # Токен вашего бота

cities = sorted(["Kyiv", "Konotop", "Odessa"])

callback_prefixes = {
    "city": "city-",
    "forecast": "forecast-"
}

def generate_inline_buttons_markup(button_names, row_len, prefix=''):
    row_len = min(row_len, 8, len(button_names))
    
    markup = types.InlineKeyboardMarkup(row_width=row_len)
    
    for i in range(0, len(button_names), row_len):
        buttons = [types.InlineKeyboardButton(text=button_text, callback_data=prefix+button_text) for button_text in button_names[i:i+row_len]]
        markup.row(*buttons)
    
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_info = f"User: {message.chat.id}, Message: {message.text}"
    logging.info(user_info)

    markup = generate_inline_buttons_markup(cities, 4, callback_prefixes['city'])

    bot.send_message(message.chat.id, "Hello there!\nSelect the name of the city.\nYou may type another city.\nMay the forse be with you.", reply_markup=markup)

        

@bot.message_handler(func=lambda message: True)
def send_weather(message):
    user_info = f"User: {message.chat.id}, Message: {message.text}"
    logging.info(user_info)
    try:
        city_name = message.text
        
        weather_info = owi.get_weather_now(city_name)
        markup = generate_inline_buttons_markup(cities, 4, callback_prefixes['forecast'])        
        bot.reply_to(message, weather_info, reply_markup=markup, parse_mode='Markdown')
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        bot.reply_to(message, "Sorry, an error occurred. Please try again later.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith(callback_prefixes['city']):
        city_name = call.data[len(callback_prefixes['city']):]
        weather_info = owi.get_weather_now(city_name)
        
        forecasts = owi.get_forecast_types()
        markup = generate_inline_buttons_markup(forecasts, 4, callback_prefixes['forecast'])
        
        bot.send_message(call.message.chat.id, weather_info, reply_markup=markup, parse_mode='Markdown')
    elif call.data.startswith(callback_prefixes['forecast']):
        forecast_type = call.data[len(callback_prefixes['forecast']):]
        # coord = owi.get_coordinates(city) 
        bot.send_message(call.message.chat.id, f"Retriewing forcasts for free using of OPENWEATHER api is not supported.\n"+
                         f"However, to access and utilize this awesome functionality, it requires a paid subscription to OPENWEATHER.\n"+
                         f"As a developer maintaining this bot, I'm currently using the free subscription.\n"+
                         f"If you find the bot helpful and wish to see it grow even better, consider contributing towards the cost of the paid subscription.\n"+
                         f"Your help will not only enable me to access the necessary data for this feature but also aid in the continuous improvement and development of the entire weather bot.\n"
                         f"To donate, click on the link below [Donation Link))))]. Any amount is greatly appreciated!"
                         )


aux.print_start_bot("weather")     
bot.polling(none_stop=True)


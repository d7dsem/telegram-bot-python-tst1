import os
from dotenv import load_dotenv
import requests
import json
import random

import telebot
from telebot import types

import libretranslatepy as libre





def get_token(name):
    load_dotenv()
    return os.getenv(name)

token = get_token("TLG_TRANSLATE_BOT_TOKEN")
bot = telebot.TeleBot(token)

def get_preferred_lang_list():
    return ['English', 'Ukranian', 'Spanish', 'Italian', 'French', 'Dutch']

def get_full_lang_list():
    response = requests.get("https://libretranslate.de/languages")
    return [lang["name"] for lang in response.json()]


def generate_inline_buttons_markup(button_names, row_len, prefix=''):
    row_len = min(row_len, 8, len(button_names))
    
    markup = types.InlineKeyboardMarkup(row_width=row_len)
    
    for i in range(0, len(button_names), row_len):
        buttons = [types.InlineKeyboardButton(text=button_text, callback_data=prefix+button_text) for button_text in button_names[i:i+row_len]]
        markup.row(*buttons)
    
    return markup

lang_list_brief = get_preferred_lang_list()

lang_list_full = get_full_lang_list()

greetings = [
    "I am the steadfast defender of your language needs. How may I serve you today?",
    "I am the despoiler of languages, bending them to your will. Speak, and your words shall be transformed!"
]

abaddon_quotes = [
    "Побач свою загибель руська свинособака! Адже Чорний Легіон прийде і розірве твою дупу!",
    "Я - Абаддон Руйнівник! Тремти перед моїм гнівом, який викликаний кацапським гавканням!",
    "Твій кінець близький, бо Хаос вічний, а ти лопочешь на руському і це ганьба!",
    "Воно тобі треба той руський? Зміни мову, читати гидко!",
    "Та шоб ти вдавився! Ну скільки ти ще будеш цією мовою користуватись? Змінюй швидко!",
    "Ти шо москаль?!"
]

help_msg="""- Use /set_lang command to set your native language.
- After setting the language, you can send any text message to the bot for translation.
- Use /clear command to clear the chat.
"""

pending_translations = {}

awaiting_language_change = {}
# Dict for users lang
user_language = dict()
# mapping full language names to their abbreviations
lang_codes = {
    'English': 'en',
    'Arabic': 'ar',
    'Azerbaijani': 'az',
    'Catalan': 'ca',
    'Chinese': 'zh',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'Esperanto': 'eo',
    'Finnish': 'fi',
    'French': 'fr',
    'German': 'de',
    'Greek': 'el',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Hungarian': 'hu',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Russian': 'ru',
    'Slovak': 'sk',
    'Spanish': 'es',
    'Swedish': 'sv',
    'Thai': 'th',
    'Turkish': 'tr',
    'Ukranian': 'uk'
}





def add_to_pending(chat_id, message):
    global pending_translations
    if chat_id in pending_translations:
        pending_translations[chat_id].append(message)
    else:
        pending_translations[chat_id] = [message]

def clear_pending(chat_id):
    global pending_translations
    if chat_id in pending_translations:
        del pending_translations[chat_id]

def detect_lang(text):
    try:
        detect_response = requests.post("https://libretranslate.de/detect", data={"q": text})
        detect_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError("Network or server error occurred during language detection.") from e

    try:
        json_response = detect_response.json()
    except json.JSONDecodeError as e:
        raise ValueError("Response could not be decoded as JSON.") from e

    if not json_response or "language" not in json_response[0]:
        raise ValueError("No language detection result from server.")

    return json_response[0]["language"]

def get_user_lang_code(lang):
    global lang_codes
    return lang_codes.get(lang, "en")  # Default to English if the language is not found.
 
def translate(text, target, source="auto"):
    try:
        lang_code = get_user_lang_code(target)
        response = requests.post("https://libretranslate.de/translate", data={
            "q": text,
            "source": source,
            "target": lang_code,
        })

        response.raise_for_status()  # это вызовет ошибку HTTPError, если статус ответа 4XX или 5XX

        data = response.json()

        # Проверка на наличие поля 'translatedText' в ответе
        if "translatedText" in data:
            return data["translatedText"]
        else:
            return "Translation error: The response from the server did not contain translated text."

    except requests.exceptions.RequestException as e:
        # это может произойти, если сервер не доступен, запрос прерван и т. д.
        error_info = ""
        try:
            error_info = response.json()  # попытаться получить дополнительные сведения об ошибке
        except ValueError:
            pass
        return f"Network error: {str(e)}" + f"response: {error_info}" if error_info != "" else ""
    except ValueError:
        # это может произойти, если ответ сервера не может быть декодирован как JSON
        return "Response error: Unable to decode the response from the server."
    except Exception as e:
        # на случай, если произойдет какая-то другая ошибка
        return f"Unexpected error: {str(e)}"


def set_user_lang(chat_id, lang):
    if lang in lang_list_full:
        user_language[chat_id] = lang
        send_message(chat_id, f'Current language - {lang}')
        awaiting_language_change[chat_id] = False
    else:
        awaiting_language_change[chat_id] = True
        send_message(chat_id, 'Language not recognized. Please choose a language from the list below:')
        send_message(chat_id, ', '.join(lang_list_full))
        
def send_message(chat_id, text, *args, **kwargs):
    # Проверка языка пользователя перед отправкой сообщения
    if chat_id in user_language and user_language[chat_id] == "Russian":
        bot.send_message(chat_id, random.choice(abaddon_quotes), *args, **kwargs)

    bot.send_message(chat_id, text, *args, **kwargs)
    
# Определение функций для команд /start, /clear и /set_lang.
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.chat.id
    if user_id not in user_language:
        send_message(user_id, f"{random.choice(greetings)}\n\n{help_msg}")
        set_lang_command(message)
    else:
        send_message(user_id, f"{random.choice(greetings)}\n\nCurrent language - {user_language[user_id]}\n\n{help_msg}")

@bot.message_handler(commands=['clear'])
def clear_command(message):
    send_message(message.chat.id, "The chat clearing feature is not implemented yet.",reply_markup=types.ReplyKeyboardRemove())




@bot.message_handler(commands=['dbg'])
def debug_info_command(message):
    user_id = message.chat.id
    if user_id in user_language:
        lang = f"{user_language[user_id]}"
    else:
        lang = "not set"

    if user_id in pending_translations:
        queue_length = len(pending_translations[user_id])
    else:
        queue_length = 0

    debug_info = f"Language: {lang}\nPending translations: {queue_length}"
    send_message(user_id, debug_info)

button_prefixes = {
    "set_lang" : "set_lang_",
    "all_lang" : 'lang_all_',
}

@bot.message_handler(commands=['set_lang'])
def set_lang_command(message):
    markup = generate_inline_buttons_markup(lang_list_brief, 3, button_prefixes["set_lang"])
    markup.add(types.InlineKeyboardButton('List of all', callback_data=button_prefixes["all_lang"]))
    user_id = message.chat.id
    if user_id in user_language:
        send_message(user_id, f'Current language - {user_language[user_id]}\nSelect new one:', reply_markup=markup)
    else:
        send_message(user_id, "Select your native language:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    if call.data.startswith('set_lang_'):
        # If the button data starts with 'lang_', set the user's native language
        new_lang = call.data[len(button_prefixes["set_lang"]):]
        user_language[call.message.chat.id] = new_lang
        send_message(call.message.chat.id, f'Native language - {new_lang}')
        global pending_translations
        if chat_id in pending_translations:
            for text in pending_translations[chat_id]:
                translated_text = translate(text, user_language[chat_id])
                send_message(chat_id, translated_text)
            clear_pending(chat_id)
            
    elif call.data == 'lang_all_':
        # If the 'List of all' button is pressed, send the full list of languages
        send_message(chat_id, ', '.join(lang_list_full))
        awaiting_language_change[chat_id] = True


# def add_kb_buttons_for_set_lang_command(message):
#     markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
#     for lang in lang_list_brief:
#         markup.add(types.KeyboardButton(lang))
#     markup.add(types.KeyboardButton('List of all'))
#     send_message(message.chat.id, "Select your native language:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text

    if awaiting_language_change.get(chat_id):            
        set_user_lang(chat_id, text)
        return

    if chat_id in user_language:
        translated_text = translate(message.text, text)
        send_message(chat_id, translated_text)
    else:
        add_to_pending(chat_id, text)
        set_lang_command(message)

if __name__ == "__main__":
    print(f"Bot Starts (use LibreTranslate)")    
    try:
        # Запуск бота
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error (on top level):")    
        print(e)



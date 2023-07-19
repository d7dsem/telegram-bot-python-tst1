import auxilary as aux
import ctypes
import telebot
from telebot import types
import openai
import webbrowser



kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


prefered_model = "gpt-3.5-turbo"
engine="text-davinci-002"

token_gpt = aux.get_gpt_token()
token_tlg = aux.get_tlg_translator_token()


google_translte_url = "https://translate.google.com/?sl=auto&tl=ru&op=translate"
youtube_url="https://www.youtube.com"

openai.api_key = token_gpt

bot = telebot.TeleBot(token_tlg)


### Commands hendlers examples
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Goto google translate')
    btn2 = types.KeyboardButton('Input text')
    btn3 = types.KeyboardButton('Foo')
    
    markup.row(btn3)
    markup.row(btn2,btn1)

    bot.send_message(message.chat.id,"Hello there!",reply_markup=markup)
    bot.register_next_step_handler(message, on_kb_button_click)

def on_kb_button_click(message):
    if message.text == 'Goto google translate':
        webbrowser.open(google_translte_url)
    elif message.text == 'Input text':
        pass
    elif message.text == 'Foo':
        pass


@bot.message_handler(commands=['hello'])
def gretting(message):
    bot.send_message(message.chat.id,f'Hellow <b>{message.from_user.first_name}</b>!',parse_mode="html")

@bot.message_handler(commands=['c'])
def curr_handler(message):
    bot.send_message(message.chat.id,f'{message}')

@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id,'<b>Help</b> <em><u>information</u></em>',parse_mode="html")

@bot.message_handler(commands=["yt"])
def redirect_youtube(message):
    webbrowser.open(youtube_url)

### Message text handlers examples (htb after command hendlers)
@bot.message_handler()
def handler_input(message):
    if message.text.lower() == "id":
        bot.send_message(message,f"ID: <b>{message.from_user.first_name}</b>\n",parse_mode="html")
    elif message.text.lower() == "g":
        bot.reply_to(message,"???")
    else:       
        input_text = message.text
        markup = types.InlineKeyboardMarkup()
        
        btn1 = types.InlineKeyboardButton('Goto google translate', url=google_translte_url)
        btn2 = types.InlineKeyboardButton('Delete message',callback_data='delete')
        btn3 = types.InlineKeyboardButton('Translate', callback_data='translate')
        
        markup.row(btn1)
        markup.row(btn2,btn3)
        
        bot.reply_to(message,message.text,reply_markup=markup)
        
        
@bot.callback_query_handler(func=lambda callback:True)
def on_button_press(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'translate':
        input_text = callback.message.text
        try:
            # Запрос к OpenAI для перевода текста
            result = openai.Completion.create(engine="text-davinci-002", prompt=f"{input_text}\n\nEnglish translation:", temperature=0.5, max_tokens=60)
            translated_text = result.choices[0].text.strip()
            bot.reply_to(callback.message, translated_text)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            # reply_msg = f"Произошла ошибка при переводе.\n{e}\nПопробуйте еще раз."           
            print(f"Input:       {input_text}")
            bot.reply_to(callback.message,f"Произошла ошибка: {e}") 

if __name__ == "__main__":
    try:
        models = aux.get_aviable_gpt_models(token_gpt)
        aux.show_models(models)

        bot.polling(none_stop=True)
    except Exception as e:
        print(f"{aux.COLOR_ERROR}Error{aux.RESET}: {e}") 

    
import webbrowser
import auxilary as aux
import ctypes
import telebot
from telebot import types




kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

token_tlg = aux.aux.get_token('TLG_TRANSLATE_BOT_TOKEN')

bot = telebot.TeleBot(token_tlg)


### Commands hendlers examples
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,"Hello there!")

@bot.message_handler(commands=['hello'])
def gretting(message):
    bot.send_message(message.chat.id,f'Hellow <b>{message.from_user.first_name}</b>!',parse_mode="html")

### Message text handlers examples (htb after command hendlers)
@bot.message_handler()
def handler_input(message):
    text = message.text    
    try:
        translator = aux.get_translator()
        eng = aux.translate_text(translator,text,"en")
        ru = aux.translate_text(translator,text,"ru")
        bot.reply_to(message,f"Eng:\n{eng.text}\n\nRu:\n{ru.text}")
    except Exception as e:
        bot.reply_to(message,f"<b>Error</b>: {e}\n",parse_mode="html")
    
       
if __name__ == "__main__":
    try:
        print(f"{aux.COLOR_FG(100,250,100)}Run bot tarnslator{aux.RESET}")
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"{aux.COLOR_ERROR}Error{aux.RESET}: {e}") 

    
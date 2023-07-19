from dotenv import load_dotenv
import os
import ctypes
from googletrans import Translator
import platform

def get_translator():
    return Translator()

def translate_text(translator, text, target_language="en"):    
    return translator.translate(text, dest=target_language)

def enable_virt_terminal():
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def COLOR_FG(r,g,b):
    return f"\033[38;2;{r};{g};{b}m"

def COLOR_BG(r,g,b):
    return f"\033[48;2;{r};{g};{b}m"

RESET="\u001b[0m"
COLOR_INT = COLOR_FG(28, 252, 3)
COLOR_FLOAT=COLOR_FG(44, 187, 212)
COLOR_ERROR="\033[31;1m"
BOLD="\033[1m"
UNDERLINED="\033[4m"

def get_token(name):
    load_dotenv()
    return os.getenv(name)

def get_tlg_translator_token():
    return get_token('TLG_TRANSLATE_BOT_TOKEN')

def init_virt_terminal():
    if platform.system() == 'Windows':
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)





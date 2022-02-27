from dotenv import load_dotenv
from os import getenv
from edamino import Bot

load_dotenv('.env')

EMAIL = getenv('email')
PASSWORD = getenv('password')

bot = Bot(email=EMAIL, password=PASSWORD, prefix="/", proxy="http://127.0.0.1:8888")

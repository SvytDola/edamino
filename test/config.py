from dotenv import load_dotenv
from os import getenv
from edamino import Bot, api

load_dotenv('.env')

EMAIL = getenv('email')
PASSWORD = getenv('password')

bot = Bot(email=EMAIL, password=PASSWORD, prefix="/")

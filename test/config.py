from dotenv import load_dotenv
from os import getenv

load_dotenv('.env')


EMAIL = getenv('email')
PASSWORD = getenv('password')

# config.py
from os import getenv
from dotenv import load_dotenv
load_dotenv()

API_KEY = getenv('API_KEY', None)

# use the key
# print(API_KEY)
# config.py
from os import getenv

SECRET_KEY = getenv('API_KEY', None)

# use the key
print(SECRET_KEY)
import os
import time

from instafame.core import PhotoUploader

from dotenv import load_dotenv

# Made to load env variables in .env
load_dotenv()

# login credentials
insta_username = os.getenv('USERNAME')
insta_password = os.getenv('PASSWORD')

bot = PhotoUploader(insta_username, insta_password)
bot.login()
time.sleep(3)
bot.upload_pic()

import re
from flask import Flask, request
import telegram
from newsbot.bot import start_bot

app = Flask(__name__)

if __name__ == '__main__':
  start_bot()
  # app.run()
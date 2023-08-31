import requests
from newsbot.credentials import rapid_api_key
from telegram.ext import ContextTypes
from telegram import Update
from newsbot.bot_common import send_message_with_inline_button

import asyncio

global last_news_coin_desk
global last_news_coin_telegraph

global RAPID_TOKEN
RAPID_TOKEN = rapid_api_key



async def fetch_static_new_first_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
  # coin_desk
  coin_desk_first = get_coin_desk_first_time()
  for item in coin_desk_first:
    await send_message_with_inline_button(update, context, item['title'])

  # coin_telegraph
  coin_telegraph_first = get_coin_telegraph_first_time()
  for item in coin_telegraph_first:
    await send_message_with_inline_button(update, context, item['title'])

async def fetch_static_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
  while True:
    new_news_coin_desk = fetch_news_coin_desk()
    if new_news_coin_desk:
      for item in new_news_coin_desk:
        await send_message_with_inline_button(update, context, item['title'])

    new_news_coin_tele_graph = fetch_news_coin_telegraph()
    if new_news_coin_tele_graph:
      for item in new_news_coin_tele_graph:
        await send_message_with_inline_button(update, context, item['title'])

    await asyncio.sleep(60)

def coin_desk():
  url = "https://crypto-news16.p.rapidapi.com/news/coindesk"

  headers = {
    "X-RapidAPI-Key": RAPID_TOKEN,
    "X-RapidAPI-Host": "crypto-news16.p.rapidapi.com"
  }

  response = requests.get(url, headers=headers)

  return response.json()

def coin_telegraph():
  url = "https://crypto-news16.p.rapidapi.com/news/cointelegraph"

  headers = {
    "X-RapidAPI-Key": RAPID_TOKEN,
    "X-RapidAPI-Host": "crypto-news16.p.rapidapi.com"
  }

  response = requests.get(url, headers=headers)

  return response.json()

def get_coin_desk_first_time():
  data = coin_desk()
  first_list = data[:5]
  globals()['last_news_coin_desk'] = first_list[0]
  return first_list[::-1]

def get_coin_telegraph_first_time():
  data = coin_telegraph()
  first_list = data[:5]
  globals()['last_news_coin_telegraph'] = first_list[0]
  return first_list[::-1]

def fetch_news_coin_desk():
  data = coin_desk()
  index = 0

  if globals()['last_news_coin_desk'] in list(data):
    index = list(data).index(globals()['last_news_coin_desk'])

  if index == 0:
    return []

  new_list = data[:index]
  globals()['last_news_coin_desk'] = new_list[0]

  return new_list[::-1]

def fetch_news_coin_telegraph():
  data = coin_telegraph()
  index = 0

  if globals()['last_news_coin_telegraph'] in list(data):
    index = list(data).index(globals()['last_news_coin_telegraph'])

  if index == 0:
    return []

  new_list = data[:index]
  globals()['last_news_coin_telegraph'] = new_list[0]

  return new_list[::-1]
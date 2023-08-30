import requests

global last_news_coin_desk
global last_news_coin_telegraph

def coin_desk():
  url = "https://crypto-news16.p.rapidapi.com/news/coindesk"

  headers = {
    "X-RapidAPI-Key": "2d443ebce2msh7b1663696b075ddp14ae2djsn6aae24db547b",
    "X-RapidAPI-Host": "crypto-news16.p.rapidapi.com"
  }

  response = requests.get(url, headers=headers)

  return response.json()

def coin_telegraph():
  url = "https://crypto-news16.p.rapidapi.com/news/cointelegraph"

  headers = {
    "X-RapidAPI-Key": "2d443ebce2msh7b1663696b075ddp14ae2djsn6aae24db547b",
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
  index = list(data).index(globals()['last_news_coin_desk'])
  if index == 0:
    return []
  new_list = data[:index]
  globals()['last_news_coin_desk'] = new_list[0]

  return new_list[::-1]

def fetch_news_coin_telegraph():
  data = coin_telegraph()
  index = list(data).index(globals()['last_news_coin_telegraph'])
  if index == 0:
    return []
  new_list = data[:index]
  globals()['last_news_coin_telegraph'] = new_list[0]

  return new_list[::-1]
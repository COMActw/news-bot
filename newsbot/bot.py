from telegram.ext import ApplicationBuilder, InlineQueryHandler, CommandHandler, ContextTypes
import logging
from newsbot.credentials import bot_token
from newsbot.static_source import *
import time
import threading
from pycoingecko import CoinGeckoAPI
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update



cg = CoinGeckoAPI()
global TOKEN
global COIN_LIST
TOKEN = bot_token

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start_bot():
  globals()['COIN_LIST'] = cg.get_coins_list()

  application = ApplicationBuilder().token(TOKEN).build()

  application.add_handler(CommandHandler('start', start))
  application.add_handler(InlineQueryHandler(button))
  application.add_handler(CommandHandler('hello', test))

  application.run_polling(allowed_updates=Update.ALL_TYPES)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text(f'Hello {update.effective_user.last_name}')

  # coin_desk
  coin_desk_first = get_coin_desk_first_time()
  for item in coin_desk_first:
    symbol = ''
    ticker_text = symbol_look_up(item['title'])

    keyboard = []
    if ticker_text:
      symbol = ticker_text
      keyboard = [
          [
              InlineKeyboardButton("Long 📈 " + symbol, callback_data="1"),
              InlineKeyboardButton("Short 📉 " + symbol, callback_data="2"),
          ]
      ]

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else InlineKeyboardMarkup([])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text= symbol + item['title'],
        reply_markup=reply_markup
    )
  # coin_telegraph
  coin_telegraph_first = get_coin_telegraph_first_time()
  for item in coin_telegraph_first:
    symbol = ''
    ticker_text = symbol_look_up(item['title'])

    keyboard = []
    if ticker_text:
      symbol = ticker_text
      keyboard = [
          [
              InlineKeyboardButton("Long 📈 " + symbol, callback_data="1"),
              InlineKeyboardButton("Short 📉 " + symbol, callback_data="2"),
          ]
      ]

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else InlineKeyboardMarkup([])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text= symbol + item['title'],
        reply_markup = reply_markup
    )

  await fetch_static_source(update, context)

async def fetch_static_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
  while True:
    new_news_coin_desk = fetch_news_coin_desk()
    if new_news_coin_desk:
      for item in new_news_coin_desk:
        symbol = ''
        ticker_text = symbol_look_up(item['title'])
        if ticker_text:
          symbol = ticker_text
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text= symbol + item['title']
        )

    new_news_coin_tele_graph = fetch_news_coin_telegraph()
    if new_news_coin_tele_graph:
      for item in new_news_coin_tele_graph:
        symbol = ''
        ticker_text = symbol_look_up(item['title'])
        if ticker_text:
          symbol = ticker_text
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text= symbol + item['title']
        )
    time.sleep(60)

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text(f'Hello {update.effective_user.last_name}')

def symbol_look_up(text):
  words = text.split(' ')
  for item in globals()['COIN_LIST']:
    for word in words:
      lower_word = word.lower()
      lower_name = item['name'].lower()
      if lower_word == lower_name:
        ticker_text = '[' + item['symbol'].upper() + 'USDT' + ']  '
        return ticker_text
      
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Parses the CallbackQuery and updates the message text."""
  query = update.callback_query
  breakpoint()
  # CallbackQueries need to be answered, even if no notification to the user is needed
  # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
  await query.answer()

  await query.edit_message_text(text=f"Selected option: {query.data}")

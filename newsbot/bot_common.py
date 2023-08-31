from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
from pycoingecko import CoinGeckoAPI


cg = CoinGeckoAPI()

globals()['COIN_LIST'] = cg.get_coins_list()


async def send_message_with_inline_button(update: Update, context: ContextTypes.DEFAULT_TYPE, title):
  symbol = ''
  keyboard = []
  ticker_text = symbol_look_up(title)

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
      text= symbol + title,
      reply_markup = reply_markup
  )

def symbol_look_up(text):
  words = text.split(' ')
  for item in globals()['COIN_LIST']:
    for word in words:
      lower_word = word.lower()
      lower_name = item['name'].lower()
      if lower_word == lower_name:
        ticker_text = '[' + item['symbol'].upper() + 'USDT' + ']  '
        return ticker_text
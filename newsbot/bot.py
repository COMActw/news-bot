from flask import Flask, jsonify
import logging
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
from telegram import Update
from newsbot.bot_common import send_message_with_inline_button

from newsbot.credentials import bot_token
from newsbot.static_source import fetch_static_new_first_time, fetch_static_source
from newsbot.dynamic_source import start_dynamic_source
import asyncio
import nest_asyncio

nest_asyncio.apply()

global TOKEN
global COIN_LIST
TOKEN = bot_token

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

update_global = Update
context_global = ContextTypes.DEFAULT_TYPE


application = ApplicationBuilder().token(TOKEN).build()

def start_bot():
  global update_global
  global context_global
  update_global = Update
  context_global = ContextTypes.DEFAULT_TYPE

  # handler
  application.add_handler(CallbackQueryHandler(button))
  application.add_handler(CommandHandler('start', start))

  # start pooling => need to change when deploy
  application.run_polling(allowed_updates=Update.ALL_TYPES)


# button handler
async def button(update: update_global, context: context_global) -> None:
  """Parses the CallbackQuery and updates the message text."""
  query = update.callback_query
  # CallbackQueries need to be answered, even if no notification to the user is needed
  # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
  await query.answer()

  await query.edit_message_text(text=f"Selected option: {query.data}")


async def start(update: update_global, context: context_global) -> None:
  await update.message.reply_text(f'Hello {update.effective_user.last_name}')

  # fetch static news first time
  # await fetch_static_new_first_time(update, context)

  # await start_dynamic_source(update, context)

  # # fetch static source by interval
  # asyncio.create_task(fetch_static_source(update, context))

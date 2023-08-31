from telethon import TelegramClient, events, sync
from newsbot.credentials import telegram_api_id, telegram_api_hash
from newsbot.bot_common import send_message_with_inline_button
from telegram.ext import ContextTypes
from telegram import Update

TELEGRAM_API_ID = telegram_api_id
TELEGRAM_API_HASH = telegram_api_hash


telegram_client = TelegramClient('InsightNews', TELEGRAM_API_ID, TELEGRAM_API_HASH)

update_global = Update
context_global = ContextTypes.DEFAULT_TYPE

async def start_telegram_tracking(update: Update, context: ContextTypes.DEFAULT_TYPE):
  global update_global
  global context_global
  update_global = update
  context_global = context

  await telegram_client.start()

@telegram_client.on(events.NewMessage(chats='test_news_coma'))
async def my_event_handler(event):
  await send_message_with_inline_button(update_global, context_global, event.raw_text)


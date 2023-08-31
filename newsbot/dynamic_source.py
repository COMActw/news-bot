
from newsbot.telegram_source import start_telegram_tracking
from telegram.ext import ContextTypes
from telegram import Update


async def start_dynamic_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await start_telegram_tracking(update, context)

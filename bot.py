from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Application, Defaults

import os
token = os.environ['TELEGRAM_TOKEN']

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# async def hw(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(update.effective_chat.id, 'Домашнее задание на **02 ноября 2024**:\n\n1. ОИБ - выполнить практическую работу №8\n2. Ист - подготовить доклад по трём темам')

# def add_handlers(app: Application):
#     start_handler = CommandHandler('start', start)
#     hw_handler = CommandHandler('hw', hw)

#     app.add_handler(start_handler)
#     app.add_handler(hw_handler)

application = ApplicationBuilder().token(token).defaults(Defaults(parse_mode="MarkdownV2")).build()
# add_handlers(application)    
# application.run_polling()
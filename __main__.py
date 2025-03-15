import os

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Defaults, MessageHandler, ApplicationHandlerStop

# Initialising bot
token = os.environ["TELEGRAM_TOKEN"]
bot = ApplicationBuilder().token(token).defaults(Defaults(parse_mode="MarkdownV2")).build()

# Initialising mongo db client
import pymongo

mongodb_url = os.environ["MONGODB_URL"]
mongodb_database = os.environ["MONGODB_DATABASE"]
client = pymongo.MongoClient(mongodb_url)

db = client["mongodb_database"]

Defaults.parse_mode = "MarkdownV2"

mongodb_url = os.environ['MONGODB_URL']

mongo_client = pymongo.MongoClient(mongodb_url)
db = mongo_client["bbbbot"]

userMemory = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = userMemory[context._user_id]

    test_reply_markup = ReplyKeyboardMarkup([
        [ InlineKeyboardButton('Домашнее задание', callback_data='homework'), InlineKeyboardButton('Расписание', callback_data='schedule') ],
        [ InlineKeyboardButton('Настройки', callback_data='settings'), InlineKeyboardButton('Полезные ссылки', callback_data='links') ],
        [ InlineKeyboardButton('Ежедневное сообщение', callback_data='daily') ],
    ])

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Привет, *{user["first_name"]}*\\! Давай начнём работу\\!\nКаждый день я буду высылать тебе расписание и домашнее задание\\.\n\nЕсли у тебя есть какие\\-то вопросы или предложения, будем рады их услышать\\!", reply_markup=test_reply_markup)

async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    if context._user_id not in userMemory:
        userMemory[context._user_id] = db["students"].find_one({"telegram_id": context._user_id})
    if not userMemory[context._user_id]:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"К сожалению тебя нет в нашей базе данных 😕\nЕсли ты считаешь, что это ошибка, обратись к старосте вашей группы\\.")
        raise ApplicationHandlerStop
    
async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(update.effective_chat.id, f"*Пары на сегодня*\n*09:00\\-10:30*\\. Информатика, _пр_\n*10:40\\-12:10*\\. Математический анализ, _лк_")
    await context.bot.send_message(update.effective_chat.id, f"*Домашнее задание на завтра*\n*1*\\. ОИБ \\- Подготовить Отчёт по Практической работе №11")
    await context.bot.send_message(update.effective_chat.id, f"_*Путь в тысячу ли всегда начинается с одного шага\\!*_")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    await update.callback_query.answer()
    
bot.add_handlers({
    0: [MessageHandler(None, auth)],
    1: [CommandHandler('start', start), CommandHandler('daily', daily)],
    2: []
})

bot.run_polling()
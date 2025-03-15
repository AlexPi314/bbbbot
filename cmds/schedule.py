from datetime import datetime, timedelta

import enum

from telegram import Update
from telegram.ext import ContextTypes

class ClassType(enum.Enum):
    lecture = "лк"
    seminar = "пр"
    independent = "сам"
    lab = "лаб"

class Campus(enum.Enum):
    V78 = "В-78"
    V86 = "В-86"
    S20 = "С-20"
    MP1 = "МП-1"

class Class:
    def __init__(self, subject: str, type: ClassType, campus: Campus, room: str, teacher: str = None, subgroup: int = None):
        self.subject = subject
        self.type = type
        self.campus = campus
        self.room = room
        self.teacher = teacher
        self.subgroup = subgroup

schedule = {
    datetime.date(2024, 11, 11): [
        Class("ИстРос", ClassType.seminar, Campus.MP1, "А-400"),
        Class("ИстРос", ClassType.lecture, Campus.MP1, "А-256"),
        Class("ОРГ", ClassType.seminar, Campus.MP1, "А-354"),
        Class("ОРГ", ClassType.seminar, Campus.MP1, "А-354")
    ]
}

def get_schedule(date: datetime.date):
    return schedule[date]

def calculate_class_time(class_number):
    # Define the duration of a class and breaks
    class_duration = timedelta(hours=1, minutes=30)
    short_break = timedelta(minutes=10)
    long_break = timedelta(minutes=30)
    
    # Start time of the first class
    start_time = datetime.strptime("09:00", "%H:%M")
    
    # Calculate the start and end time for the given class number
    for i in range(1, class_number + 1):
        if i > 1:
            if i % 2 == 1:
                # After every 2 classes, add a long break
                start_time += long_break
            else:
                # Add a short break between classes
                start_time += short_break
        
        # Calculate the end time of the current class
        end_time = start_time + class_duration
        
        # If this is the class we're looking for, return the times
        if i == class_number:
            return (start_time.strftime("%H:%M"), end_time.strftime("%H:%M"))
        
        # Update the start time for the next class
        start_time = end_time

async def send_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_schedule = get_schedule(datetime.date(2024, 11, 11))

    print(current_schedule)
    await context.bot.send_message(update.effective_chat.id, f"*Пары на сегодня*\n*09:00\\-10:30*\\. Информатика, _пр_\n*10:40\\-12:10*\\. Математический анализ, _лк_")
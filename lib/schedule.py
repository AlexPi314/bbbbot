import icalendar
from datetime import datetime
from enum import Enum
import requests

# Классы перечислений
class ClassType(Enum):
    lecture = "лк"
    seminar = "пр"
    independent = "сам"
    lab = "лаб"
  
class Campus(Enum):
    V78 = "В-78"
    V86 = "В-86"
    S20 = "С-20"
    MP1 = "МП-1"
    Online = "СДО"
  
# Класс занятия
class Class:
    def __init__(self, subject: str, type: ClassType, campus: Campus, room: str, teacher: str = None, groups: list = None, subgroup: int = None):
        self.subject = subject
        self.type = type
        self.campus = campus
        self.room = room
        self.teacher = teacher
        self.groups = groups
        self.subgroup = subgroup
  
    def __repr__(self):
        if self.campus == None:
            return (f"Class(subject={self.subject}, type={self.type.name}, campus={self.campus}, "
                    f"room={self.room}, teacher={self.teacher}, groups={self.groups}, subgroup={self.subgroup})")
        return (f"Class(subject={self.subject}, type={self.type.name}, campus={self.campus.name}, "
                f"room={self.room}, teacher={self.teacher}, groups={self.groups}, subgroup={self.subgroup})")

def parse_class_type(summary: str) -> ClassType:
    """
    Определяет тип занятия на основе текста в SUMMARY.
    """
    if "лк" in summary.lower():
        return ClassType.lecture
    elif "пр" in summary.lower():
        return ClassType.seminar
    elif "лаб" in summary.lower():
        return ClassType.lab
    elif "сам" in summary.lower():
        return ClassType.independent
    else:
        raise ValueError(f"Не удалось определить тип занятия для: {summary}")
  
def parse_campus_and_room(location: str) -> tuple[Campus, str]:
    """
    Разделяет LOCATION на кампус и аудиторию.
    """
    for campus in Campus:
        if campus.value in location:
            room = location.replace(campus.value, "").strip()
            return campus, room
    raise ValueError(f"Не удалось определить кампус для: {location}")
  
def getSchedule(url: str) -> list[Class]:
    """
    Читает ical файл и формирует список объектов Class.
    """
    classes = []
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return -1
    cal = icalendar.Calendar.from_ical(response.content)

    for event in cal.walk():
        if event.name == 'VEVENT':
            # Извлечение основных полей
            start = event['DTSTART'].dt
            end = event['DTEND'].dt
            teacher = event.get("DESCRIPTION")
            location = event.get("LOCATION")
            subject = event.get("SUMMARY")

            # Проверка наличия основных полей
            if teacher is None and location is None:
                continue

            # Обработка DESCRIPTION (преподаватель, группы)
            try:
                if "Преподаватель: " not in teacher:
                    groups = teacher
                    teacher = None
                else:
                    teacher, groups = teacher.split("\n\nГруппы:\n")
                    teacher = teacher.replace("Преподаватель: ", "").strip()
                groups = groups.split("\n")
                # Delete last if empty
                if groups[-1] == "":
                    groups = groups[:-1]
            except:
                teacher = teacher.replace("Преподаватель: ", "").strip() if teacher else None
                groups = None

            # Определение типа занятия
            class_type = parse_class_type(subject)

            # Деление LOCATION на кампус и аудиторию
            try:
                if location != None:
                    campus, room = parse_campus_and_room(location)
                    if room.find(" ") != -1:
                        room = room[:room.find(" ")].strip()
                else:
                    campus = None
                    room = None
            except ValueError as e:
                print(f"Ошибка при разборе LOCATION: {e}")
                continue

            # Удаление приписки предмета
            subject = subject[subject.find(" "):].strip()
            # Выделение subgroup
            subgroup = None
            if subject.find(" п/г") != -1:
                subgroup = int(subject[subject.find("п/г") - 2].strip())
                subject = subject[:subject.find("п/г") - 2].strip()


            print(subject, class_type, campus, room, teacher, groups, sep="\t")
            # Создание объекта Class
            cls = Class(
                subject=subject,
                type=class_type,
                campus=campus,
                room=room,
                teacher=teacher,
                groups=groups,
                subgroup=subgroup,
            )
            classes.append(cls)

    return classes


def searchSchedule(query:str):
    url = "https://schedule-of.mirea.ru/schedule/api/search?limit=100&match="

    response = requests.get(url + query)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return -1
    
    response = response.json()["data"]

    if len(response) == 0:
        print("No classes found")
        return

    print(type(response))
    for i in response:
        id = i.get("id")
        name = i.get("targetTitle")
        link = i.get("iCalLink")

        print(f"\nID: {id}\tName: {name}\nLink: {link}\n")


if __name__ == "__main__":
    # Получаем расписание
    schedule = getSchedule("https://schedule-of.mirea.ru/schedule/api/ical/1/4730")

    # Вывод
    for cls in schedule:
        print(cls)



### 1. `lunar_calendar.py` (Python)

```python
# lunar_calendar.py — Python версия

import math
import sys
from datetime import datetime, timedelta
from colorama import init, Fore, Style

init(autoreset=True)

def julian_day(year, month, day):
    """Вычисляет юлианский день для даты (григорианский календарь)."""
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045

def moon_phase(year, month, day):
    """Возвращает возраст Луны (в днях) и фазу для заданной даты."""
    # Известное новолуние: 2000-01-06 18:14:00 UTC (JD 2451550.26)
    known_new_moon = 2451550.26  # JD
    target_jd = julian_day(year, month, day) + 0.5  # добавляем 0.5 для полудня
    days_since = target_jd - known_new_moon
    # Синодический месяц 29.53058867 дней
    age = days_since % 29.53058867
    return age

def phase_name(age):
    """Определяет фазу Луны по возрасту."""
    if age < 1.0 or age >= 29.0:
        return "🌑 Новолуние"
    elif 1.0 <= age < 7.0:
        return "🌒 Молодая Луна"
    elif 7.0 <= age < 8.0:
        return "🌓 Первая четверть"
    elif 8.0 <= age < 14.0:
        return "🌔 Растущая Луна"
    elif 14.0 <= age < 15.0:
        return "🌕 Полнолуние"
    elif 15.0 <= age < 21.0:
        return "🌖 Убывающая Луна"
    elif 21.0 <= age < 22.0:
        return "🌗 Последняя четверть"
    else:
        return "🌘 Старая Луна"

def illumination(age):
    """Вычисляет процент освещённости по возрасту."""
    # Используем формулу: освещённость = (1 - cos(2*pi*age/29.53)) / 2
    angle = 2 * math.pi * age / 29.53058867
    illum = (1 - math.cos(angle)) / 2 * 100
    return illum

def draw_moon(age):
    """Рисует ASCII-луну."""
    # Упрощённо: рисуем круг с закрашиванием в зависимости от освещённости
    illum = illumination(age)
    size = 10
    moon = []
    for y in range(size):
        line = ""
        for x in range(size):
            # Определяем, находится ли точка внутри круга
            dx = x - size/2
            dy = y - size/2
            if dx*dx + dy*dy <= (size/2)*(size/2):
                # Освещённая часть зависит от фазы
                # Нормализуем x от -1 до 1
                nx = dx / (size/2)
                # Определяем, освещена ли точка
                # Для фазы > 50% правая часть тёмная, и наоборот
                if illum > 50:
                    # светлая часть слева
                    if nx < 0:
                        line += "██"
                    else:
                        line += "  "
                else:
                    if nx < 0:
                        line += "  "
                    else:
                        line += "██"
            else:
                line += "  "
        moon.append(line)
    return "\n".join(moon)

def main():
    # Парсим дату из аргументов или берём сегодня
    if len(sys.argv) > 1:
        try:
            date_str = sys.argv[1]
            year, month, day = map(int, date_str.split('-'))
            date = datetime(year, month, day)
        except:
            print("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            sys.exit(1)
    else:
        date = datetime.now()
        year, month, day = date.year, date.month, date.day

    age = moon_phase(year, month, day)
    phase = phase_name(age)
    illum = illumination(age)

    print(Fore.CYAN + "🌙 Lunar Calendar (Python)")
    print(f"Дата: {date.strftime('%Y-%m-%d')}")
    print()
    print(Fore.GREEN + f"{phase}")
    print(f"Возраст: {age:.1f} дней")
    print(f"Освещённость: {illum:.1f}%")
    print()
    print(draw_moon(age))

if __name__ == "__main__":
    main()

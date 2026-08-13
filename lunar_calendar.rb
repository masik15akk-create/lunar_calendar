# lunar_calendar.rb — Ruby версия

require 'date'

def julian_day(year, month, day)
  a = (14 - month) / 12
  y = year + 4800 - a
  m = month + 12 * a - 3
  day + (153 * m + 2) / 5 + 365 * y + y / 4 - y / 100 + y / 400 - 32045
end

def moon_phase(year, month, day)
  known_new_moon = 2451550.26
  target_jd = julian_day(year, month, day) + 0.5
  days_since = target_jd - known_new_moon
  age = days_since % 29.53058867
  age += 29.53058867 if age < 0
  age
end

def phase_name(age)
  if age < 1.0 || age >= 29.0
    "🌑 Новолуние"
  elsif age < 7.0
    "🌒 Молодая Луна"
  elsif age < 8.0
    "🌓 Первая четверть"
  elsif age < 14.0
    "🌔 Растущая Луна"
  elsif age < 15.0
    "🌕 Полнолуние"
  elsif age < 21.0
    "🌖 Убывающая Луна"
  elsif age < 22.0
    "🌗 Последняя четверть"
  else
    "🌘 Старая Луна"
  end
end

def illumination(age)
  angle = 2 * Math::PI * age / 29.53058867
  (1 - Math.cos(angle)) / 2 * 100
end

def draw_moon(age)
  illum = illumination(age)
  size = 10
  lines = []
  (0...size).each do |y|
    line = ""
    (0...size).each do |x|
      dx = x - size/2.0
      dy = y - size/2.0
      if dx*dx + dy*dy <= (size/2.0)**2
        nx = dx / (size/2.0)
        if illum > 50
          line << (nx < 0 ? "██" : "  ")
        else
          line << (nx < 0 ? "  " : "██")
        end
      else
        line << "  "
      end
    end
    lines << line
  end
  lines.join("\n")
end

def main
  if ARGV.length > 0
    begin
      year, month, day = ARGV[0].split('-').map(&:to_i)
    rescue
      puts "Неверный формат даты. Используйте ГГГГ-ММ-ДД"
      exit 1
    end
  else
    now = Date.today
    year, month, day = now.year, now.month, now.day
  end

  age = moon_phase(year, month, day)
  phase = phase_name(age)
  illum = illumination(age)

  puts "\e[36m🌙 Lunar Calendar (Ruby)\e[0m"
  puts "Дата: %04d-%02d-%02d" % [year, month, day]
  puts
  puts "\e[32m#{phase}\e[0m"
  puts "Возраст: %.1f дней" % age
  puts "Освещённость: %.1f%%" % illum
  puts
  puts draw_moon(age)
end

main if __FILE__ == $0

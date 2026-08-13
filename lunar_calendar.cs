// lunar_calendar.cs — C# версия

using System;

class LunarCalendar {
    static void Main(string[] args) {
        int year, month, day;
        if (args.Length > 0) {
            try {
                var parts = args[0].Split('-');
                year = int.Parse(parts[0]);
                month = int.Parse(parts[1]);
                day = int.Parse(parts[2]);
            } catch {
                Console.WriteLine("Неверный формат даты. Используйте ГГГГ-ММ-ДД");
                return;
            }
        } else {
            var now = DateTime.Now;
            year = now.Year;
            month = now.Month;
            day = now.Day;
        }

        double age = MoonPhase(year, month, day);
        string phase = PhaseName(age);
        double illum = Illumination(age);

        Console.WriteLine("\u001B[36m🌙 Lunar Calendar (C#)\u001B[0m");
        Console.WriteLine($"Дата: {year:0000}-{month:00}-{day:00}");
        Console.WriteLine();
        Console.WriteLine($"\u001B[32m{phase}\u001B[0m");
        Console.WriteLine($"Возраст: {age:F1} дней");
        Console.WriteLine($"Освещённость: {illum:F1}%");
        Console.WriteLine();
        Console.WriteLine(DrawMoon(age));
    }

    static double JulianDay(int year, int month, int day) {
        int a = (14 - month) / 12;
        int y = year + 4800 - a;
        int m = month + 12 * a - 3;
        return day + (153 * m + 2) / 5 + 365 * y + y / 4 - y / 100 + y / 400 - 32045;
    }

    static double MoonPhase(int year, int month, int day) {
        const double knownNewMoon = 2451550.26;
        double targetJD = JulianDay(year, month, day) + 0.5;
        double daysSince = targetJD - knownNewMoon;
        double age = daysSince % 29.53058867;
        if (age < 0) age += 29.53058867;
        return age;
    }

    static string PhaseName(double age) {
        if (age < 1.0 || age >= 29.0) return "🌑 Новолуние";
        if (age < 7.0) return "🌒 Молодая Луна";
        if (age < 8.0) return "🌓 Первая четверть";
        if (age < 14.0) return "🌔 Растущая Луна";
        if (age < 15.0) return "🌕 Полнолуние";
        if (age < 21.0) return "🌖 Убывающая Луна";
        if (age < 22.0) return "🌗 Последняя четверть";
        return "🌘 Старая Луна";
    }

    static double Illumination(double age) {
        double angle = 2 * Math.PI * age / 29.53058867;
        return (1 - Math.Cos(angle)) / 2 * 100;
    }

    static string DrawMoon(double age) {
        double illum = Illumination(age);
        int size = 10;
        var sb = new System.Text.StringBuilder();
        for (int y = 0; y < size; y++) {
            for (int x = 0; x < size; x++) {
                double dx = x - size/2.0;
                double dy = y - size/2.0;
                if (dx*dx + dy*dy <= (size/2.0)*(size/2.0)) {
                    double nx = dx / (size/2.0);
                    if (illum > 50) {
                        sb.Append(nx < 0 ? "██" : "  ");
                    } else {
                        sb.Append(nx < 0 ? "  " : "██");
                    }
                } else {
                    sb.Append("  ");
                }
            }
            sb.Append("\n");
        }
        return sb.ToString();
    }
}

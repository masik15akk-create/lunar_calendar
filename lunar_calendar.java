// lunar_calendar.java — Java версия

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class lunar_calendar {
    public static void main(String[] args) {
        int year, month, day;
        if (args.length > 0) {
            try {
                String[] parts = args[0].split("-");
                year = Integer.parseInt(parts[0]);
                month = Integer.parseInt(parts[1]);
                day = Integer.parseInt(parts[2]);
            } catch (Exception e) {
                System.out.println("Неверный формат даты. Используйте ГГГГ-ММ-ДД");
                return;
            }
        } else {
            LocalDate now = LocalDate.now();
            year = now.getYear();
            month = now.getMonthValue();
            day = now.getDayOfMonth();
        }

        double age = moonPhase(year, month, day);
        String phase = phaseName(age);
        double illum = illumination(age);

        System.out.println("\u001B[36m🌙 Lunar Calendar (Java)\u001B[0m");
        System.out.printf("Дата: %04d-%02d-%02d%n", year, month, day);
        System.out.println();
        System.out.println("\u001B[32m" + phase + "\u001B[0m");
        System.out.printf("Возраст: %.1f дней%n", age);
        System.out.printf("Освещённость: %.1f%%%n", illum);
        System.out.println();
        System.out.println(drawMoon(age));
    }

    private static double julianDay(int year, int month, int day) {
        int a = (14 - month) / 12;
        int y = year + 4800 - a;
        int m = month + 12 * a - 3;
        return day + (153 * m + 2) / 5 + 365 * y + y / 4 - y / 100 + y / 400 - 32045;
    }

    private static double moonPhase(int year, int month, int day) {
        double knownNewMoon = 2451550.26;
        double targetJD = julianDay(year, month, day) + 0.5;
        double daysSince = targetJD - knownNewMoon;
        double age = daysSince % 29.53058867;
        if (age < 0) age += 29.53058867;
        return age;
    }

    private static String phaseName(double age) {
        if (age < 1.0 || age >= 29.0) return "🌑 Новолуние";
        if (age < 7.0) return "🌒 Молодая Луна";
        if (age < 8.0) return "🌓 Первая четверть";
        if (age < 14.0) return "🌔 Растущая Луна";
        if (age < 15.0) return "🌕 Полнолуние";
        if (age < 21.0) return "🌖 Убывающая Луна";
        if (age < 22.0) return "🌗 Последняя четверть";
        return "🌘 Старая Луна";
    }

    private static double illumination(double age) {
        double angle = 2 * Math.PI * age / 29.53058867;
        return (1 - Math.cos(angle)) / 2 * 100;
    }

    private static String drawMoon(double age) {
        double illum = illumination(age);
        int size = 10;
        StringBuilder sb = new StringBuilder();
        for (int y = 0; y < size; y++) {
            for (int x = 0; x < size; x++) {
                double dx = x - size/2.0;
                double dy = y - size/2.0;
                if (dx*dx + dy*dy <= (size/2.0)*(size/2.0)) {
                    double nx = dx / (size/2.0);
                    if (illum > 50) {
                        sb.append(nx < 0 ? "██" : "  ");
                    } else {
                        sb.append(nx < 0 ? "  " : "██");
                    }
                } else {
                    sb.append("  ");
                }
            }
            sb.append("\n");
        }
        return sb.toString();
    }
}

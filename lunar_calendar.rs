// lunar_calendar.rs — Rust версия

use std::env;
use std::f64::consts::PI;
use chrono::{Local, NaiveDate};

fn julian_day(year: i32, month: u32, day: u32) -> f64 {
    let a = (14 - month as i32) / 12;
    let y = year + 4800 - a;
    let m = month as i32 + 12 * a - 3;
    (day as i32 + (153 * m + 2) / 5 + 365 * y + y / 4 - y / 100 + y / 400 - 32045) as f64
}

fn moon_phase(year: i32, month: u32, day: u32) -> f64 {
    let known_new_moon = 2451550.26;
    let target_jd = julian_day(year, month, day) + 0.5;
    let days_since = target_jd - known_new_moon;
    let mut age = days_since % 29.53058867;
    if age < 0.0 { age += 29.53058867; }
    age
}

fn phase_name(age: f64) -> &'static str {
    if age < 1.0 || age >= 29.0 { "🌑 Новолуние" }
    else if age < 7.0 { "🌒 Молодая Луна" }
    else if age < 8.0 { "🌓 Первая четверть" }
    else if age < 14.0 { "🌔 Растущая Луна" }
    else if age < 15.0 { "🌕 Полнолуние" }
    else if age < 21.0 { "🌖 Убывающая Луна" }
    else if age < 22.0 { "🌗 Последняя четверть" }
    else { "🌘 Старая Луна" }
}

fn illumination(age: f64) -> f64 {
    let angle = 2.0 * PI * age / 29.53058867;
    (1.0 - angle.cos()) / 2.0 * 100.0
}

fn draw_moon(age: f64) -> String {
    let illum = illumination(age);
    let size = 10;
    let mut lines = Vec::new();
    for y in 0..size {
        let mut line = String::new();
        for x in 0..size {
            let dx = x as f64 - size as f64 / 2.0;
            let dy = y as f64 - size as f64 / 2.0;
            if dx*dx + dy*dy <= (size as f64 / 2.0).powi(2) {
                let nx = dx / (size as f64 / 2.0);
                if illum > 50.0 {
                    line.push_str(if nx < 0.0 { "██" } else { "  " });
                } else {
                    line.push_str(if nx < 0.0 { "  " } else { "██" });
                }
            } else {
                line.push_str("  ");
            }
        }
        lines.push(line);
    }
    lines.join("\n")
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let (year, month, day) = if args.len() > 1 {
        let parts: Vec<&str> = args[1].split('-').collect();
        if parts.len() == 3 {
            let y = parts[0].parse().unwrap();
            let m = parts[1].parse().unwrap();
            let d = parts[2].parse().unwrap();
            (y, m, d)
        } else {
            eprintln!("Неверный формат даты. Используйте ГГГГ-ММ-ДД");
            std::process::exit(1);
        }
    } else {
        let now = Local::now().naive_local().date();
        (now.year(), now.month(), now.day())
    };

    let age = moon_phase(year, month, day);
    let phase = phase_name(age);
    let illum = illumination(age);

    println!("\x1b[36m🌙 Lunar Calendar (Rust)\x1b[0m");
    println!("Дата: {:04}-{:02}-{:02}", year, month, day);
    println!();
    println!("\x1b[32m{}\x1b[0m", phase);
    println!("Возраст: {:.1} дней", age);
    println!("Освещённость: {:.1}%", illum);
    println!();
    println!("{}", draw_moon(age));
}

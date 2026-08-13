// lunar_calendar.js — JavaScript версия

const readline = require('readline');

function julianDay(year, month, day) {
    let a = Math.floor((14 - month) / 12);
    let y = year + 4800 - a;
    let m = month + 12 * a - 3;
    return day + Math.floor((153 * m + 2) / 5) + 365 * y + Math.floor(y / 4) - Math.floor(y / 100) + Math.floor(y / 400) - 32045;
}

function moonPhase(year, month, day) {
    const knownNewMoon = 2451550.26;
    let targetJD = julianDay(year, month, day) + 0.5;
    let daysSince = targetJD - knownNewMoon;
    let age = daysSince % 29.53058867;
    if (age < 0) age += 29.53058867;
    return age;
}

function phaseName(age) {
    if (age < 1.0 || age >= 29.0) return "🌑 Новолуние";
    if (age < 7.0) return "🌒 Молодая Луна";
    if (age < 8.0) return "🌓 Первая четверть";
    if (age < 14.0) return "🌔 Растущая Луна";
    if (age < 15.0) return "🌕 Полнолуние";
    if (age < 21.0) return "🌖 Убывающая Луна";
    if (age < 22.0) return "🌗 Последняя четверть";
    return "🌘 Старая Луна";
}

function illumination(age) {
    let angle = 2 * Math.PI * age / 29.53058867;
    return (1 - Math.cos(angle)) / 2 * 100;
}

function drawMoon(age) {
    let illum = illumination(age);
    let size = 10;
    let lines = [];
    for (let y = 0; y < size; y++) {
        let line = '';
        for (let x = 0; x < size; x++) {
            let dx = x - size/2;
            let dy = y - size/2;
            if (dx*dx + dy*dy <= (size/2)*(size/2)) {
                let nx = dx / (size/2);
                if (illum > 50) {
                    line += nx < 0 ? '██' : '  ';
                } else {
                    line += nx < 0 ? '  ' : '██';
                }
            } else {
                line += '  ';
            }
        }
        lines.push(line);
    }
    return lines.join('\n');
}

function main() {
    const args = process.argv.slice(2);
    let year, month, day;
    if (args.length > 0) {
        let parts = args[0].split('-');
        if (parts.length === 3) {
            year = parseInt(parts[0]);
            month = parseInt(parts[1]);
            day = parseInt(parts[2]);
        } else {
            console.log('Неверный формат даты. Используйте ГГГГ-ММ-ДД');
            process.exit(1);
        }
    } else {
        let now = new Date();
        year = now.getFullYear();
        month = now.getMonth() + 1;
        day = now.getDate();
    }

    let age = moonPhase(year, month, day);
    let phase = phaseName(age);
    let illum = illumination(age);

    console.log('\x1b[36m🌙 Lunar Calendar (JavaScript)\x1b[0m');
    console.log(`Дата: ${year}-${String(month).padStart(2,'0')}-${String(day).padStart(2,'0')}`);
    console.log();
    console.log(`\x1b[32m${phase}\x1b[0m`);
    console.log(`Возраст: ${age.toFixed(1)} дней`);
    console.log(`Освещённость: ${illum.toFixed(1)}%`);
    console.log();
    console.log(drawMoon(age));
}

if (require.main === module) main();

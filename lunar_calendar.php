<?php
// lunar_calendar.php — PHP версия

function julianDay($year, $month, $day) {
    $a = (int)((14 - $month) / 12);
    $y = $year + 4800 - $a;
    $m = $month + 12 * $a - 3;
    return $day + (int)((153 * $m + 2) / 5) + 365 * $y + (int)($y / 4) - (int)($y / 100) + (int)($y / 400) - 32045;
}

function moonPhase($year, $month, $day) {
    $knownNewMoon = 2451550.26;
    $targetJD = julianDay($year, $month, $day) + 0.5;
    $daysSince = $targetJD - $knownNewMoon;
    $age = fmod($daysSince, 29.53058867);
    if ($age < 0) $age += 29.53058867;
    return $age;
}

function phaseName($age) {
    if ($age < 1.0 || $age >= 29.0) return "🌑 Новолуние";
    if ($age < 7.0) return "🌒 Молодая Луна";
    if ($age < 8.0) return "🌓 Первая четверть";
    if ($age < 14.0) return "🌔 Растущая Луна";
    if ($age < 15.0) return "🌕 Полнолуние";
    if ($age < 21.0) return "🌖 Убывающая Луна";
    if ($age < 22.0) return "🌗 Последняя четверть";
    return "🌘 Старая Луна";
}

function illumination($age) {
    $angle = 2 * M_PI * $age / 29.53058867;
    return (1 - cos($angle)) / 2 * 100;
}

function drawMoon($age) {
    $illum = illumination($age);
    $size = 10;
    $lines = [];
    for ($y = 0; $y < $size; $y++) {
        $line = "";
        for ($x = 0; $x < $size; $x++) {
            $dx = $x - $size/2;
            $dy = $y - $size/2;
            if ($dx*$dx + $dy*$dy <= ($size/2)*($size/2)) {
                $nx = $dx / ($size/2);
                if ($illum > 50) {
                    $line .= ($nx < 0) ? "██" : "  ";
                } else {
                    $line .= ($nx < 0) ? "  " : "██";
                }
            } else {
                $line .= "  ";
            }
        }
        $lines[] = $line;
    }
    return implode("\n", $lines);
}

$year = $month = $day = null;
if ($argc > 1) {
    $parts = explode('-', $argv[1]);
    if (count($parts) == 3) {
        $year = (int)$parts[0];
        $month = (int)$parts[1];
        $day = (int)$parts[2];
    } else {
        echo "Неверный формат даты. Используйте ГГГГ-ММ-ДД\n";
        exit(1);
    }
} else {
    $now = new DateTime();
    $year = (int)$now->format('Y');
    $month = (int)$now->format('m');
    $day = (int)$now->format('d');
}

$age = moonPhase($year, $month, $day);
$phase = phaseName($age);
$illum = illumination($age);

echo "\033[36m🌙 Lunar Calendar (PHP)\033[0m\n";
printf("Дата: %04d-%02d-%02d\n", $year, $month, $day);
echo "\n";
echo "\033[32m$phase\033[0m\n";
printf("Возраст: %.1f дней\n", $age);
printf("Освещённость: %.1f%%\n", $illum);
echo "\n";
echo drawMoon($age);
?>

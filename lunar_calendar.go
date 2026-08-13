// lunar_calendar.go — Go версия

package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
	"time"
)

func julianDay(year, month, day int) float64 {
	a := (14 - month) / 12
	y := year + 4800 - a
	m := month + 12*a - 3
	return float64(day + (153*m+2)/5 + 365*y + y/4 - y/100 + y/400 - 32045)
}

func moonPhase(year, month, day int) float64 {
	knownNewMoon := 2451550.26
	targetJD := julianDay(year, month, day) + 0.5
	daysSince := targetJD - knownNewMoon
	age := math.Mod(daysSince, 29.53058867)
	if age < 0 {
		age += 29.53058867
	}
	return age
}

func phaseName(age float64) string {
	switch {
	case age < 1.0 || age >= 29.0:
		return "🌑 Новолуние"
	case age < 7.0:
		return "🌒 Молодая Луна"
	case age < 8.0:
		return "🌓 Первая четверть"
	case age < 14.0:
		return "🌔 Растущая Луна"
	case age < 15.0:
		return "🌕 Полнолуние"
	case age < 21.0:
		return "🌖 Убывающая Луна"
	case age < 22.0:
		return "🌗 Последняя четверть"
	default:
		return "🌘 Старая Луна"
	}
}

func illumination(age float64) float64 {
	angle := 2 * math.Pi * age / 29.53058867
	return (1 - math.Cos(angle)) / 2 * 100
}

func drawMoon(age float64) string {
	illum := illumination(age)
	size := 10
	var lines []string
	for y := 0; y < size; y++ {
		line := ""
		for x := 0; x < size; x++ {
			dx := float64(x - size/2)
			dy := float64(y - size/2)
			if dx*dx+dy*dy <= float64(size/2*size/2) {
				nx := dx / (float64(size) / 2)
				if illum > 50 {
					if nx < 0 {
						line += "██"
					} else {
						line += "  "
					}
				} else {
					if nx < 0 {
						line += "  "
					} else {
						line += "██"
					}
				}
			} else {
				line += "  "
			}
		}
		lines = append(lines, line)
	}
	return strings.Join(lines, "\n")
}

func main() {
	var year, month, day int
	if len(os.Args) > 1 {
		parts := strings.Split(os.Args[1], "-")
		if len(parts) == 3 {
			year, _ = strconv.Atoi(parts[0])
			month, _ = strconv.Atoi(parts[1])
			day, _ = strconv.Atoi(parts[2])
		} else {
			fmt.Println("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
			os.Exit(1)
		}
	} else {
		now := time.Now()
		year, month, day = now.Year(), int(now.Month()), now.Day()
	}

	age := moonPhase(year, month, day)
	phase := phaseName(age)
	illum := illumination(age)

	fmt.Println("\x1b[36m🌙 Lunar Calendar (Go)\x1b[0m")
	fmt.Printf("Дата: %04d-%02d-%02d\n", year, month, day)
	fmt.Println()
	fmt.Printf("\x1b[32m%s\x1b[0m\n", phase)
	fmt.Printf("Возраст: %.1f дней\n", age)
	fmt.Printf("Освещённость: %.1f%%\n", illum)
	fmt.Println()
	fmt.Println(drawMoon(age))
}

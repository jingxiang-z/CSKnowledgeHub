package main

import (
	"fmt"
	"strconv"
	"strings"
)

const threshold = 75

type result struct {
	score  int
	passed bool
}

// parseRecord parses "<name> <score>"; ok is false for malformed records
// (wrong field count, non-numeric score, or negative score).
func parseRecord(record string) (name string, score int, ok bool) {
	fields := strings.Fields(record)
	if len(fields) != 2 {
		return "", 0, false
	}
	score, err := strconv.Atoi(fields[1])
	if err != nil || score < 0 {
		return "", 0, false
	}
	return fields[0], score, true
}

func transform(records []string) (map[string]result, int) {
	results := make(map[string]result)
	skippedCount := 0
	for _, record := range records {
		name, score, ok := parseRecord(record)
		if !ok {
			skippedCount++
			continue
		}
		results[name] = result{score: score, passed: score >= threshold}
	}
	return results, skippedCount
}

func report(results map[string]result, skippedCount int) {
	if len(results) == 0 {
		fmt.Println("No valid records.")
		return
	}

	topName := ""
	topScore := -1
	for name, r := range results {
		status := "FAIL"
		if r.passed {
			status = "PASS"
		}
		fmt.Printf("%s: %d — %s\n", name, r.score, status)
		if r.score > topScore {
			topScore = r.score
			topName = name
		}
	}
	fmt.Printf("Skipped %d malformed record(s).\n", skippedCount)
	fmt.Printf("Highest score: %s with %d\n", topName, topScore)
}

func main() {
	records := []string{
		"Alice 92",
		"Bob abc",
		"Charlie 45",
		"",
		"David 78",
	}

	results, skippedCount := transform(records)
	report(results, skippedCount)
}

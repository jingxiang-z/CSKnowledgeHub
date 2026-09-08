THRESHOLD = 85

RECORDS = [
    "Alice 92",
    "Bob abc",
    "Charlie 45",
    "",
    "David 78"
]

def transform(records):
    results = {}
    skipped_count = 0
    for record in records:
        try:
            name, score = record.split(" ")
            score = int(score)
            if score < 0:
                skipped_count += 1
                continue
        except ValueError:
            skipped_count += 1
            continue
        status = score >= THRESHOLD
        results[name] = (score, status)
    return results, skipped_count

def report(results, skipped_count):
    if len(results) == 0:
        print("No valid records.")
        return
    maxscore, maxname = 0, ""
    for name, (score, status) in results.items():
        if score >= maxscore:
            maxscore = score
            maxname = name
        status_str = "PASS" if status else "FAIL"
        print(f"{name}: {score} — {status_str}")
    print(f"Skipped {skipped_count} malformed record(s).")
    print(f"Highest score: {maxname} with {maxscore}")

if __name__ == "__main__":
    results, skipped_count = transform(RECORDS)
    report(results, skipped_count)
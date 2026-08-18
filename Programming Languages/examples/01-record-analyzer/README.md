# Record Analyzer

Implement a score reporter for records containing a student name and numeric score.

## Input / Output

**Input:** Records provided as lines of text (hardcoded list or stdin), each in the format:

```
<Name> <Score>
```

Example input:
```
Alice 92
Bob abc
Charlie 45

David 78
```

**Output:** For each valid record, print the student name, score, and pass/fail classification.
After processing all records, print the count of skipped (malformed) records and the top scorer.

Example output (pass threshold = 60):
```
Alice: 92 — PASS
Charlie: 45 — FAIL
David: 78 — PASS
Skipped 2 malformed record(s).
Highest score: Alice with 92
```

A record is **malformed** if the score field is missing, non-numeric, or negative; blank lines are also skipped.
If there are no valid records, print a message such as `"No valid records."` instead of a top scorer.

## Requirements

- Store the input, score, threshold, and result in appropriately typed variables; use named constants where appropriate.
- Convert text input to a number and reject invalid input rather than silently using a value.
- Store valid scores in a collection appropriate for name-to-score lookup.
- Classify every valid score as pass or fail, skip malformed records, and count skipped records.
- Put parsing/validation and score reporting in separate, focused functions.
- Print the highest valid score and its student; define the behavior for empty input.

## Done when

The program deliberately uses branches, loops, and early exit or `continue`; it has no duplicated score logic and reports ordinary invalid input without crashing.

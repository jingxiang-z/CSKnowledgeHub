# Record Analyzer

Implement a score reporter for records containing a student name and numeric score.

## Requirements

- Store the input, score, threshold, and result in appropriately typed variables; use named constants where appropriate.
- Convert text input to a number and reject invalid input rather than silently using a value.
- Store valid scores in a collection appropriate for name-to-score lookup.
- Classify every valid score as pass or fail, skip malformed records, and count skipped records.
- Put parsing/validation and score reporting in separate, focused functions.
- Print the highest valid score and its student; define the behavior for empty input.

## Done when

The program deliberately uses branches, loops, and early exit or `continue`; it has no duplicated score logic and reports ordinary invalid input without crashing.

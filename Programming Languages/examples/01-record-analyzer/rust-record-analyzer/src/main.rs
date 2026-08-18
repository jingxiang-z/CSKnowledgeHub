use std::collections::HashMap;

const THRESHOLD: i32 = 75;

/// Parses "<name> <score>"; returns None for malformed records
/// (wrong field count, non-numeric score, or negative score).
fn parse_record(record: &str) -> Option<(String, i32)> {
    let fields: Vec<&str> = record.split_whitespace().collect();
    if fields.len() != 2 {
        return None;
    }
    let score: i32 = match fields[1].parse() {
        Ok(n) if n >= 0 => n,
        _ => return None,
    };
    Some((fields[0].to_string(), score))
}

fn transform(records: &[&str]) -> (HashMap<String, (i32, bool)>, i32) {
    let mut results: HashMap<String, (i32, bool)> = HashMap::new();
    let mut skipped_count = 0;
    for record in records {
        match parse_record(record) {
            Some((name, score)) => {
                let passed = score >= THRESHOLD;
                results.insert(name, (score, passed));
            }
            None => skipped_count += 1,
        }
    }
    (results, skipped_count)
}

fn report(results: &HashMap<String, (i32, bool)>, skipped_count: i32) {
    if results.is_empty() {
        println!("No valid records.");
        return;
    }

    let mut top_name = "";
    let mut top_score = -1;
    for (name, (score, passed)) in results {
        let status = if *passed { "PASS" } else { "FAIL" };
        println!("{}: {} — {}", name, score, status);
        if *score > top_score {
            top_score = *score;
            top_name = name;
        }
    }
    println!("Skipped {} malformed record(s).", skipped_count);
    println!("Highest score: {} with {}", top_name, top_score);
}

fn main() {
    let records = vec![
        "Alice 92",
        "Bob abc",
        "Charlie 45",
        "",
        "David 78",
    ];

    let (results, skipped_count) = transform(&records);
    report(&results, skipped_count);
}

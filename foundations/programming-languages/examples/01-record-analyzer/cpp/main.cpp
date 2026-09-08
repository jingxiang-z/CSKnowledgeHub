#include <iostream>
#include <string>
#include <unordered_map>
#include <tuple>
#include <sstream>
#include <vector>

const int THRESHOLD = 75;

using ResultMap = std::unordered_map<std::string, std::tuple<int, bool>>;

// Parses "<name> <score>"; returns false (leaving name/score untouched) if malformed.
bool parse_record(const std::string& record, std::string& name, int& score) {
    std::string score_text;
    std::istringstream stream(record);
    if (!(stream >> name >> score_text)) {
        return false;
    }
    try {
        score = std::stoi(score_text);
    } catch (const std::exception&) {
        return false;
    }
    return score >= 0;
}

ResultMap transform(const std::vector<std::string>& records, int& skipped_count) {
    ResultMap results;
    skipped_count = 0;
    for (const auto& record : records) {
        std::string name;
        int score;
        if (!parse_record(record, name, score)) {
            skipped_count++;
            continue;
        }
        bool passed = score >= THRESHOLD;
        results[name] = {score, passed};
    }
    return results;
}

void report(const ResultMap& results, int skipped_count) {
    if (results.empty()) {
        std::cout << "No valid records.\n";
        return;
    }

    std::string top_name;
    int top_score = -1;
    for (const auto& [name, entry] : results) {
        int score = std::get<0>(entry);
        bool passed = std::get<1>(entry);
        std::cout << name << ": " << score << " — " << (passed ? "PASS" : "FAIL") << "\n";
        if (score > top_score) {
            top_score = score;
            top_name = name;
        }
    }
    std::cout << "Skipped " << skipped_count << " malformed record(s).\n";
    std::cout << "Highest score: " << top_name << " with " << top_score << "\n";
}

int main() {
    std::vector<std::string> records = {
        "Alice 92",
        "Bob abc",
        "Charlie 45",
        "",
        "David 78"
    };

    int skipped_count = 0;
    ResultMap results = transform(records, skipped_count);
    report(results, skipped_count);

    return 0;
}
from datetime import datetime, timezone
import hashlib
from collections import Counter
import re

def current_utc_iso():
   
    return datetime.now(timezone.utc).isoformat()

def analyze_string(value: str):
    value = value.strip()
    sha = hashlib.sha256(value.encode()).hexdigest()

    properties = {
        "length": len(value),
        "is_palindrome": value.lower() == value[::-1].lower(),
        "unique_characters": len(set(value)),
        "word_count": len(value.split()),
        "sha256_hash": sha,
        "character_frequency_map": dict(Counter(value)),
    }

    return sha, properties



def parse_natural_language_query(query: str):
    query = query.lower().strip()
    filters = {}

    # Example 1: "single word palindromic strings"
    if "palindromic" in query:
        filters["is_palindrome"] = True

    # Example 2: "single word"
    if "single word" in query:
        filters["word_count"] = 1
    elif "two words" in query or "double word" in query:
        filters["word_count"] = 2

    # Example 3: "longer than X characters"
    match = re.search(r"longer than (\d+) characters", query)
    if match:
        filters["min_length"] = int(match.group(1)) + 1

    # Example 4: "containing the letter X"
    match = re.search(r"containing the letter (\w)", query)
    if match:
        filters["contains_character"] = match.group(1)

    # Example 5: "contain the first vowel"
    if "contain the first vowel" in query:
        filters["contains_character"] = "a"

    # If we found nothing meaningful
    if not filters:
        return None

    return filters

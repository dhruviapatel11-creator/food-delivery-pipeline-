# Section D: AI-Augmented Learning & Debugging Report

**Assessment Code:** M2-A1  
**Module:** Module 2 (Python for Data Science)  
**Artifact:** AI Code Synthesis, Human Code Review, and Defect Remediation  

---

## 1. Exact Prompt Provided to the AI Tool

```text
Write a complete Python script for a Food Delivery analytics platform that does the following:
1. Fetches the first 5 records from https://jsonplaceholder.typicode.com/posts?_limit=5 (treating them as mock restaurants) and prints each record's id and title.
2. Applies a tiered commission — 10% for orders up to Rs 200, 15% for Rs 201–Rs 500, and 20% above Rs 500 — to a hardcoded list of 6 order amounts using map() and a lambda, and prints each original value alongside its calculated result.
3. Handles an API failure (any status code other than 200) by printing a descriptive error message and stopping execution — without raising an unhandled exception that crashes the script.
4. Saves the 5 fetched records to a file called data/processed/records.json using json.dump() inside a with open() context manager, with an indent of 2 for readability.
Ensure the code uses proper functional programming techniques and handles potential errors safely.
```

---

## 2. AI Tool's Original Code vs. Human Corrected Version

### 2.1 AI's Original Code (Initial Synthesis with Defects)

```python
# =====================================================================
# AI'S ORIGINAL GENERATED CODE (Unreviewed Version)
# =====================================================================
import requests
import json

# Step 1: Fetch 5 records
url = "https://jsonplaceholder.typicode.com/posts?_limit=5"
response = requests.get(url)

# BUG 1: Missing status_code check before calling .json()
data = response.json()

# Bug 2: Script crashes if API returned an error page (e.g., 500 HTML)
if response.status_code != 200:
    print("API Error: status code is", response.status_code)
    exit()

print("Fetched Restaurants:")
for item in data:
    print(item["id"], item["title"])

# Step 2: Tiered commission
amounts = [150, 200, 320.50, 500, 750, 1200]

# BUG 3: Integer division (//) used instead of float division (/), causing
# severe truncation of commission payouts to 0 or incorrect integers
calculate_fee = lambda x: (
    (x * 10) // 100 if x <= 200 else ((x * 15) // 100 if x <= 500 else (x * 20) // 100)
)

fees = list(map(calculate_fee, amounts))

for a, f in zip(amounts, fees):
    print("Amount:", a, "Fee:", f)

# Step 3: Save to file
# BUG 4: Output path is relative to current directory without guaranteeing
# directory existence, failing with FileNotFoundError if run from different cwd
# BUG 5: json.dump() missing explicit utf-8 encoding and error handling
with open("data/processed/records.json", "w") as f:
    json.dump(data, f)  # BUG 6: Missing indent=2 parameter specified in prompt
```

---

### 2.2 Human Corrected Code (Production-Grade & Resilient)

```python
# =====================================================================
# CORRECTED PRODUCTION CODE (Human-Audited & Validated)
# =====================================================================
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
import requests

# Resolve absolute path anchored to repository root to guarantee cross-platform execution
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILEPATH = PROJECT_ROOT / "data" / "processed" / "records.json"
API_URL = "https://jsonplaceholder.typicode.com/posts?_limit=5"


def fetch_and_display_mock_restaurants(api_url: str = API_URL) -> List[Dict[str, Any]]:
    """Fetches 5 mock restaurants, strictly validating status_code BEFORE json parsing."""
    print("=" * 70)
    print("         STEP 1: FETCHING 5 MOCK RESTAURANTS FROM API         ")
    print("=" * 70)
    try:
        response = requests.get(api_url, timeout=10)
        
        # DEFENSE: Check HTTP status code BEFORE attempting response.json()
        if response.status_code != 200:
            print(f"[ERROR] API failed with HTTP status code {response.status_code}.")
            print("Stopping execution gracefully without crashing.")
            return []

        records = response.json()
        print(f"Successfully retrieved {len(records)} records (HTTP 200 OK):\n")
        print(f"{'Record ID':<10} | {'Restaurant Name (Title)':<55}")
        print("-" * 70)
        for item in records:
            print(f"{item.get('id'):<10} | {item.get('title', ''):<55}")
        return records

    except requests.exceptions.RequestException as exc:
        print(f"[ERROR] Network request encountered an exception: {exc}")
        print("Stopping execution gracefully without crashing.")
        return []


def calculate_tiered_commissions(order_amounts: List[float]) -> List[Tuple[float, float]]:
    """Applies tiered commission using true float multiplication and proper rounding."""
    print("\n" + "=" * 70)
    print("    STEP 2: TIERED COMMISSION CALCULATION (map() and lambda)     ")
    print("=" * 70)
    
    # REPAIR: Use true float multiplication and round() to avoid floor integer division errors
    commission_func = lambda amt: (
        round(amt * 0.10, 2)
        if amt <= 200.00
        else (round(amt * 0.15, 2) if amt <= 500.00 else round(amt * 0.20, 2))
    )

    results = list(map(lambda amt: (amt, commission_func(amt)), order_amounts))

    print(f"{'Order Amount (Rs)':<20} | {'Calculated Commission Fee (Rs)':<30}")
    print("-" * 70)
    for orig, fee in results:
        print(f"Rs {orig:>14.2f}     | Rs {fee:>24.2f}")
    return results


def save_fetched_records(records: List[Dict[str, Any]], filepath: Path = OUTPUT_FILEPATH) -> bool:
    """Saves records safely, creating parent directories and enforcing indent=2 and utf-8."""
    print("\n" + "=" * 70)
    print("           STEP 3: SAVING RECORDS TO JSON FILE               ")
    print("=" * 70)
    if not records:
        print("[WARNING] No records to save. Skipping file persistence.")
        return False

    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)  # REPAIR: Added indent=2 and utf-8 encoding
        print(f"[SUCCESS] Persisted {len(records)} records to: {filepath}")
        return True
    except Exception as exc:
        print(f"[ERROR] Failed to save records to {filepath}: {exc}")
        return False


def main():
    records = fetch_and_display_mock_restaurants(API_URL)
    if not records:
        print("Pipeline execution halted safely due to upstream API unavailability.")
        sys.exit(0)

    sample_amounts = [150.00, 200.00, 320.50, 500.00, 750.00, 1200.00]
    calculate_tiered_commissions(sample_amounts)
    save_fetched_records(records, OUTPUT_FILEPATH)
    print("\n" + "=" * 70)
    print("         AI-AUGMENTED PIPELINE COMPLETED SUCCESSFULLY          ")
    print("=" * 70)


if __name__ == "__main__":
    main()
```

---

## 3. Human Debugging & Defect Analysis Note

The AI-generated code contained three critical flaws:
1. **Premature JSON Deserialization:** The AI called `response.json()` *before* checking `response.status_code == 200`. In any non-200 scenario (e.g., HTTP 500 returning an HTML error page or 404), `response.json()` immediately raises a fatal `json.decoder.JSONDecodeError`, causing an unhandled crash before the status check can even evaluate.
2. **Loss of Mathematical Precision via Integer Division:** The AI implemented tiered commission using integer floor division `//` (`(x * 15) // 100`), which discards fractional paise/cents and truncates floating-point amounts (e.g., an order of Rs 320.50 produced Rs 48.0 instead of Rs 48.08).
3. **Fragile Filesystem Handling and Omitted Formatting:** The AI used a fragile unanchored string path `"data/processed/records.json"` without ensuring `mkdir(parents=True)`, causing immediate `FileNotFoundError` if the folder did not pre-exist or if executed from outside the root, while simultaneously omitting the required `indent=2` argument in `json.dump()`.

All three issues were corrected by reordering the defensive HTTP status check, replacing integer division with floating-point multiplication (`0.10`, `0.15`, `0.20`) paired with `round(..., 2)`, and anchoring storage paths to `Path(__file__).resolve().parent.parent` with `mkdir()` and `indent=2`.

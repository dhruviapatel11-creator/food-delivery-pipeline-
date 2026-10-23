"""
Food Delivery AI-Augmented Pipeline (Section D)
Assessment: M2-A1 | Stack: Python for Data Science

Fetches mock restaurant records from REST API with status verification,
calculates tiered commissions over hardcoded order amounts using map() and a lambda,
handles non-200 responses safely without crashing, and saves formatted records to disk.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
import requests

# Derive platform-independent path to data/processed/records.json
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILEPATH = PROJECT_ROOT / "data" / "processed" / "records.json"
API_URL = "https://jsonplaceholder.typicode.com/posts?_limit=5"


def fetch_and_display_mock_restaurants(api_url: str = API_URL) -> List[Dict[str, Any]]:
    """
    Fetches the first 5 records from the REST API, validates HTTP 200 status code,
    and prints each record's id and title.
    
    Returns:
        List of fetched dictionary records, or empty list on failure.
    """
    print("=" * 70)
    print("         STEP 1: FETCHING 5 MOCK RESTAURANTS FROM API         ")
    print("=" * 70)
    print(f"Target Endpoint: {api_url}")

    try:
        response = requests.get(api_url, timeout=10)

        # Defensive HTTP status code verification before invoking .json()
        if response.status_code != 200:
            print(f"[ERROR] API failed with HTTP status code {response.status_code}.")
            print("Stopping execution gracefully without crashing.")
            return []

        records = response.json()
        print(f"\nSuccessfully retrieved {len(records)} records (HTTP 200 OK):\n")
        print(f"{'Record ID':<10} | {'Restaurant Name (Title)':<55}")
        print("-" * 70)
        for item in records:
            item_id = item.get("id")
            title = item.get("title", "")
            print(f"{item_id:<10} | {title:<55}")

        return records

    except requests.exceptions.RequestException as exc:
        print(f"[ERROR] Network request encountered an exception: {exc}")
        print("Stopping execution gracefully without crashing.")
        return []


def calculate_tiered_commissions(
    order_amounts: List[float],
) -> List[Tuple[float, float]]:
    """
    Applies tiered commissions to a list of order amounts using map() and lambda:
    - 10% for orders up to Rs 200 (<= 200)
    - 15% for Rs 201 - Rs 500 (200.01 to 500)
    - 20% above Rs 500 (> 500)
    
    Returns:
        List of tuples: (original_amount, calculated_fee)
    """
    print("\n" + "=" * 70)
    print("    STEP 2: TIERED COMMISSION CALCULATION (map() and lambda)     ")
    print("=" * 70)
    print("Tiers: <= Rs 200 (10%) | Rs 201 - Rs 500 (15%) | > Rs 500 (20%)\n")

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


def save_fetched_records(
    records: List[Dict[str, Any]], filepath: Path = OUTPUT_FILEPATH
) -> bool:
    """
    Saves the fetched records to data/processed/records.json using json.dump()
    with indent=2 inside a with open() context manager.
    
    Returns:
        True if save succeeded, False otherwise.
    """
    print("\n" + "=" * 70)
    print("           STEP 3: SAVING RECORDS TO JSON FILE               ")
    print("=" * 70)

    if not records:
        print("[WARNING] No records to save. Skipping file persistence.")
        return False

    try:
        # Guarantee destination directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

        print(f"[SUCCESS] Persisted {len(records)} records to:")
        print(f" -> {filepath}")
        return True

    except Exception as exc:
        print(f"[ERROR] Failed to save records to {filepath}: {exc}")
        return False


def main():
    # 1. Fetch 5 mock records
    records = fetch_and_display_mock_restaurants(API_URL)
    if not records:
        print("\nPipeline execution halted due to upstream API unavailability.")
        sys.exit(0)

    # 2. Hardcoded list of 6 order amounts
    sample_amounts = [150.00, 200.00, 320.50, 500.00, 750.00, 1200.00]
    calculate_tiered_commissions(sample_amounts)

    # 3. Save records to data/processed/records.json
    save_fetched_records(records, OUTPUT_FILEPATH)

    print("\n" + "=" * 70)
    print("         AI-AUGMENTED PIPELINE COMPLETED SUCCESSFULLY          ")
    print("=" * 70)


if __name__ == "__main__":
    main()

"""
Food Delivery Record Cleaning Script (Task 2)
Assessment: M2-A1 | Stack: Python for Data Science

This script cleans and validates raw restaurant names and associated order amounts
using string manipulation methods, type casting, and conditional logic.
"""

from typing import List, Tuple, Optional


def clean_restaurant_name(raw_name: str) -> Optional[str]:
    """
    Cleans a raw restaurant name by stripping whitespace, standardizing casing,
    and replacing irregular characters. Returns None if invalid or empty.
    
    Args:
        raw_name: The raw string entry for a restaurant name.
        
    Returns:
        The cleaned name in Title Case, or None if the record is invalid.
    """
    if not isinstance(raw_name, str):
        return None

    # Step 1: Strip leading and trailing whitespace
    stripped = raw_name.strip()

    # Step 2: Validate against empty or purely numeric entries
    if not stripped or stripped.isnumeric():
        return None

    # Step 3: Replace excessive internal punctuation/symbols if needed
    cleaned = stripped.replace("_", " ").replace("-", " ")
    
    # Step 4: Normalize casing to Title Case
    cleaned = cleaned.title()

    # Remove duplicate internal spaces
    cleaned = " ".join(cleaned.split())

    return cleaned


def parse_currency_amount(amount_str: str) -> Optional[float]:
    """
    Converts a raw currency string into a clean float value.
    Handles prefixes like 'Rs', 'INR', '$', commas, and whitespace.
    
    Args:
        amount_str: Raw amount representation (e.g., 'Rs 150', '200.50').
        
    Returns:
        Float value of the amount, or None if conversion fails.
    """
    if not isinstance(amount_str, str):
        try:
            return float(amount_str)
        except (ValueError, TypeError):
            return None

    # Strip currency symbols and whitespace
    sanitized = amount_str.strip().upper()
    sanitized = sanitized.replace("RS", "").replace("INR", "").replace("$", "")
    sanitized = sanitized.replace(",", "").strip()

    try:
        return float(sanitized)
    except ValueError:
        return None


def run_cleaning_pipeline(
    raw_restaurants: List[str], raw_amounts: List[str]
) -> Tuple[List[Tuple[str, float]], int, int, float]:
    """
    Processes paired restaurant names and amounts, calculating running totals
    and reporting invalid entries.
    
    Returns:
        Tuple containing:
        - List of (cleaned_name, amount) tuples
        - Valid record count
        - Skipped record count
        - Total valid amount
    """
    print("=" * 70)
    print("       FOOD DELIVERY RECORD CLEANING PIPELINE - EXECUTION LOG       ")
    print("=" * 70)

    valid_records: List[Tuple[str, float]] = []
    skipped_count = 0
    running_total = 0.0

    total_entries = max(len(raw_restaurants), len(raw_amounts))

    for idx in range(total_entries):
        raw_name = raw_restaurants[idx] if idx < len(raw_restaurants) else ""
        raw_amt = raw_amounts[idx] if idx < len(raw_amounts) else "0.0"

        # Cleaning restaurant name
        cleaned_name = clean_restaurant_name(raw_name)

        if cleaned_name is None:
            skipped_count += 1
            reason = "Empty string" if not str(raw_name).strip() else "Purely numeric / invalid format"
            print(f"[SKIPPED] Record #{idx + 1:02d}: Raw entry '{raw_name}' rejected ({reason})")
            continue

        # Parsing currency amount
        parsed_amount = parse_currency_amount(raw_amt)
        if parsed_amount is None:
            skipped_count += 1
            print(f"[SKIPPED] Record #{idx + 1:02d}: Name '{cleaned_name}' but invalid amount '{raw_amt}'")
            continue

        # Running total calculation
        running_total += parsed_amount
        valid_records.append((cleaned_name, parsed_amount))

        print(
            f"[VALID]   Record #{idx + 1:02d}: '{cleaned_name:<25}' | "
            f"Amount: Rs {parsed_amount:>8.2f} | Running Total: Rs {running_total:>9.2f}"
        )

    print("-" * 70)
    print("                     PIPELINE EXECUTION SUMMARY                      ")
    print("-" * 70)
    print(f"Total Records Processed : {total_entries}")
    print(f"Total Valid Records     : {len(valid_records)}")
    print(f"Total Skipped Records   : {skipped_count}")
    print(f"Final Total Order Value : Rs {running_total:.2f}")
    print("=" * 70)

    return valid_records, len(valid_records), skipped_count, running_total


def main():
    # Hardcoded dataset with at least 8 raw restaurant names, inconsistent casing,
    # extra whitespace, and at least 2 invalid/empty entries (total 10 items)
    raw_restaurants = [
        "  tandoori nights  ",       # Valid (needs trim and title)
        "SPICE BAZAAR",              # Valid (needs title)
        "",                          # Invalid (empty entry)
        "   ",                       # Invalid (whitespace-only entry)
        "123456",                    # Invalid (purely numeric entry)
        "the yellow CHILLI  ",       # Valid (mixed casing, trailing space)
        "royal-punjab",              # Valid (symbol replace, title)
        "   curry_leaf_express   ",  # Valid (symbol replace, title)
        "9876543210",                # Invalid (purely numeric entry)
        "Urban Dhaba",               # Valid (already title case)
    ]

    # Associated list of raw amount strings with currency symbols and formatting
    raw_amounts = [
        "Rs 350.50",
        "Rs 180.00",
        "Rs 0.00",
        "Rs 250.00",
        "Rs 499.00",
        "520.75",
        "Rs 240.00",
        "Rs 610.25",
        "Rs 150.00",
        "Rs 195.50",
    ]

    run_cleaning_pipeline(raw_restaurants, raw_amounts)


if __name__ == "__main__":
    main()

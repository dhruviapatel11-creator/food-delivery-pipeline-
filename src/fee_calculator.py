"""
Food Delivery Fee Calculator with Functional Tools (Task 3)
Assessment: M2-A1 | Stack: Python for Data Science

This script calculates tiered commission fees across delivery order records
using pure named functions, lambda expressions, map(), filter(), and functools.reduce().
"""

import functools
from typing import List, Dict, Any

# Audit threshold for isolating high-value commissions
AUDIT_FEE_THRESHOLD = 50.00


def calculate_tiered_commission(amount: float) -> float:
    """
    Applies a three-tier commission schedule based on order amount:
    - Tier 1: Orders up to Rs 200.00          -> 10% (0.10)
    - Tier 2: Orders from Rs 200.01 to 500.00 -> 15% (0.15)
    - Tier 3: Orders above Rs 500.00          -> 20% (0.20)

    Args:
        amount: Order monetary value.

    Returns:
        Commission fee rounded to 2 decimal places.
    """
    if amount < 0:
        raise ValueError("Order amount cannot be negative.")

    if amount <= 200.00:
        commission_rate = 0.10
    elif amount <= 500.00:
        commission_rate = 0.15
    else:
        commission_rate = 0.20

    return round(amount * commission_rate, 2)


def compute_fees(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Applies calculate_tiered_commission across all records using map() and a lambda.
    
    Args:
        records: List of restaurant dictionary records with 'amount'.
        
    Returns:
        New list of dictionaries with added 'fee' key.
    """
    return list(
        map(
            lambda record: {
                **record,
                "fee": calculate_tiered_commission(record["amount"]),
            },
            records,
        )
    )


def filter_audit_records(
    records_with_fees: List[Dict[str, Any]], threshold: float = AUDIT_FEE_THRESHOLD
) -> List[Dict[str, Any]]:
    """
    Uses filter() with a lambda to isolate records whose fee exceeds the audit threshold.
    
    Args:
        records_with_fees: List of records containing 'fee'.
        threshold: Minimum fee to qualify for audit.
        
    Returns:
        Filtered list of audit-flagged records.
    """
    return list(filter(lambda record: record["fee"] > threshold, records_with_fees))


def generate_audit_report(
    records_with_fees: List[Dict[str, Any]], threshold: float = AUDIT_FEE_THRESHOLD
) -> Dict[str, Any]:
    """
    Generates a structured analytical audit report summarizing high-value commissions.
    
    Args:
        records_with_fees: List of records containing 'fee'.
        threshold: Minimum fee to qualify for audit.
        
    Returns:
        Dictionary containing audit metrics and isolated records.
    """
    flagged = filter_audit_records(records_with_fees, threshold)
    total_flagged_fee = round(sum(r["fee"] for r in flagged), 2)
    max_fee_record = max(flagged, key=lambda r: r["fee"], default=None)
    
    return {
        "threshold": threshold,
        "total_records": len(records_with_fees),
        "flagged_count": len(flagged),
        "flagged_percentage": round((len(flagged) / len(records_with_fees) * 100), 2) if records_with_fees else 0.0,
        "total_flagged_fee": total_flagged_fee,
        "max_fee_record": max_fee_record,
        "flagged_records": flagged,
    }


def calculate_total_commission(records_with_fees: List[Dict[str, Any]]) -> float:
    """
    Uses functools.reduce() in a single expression to aggregate total commission.
    
    Args:
        records_with_fees: List of records containing 'fee'.
        
    Returns:
        Total aggregated commission rounded to 2 decimal places.
    """
    total = functools.reduce(
        lambda accumulator, record: accumulator + record["fee"],
        records_with_fees,
        0.0,
    )
    return round(total, 2)


def run_fee_pipeline(restaurants: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Executes the full functional pipeline and prints formatted summaries.
    """
    print("=" * 75)
    print("      FOOD DELIVERY TIERED COMMISSION CALCULATOR (FUNCTIONAL PIPELINE)     ")
    print("=" * 75)
    print(f"Commission Tiers: <= Rs 200 (10%) | Rs 201 - Rs 500 (15%) | > Rs 500 (20%)")
    print(f"Audit Threshold : Commission Fee > Rs {AUDIT_FEE_THRESHOLD:.2f}")
    print("-" * 75)

    # 1. Map: Calculate fees using named function and lambda
    records_with_fees = compute_fees(restaurants)

    print("\n[ALL RESTAURANT COMMISSIONS COMPUTED VIA map()]:")
    print(f"{'ID':<6} | {'Restaurant Name':<28} | {'Amount (Rs)':<12} | {'Fee (Rs)':<10}")
    print("-" * 75)
    for r in records_with_fees:
        print(f"{r['id']:<6} | {r['name']:<28} | Rs {r['amount']:>9.2f} | Rs {r['fee']:>7.2f}")

    # 2. Filter: Isolate records where fee exceeds threshold
    audit_records = filter_audit_records(records_with_fees, AUDIT_FEE_THRESHOLD)

    print("\n" + "=" * 75)
    print(f"[AUDIT FLAGGED RECORDS VIA filter()] (Fee > Rs {AUDIT_FEE_THRESHOLD:.2f}):")
    print("-" * 75)
    if audit_records:
        for r in audit_records:
            print(
                f"[AUDIT REQUIRED] ID: {r['id']:<4} | Name: {r['name']:<25} | "
                f"Order: Rs {r['amount']:>7.2f} | Commission Fee: Rs {r['fee']:>6.2f}"
            )
    else:
        print("No records exceeded the audit threshold.")

    # 3. Reduce: Compute total fee across all records in a single expression
    total_fee = calculate_total_commission(records_with_fees)

    print("\n" + "=" * 75)
    print("                       FINANCIAL SUMMARY METRICS                            ")
    print("=" * 75)
    print(f"Total Restaurant Records Processed : {len(records_with_fees)}")
    print(f"Total Records Flagged for Audit     : {len(audit_records)}")
    print(f"Total Commission Payout (reduce)    : Rs {total_fee:.2f}")
    print("=" * 75)

    return {
        "records_with_fees": records_with_fees,
        "audit_records": audit_records,
        "total_fee": total_fee,
    }


def main():
    # Hardcoded dataset with at least 6 restaurant dictionaries
    restaurants_data = [
        {"id": 101, "name": "Tandoori Nights", "amount": 180.00},  # Tier 1 (10% -> 18.00)
        {"id": 102, "name": "Spice Bazaar", "amount": 200.00},     # Tier 1 boundary (10% -> 20.00)
        {"id": 103, "name": "The Yellow Chilli", "amount": 350.00},# Tier 2 (15% -> 52.50, Audit > 50)
        {"id": 104, "name": "Royal Punjab", "amount": 500.00},     # Tier 2 boundary (15% -> 75.00, Audit > 50)
        {"id": 105, "name": "Curry Leaf Express", "amount": 650.00},# Tier 3 (20% -> 130.00, Audit > 50)
        {"id": 106, "name": "Urban Dhaba", "amount": 820.50},      # Tier 3 (20% -> 164.10, Audit > 50)
        {"id": 107, "name": "Biryani Junction", "amount": 150.00}, # Tier 1 (10% -> 15.00)
    ]

    run_fee_pipeline(restaurants_data)


if __name__ == "__main__":
    main()

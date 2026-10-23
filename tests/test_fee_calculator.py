"""
Unit Tests for Fee Calculator Module (src/fee_calculator.py)
Assessment: M2-A1 | Stack: Python for Data Science
"""

import unittest
from src.fee_calculator import (
    calculate_tiered_commission,
    compute_fees,
    filter_audit_records,
    generate_audit_report,
    calculate_total_commission,
)


class TestFeeCalculator(unittest.TestCase):
    """Test suite for commission calculation, map, filter, and reduce operations."""

    def test_tiered_commission_boundaries(self):
        """Test exact boundary points for Tier 1 (10%), Tier 2 (15%), and Tier 3 (20%)."""
        # Tier 1: <= 200.00 (10%)
        self.assertEqual(calculate_tiered_commission(0.00), 0.00)
        self.assertEqual(calculate_tiered_commission(100.00), 10.00)
        self.assertEqual(calculate_tiered_commission(200.00), 20.00)

        # Tier 2: 200.01 to 500.00 (15%)
        self.assertEqual(calculate_tiered_commission(200.01), 30.00)
        self.assertEqual(calculate_tiered_commission(300.00), 45.00)
        self.assertEqual(calculate_tiered_commission(500.00), 75.00)

        # Tier 3: > 500.00 (20%)
        self.assertEqual(calculate_tiered_commission(500.01), 100.00)
        self.assertEqual(calculate_tiered_commission(600.00), 120.00)
        self.assertEqual(calculate_tiered_commission(1000.00), 200.00)

    def test_negative_amount_raises_error(self):
        """Test that negative amounts raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_tiered_commission(-50.00)

    def test_compute_fees_map(self):
        """Test that compute_fees enriches each dictionary with the correct 'fee'."""
        sample_records = [
            {"id": 1, "name": "Rest A", "amount": 100.00},
            {"id": 2, "name": "Rest B", "amount": 400.00},
            {"id": 3, "name": "Rest C", "amount": 600.00},
        ]
        result = compute_fees(sample_records)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["fee"], 10.00)
        self.assertEqual(result[1]["fee"], 60.00)
        self.assertEqual(result[2]["fee"], 120.00)

    def test_filter_audit_records(self):
        """Test isolating records whose computed fee strictly exceeds the threshold."""
        sample_with_fees = [
            {"id": 1, "name": "Rest A", "amount": 100.00, "fee": 10.00},
            {"id": 2, "name": "Rest B", "amount": 400.00, "fee": 60.00},
            {"id": 3, "name": "Rest C", "amount": 350.00, "fee": 50.00},  # Exactly 50.00
            {"id": 4, "name": "Rest D", "amount": 700.00, "fee": 140.00},
        ]
        audit_50 = filter_audit_records(sample_with_fees, threshold=50.00)
        # Fees > 50.00 should only match id 2 (60.00) and id 4 (140.00)
        self.assertEqual(len(audit_50), 2)
        self.assertEqual([r["id"] for r in audit_50], [2, 4])

    def test_generate_audit_report(self):
        """Test structured analytical audit report generation."""
        sample_with_fees = [
            {"id": 1, "name": "Rest A", "amount": 100.00, "fee": 10.00},
            {"id": 2, "name": "Rest B", "amount": 400.00, "fee": 60.00},
            {"id": 3, "name": "Rest C", "amount": 700.00, "fee": 140.00},
        ]
        report = generate_audit_report(sample_with_fees, threshold=50.00)
        self.assertEqual(report["total_records"], 3)
        self.assertEqual(report["flagged_count"], 2)
        self.assertEqual(report["flagged_percentage"], 66.67)
        self.assertEqual(report["total_flagged_fee"], 200.00)
        self.assertEqual(report["max_fee_record"]["id"], 3)

    def test_calculate_total_commission_reduce(self):
        """Test total fee reduction across all records in a single expression."""
        sample_with_fees = [
            {"id": 1, "fee": 15.50},
            {"id": 2, "fee": 45.25},
            {"id": 3, "fee": 60.00},
        ]
        total = calculate_total_commission(sample_with_fees)
        self.assertEqual(total, 120.75)

    def test_empty_list_reduce(self):
        """Test calculate_total_commission with an empty list."""
        self.assertEqual(calculate_total_commission([]), 0.0)


if __name__ == "__main__":
    unittest.main()

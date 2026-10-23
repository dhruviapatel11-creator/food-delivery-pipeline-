"""
Unit Tests for Record Cleaning Module (src/record_cleaning.py)
Assessment: M2-A1 | Stack: Python for Data Science
"""

import unittest
from src.record_cleaning import (
    clean_restaurant_name,
    parse_currency_amount,
    run_cleaning_pipeline,
)


class TestRecordCleaning(unittest.TestCase):
    """Test suite for restaurant name and currency amount cleaning functions."""

    def test_clean_restaurant_name_valid(self):
        """Test valid names with whitespace, irregular casing, and hyphens/underscores."""
        self.assertEqual(clean_restaurant_name("  tandoori nights  "), "Tandoori Nights")
        self.assertEqual(clean_restaurant_name("SPICE BAZAAR"), "Spice Bazaar")
        self.assertEqual(clean_restaurant_name("the yellow CHILLI  "), "The Yellow Chilli")
        self.assertEqual(clean_restaurant_name("royal-punjab"), "Royal Punjab")
        self.assertEqual(clean_restaurant_name("curry_leaf_express"), "Curry Leaf Express")

    def test_clean_restaurant_name_invalid_and_empty(self):
        """Test that empty, whitespace-only, and purely numeric entries return None."""
        self.assertIsNone(clean_restaurant_name(""))
        self.assertIsNone(clean_restaurant_name("    "))
        self.assertIsNone(clean_restaurant_name("123456"))
        self.assertIsNone(clean_restaurant_name("9876543210"))
        self.assertIsNone(clean_restaurant_name(None))  # Non-string input

    def test_parse_currency_amount_valid(self):
        """Test parsing valid currency strings with various prefixes and formats."""
        self.assertEqual(parse_currency_amount("Rs 150"), 150.0)
        self.assertEqual(parse_currency_amount("Rs 200.50"), 200.50)
        self.assertEqual(parse_currency_amount("350.75"), 350.75)
        self.assertEqual(parse_currency_amount("INR 1,200.00"), 1200.00)
        self.assertEqual(parse_currency_amount("$45.50"), 45.50)
        self.assertEqual(parse_currency_amount(100), 100.0)

    def test_parse_currency_amount_invalid(self):
        """Test parsing invalid or corrupted currency strings."""
        self.assertIsNone(parse_currency_amount("FREE"))
        self.assertIsNone(parse_currency_amount("N/A"))
        self.assertIsNone(parse_currency_amount("Rs ABC"))

    def test_run_cleaning_pipeline(self):
        """Test the integration pipeline calculating running totals and counts."""
        names = ["  tandoori nights  ", "", "1234", "spice bazaar"]
        amounts = ["Rs 150.00", "Rs 200.00", "Rs 50.00", "Rs 250.00"]
        valid_records, valid_count, skipped_count, total = run_cleaning_pipeline(names, amounts)

        self.assertEqual(valid_count, 2)
        self.assertEqual(skipped_count, 2)
        self.assertEqual(total, 400.00)
        self.assertEqual(len(valid_records), 2)
        self.assertEqual(valid_records[0], ("Tandoori Nights", 150.00))
        self.assertEqual(valid_records[1], ("Spice Bazaar", 250.00))


if __name__ == "__main__":
    unittest.main()

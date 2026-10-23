"""
Unit Tests for Record Manager Module (src/record_manager.py)
Assessment: M2-A1 | Stack: Python for Data Science
"""

import io
import sys
import unittest
import tempfile
from pathlib import Path
from src.record_manager import Order, save_records, load_records


class TestRecordManager(unittest.TestCase):
    """Test suite for Order class, JSON persistence, and exception handling."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_filepath = Path(self.temp_dir.name) / "test_records.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_order_creation_and_attributes(self):
        """Test Order class instantiation and default attributes."""
        order = Order(
            order_id=101,
            restaurant_name="  Tandoori Nights  ",
            amount=350.50,
            delivery_time_minutes=30,
            is_delivered=True,
        )
        self.assertEqual(order.order_id, 101)
        self.assertEqual(order.restaurant_name, "Tandoori Nights")  # Stripped
        self.assertEqual(order.amount, 350.50)
        self.assertEqual(order.delivery_time_minutes, 30)
        self.assertTrue(order.is_delivered)

    def test_order_serialization_to_dict(self):
        """Test to_dict serialization method."""
        order = Order(102, "Spice Bazaar", 200.0, 25, is_delivered=False)
        data = order.to_dict()
        expected = {
            "order_id": 102,
            "restaurant_name": "Spice Bazaar",
            "amount": 200.0,
            "delivery_time_minutes": 25,
            "is_delivered": False,
        }
        self.assertEqual(data, expected)

    def test_order_deserialization_from_dict(self):
        """Test from_dict class method reconstructing Order instance."""
        payload = {
            "order_id": 103,
            "restaurant_name": "The Yellow Chilli",
            "amount": 520.75,
            "delivery_time_minutes": 45,
            "is_delivered": True,
        }
        order = Order.from_dict(payload)
        self.assertIsInstance(order, Order)
        self.assertEqual(order.order_id, 103)
        self.assertEqual(order.restaurant_name, "The Yellow Chilli")
        self.assertEqual(order.amount, 520.75)
        self.assertEqual(order.delivery_time_minutes, 45)
        self.assertTrue(order.is_delivered)

    def test_save_and_load_records_roundtrip(self):
        """Test writing orders to JSON and reconstructing them cleanly."""
        orders = [
            Order(1, "Rest 1", 150.0, 20, True),
            Order(2, "Rest 2", 300.0, 35, False),
        ]
        save_success = save_records(orders, self.test_filepath)
        self.assertTrue(save_success)
        self.assertTrue(self.test_filepath.exists())

        loaded_orders = load_records(self.test_filepath)
        self.assertEqual(len(loaded_orders), 2)
        self.assertEqual(loaded_orders[0].order_id, 1)
        self.assertEqual(loaded_orders[0].restaurant_name, "Rest 1")
        self.assertEqual(loaded_orders[1].order_id, 2)
        self.assertEqual(loaded_orders[1].amount, 300.0)

    def test_load_records_file_not_found_handling(self):
        """Test that missing files return an empty list and do not crash."""
        non_existent = Path(self.temp_dir.name) / "does_not_exist.json"
        
        # Capture stdout to verify 'Operation complete' from finally
        captured_output = io.StringIO()
        original_stdout = sys.stdout
        try:
            sys.stdout = captured_output
            result = load_records(non_existent)
        finally:
            sys.stdout = original_stdout

        self.assertEqual(result, [])
        self.assertIn("Operation complete", captured_output.getvalue())

    def test_finally_block_prints_operation_complete_on_save(self):
        """Test that save_records unconditionally prints 'Operation complete'."""
        captured_output = io.StringIO()
        original_stdout = sys.stdout
        try:
            sys.stdout = captured_output
            save_records([], self.test_filepath)
        finally:
            sys.stdout = original_stdout

        self.assertIn("Operation complete", captured_output.getvalue())


if __name__ == "__main__":
    unittest.main()

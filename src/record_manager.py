"""
Food Delivery Record Manager with Persistence (Task 4)
Assessment: M2-A1 | Stack: Python for Data Science

This module implements an object-oriented Order domain model and JSON file persistence
with robust exception handling using try-except-finally blocks.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# Derived relative paths for platform-agnostic persistence
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILEPATH = PROJECT_ROOT / "data" / "processed" / "records.json"


class Order:
    """
    Domain entity representing a food delivery order.
    
    Attributes:
        order_id: Unique identifier for the order (int or str).
        restaurant_name: Name of the originating restaurant (str).
        amount: Order monetary value (float).
        delivery_time_minutes: Estimated or actual delivery duration in minutes (int).
        is_delivered: Delivery fulfillment status flag (bool).
    """

    def __init__(
        self,
        order_id: Any,
        restaurant_name: str,
        amount: float,
        delivery_time_minutes: int,
        is_delivered: bool = False,
    ):
        self.order_id = order_id
        self.restaurant_name = str(restaurant_name).strip()
        self.amount = float(amount)
        self.delivery_time_minutes = int(delivery_time_minutes)
        self.is_delivered = bool(is_delivered)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the Order instance into a standard dictionary for JSON persistence.
        """
        return {
            "order_id": self.order_id,
            "restaurant_name": self.restaurant_name,
            "amount": round(self.amount, 2),
            "delivery_time_minutes": self.delivery_time_minutes,
            "is_delivered": self.is_delivered,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Order":
        """
        Reconstructs an Order instance from a loaded dictionary.
        """
        return cls(
            order_id=data.get("order_id"),
            restaurant_name=data.get("restaurant_name", "Unknown Restaurant"),
            amount=data.get("amount", 0.0),
            delivery_time_minutes=data.get("delivery_time_minutes", 0),
            is_delivered=data.get("is_delivered", False),
        )

    def __repr__(self) -> str:
        status = "Delivered" if self.is_delivered else "In Transit"
        return (
            f"Order(id={self.order_id}, restaurant='{self.restaurant_name}', "
            f"amount=Rs {self.amount:.2f}, time={self.delivery_time_minutes}m, status='{status}')"
        )


def save_records(records: List[Order], filepath: Path | str = DEFAULT_FILEPATH) -> bool:
    """
    Saves a list of Order objects to a JSON file.
    Wraps the file operation in a try-except-finally block.
    
    Args:
        records: List of Order domain instances.
        filepath: Destination filesystem path.
        
    Returns:
        True if write succeeded, False otherwise.
    """
    target_path = Path(filepath)
    success = False
    try:
        # Ensure parent directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)

        serialized_data = [order.to_dict() for order in records]
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(serialized_data, f, indent=2)
        success = True
        print(f"[SUCCESS] Successfully saved {len(records)} orders to {target_path}")

    except Exception as e:
        print(f"[ERROR] Failed to save records to {target_path}: {e}")
        success = False

    finally:
        print("Operation complete")

    return success


def load_records(filepath: Path | str = DEFAULT_FILEPATH) -> List[Order]:
    """
    Reads a list of Order dictionaries from a JSON file and reconstructs Order instances.
    Wraps the read in a try-except-finally block: catches FileNotFoundError specifically
    (returning an empty list), catches generic Exception for other failures,
    and unconditionally prints 'Operation complete' via finally.
    
    Args:
        filepath: Source filesystem path.
        
    Returns:
        List of reconstructed Order instances, or empty list on failure.
    """
    target_path = Path(filepath)
    orders: List[Order] = []
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            if isinstance(raw_data, list):
                orders = [Order.from_dict(item) for item in raw_data]
            else:
                print(f"[WARNING] Expected JSON list in {target_path}, got {type(raw_data)}")
        print(f"[SUCCESS] Successfully loaded {len(orders)} orders from {target_path}")

    except FileNotFoundError:
        print(f"[WARNING] Target file not found at '{target_path}'. Returning an empty list.")
        orders = []

    except Exception as e:
        print(f"[ERROR] Unexpected error while loading from '{target_path}': {e}")
        orders = []

    finally:
        print("Operation complete")

    return orders


def main():
    print("=" * 70)
    print("       FOOD DELIVERY RECORD MANAGER & JSON PERSISTENCE TEST        ")
    print("=" * 70)

    # 1. Test missing file handling
    missing_path = PROJECT_ROOT / "data" / "processed" / "non_existent_orders.json"
    print("\n--- TEST 1: Loading from a non-existent file (FileNotFoundError handling) ---")
    missing_results = load_records(missing_path)
    print(f"Result count: {len(missing_results)} (Expected: 0)\n")

    # 2. Create sample Order instances
    print("--- TEST 2: Creating and saving sample Order objects ---")
    sample_orders = [
        Order(101, "Tandoori Nights", 350.50, 32, is_delivered=True),
        Order(102, "Spice Bazaar", 180.00, 25, is_delivered=True),
        Order(103, "The Yellow Chilli", 520.75, 45, is_delivered=False),
        Order(104, "Royal Punjab", 240.00, 28, is_delivered=True),
        Order(105, "Curry Leaf Express", 610.25, 50, is_delivered=False),
        Order(106, "Urban Dhaba", 195.50, 22, is_delivered=True),
    ]

    for order in sample_orders:
        print(f"Created: {order}")

    save_records(sample_orders, DEFAULT_FILEPATH)

    # 3. Load saved orders back and verify reconstructability
    print("\n--- TEST 3: Loading records back from JSON and verifying reconstructability ---")
    loaded_orders = load_records(DEFAULT_FILEPATH)
    print(f"\nTotal reconstructed orders: {len(loaded_orders)}")
    for loaded_order in loaded_orders:
        print(f"Reconstructed: {loaded_order}")

    print("\n" + "=" * 70)
    print("                   RECORD MANAGER VALIDATION FINISHED                ")
    print("=" * 70)


if __name__ == "__main__":
    main()

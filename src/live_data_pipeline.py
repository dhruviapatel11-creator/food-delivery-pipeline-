"""
Food Delivery Live Data Pipeline - Console Tool (Section C Mini Capstone)
Assessment: M2-A1 | Stack: Python for Data Science

An interactive, menu-driven console application integrating REST API ingestion,
object-oriented domain modeling, functional commission analytics, resilient error handling,
and persistent JSON storage.
"""

import sys
import requests
from pathlib import Path
from typing import List, Optional

# Ensure project root is in sys.path for relative imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.record_manager import Order, save_records, load_records, DEFAULT_FILEPATH
from src.fee_calculator import calculate_tiered_commission, AUDIT_FEE_THRESHOLD

API_URL = "https://jsonplaceholder.typicode.com/posts?_limit=10"


class LiveDataPipeline:
    """
    Manages in-memory delivery orders and coordinates API ingestion,
    interactive input, functional analytics, and JSON persistence.
    """

    def __init__(self, storage_path: Path = DEFAULT_FILEPATH):
        self.storage_path = storage_path
        self.orders: List[Order] = []

    def fetch_mock_restaurants(self, api_url: str = API_URL) -> List[Order]:
        """
        Option 1: Fetches mock restaurant data from REST API.
        Validates HTTP status code prior to parsing JSON.
        Safely catches network exceptions without crashing.
        """
        print("\n" + "=" * 70)
        print("          FETCHING RESTAURANT DATA FROM REST API           ")
        print("=" * 70)
        print(f"Connecting to: {api_url}")

        try:
            response = requests.get(api_url, timeout=10)
            
            # Mandatory HTTP status code verification
            if response.status_code == 200:
                data = response.json()
                fetched_orders: List[Order] = []

                # Default fallback order amounts and delivery times for mock records
                mock_amounts = [220.0, 180.5, 450.0, 520.0, 150.0, 310.0, 680.0, 190.0, 410.0, 275.5]
                mock_times = [25, 30, 45, 35, 20, 40, 50, 22, 38, 28]

                for index, item in enumerate(data):
                    post_id = item.get("id", index + 1)
                    raw_title = item.get("title", f"Mock Restaurant {post_id}")
                    # Clean title: take first 3 words and title-case for clean restaurant names
                    restaurant_name = " ".join(raw_title.split()[:3]).title()
                    amount = mock_amounts[index % len(mock_amounts)]
                    duration = mock_times[index % len(mock_times)]

                    order = Order(
                        order_id=post_id,
                        restaurant_name=restaurant_name,
                        amount=amount,
                        delivery_time_minutes=duration,
                        is_delivered=(index % 2 == 0),
                    )
                    fetched_orders.append(order)

                self.orders = fetched_orders
                print(f"[SUCCESS] Ingested {len(fetched_orders)} restaurant records successfully (HTTP 200 OK).\n")
                self.display_records()
                return fetched_orders

            else:
                print(f"[ERROR] API request failed with HTTP Status Code: {response.status_code}")
                print("Skipping data ingestion gracefully. In-memory records remain unchanged.")
                return []

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Network connection failed: {e}")
            print("Skipping data ingestion gracefully. Program will not crash.")
            return []

    def add_restaurant_interactive(self) -> Optional[Order]:
        """
        Option 2: Interactively prompts the user to add a new restaurant order.
        Validates numeric fields and re-prompts on invalid input without crashing.
        """
        print("\n" + "=" * 70)
        print("                 ADD NEW RESTAURANT ORDER                   ")
        print("=" * 70)

        # 1. Validate Order ID (Positive Integer)
        while True:
            raw_id = input("Enter Order ID (numeric integer): ").strip()
            if raw_id.isdigit() and int(raw_id) > 0:
                order_id = int(raw_id)
                # Check for duplicate ID
                if any(o.order_id == order_id for o in self.orders):
                    print(f"[WARNING] Order ID {order_id} already exists. Please enter a unique ID.")
                    continue
                break
            print("[INVALID INPUT] Order ID must be a positive integer. Please re-enter.")

        # 2. Validate Restaurant Name (Non-empty String)
        while True:
            restaurant_name = input("Enter Restaurant Name: ").strip()
            if restaurant_name and not restaurant_name.isnumeric():
                restaurant_name = restaurant_name.title()
                break
            print("[INVALID INPUT] Restaurant name cannot be empty or purely numeric. Please re-enter.")

        # 3. Validate Amount (Positive Float)
        while True:
            raw_amt = input("Enter Order Amount in Rs (numeric float): ").strip()
            # Support optional 'Rs' prefix stripping for user convenience
            sanitized = raw_amt.upper().replace("RS", "").replace(",", "").strip()
            try:
                amount = float(sanitized)
                if amount > 0:
                    break
                print("[INVALID INPUT] Order amount must be greater than zero.")
            except ValueError:
                print("[INVALID INPUT] Non-numeric value entered. Please enter a valid numerical amount.")

        # 4. Validate Delivery Time (Positive Integer)
        while True:
            raw_time = input("Enter Estimated Delivery Time in minutes (integer): ").strip()
            if raw_time.isdigit() and int(raw_time) > 0:
                delivery_time = int(raw_time)
                break
            print("[INVALID INPUT] Delivery time must be a positive integer. Please re-enter.")

        # 5. Delivery Status Flag
        raw_status = input("Is the order delivered? (y/n, default: n): ").strip().lower()
        is_delivered = raw_status in ("y", "yes", "true", "1")

        # Instantiate Order class
        new_order = Order(
            order_id=order_id,
            restaurant_name=restaurant_name,
            amount=amount,
            delivery_time_minutes=delivery_time,
            is_delivered=is_delivered,
        )

        self.orders.append(new_order)
        print(f"\n[SUCCESS] Successfully created and added record:")
        print(f" -> {new_order}\n")
        return new_order

    def calculate_commissions(self) -> None:
        """
        Option 3: Calculates commission for all active records using map(),
        isolates high-value records exceeding the audit threshold using filter(),
        and prints formatted financial summaries.
        """
        print("\n" + "=" * 70)
        print("          COMMISSION & AUDIT ANALYTICS (map & filter)          ")
        print("=" * 70)

        if not self.orders:
            print("[WARNING] No records available in memory. Please fetch or add records first.")
            return

        # Using map() with a lambda to compute fees
        enriched_orders = list(
            map(
                lambda order: {
                    "id": order.order_id,
                    "name": order.restaurant_name,
                    "amount": order.amount,
                    "fee": calculate_tiered_commission(order.amount),
                    "status": "Delivered" if order.is_delivered else "In Transit",
                },
                self.orders,
            )
        )

        print("\n[ALL ORDERS WITH COMPUTED COMMISSION VIA map()]:")
        print(f"{'ID':<6} | {'Restaurant Name':<25} | {'Amount (Rs)':<12} | {'Fee (Rs)':<10} | {'Status'}")
        print("-" * 70)
        for o in enriched_orders:
            print(f"{o['id']:<6} | {o['name']:<25} | Rs {o['amount']:>9.2f} | Rs {o['fee']:>7.2f} | {o['status']}")

        # Using filter() to isolate audit records
        audit_records = list(
            filter(lambda o: o["fee"] > AUDIT_FEE_THRESHOLD, enriched_orders)
        )

        print("\n" + "-" * 70)
        print(f"[AUDIT FLAGGED ORDERS VIA filter()] (Fee > Rs {AUDIT_FEE_THRESHOLD:.2f}):")
        print("-" * 70)
        if audit_records:
            for o in audit_records:
                print(f"[AUDIT] ID: {o['id']:<4} | {o['name']:<22} | Order: Rs {o['amount']:>7.2f} | Fee: Rs {o['fee']:>6.2f}")
        else:
            print("No orders exceed the current audit threshold.")

        total_orders_val = sum(o["amount"] for o in enriched_orders)
        total_comm_val = sum(o["fee"] for o in enriched_orders)
        print("-" * 70)
        print(f"Total Active Orders       : {len(enriched_orders)}")
        print(f"Total Order Volume        : Rs {total_orders_val:.2f}")
        print(f"Total Commission Generated: Rs {total_comm_val:.2f}")
        print("=" * 70)

    def persist_and_reload(self) -> bool:
        """
        Option 4: Saves all active Order objects to data/processed/records.json
        and reads them back to verify roundtrip reconstructability.
        """
        print("\n" + "=" * 70)
        print("             JSON PERSISTENCE & ROUNDTRIP SYNC              ")
        print("=" * 70)

        if not self.orders:
            print("[WARNING] In-memory order list is empty. Saving will write an empty list.")

        print(f"[1/2] Saving {len(self.orders)} active order(s) to disk...")
        saved = save_records(self.orders, self.storage_path)

        if saved:
            print(f"\n[2/2] Reloading order instances from '{self.storage_path}' to verify state...")
            reloaded_orders = load_records(self.storage_path)
            self.orders = reloaded_orders
            print(f"[SUCCESS] Roundtrip reload completed. {len(self.orders)} active records in memory.")
            return True
        else:
            print("[ERROR] Persistence failed.")
            return False

    def display_records(self) -> None:
        """Displays currently loaded in-memory records."""
        if not self.orders:
            print("\n[INFO] No records currently stored in memory.")
            return

        print(f"\nCURRENT IN-MEMORY ORDERS ({len(self.orders)} records):")
        print(f"{'ID':<6} | {'Restaurant Name':<25} | {'Amount':<12} | {'Time':<8} | {'Status'}")
        print("-" * 70)
        for order in self.orders:
            status = "Delivered" if order.is_delivered else "In Transit"
            print(
                f"{order.order_id:<6} | {order.restaurant_name:<25} | "
                f"Rs {order.amount:>9.2f} | {order.delivery_time_minutes:>4} min | {status}"
            )


def print_menu():
    print("\n" + "=" * 70)
    print("      FOOD DELIVERY DEMAND ANALYTICS - LIVE DATA PIPELINE       ")
    print("=" * 70)
    print(" 1. Fetch & Display Top 10 Mock Restaurants (Public REST API)")
    print(" 2. Add New Restaurant Order (Interactive Validation)")
    print(" 3. Calculate & Display Commission Analytics (map & filter)")
    print(" 4. Save Orders to JSON & Reload (data/processed/records.json)")
    print(" 5. View Current In-Memory Records")
    print(" 6. Exit Pipeline")
    print("=" * 70)


def run_pipeline_menu():
    pipeline = LiveDataPipeline()

    while True:
        print_menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            pipeline.fetch_mock_restaurants()
        elif choice == "2":
            pipeline.add_restaurant_interactive()
        elif choice == "3":
            pipeline.calculate_commissions()
        elif choice == "4":
            pipeline.persist_and_reload()
        elif choice == "5":
            pipeline.display_records()
        elif choice == "6":
            print("\nExiting Food Delivery Demand Analytics Pipeline. Goodbye!\n")
            break
        else:
            print("\n[INVALID OPTION] Please enter a valid numeric choice between 1 and 6.")


if __name__ == "__main__":
    run_pipeline_menu()

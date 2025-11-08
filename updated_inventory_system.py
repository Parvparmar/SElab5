"""
A simple, class-based inventory management system.

This module provides an Inventory class to add, remove, and track items
in an inventory, with methods to load from and save to a JSON file.
"""

import json
import sys
from datetime import datetime


class Inventory:
    """
    Manages a stock inventory, allowing items to be added, removed,
    loaded, and saved.
    """

    def __init__(self):
        """Initializes the inventory with empty stock data."""
        self.stock_data = {}

    def add_item(self, item, qty, logs=None):
        """
        Adds a given quantity of an item to the stock.

        Args:
            item (str): The name of the item to add.
            qty (int): The quantity to add. Must be a positive integer.
            logs (list, optional): A list to append log messages to.
        """
        if not isinstance(item, str) or not item:
            error_msg = f"Error: Item name '{item}' is not a valid string."
            print(error_msg, file=sys.stderr)
            return

        if not isinstance(qty, int) or qty < 0:
            error_msg = (
                f"Error: Quantity '{qty}' is not a valid non-negative integer."
            )
            print(error_msg, file=sys.stderr)
            return

        # Correctly initialize default mutable argument
        if logs is None:
            logs = []

        self.stock_data[item] = self.stock_data.get(item, 0) + qty
        # Use f-string for cleaner formatting
        logs.append(f"{datetime.now()}: Added {qty} of {item}")

    def remove_item(self, item, qty):
        """
        Removes a given quantity of an item from the stock.

        Args:
            item (str): The name of the item to remove.
            qty (int): The quantity to remove. Must be a positive integer.
        """
        if not isinstance(item, str) or not item:
            error_msg = f"Error: Item name '{item}' is not a valid string."
            print(error_msg, file=sys.stderr)
            return

        if not isinstance(qty, int) or qty < 0:
            error_msg = (
                f"Error: Quantity '{qty}' is not a valid non-negative integer."
            )
            print(error_msg, file=sys.stderr)
            return

        try:
            # Check if item exists before trying to remove
            if item not in self.stock_data:
                raise KeyError(f"Item '{item}' not in stock. Cannot remove.")

            self.stock_data[item] -= qty
            # Remove item from inventory if stock is zero or less
            if self.stock_data[item] <= 0:
                del self.stock_data[item]
        # Catch specific exceptions, not a bare 'except'
        except (KeyError, TypeError) as e:
            print(f"Error removing item: {e}", file=sys.stderr)

    def get_qty(self, item):
        """
        Gets the current quantity of a specific item.

        Args:
            item (str): The name of the item.

        Returns:
            int: The quantity of the item, or 0 if not found.
        """
        return self.stock_data.get(item, 0)

    def load_data(self, file="inventory.json"):
        """
        Loads inventory data from a JSON file, replacing current stock.

        Args:
            file (str, optional): The name of the file to load from.
        """
        try:
            # Use 'with' statement for safe file handling
            # Specify encoding to prevent OS-dependent errors
            with open(file, "r", encoding="utf-8") as f:
                self.stock_data = json.load(f)
        except FileNotFoundError:
            error_msg = (
                f"Warning: File '{file}' not found. "
                "Starting with empty inventory."
            )
            print(error_msg, file=sys.stderr)
            self.stock_data = {}
        except json.JSONDecodeError:
            error_msg = (
                f"Error: Could not decode JSON from '{file}'. "
                "Starting with empty inventory."
            )
            print(error_msg, file=sys.stderr)
            self.stock_data = {}

    def save_data(self, file="inventory.json"):
        """
        Saves the current inventory data to a JSON file.

        Args:
            file (str, optional): The name of the file to save to.
        """
        try:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(self.stock_data, f, indent=4)
        except IOError as e:
            print(f"Error saving data to '{file}': {e}", file=sys.stderr)

    def print_data(self):
        """Prints a report of all items and their quantities."""
        print("\n--- Items Report ---")
        if not self.stock_data:
            print("Inventory is empty.")
        else:
            for item, qty in self.stock_data.items():
                print(f"{item} -> {qty}")
        print("--------------------\n")

    def check_low_items(self, threshold=5):
        """
        Gets a list of items with stock below a given threshold.

        Args:
            threshold (int, optional): The stock level to check against.

        Returns:
            list: A list of item names below the threshold.
        """
        # Break list comprehension into a loop for readability and line length
        low_stock_items = []
        for item, qty in self.stock_data.items():
            if qty < threshold:
                low_stock_items.append(item)
        return low_stock_items


# Two blank lines before the main function
def main():
    """Main function to demonstrate inventory usage."""

    # Create an instance of the inventory
    inventory = Inventory()
    session_logs = []

    # Add items
    inventory.add_item("apple", 10, logs=session_logs)
    inventory.add_item("banana", 15, logs=session_logs)

    # Test invalid inputs
    print("\nTesting invalid inputs:")
    inventory.add_item("banana", -2, logs=session_logs)  # Fails validation
    inventory.add_item(123, 10, logs=session_logs)       # Fails validation
    inventory.remove_item("orange", 1)                   # Fails (KeyError)

    # Perform valid operations
    inventory.remove_item("apple", 3)
    inventory.print_data()

    print(f"Apple stock: {inventory.get_qty('apple')}")
    # Break long line by assigning to variable first
    low_items = inventory.check_low_items(threshold=10)
    print(f"Low items (threshold=10): {low_items}")

    # Save and load data
    inventory.save_data("inventory_clean.json")

    print("Loading data into new inventory...")
    new_inventory = Inventory()
    new_inventory.load_data("inventory_clean.json")
    new_inventory.print_data()

    print("Session Logs:")
    for log in session_logs:
        print(log)


# Standard check to run main() only when script is executed directly
if __name__ == "__main__":
    main()

#!/usr/bin/env python3

"""
E-commerce Data Generator
Author: Marvin
Description: Generates mock product, customer, and order data for cloud engineering practice.

Usage:
    python generate_data.py --count 500
"""

# -----------------------------------------
# E-commerce Data Generator (Pseudocode)
# -----------------------------------------

# Imports
# Standard library
import argparse  # for command-line arguments
import random  # for random choices, prices, quantities
import json  # for exporting data to JSON
import datetime  # for realistic timestamps
import uuid  # for unique IDs
import os  # for file operations

# External libraries
from faker import Faker  # for realistic names, addresses, emails
import pandas as pd  # for tabular data manipulation/export (CSV, Excel)

# -----------------------------------------
# Data Pools
# -----------------------------------------

# Example product catalog (name + price)
products = [
    {"name": "Laptop", "price": 999.99},
    {"name": "Smartphone", "price": 699.99},
    {"name": "Headphones", "price": 199.99},
    {"name": "Keyboard", "price": 89.99},
    {"name": "Monitor", "price": 249.99},
]

# Payment methods
payment_methods = ["credit_card", "paypal", "bank_transfer", "gift_card"]

# Order statuses
order_statuses = ["pending", "shipped", "delivered", "cancelled"]

fake = Faker()


# Function to generate just one order
def generate_order(fake):
    """
    Generate a single mock e-commerce order.
    Returns a dictionary representing the order.
    """
    # Unique order ID
    order_id = str(uuid.uuid4())

    # Random customer details
    customer = {
        "customer_id": str(uuid.uuid4()),
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
    }

    # Random order date (within last 365 days)
    order_date = fake.date_time_between(start_date="-365d", end_date="now").isoformat()

    # Random items (1–5)
    items = []
    num_items = random.randint(1, 5)
    for _ in range(num_items):
        product = random.choice(products)
        quantity = random.randint(1, 3)
        item_total = round(product["price"] * quantity, 2)
        items.append(
            {
                "product_name": product["name"],
                "unit_price": product["price"],
                "quantity": quantity,
                "item_total": item_total,
            }
        )

    # Calculate total amount
    total_amount = round(sum(item["item_total"] for item in items), 2)

    # Random payment method and status
    payment_method = random.choice(payment_methods)
    status = random.choice(order_statuses)

    # Return order dictionary
    return {
        "order_id": order_id,
        "customer": customer,
        "order_date": order_date,
        "items": items,
        "total_amount": total_amount,
        "payment_method": payment_method,
        "status": status,
    }


# Loop to generate N orders
if __name__ == "__main__":
    import argparse

    # Command-line arguments
    parser = argparse.ArgumentParser(description="Generate mock e-commerce orders")
    parser.add_argument(
        "--count",
        type=int,
        default=100,  # fallback if not provided
        help="Number of orders to generate",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Generate and print a single test order instead of saving many",
    )
    args = parser.parse_args()

    fake = Faker()

    if args.test:
        # Run a single test order
        order = generate_order(fake)
        print(json.dumps(order, indent=2))
    else:
        # Loop to generate N orders
        orders = [generate_order(fake) for _ in range(args.count)]

        # Save to JSON file
        os.makedirs("data", exist_ok=True)
        with open("data/orders.json", "w") as f:
            json.dump(orders, f, indent=2)

        print(f"Generated {args.count} orders and saved to data/orders.json")

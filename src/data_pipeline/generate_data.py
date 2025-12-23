"""
generate_data.py
Author: Marvin
Description: Core functions and data pools for generating mock e-commerce orders.
"""

# Imports
# Standard library
import random  # for random choices, prices, quantities
import uuid  # for unique IDs

# External libraries
from faker import Faker  # for realistic names, addresses, emails
from .products import products

# Payment methods
payment_methods = ["credit_card", "paypal", "bank_transfer", "gift_card"]

# Order statuses
order_statuses = ["pending", "shipped", "delivered", "cancelled"]

fake = Faker()


# Function to generate just one order
def generate_order(fake=fake):
    """
    Generate a single mock e-commerce order.

    Args:
        fake (Faker, optional): Faker instance for generating customer/order data.

    Returns:
        dict: A dictionary representing the order.
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

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
import random  # for random choices, prices, quantities
import json  # for exporting data to JSON
import datetime  # for realistic timestamps
import uuid  # for unique IDs

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

# Step 3: Function to generate a single order
#   - Create a unique order_id
#   - Pick a random customer
#   - Pick a random date
#   - Generate a random number of items (1–5)
#       - For each item, pick a product, quantity, and price
#   - Calculate total_amount
#   - Pick a random payment method
#   - Pick a random status
#   - Return the order as a dictionary (JSON object)

# Step 4: Loop to generate N orders
#   - Initialize an empty list
#   - For i in range(N):
#       - Call the order generator function
#       - Append the result to the list

# Step 5: Write the list of orders to a JSON file
#   - Open a file in the /data folder (e.g., "orders.json")
#   - Use json.dump() to write the list with indentation

# Step 6: Print confirmation
#   - Example: "Generated 500 orders and saved to data/orders.json"

"""
transform.py

Business logic for transforming raw JSON ecommerce data into
normalized CSV tables for downstream processing.
"""

import json
import csv
import io
from typing import Dict, List

from .errors import TransformError, SchemaValidationError


def transform_data(raw_json: str) -> Dict[str, str]:
    """
    Transform raw JSON orders into three normalized CSV datasets:
    - orders.csv
    - customers.csv (deduplicated)
    - order_items.csv

    Returns a dict containing CSV strings.
    Raises TransformError or SchemaValidationError on invalid input.
    """

    # -----------------------------
    # Parse JSON safely
    # -----------------------------
    try:
        orders = json.loads(raw_json)
    except json.JSONDecodeError as e:
        raise TransformError(f"Invalid JSON input: {e}")

    if not isinstance(orders, list):
        raise SchemaValidationError("Top-level JSON must be a list of orders")

    # Storage for normalized tables
    orders_rows: List[dict] = []
    customers_dict: Dict[str, dict] = {}
    items_rows: List[dict] = []

    # Required fields for validation
    required_order_fields = [
        "order_id",
        "order_date",
        "customer",
        "items",
        "total_amount",
        "payment_method",
        "status",
    ]

    required_customer_fields = ["customer_id", "name", "email", "address"]
    required_item_fields = ["product_name", "unit_price", "quantity", "item_total"]

    # -----------------------------
    # Transform each order
    # -----------------------------
    for order in orders:

        # Validate order structure
        for field in required_order_fields:
            if field not in order:
                raise SchemaValidationError(
                    f"Order missing required field '{field}': {order}"
                )

        customer = order["customer"]
        items = order["items"]

        # Validate customer structure
        for field in required_customer_fields:
            if field not in customer:
                raise SchemaValidationError(
                    f"Customer missing required field '{field}': {customer}"
                )

        # Validate items structure
        if not isinstance(items, list):
            raise SchemaValidationError("Order 'items' must be a list")

        for item in items:
            for field in required_item_fields:
                if field not in item:
                    raise SchemaValidationError(
                        f"Order item missing required field '{field}': {item}"
                    )

        order_id = order["order_id"]

        # -----------------------------
        # 1. ORDERS TABLE
        # -----------------------------
        orders_rows.append(
            {
                "order_id": order_id,
                "order_date": order["order_date"],
                "customer_id": customer["customer_id"],
                "total_amount": order["total_amount"],
                "payment_method": order["payment_method"],
                "status": order["status"],
            }
        )

        # -----------------------------
        # 2. CUSTOMERS TABLE (dedupe)
        # -----------------------------
        cust_id = customer["customer_id"]
        if cust_id not in customers_dict:
            customers_dict[cust_id] = {
                "customer_id": cust_id,
                "name": customer["name"],
                "email": customer["email"],
                "address": customer["address"],
            }

        # -----------------------------
        # 3. ORDER ITEMS TABLE
        # -----------------------------
        for item in items:
            items_rows.append(
                {
                    "order_id": order_id,
                    "product_name": item["product_name"],
                    "unit_price": item["unit_price"],
                    "quantity": item["quantity"],
                    "item_total": item["item_total"],
                }
            )

    # -----------------------------
    # Convert lists → CSV strings
    # -----------------------------
    def to_csv(rows: List[dict]) -> str:
        if not rows:
            return ""

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        return output.getvalue()

    return {
        "orders": to_csv(orders_rows),
        "customers": to_csv(list(customers_dict.values())),
        "items": to_csv(items_rows),
    }

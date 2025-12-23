import re
import uuid
import json
import pytest
from data_pipeline.generate_data import generate_order, payment_methods, order_statuses


def test_generate_order_returns_dict():
    order = generate_order()
    assert isinstance(order, dict)


def test_order_has_expected_keys():
    order = generate_order()
    expected_keys = {
        "order_id",
        "customer",
        "order_date",
        "items",
        "total_amount",
        "payment_method",
        "status",
    }
    assert expected_keys.issubset(order.keys())


def test_customer_structure():
    order = generate_order()
    customer = order["customer"]
    assert uuid.UUID(customer["customer_id"])  # valid UUID
    assert re.match(r"[^@]+@[^@]+\.[^@]+", customer["email"])  # valid email
    assert customer["name"]


def test_items_structure_and_totals():
    order = generate_order()
    items = order["items"]
    assert isinstance(items, list)
    assert len(items) >= 1
    for item in items:
        assert "product_name" in item
        assert "unit_price" in item
        assert "quantity" in item
        assert "item_total" in item
        assert item["item_total"] == round(item["unit_price"] * item["quantity"], 2)
    assert order["total_amount"] == round(sum(i["item_total"] for i in items), 2)


def test_payment_and_status_values():
    order = generate_order()
    assert order["payment_method"] in payment_methods
    assert order["status"] in order_statuses


def test_json_serialization():
    order = generate_order()
    serialized = json.dumps(order)
    assert isinstance(serialized, str)


def test_randomization_produces_variety():
    orders = [generate_order() for _ in range(5)]
    ids = {o["order_id"] for o in orders}
    assert len(ids) == 5  # unique IDs

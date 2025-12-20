import pytest
from lambda_function.transform import transform_data
from lambda_function.errors import TransformError, SchemaValidationError


def test_transform_valid_json():
    raw_json = """
    [
        {
            "order_id": "123",
            "order_date": "2024-01-01",
            "customer": {
                "customer_id": "C1",
                "name": "John Doe",
                "email": "john@example.com",
                "address": "123 Main St"
            },
            "items": [
                {
                    "product_name": "Widget",
                    "unit_price": 10.0,
                    "quantity": 2,
                    "item_total": 20.0
                }
            ],
            "total_amount": 20.0,
            "payment_method": "card",
            "status": "completed"
        }
    ]
    """

    result = transform_data(raw_json)

    assert "orders" in result
    assert "customers" in result
    assert "items" in result

    assert "order_id" in result["orders"]
    assert "customer_id" in result["customers"]
    assert "product_name" in result["items"]


def test_transform_invalid_json():
    with pytest.raises(TransformError):
        transform_data("not valid json")


def test_transform_missing_field():
    raw_json = """
    [
        {
            "order_id": "123"
        }
    ]
    """
    with pytest.raises(SchemaValidationError):
        transform_data(raw_json)

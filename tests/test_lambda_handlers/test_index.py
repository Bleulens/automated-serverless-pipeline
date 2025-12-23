import json
import pytest
from unittest.mock import patch, MagicMock

from lambda_handlers.index import handler
from data_pipeline.errors import InvalidEventError


class FakeContext:
    aws_request_id = "test-id"


def test_handler_success():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "input-bucket"},
                    "object": {"key": "orders.json"},
                }
            }
        ]
    }

    with patch(
        "lambda_handlers.index.read_from_s3", return_value="raw"
    ) as mock_read, patch(
        "lambda_handlers.index.transform_data",
        return_value={"orders": "csv1", "customers": "csv2", "items": "csv3"},
    ) as mock_transform, patch(
        "lambda_handlers.index.write_processed_file",
        return_value="processed/orders.csv",
    ) as mock_write:

        response = handler(event, FakeContext())
        body = json.loads(response["body"])

        assert response["statusCode"] == 200
        assert "processed_files" in body
        assert len(body["processed_files"]) == 3


def test_handler_invalid_event():
    event = {"bad": "event"}

    response = handler(event, FakeContext())
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "error" in body

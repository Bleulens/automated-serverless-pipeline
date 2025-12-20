import pytest
from unittest.mock import patch, MagicMock
from lambda_function.s3_utils import read_from_s3, write_processed_file
from lambda_function.errors import S3ReadError, S3WriteError


@patch("lambda.s3_utils.s3")
def test_read_from_s3_success(mock_s3):
    mock_s3.get_object.return_value = {"Body": MagicMock(read=lambda: b"hello world")}

    result = read_from_s3("bucket", "key")
    assert result == "hello world"


@patch("lambda.s3_utils.s3")
def test_read_from_s3_failure(mock_s3):
    mock_s3.get_object.side_effect = Exception("boom")

    with pytest.raises(S3ReadError):
        read_from_s3("bucket", "key")


@patch("lambda.s3_utils.s3")
def test_write_processed_file_success(mock_s3):
    mock_s3.put_object.return_value = {}

    key = write_processed_file("csv,data", "orders.csv")
    assert key.endswith("orders.csv")


@patch("lambda.s3_utils.s3")
def test_write_processed_file_failure(mock_s3):
    mock_s3.put_object.side_effect = Exception("boom")

    with pytest.raises(S3WriteError):
        write_processed_file("csv,data", "orders.csv")

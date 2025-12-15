"""
s3_utils.py

Helper utilities for interacting with Amazon S3.

Responsible for:
- Reading raw files from S3
- Writing transformed files back to S3
- Generating output keys based on the original key
- Handling S3-specific exceptions cleanly
- Keeping S3 logic separate from the Lambda handler
"""

import boto3
import os
from botocore.exceptions import ClientError
from .errors import S3ReadError, S3WriteError

# Initialize S3 client once per container (Lambda best practice)
s3 = boto3.client("s3")


def read_from_s3(bucket: str, key: str) -> str:
    """
    Read an object from S3 and return its contents as a string.

    Raises:
        S3ReadError: If the object cannot be retrieved.
    """
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return response["Body"].read().decode("utf-8")
    except ClientError as e:
        raise S3ReadError(f"Failed to read s3://{bucket}/{key}: {e}")


def write_processed_file(data: str, original_key: str) -> str:
    """
    Write transformed data back to S3 under a new key.

    Returns:
        output_key (str): The S3 key where the processed file was written.

    Raises:
        S3WriteError: If the write operation fails.
    """
    output_key = _build_output_key(original_key)

    try:
        s3.put_object(
            Bucket=_get_output_bucket(),
            Key=output_key,
            Body=data.encode("utf-8"),
        )
        return output_key
    except ClientError as e:
        raise S3WriteError(f"Failed to write processed file to {output_key}: {e}")


def _build_output_key(original_key: str) -> str:
    """
    Build the output S3 key for the processed CSV file.
    Converts:
        incoming/orders.json → processed/orders.csv
    """
    base = os.path.basename(original_key)  # orders.json
    name, _ = os.path.splitext(base)  # ("orders", ".json")
    new_filename = f"{name}.csv"  # orders.csv
    return f"processed/{new_filename}"


def _get_output_bucket() -> str:
    """
    Return the bucket where processed files should be written.
    This keeps the bucket name in one place for easy modification.
    """
    return "my-output-bucket"

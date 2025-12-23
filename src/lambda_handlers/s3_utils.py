"""
s3_utils.py

Helper utilities for interacting with Amazon S3.
Handles:
- Reading raw files
- Writing processed CSV files
- Generating output keys
"""

import boto3
from botocore.exceptions import ClientError
from data_pipeline.errors import S3ReadError, S3WriteError
from data_pipeline import config

s3 = boto3.client("s3")


def read_from_s3(bucket: str, key: str) -> str:
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return response["Body"].read().decode("utf-8")
    except ClientError as e:
        raise S3ReadError(f"Failed to read s3://{bucket}/{key}: {e}")


def write_processed_file(data: str, filename: str) -> str:
    """
    Write a single CSV file to S3.
    filename: e.g., 'orders.csv'
    """
    output_key = f"{config.PROCESSED_PREFIX}{filename}"

    try:
        s3.put_object(
            Bucket=config.OUTPUT_BUCKET,
            Key=output_key,
            Body=data.encode("utf-8"),
        )
        return output_key
    except ClientError as e:
        raise S3WriteError(f"Failed to write processed file to {output_key}: {e}")

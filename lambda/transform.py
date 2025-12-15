"""
transform.py

Business logic for transforming raw JSON ecommerce data into tabular CSV format.
"""

import json
import csv
import io
from .errors import TransformError


def transform_data(raw_json: str) -> str:
    """
    Transform synthetic ecommerce JSON data into CSV format.

    Args:
        raw_json (str): The raw JSON string read from S3.

    Returns:
        str: The transformed data as CSV text.

    Raises:
        TransformError: If the JSON cannot be parsed or transformed.
    """
    try:
        # Parse JSON string into Python objects
        records = json.loads(raw_json)

        # Ensure we have a list of records
        if not isinstance(records, list):
            raise TransformError("Expected a list of records in JSON input")

        # Use StringIO as an in-memory file for CSV writing
        output = io.StringIO()
        writer = None

        for record in records:
            if writer is None:
                # Initialize CSV writer with headers from the first record
                headers = list(record.keys())
                writer = csv.DictWriter(output, fieldnames=headers)
                writer.writeheader()

            # Write each record as a row
            writer.writerow(record)

        return output.getvalue()

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        raise TransformError(f"Failed to transform JSON to CSV: {e}")

"""
index.py

Lambda entrypoint for the automated serverless pipeline.
Responsible for:
- Receiving the S3 event
- Extracting bucket and key
- Coordinating read → transform → write
- Returning a structured response
"""

from .s3_utils import read_from_s3, write_processed_file
from .transform import transform_data
from .errors import InvalidEventError

# Handler Structure
# Step 1: parse_event
# Step 2: read_from_s3
# Step 3: transform_data
# Step 4: write_processed_file
# Step 5: build_response


def handler(event, context):
    # Step 1: Parse the event
    bucket, key = parse_event(event)

    # Step 2: Read the raw file from S3
    raw_data = read_from_s3(bucket, key)

    # Step 3: Transform the data
    transformed_data = transform_data(raw_data)

    # Step 4: Write the processed file
    output_key = write_processed_file(transformed_data, key)

    # Step 5: Build and return the final response
    return build_response(output_key)


def parse_event(event):
    """
    Extract and validate bucket and key from the event.
    """
    try:
        record = event["Records"][0]
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        return bucket, key
    except (KeyError, IndexError, TypeError) as e:
        raise InvalidEventError(f"Malformed S3 event structure: {e}")


def build_response(output_key):
    """
    Build the final Lambda response payload.
    """
    response = {"statusCode": 200, "body": f"Processed file written to {output_key}"}
    return response

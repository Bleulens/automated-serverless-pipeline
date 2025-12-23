"""
index.py

Lambda entrypoint for the automated serverless pipeline.
Coordinates:
- Event parsing
- S3 read
- Data transformation
- S3 writes (multiple CSVs)
- Structured response building
"""

import json
import logging

from .s3_utils import write_processed_file, read_from_s3
from data_pipeline.transform import transform_data
from data_pipeline.errors import (
    PipelineError,
    InvalidEventError,
    S3ReadError,
    S3WriteError,
    TransformError,
    SchemaValidationError,
)
from data_pipeline import config

# Configure logging
logger = logging.getLogger()
logger.setLevel(config.LOG_LEVEL)


def handler(event, context):
    request_id = context.aws_request_id

    # Ensure event is JSON-serializable for logging
    safe_event = json.loads(json.dumps(event))

    logger.info(
        {"event": "LAMBDA_START", "request_id": request_id, "raw_event": safe_event}
    )

    try:
        # Step 1: Parse event
        bucket, key = parse_event(event)
        logger.info(
            {
                "event": "EVENT_PARSED",
                "request_id": request_id,
                "bucket": bucket,
                "key": key,
            }
        )

        # Step 2: Read raw data
        raw_data = read_from_s3(bucket, key)
        logger.info(
            {
                "event": "S3_READ_SUCCESS",
                "request_id": request_id,
                "bytes_read": len(raw_data),
            }
        )

        # Step 3: Transform
        transformed_data = transform_data(raw_data)
        logger.info(
            {
                "event": "TRANSFORM_SUCCESS",
                "request_id": request_id,
                "tables": list(transformed_data.keys()),
            }
        )

        # Step 4: Write each CSV file
        output_keys = []
        for name, csv_data in transformed_data.items():
            filename = f"{name}.csv"
            output_key = write_processed_file(csv_data, filename)
            output_keys.append(output_key)

            logger.info(
                {
                    "event": "S3_WRITE_SUCCESS",
                    "request_id": request_id,
                    "output_key": output_key,
                }
            )

        # Step 5: Respond
        return build_response(200, {"processed_files": output_keys})

    except Exception as e:
        logger.exception(
            {"event": "UNEXPECTED_ERROR", "request_id": request_id, "error": str(e)}
        )
        return build_response(500, {"error": str(e)})


def parse_event(event):
    """
    Extract bucket and key from the S3 event.
    """
    try:
        record = event["Records"][0]
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        return bucket, key
    except (KeyError, IndexError, TypeError) as e:
        raise InvalidEventError(f"Malformed S3 event structure: {e}")


def build_response(status_code, body):
    """
    Build a structured Lambda response.
    """
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
    }

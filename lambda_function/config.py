"""
config.py

Centralized configuration for the automated serverless pipeline.
Keeps environment-specific values in one place.
"""

import os

# Bucket where processed CSVs will be written
OUTPUT_BUCKET = os.getenv("OUTPUT_BUCKET", "my-output-bucket")

# Prefix for processed files
PROCESSED_PREFIX = os.getenv("PROCESSED_PREFIX", "processed/")

# Logging level (INFO, DEBUG, WARNING)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

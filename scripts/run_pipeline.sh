#!/usr/bin/env bash

set -euo pipefail

# --- Variables ---

INGEST_BUCKET=$(terraform -chdir=infra/terraform output -raw ingest_bucket_name)
INPUT_FILE="data/sample.json"
S3_KEY="input/sample.json"

# --- Upload sample file ---

echo "Uploading $INPUT_FILE to s3://$INGEST_BUCKET/$S3_KEY"
aws s3 cp "$INPUT_FILE" "s3://$INGEST_BUCKET/$S3_KEY"

echo "File uploaded. Pipeline has been triggered automatically by the s3 event."
echo "Use ./scripts/monitor_pipeline.sh to check progress."
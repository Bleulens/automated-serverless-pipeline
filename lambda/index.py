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

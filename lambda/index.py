def handler(event, context):
    # Step 1: Extract bucket and key from the event
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    # Step 2: For now, just log them so you know it works
    print(f"Bucket: {bucket}, Key: {key}")

########################################
# Compute / Lambda Outputs
########################################

output "lambda_arn" {
  description = "ARN of the created Lambda function"
  value       = module.lambda.lambda_arn
}

output "lambda_name" {
  description = "Name of the created Lambda function"
  value       = module.lambda.lambda_name
}

output "log_group_name" {
  description = "Name of the CloudWatch log group for the Lambda"
  value       = module.lambda.log_group_name
}

output "lambda_role_arn" {
  description = "IAM role assigned to the Lambda function"
  value       = module.lambda.lambda_role_arn
}

output "ingest_bucket_name" {
  description = "Final name of the ingest bucket (with random suffix)"
  value       = module.ingest_bucket.s3_bucket_name
}

output "processed_bucket_name" {
  description = "Final name of the processed bucket (with random suffix)"
  value       = module.processed_bucket.s3_bucket_name
}

output "ingest_bucket_arn" {
  description = "ARN of the ingest bucket"
  value       = module.ingest_bucket.s3_bucket_arn
}

output "processed_bucket_arn" {
  description = "ARN of the processed bucket"
  value       = module.processed_bucket.s3_bucket_arn
}

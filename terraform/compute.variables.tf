variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "example-lambda"
}

variable "log_retention_days" {
  description = "Number of days to retain logs in CloudWatch"
  type        = number
  default     = 7
}

variable "policy_actions" {
  description = "List of IAM actions to allow in the Lambda's policy"
  type        = list(string)
  default = [
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents"
  ]
}

variable "policy_resources" {
  description = "List of resources the IAM policy applies to"
  type        = list(string)
  default     = ["*"]
}

variable "source_code_hash" {
  description = "Base64-encoded SHA256 hash of the deployment package"
  type        = string
  default     = null
}

variable "source_file" {
  description = "Path to local source file for packaging"
  type        = string
  default     = "index.py"
}

variable "output_path" {
  description = "Path to output the packaged zip file"
  type        = string
  default     = "lambda.zip"
}

variable "timeout" {
  description = "Function execution timeout in seconds"
  type        = number
  default     = 3
}

variable "ingest_bucket_name" {
  description = "Name of the ingest S3 bucket"
  type        = string
  default     = "example-ingest-bucket"
}

variable "processed_bucket_name" {
  description = "Name of the processed S3 bucket"
  type        = string
  default     = "example-processed-bucket"
}

variable "force_destroy" {
  type        = bool
  default     = false
  description = "Delete all objects (and versions) when destroying the bucket"
}

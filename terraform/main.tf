########################################
# Data Sources (lookups & helpers)
########################################
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

data "archive_file" "lambda" {
  type        = "zip"
  source_file = "${path.root}/../lambda/index.py"
  output_path = "${path.module}/lambda.zip"
}

########################################
# Compute / Lambda Modules
########################################
module "lambda" {
  source             = "git::https://github.com/marvin-aws-modules/terraform-aws-lambda.git?ref=v1.0.1"
  function_name      = var.function_name
  log_retention_days = var.log_retention_days
  policy_actions = [
    "s3:GetObject",
    "s3:PutObject",
    "s3:ListBucket",
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents"
  ]
  policy_resources = [
    "arn:aws:s3:::${module.ingest_bucket.s3_bucket_name}",
    "arn:aws:s3:::${module.ingest_bucket.s3_bucket_name}/*",
    "arn:aws:s3:::${module.ingest_bucket.s3_bucket_name}",
    "arn:aws:s3:::${module.ingest_bucket.s3_bucket_name}/*",
    "arn:aws:logs:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.function_name}:*"
  ]
  source_code_hash = data.archive_file.lambda.output_base64sha256
  source_file      = "${path.root}/../lambda/index.py"
  output_path      = "${path.module}/lambda.zip"
  timeout          = 10
  tags = {
    module = "lambda"
  }
  default_tags = local.global_tags

}

module "ingest_bucket" {
  source        = "git::https://github.com/marvin-aws-modules/terraform-aws-s3.git?ref=v1.0.1"
  bucket_name   = var.ingest_bucket_name
  force_destroy = var.force_destroy
  tags = {
    module = "s3"
    name   = "ingest"
  }
  default_tags = local.global_tags

}

resource "aws_s3_bucket_notification" "ingest_trigger" {
  bucket = module.ingest_bucket.s3_bucket_name

  lambda_function {
    lambda_function_arn = module.lambda.lambda_arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [
    module.lambda,
    aws_lambda_permission.allow_s3_ingest
  ]
}

resource "aws_lambda_permission" "allow_s3_ingest" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda.lambda_name # or aws_lambda_function.lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = module.ingest_bucket.s3_bucket_arn
}

module "processed_bucket" {
  source        = "git::https://github.com/marvin-aws-modules/terraform-aws-s3.git?ref=v1.0.1"
  bucket_name   = var.processed_bucket_name
  force_destroy = var.force_destroy
  tags = {
    module = "s3"
    name   = "processed"
  }
  default_tags = local.global_tags

}

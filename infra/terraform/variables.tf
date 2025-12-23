variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
}

variable "project_name" {
  description = "Name of the project for tagging"
  type        = string
}

variable "environment" {
  description = "Deployment environment (e.g. dev, staging, prod)"
  type        = string
}

variable "owner_name" {
  description = "Owner or team responsible for the stack"
  type        = string
}
variable "tags" {
  type        = map(string)
  default     = {}
  description = "Optional tags to override or extend default_tags"
}

variable "default_tags" {
  type        = map(string)
  default     = {}
  description = "Baseline tags applied across all modules"
}

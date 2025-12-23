terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.5.0" # Adjust as needed
    }
    # Add other providers here if needed
    # random = {
    #   source  = "hashicorp/random"
    #   version = "~> 3.5"
    # }
  }

  required_version = ">= 1.5.0" # Pin Terraform CLI version
}

provider "aws" {
  region = var.aws_region

}

# Optional: Aliased providers for multi-region or multi-account setups
# provider "aws" {
#   alias  = "us_east_1"
#   region = "us-east-1"
#   default_tags {
#     tags = {
#       Project     = var.project_name
#       Environment = var.environment
#       Owner       = var.owner_name
#     }
#   }
# }

# provider "aws" {
#   alias  = "us_west_2"
#   region = "us-west-2"
#   default_tags {
#     tags = {
#       Project     = var.project_name
#       Environment = var.environment
#       Owner       = var.owner_name
#     }
#   }
# }

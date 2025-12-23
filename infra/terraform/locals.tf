locals {
  global_tags = {
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner_name
    Registry    = "true"
  }
}

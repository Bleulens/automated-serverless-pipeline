# Set the default goal so plain `make` shows help
.DEFAULT_GOAL := help

# === Infrastructure Deployment ===
infra-init: ## Initialize Terraform
	terraform -chdir=terraform init

infra-plan: ## Run terraform plan with aws-vault
	aws-vault exec readyplayerone --no-session -- terraform -chdir=terraform plan -detailed-exitcode -out=tfplan || { code=$$?; [ $$code -eq 2 ] || exit $$code; }


infra-apply: ## Apply terraform plan with aws-vault
	aws-vault exec readyplayerone --no-session -- terraform -chdir=terraform apply tfplan

infra-destroy: ## Destroy infra with aws-vault
	aws-vault exec readyplayerone --no-session -- terraform -chdir=terraform destroy -auto-approve

.PHONY: infra-init infra-plan infra-apply infra-destroy


# === Bash Deployment Script ===
deploy-infra: ## Run deploy_infra.sh with aws-vault
	aws-vault exec readyplayerone --no-session -- bash scripts/deploy_infra.sh

.PHONY: deploy-infra


# === Data Ingestion ===
run-pipeline: ## Run pipeline script with aws-vault
	aws-vault exec readyplayerone -- bash scripts/run_pipeline.sh

.PHONY: run-pipeline


# === Monitoring ===
monitor: ## Run monitoring script with aws-vault
	aws-vault exec readyplayerone -- bash scripts/monitor_pipeline.sh

.PHONY: monitor


# === Cleanup ===
clean: ## Clean Terraform state (PowerShell)
	powershell -Command "cleanTF"

clean-dry: ## Dry-run clean Terraform state (PowerShell)
	powershell -Command "cleanTF -DryRun"

.PHONY: clean clean-dry


# === Lambda Packaging (Optional) ===
package-lambda: ## Package Lambda into zip
	cd lambda && zip -r lambda.zip .

.PHONY: package-lambda


# === Format & Validate Terraform ===
fmt: ## Format Terraform code
	terraform -chdir=terraform fmt -recursive

validate: ## Validate Terraform code
	terraform -chdir=terraform validate

.PHONY: fmt validate


# === Bootstrap Full Flow ===
bootstrap: deploy-infra run-pipeline monitor ## Deploy infra, run pipeline, monitor

.PHONY: bootstrap


# === Help ===
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

.PHONY: help
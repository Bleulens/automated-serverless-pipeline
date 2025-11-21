# 📦 Automated Serverless Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
![Terraform](https://img.shields.io/badge/Terraform-v1.5%2B-623CE4?logo=terraform)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazon-aws)

_Build a small but realistic workflow that ingests data, processes it using Bash for orchestration, Python for logic, and my own Terraform registry modules for deployment._

---

## 📖 Overview

- **Problem this project solves:**

  Data ingestion and processing is often manual, inconsistent, and hard to scale. This project demonstrates how to build a fully automated, serverless data pipeline on AWS using Terraform, Bash, and Python. By combining infrastructure‑as‑code, event‑driven triggers, and scripted orchestration, it provides a repeatable pattern for ingesting, processing, and storing data with minimal manual effort.

- **Why does this exist?**

  This project exists as a learning and portfolio exercise to demonstrate how to design and automate a realistic serverless data pipeline on AWS. It shows how Terraform, Bash, and Python can work together to provision infrastructure, orchestrate workflows, and process data in a repeatable, event‑driven way.

- **High‑level architecture**

  ![Architecture Diagram](link-to-your-diagram.png)

  The pipeline consists of:

  - **Ingest S3 bucket** → stores raw input files
  - **S3 event notification** → automatically triggers the Lambda
  - **Lambda processor (Python)** → transforms/cleans the data
  - **Processed S3 bucket** → stores the transformed output
  - **CloudWatch Logs/Alarms** → capture execution details and errors

---

## 🛠 Tech Stack

- **Infrastructure as Code:** Terraform
- **Orchestration:** Bash
- **Application Logic:** Python (AWS Lambda)
- **Cloud Services:** S3, Lambda, IAM, CloudWatch

---

## 🚀 Getting Started

### 1. Prerequisites

- AWS account with programmatic access
- AWS CLI installed and configured
- Terraform v1.5+ (tested on v1.13.3)
- Python 3.9+ (tested on 3.13.2)
- Personal Terraform module registry (used for S3 and Lambda modules)

### 2. Setup

```bash
# Clone the repository
git clone <repo-url>
cd <project-folder>

# Install dependencies (if any)
pip install -r requirements.txt
```

---

## 📂 Project Structure

```
data/                # Sample data files (CSV/JSON for testing)
├── sample.csv
└── sample.json

docs/                # Documentation and design notes
├── decisions.md
├── README.md
└── diagrams/        # Architecture diagrams

lambda/              # AWS Lambda function code
└── index.py

scripts/             # Bash orchestration scripts
├── deploy_infra.sh      # Deploy infrastructure with Terraform
├── monitor_pipeline.sh  # Fetch logs / monitor pipeline
└── run_pipeline.sh      # Upload file to S3 and trigger pipeline

terraform/           # Terraform IaC configs
├── backend.tf
├── compute.variables.tf
├── locals.tf
├── main.tf
├── outputs.tf
├── providers.tf
├── terraform.tfvars
└── variables.tf

.gitignore
LICENSE
Makefile
```

---

## ⚙️ Usage

### Discover Commands

Run `make help` to see all available commands:

```bash
make help
```

Example output:

```
Available targets:
  infra-init           Initialize Terraform
  infra-plan           Run terraform plan with aws-vault
  infra-apply          Apply terraform plan with aws-vault
  infra-destroy        Destroy infra with aws-vault
  deploy-infra         Run deploy_infra.sh with aws-vault
  run-pipeline         Run pipeline script with aws-vault
  monitor              Run monitoring script with aws-vault
  clean                Clean Terraform state (PowerShell)
  clean-dry            Dry-run clean Terraform state (PowerShell)
  package-lambda       Package Lambda into zip
  fmt                  Format Terraform code
  validate             Validate Terraform code
  bootstrap            Deploy infra, run pipeline, monitor
  help                 Show this help message
```

### Common Workflows

```bash
# Deploy infrastructure
make deploy-infra

# Run the pipeline
make run-pipeline

# Monitor pipeline logs
make monitor

# Destroy infrastructure
make infra-destroy
```

---

## 🔍 How It Works

1. **Ingestion:** Bash script pulls dataset and uploads to S3 ingest bucket.
2. **Processing:** S3 event triggers Lambda, which processes and stores data.
3. **Storage:** Processed data saved to S3 processed bucket (or DynamoDB).
4. **Monitoring:** CloudWatch logs checked for errors; optional alerts sent.

---

## 🧪 Testing

- Add unit tests for Lambda functions (e.g., with `pytest`)
- Add integration tests for pipeline execution

---

## 📊 Monitoring & Troubleshooting

- **Check logs:**
  ```bash
  aws logs tail /aws/lambda/<function-name>
  ```
- **Common issues & fixes:**
  - _AccessDenied_ → Check IAM role permissions.
  - _Bucket not found_ → Verify Terraform applied successfully.

---

## 📈 Future Improvements

- Add CI/CD pipeline
- Support multiple data sources
- Add cost monitoring

---

## 📜 License

This project is licensed under the [MIT License](../LICENSE).

---

## 🙌 Acknowledgements

- Inspiration, references, or libraries used

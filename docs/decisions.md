# 🧠 Decision Log

A running record of key technical and design decisions for this project.  
Each entry captures the context, the choice made, and the consequences — so future‑me (or anyone reading) understands the “why” behind the “what.”

## 📌 How to Use This Log

- Add a new entry whenever you make a significant decision.
- Keep entries short but clear — bullet points are fine.
- If you change your mind later, add a new entry and mark the old one as **Superseded**.

---

## 📝 Entries

### Use locals for global tags instead of Terraform `default_tags`

**Context:**  
Needed a consistent tagging strategy across AWS resources. Terraform’s `default_tags` feature applies tags at the provider level but can be harder to override per resource and doesn’t translate well to multi‑provider setups.

**Decision:**  
Define `local.global_tags` and explicitly merge them into each resource’s `tags` block.

**Rationale:**

- Full control over tag merging and overrides.
- Works across multiple providers, not just AWS.
- Keeps tags explicit in resource definitions, improving clarity and portability.
- Avoids hidden provider‑level behavior that can surprise new contributors.

**Consequences:**

- Slightly more verbose resource definitions (must call `merge()` in each).
- Easier to audit and modify tags without changing provider config.
- Can be wrapped in modules later to reduce repetition.

**Status:**  
Accepted

---

### Remove networking section and modules from root module

**Context:**  
S3, Lambda, and CloudWatch are AWS‑managed services and do not require VPC networking for this pipeline.

**Decision:**  
Remove networking resources entirely from the root module.

**Rationale:**

- Managed services reduce operational overhead.
- No need for subnets, routing tables, or VPC configuration for this architecture.
- Keeps the project lightweight and focused on serverless components.

**Consequences:**

- Networking must be added later if the Lambda function needs access to private VPC resources.

**Status:**  
Accepted

---

### Introduce a Python data generator for test payloads

**Context:**  
Needed a reliable way to generate structured test data for S3 uploads and pipeline validation.

**Decision:**  
Create a standalone Python script that generates JSON payloads and stores them in the `data/` directory.

**Rationale:**

- Ensures consistent, reproducible test inputs.
- Makes it easy to simulate real‑world ingestion scenarios.
- Allows rapid iteration without manually crafting JSON files.
- Keeps test data generation separate from Terraform and Lambda code.

**Consequences:**

- Adds a small Python dependency, but isolated from infrastructure code.
- Enables future enhancements like schema validation or randomized datasets.

**Status:**  
Accepted

---

### Restructure the Lambda directory to separate concerns

**Context:**  
The initial Lambda directory mixed handler code, utilities, and configuration in a single flat structure, making it harder to scale or modify.

**Decision:**  
Refactor the Lambda directory into a clearer structure (e.g., `handlers/`, `utils/`, `models/`, `config/`).

**Rationale:**

- Improves readability and maintainability.
- Makes it easier to add new features or additional Lambda functions.
- Encourages separation of concerns and modular design.
- Aligns with professional Python project structure.

**Consequences:**

- Slightly more directories, but far more clarity.
- Easier to test individual components.
- Future Lambdas can reuse shared utilities.

**Status:**  
Accepted

---

### Use aws‑vault for secure credential management

**Context:**  
Needed a secure, reproducible way to manage AWS credentials across Windows and WSL without storing long‑lived keys in plaintext.

**Decision:**  
Adopt `aws‑vault` as the primary method for authentication and session management.

**Rationale:**

- Eliminates long‑lived credentials from disk.
- Provides MFA‑protected, short‑lived session tokens.
- Works cleanly inside WSL and integrates with Terraform.
- Matches industry best practices for cloud engineering.

**Consequences:**

- Requires entering MFA/passphrase when starting a session.
- Must run Terraform inside an `aws‑vault exec` session or remove `aws‑vault exec` from Makefiles.
- More secure and professional workflow.

**Status:**  
Accepted

---

### Run Terraform inside WSL instead of Windows

**Context:**  
Terraform performance and output formatting were noticeably slower and noisier on Windows compared to WSL.

**Decision:**  
Standardize Terraform execution inside WSL.

**Rationale:**

- Linux filesystem operations are significantly faster for Terraform workloads.
- Cleaner terminal output and ANSI handling.
- Avoids Windows Defender overhead scanning `.terraform` directories.
- Matches production Linux environments more closely.

**Consequences:**

- Terraform commands must be run from WSL terminals.
- Ensures consistent behavior across machines and environments.

**Status:**  
Accepted

---

### Use S3 event notifications instead of EventBridge

**Context:**  
Needed a simple, low‑latency way to trigger the Lambda function when new data is uploaded.

**Decision:**  
Use native S3 → Lambda event notifications.

**Rationale:**

- Lowest latency path for ingestion pipelines.
- No additional services or configuration required.
- Zero cost compared to EventBridge.
- Perfect fit for simple serverless pipelines.

**Consequences:**

- Less flexible than EventBridge for complex routing.
- If future fan‑out or filtering is needed, EventBridge may be introduced later.

**Status:**  
Accepted

---

### Keep Lambda outside a VPC

**Context:**  
The Lambda function only interacts with S3 and CloudWatch, both public AWS services.

**Decision:**  
Deploy Lambda without VPC attachment.

**Rationale:**

- Faster cold starts.
- No need for NAT gateways or VPC networking.
- Simpler architecture and lower cost.
- Matches AWS best practices for public‑service‑only Lambdas.

**Consequences:**

- Lambda cannot access private VPC resources unless networking is added later.

**Status:**  
Accepted

---

### Use separate S3 buckets for ingest and processed data

**Context:**  
Needed a clean separation between raw input data and processed output.

**Decision:**  
Create two buckets: one for ingestion, one for processed artifacts.

**Rationale:**

- Clear separation of concerns.
- Easier debugging and auditing.
- Prevents accidental overwrites or mixing of data.
- Scales naturally as pipeline complexity grows.

**Consequences:**

- Slightly more Terraform resources.
- Enables future multi‑stage pipelines.

**Status:**  
Accepted

---

### Set CloudWatch log retention instead of infinite retention

**Context:**  
By default, CloudWatch log groups retain logs forever, which can lead to unnecessary storage costs and clutter.

**Decision:**  
Explicitly set a retention period on Lambda log groups.

**Rationale:**

- Controls long‑term cost.
- Keeps CloudWatch clean and manageable.
- Matches real‑world production practices.

**Consequences:**

- Old logs are automatically deleted after the retention window.
- If long‑term audit logs are needed, they must be exported to S3.

**Status:**  
Accepted

---

### Use fixed naming conventions via locals

**Context:**  
Terraform‑generated names (especially for Lambda functions) often include random suffixes, which cause new CloudWatch log groups to be created on each deployment.

**Decision:**  
Define naming patterns in `locals` (e.g., `local.prefix`, `local.env`, `local.lambda_name`) and use them consistently across resources.

**Rationale:**

- Ensures stable resource names across deployments.
- Prevents unnecessary log group churn.
- Makes it easier to search, monitor, and debug resources.
- Centralizes naming logic in one place.

**Consequences:**

- Must avoid name collisions when deploying multiple environments.
- Requires careful planning for multi‑env naming (dev/stage/prod).

**Status:**  
Accepted

---

### Destroy infrastructure after testing to control cost

**Context:**  
This project is exploratory and not running in a production environment.

**Decision:**  
Destroy the pipeline after each test cycle to avoid unnecessary AWS charges.

**Rationale:**

- S3 storage, Lambda logs, and CloudWatch retention can accumulate over time.
- Keeps monthly AWS bill near zero.
- Reinforces cost‑conscious engineering habits.

**Consequences:**

- Must re‑deploy before each new test cycle.
- Terraform state must remain clean and consistent.

**Status:**  
Accepted

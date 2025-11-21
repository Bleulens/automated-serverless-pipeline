# 🧠 Decision Log

_A running record of key technical and design decisions for this project. Each entry captures the context, the choice made, and the consequences — so future‑me (or anyone reading) understands the “why” behind the “what.”_

## 📌 How to Use This Log

- Add a new entry whenever you make a significant decision.
- Keep entries short but clear — bullet points are fine.
- If you change your mind later, add a new entry and mark the old one as **Superseded**.

## 📝 Entry Template

### YYYY‑MM‑DD — Short Title of Decision

**Context:**  
Briefly describe the situation, problem, or requirement that led to this decision.

**Decision:**  
State the choice you made.

**Rationale:**  
Why you chose this option over alternatives.

**Consequences:**  
Impacts, trade‑offs, or follow‑up actions required.

**Status:**  
Accepted | Superseded | Proposed

### 2025‑09‑14 — Use locals for global tags instead of Terraform default_tags

**Context:**  
Needed a consistent tagging strategy across AWS resources. Terraform’s default_tags feature applies tags at the provider level, but can be harder to override per resource and doesn’t translate well to multi‑provider setups.

**Decision:**  
Define local.global_tags and explicitly merge them into each resource’s tags block.

**Rationale:**

- Full control over tag merging and overrides.
- Works across multiple providers, not just AWS.
- Keeps tags explicit in resource definitions, improving clarity and portability.
- Avoids hidden provider‑level behavior that can surprise new contributors.

**Consequences:**

- Slightly more verbose resource definitions (must call merge() in each).
- Easier to audit and modify tags without changing provider config.
- Can be wrapped in modules later to reduce repetition.

**Status:**  
Accepted

### 2025‑09‑14 — Remove networking section and modules from root module

**Context:**  
I forgot that S3, lambda, and cloudwatch are aws managed resources and therefore don't need to be setup networking wise.

**Decision:**  
Remove networking section all together.

**Rationale:**

- AWS managed resources were created to reduce overhead in production.
- Networking like subnets, vpc, and routing tables aren't needed in this particular setup.
- In production this gets data pipelines up and running faster while still being secure.

**Consequences:**

- I would need to add networking if I wanted to connect the lambda function to private internal resources inside of a vpc.

**Status:**  
Accepted

---
service: Meta
category: Guidelines
difficulty_levels: ["All"]
aws_exam_relevance: ["All"]
maturity_tier: N/A
last_validated_date: "2026-08-29"
version: "1.0"
cross_references: []
---

# Contribution and Extensibility Guide

This guide explains how to add new AWS services, update existing ones, and maintain the high quality of this interview preparation repository.

## Adding a New AWS Service

When a new AWS service becomes relevant for DevOps Lead interviews, follow these steps to add it.

### Step 1: Scaffold the Directory and Files

Run the following shell commands to scaffold a new service (replace `<service_name>` with the lowercase service identifier):

```bash
SERVICE="<service_name>"
mkdir -p services/$SERVICE
touch services/$SERVICE/overview.md
```

### Step 2: Use the Template

Paste the following template into `overview.md`:

```markdown
---
service: [Service Name]
category: [Compute/Storage/Networking/etc.]
difficulty_levels: ["L1", "L2", "L3", "L4"]
aws_exam_relevance: ["AWS Certified DevOps Engineer - Professional"]
maturity_tier: [Core/Emerging]
last_validated_date: "YYYY-MM-DD"
version: "1.0"
cross_references:
  - ../other_service/overview.md
---

# [Service Name] Deep Dive for DevOps Leads

## 1. Core Concepts & Overview
> **Quick Summary:** [1-3 sentences describing the service and its primary use case in DevOps.]

## 2. Interview Questions

### Q1: [Question Title]
**Level:** L2 | **Category:** conceptual
**Target Services:** [[Service Name]]

> **Quick Answer:** [1-3 sentences]

#### Detailed Answer
[Comprehensive explanation]
<details>
<summary>View Code Example (Terraform/CloudFormation/CLI)</summary>

\`\`\`hcl
# Code here
\`\`\`
</details>

#### Follow-up Questions
- [Follow-up 1]

#### Related Services
- [Link to related services]

#### References
- [AWS Documentation Link]
```

### Step 3: Quality Checklist for New Content

Before submitting a Pull Request, ensure:
- [ ] YAML frontmatter is complete and accurate.
- [ ] All questions follow the required format exactly.
- [ ] Answers provide DevOps Lead-level depth (IaC, Multi-account, Security, CI/CD).
- [ ] Code snippets are syntax highlighted.
- [ ] Long answers or extensive code blocks use `<details><summary>` tags.
- [ ] Cross-references use relative paths correctly.
- [ ] The service is added to `meta/progress-tracker.md`.

## Cross-Referencing Guidelines

- Always use relative paths (e.g., `../vpc/overview.md`).
- Link to specific headers if relevant (e.g., `../iam/overview.md#cross-account-roles`).

## Versioning Strategy

- Update the `last_validated_date` in the frontmatter whenever you verify the content against the latest AWS updates.
- Increment the `version` string if significant structural changes or major feature additions are made.

## Content Style Guide

- **Tone:** Professional, authoritative, and direct. Tailored for Senior/Lead engineers.
- **Formatting:** Use bolding for emphasis on key AWS terms (e.g., **Transit Gateway**, **SCP**).
- **Code:** Prefer Terraform (HCL) and AWS CLI examples for infrastructure questions. Python (Boto3) is acceptable for automation/Lambda questions.

---
service: AWS Secrets Manager
category: Security, Identity, & Compliance
difficulty_levels: L1-L2
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../systems-manager-ssm/overview.md
---

# AWS Secrets Manager Interview Questions: Basics

### Q1: What is AWS Secrets Manager?
**Level:** L1 | **Category:** conceptual
**Target Services:** Secrets Manager

> **Quick Answer:** AWS Secrets Manager is a service that helps you securely store, manage, retrieve, and rotate secrets like database credentials and API keys.

### Q2: How does Secrets Manager differ from AWS Systems Manager (SSM) Parameter Store?
**Level:** L2 | **Category:** conceptual
**Target Services:** Secrets Manager, SSM Parameter Store

> **Quick Answer:** While both store sensitive data, Secrets Manager supports built-in automatic credential rotation and cross-account access via resource policies. SSM Parameter Store is primarily for configuration data (though it supports SecureStrings) and standard parameters are free, whereas Secrets Manager has a per-secret monthly cost.

### Q3: What happens when you delete a secret in Secrets Manager?
**Level:** L1 | **Category:** practical
**Target Services:** Secrets Manager

> **Quick Answer:** By default, the secret is scheduled for deletion with a recovery window of 7 to 30 days. You cannot immediately create a new secret with the same name until it is permanently deleted (unless you force delete it via CLI).

### Q4: How do you rotate a database password using Secrets Manager?
**Level:** L2 | **Category:** practical
**Target Services:** Secrets Manager, Lambda

> **Quick Answer:** You configure automatic rotation by specifying a schedule (e.g., 30 days) and assigning an AWS Lambda function that contains the logic to connect to the database, generate a new password, update the database, and update the secret in Secrets Manager.

### Q5: Can Secrets Manager encrypt the secrets it stores?
**Level:** L1 | **Category:** security
**Target Services:** Secrets Manager, KMS

> **Quick Answer:** Yes, all secrets are encrypted at rest by default using AWS KMS. You can use the default AWS-managed key or a Customer Managed Key (CMK).

### Q6: How do applications authenticate to Secrets Manager to retrieve a secret?
**Level:** L1 | **Category:** security
**Target Services:** Secrets Manager, IAM

> **Quick Answer:** Applications use standard AWS IAM roles (e.g., an EC2 instance profile or an ECS task role) to securely call the `GetSecretValue` API without needing hardcoded AWS credentials.

### Q7: What is the maximum size of a secret in Secrets Manager?
**Level:** L2 | **Category:** conceptual
**Target Services:** Secrets Manager

> **Quick Answer:** The maximum size of the secret string or binary data is 64 KB.

### Q8: Can you share a secret with another AWS account?
**Level:** L2 | **Category:** security
**Target Services:** Secrets Manager

> **Quick Answer:** Yes. Secrets Manager supports resource-based policies, allowing you to attach a policy directly to the secret that grants read access to a principal in a different AWS account.

### Q9: What formats can a secret be stored in?
**Level:** L1 | **Category:** practical
**Target Services:** Secrets Manager

> **Quick Answer:** Secrets are typically stored as JSON strings (key-value pairs, ideal for DB credentials) or as raw text/binary data (ideal for certificates or API tokens).

### Q10: Does Secrets Manager support multi-region deployments?
**Level:** L2 | **Category:** architecture
**Target Services:** Secrets Manager

> **Quick Answer:** Yes, Secrets Manager supports Multi-Region Secrets. You can designate a primary secret and replicate it to other regions, ensuring high availability and local read access for global applications.

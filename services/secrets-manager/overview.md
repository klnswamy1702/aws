---
service: AWS Secrets Manager
category: Security, Identity, & Compliance
difficulty_levels: L1-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional, Security Specialty
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../systems-manager-ssm/overview.md
---

# AWS Secrets Manager Overview

AWS Secrets Manager helps you protect secrets needed to access your applications, services, and IT resources. The service enables you to easily rotate, manage, and retrieve database credentials, API keys, and other secrets throughout their lifecycle. Users and applications retrieve secrets with a call to Secrets Manager APIs, eliminating the need to hardcode sensitive information in plain text.

## Key Concepts

### Secret Rotation
Secrets Manager offers built-in integration for rotating credentials for AWS services like Amazon RDS, Redshift, and DocumentDB. You can also configure a custom AWS Lambda function to rotate secrets for other APIs or custom databases. Rotation ensures that long-lived credentials don't become a security liability.

### Cross-Account Access
Since Secrets Manager supports resource-based policies, you can easily share secrets across different AWS accounts within your organization, allowing a central security account to manage database credentials that are accessed by workload accounts.

### Multi-Region Secrets
You can replicate secrets across multiple AWS Regions. The replicas remain in sync with the primary secret. If a rotation occurs in the primary region, the new secret value is automatically propagated to all replicas, facilitating multi-region high availability architectures.

### Dynamic References in IaC
CloudFormation supports resolving secrets securely at runtime using dynamic references (e.g., `{{resolve:secretsmanager:SecretId:SecretString:jsonKey}}`). This keeps the actual secret value out of the CloudFormation template and state files.

### Pricing Model
Unlike Systems Manager (SSM) Parameter Store standard parameters which are free, Secrets Manager charges per secret stored per month, plus a fee per 10,000 API calls.

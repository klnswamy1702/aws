---
service: AWS Secrets Manager
category: Security, Identity, & Compliance
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, Security Specialty
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../secrets-manager/overview.md
---

# AWS Secrets Manager Best Practices

## Secret Lifecycle
- **Automate Rotation**: Always enable automatic rotation for database credentials. Set the rotation schedule based on your organization's compliance requirements (e.g., every 30, 60, or 90 days).
- **Avoid Hardcoding**: Never hardcode secrets in application code or configuration files. Use the AWS SDK to retrieve them dynamically at runtime.

## Security and Access Control
- **Least Privilege**: Use IAM policies to restrict `secretsmanager:GetSecretValue` to only the specific Lambda execution roles, ECS task roles, or EC2 instance profiles that absolutely need them.
- **Resource Policies**: Use resource-based policies on the secret itself to enforce conditions, such as restricting access to specific VPC endpoints or denying access from outside your AWS Organization.
- **KMS Encryption**: By default, secrets are encrypted with the AWS managed key `aws/secretsmanager`. For production secrets, use a Customer Managed Key (CMK) in KMS. This allows you to define a separate layer of access control via the KMS Key Policy.

## Architecture and Cost
- **Client-side Caching**: Use the AWS Secrets Manager client-side caching libraries (available in Java, Python, Go, etc.) to cache secrets in memory. This drastically reduces the number of API calls made to Secrets Manager, lowering costs and improving application latency.
- **VPC Endpoints**: If your compute resources are in a private subnet, configure an Interface VPC Endpoint (AWS PrivateLink) for Secrets Manager so traffic doesn't traverse the public internet or require a NAT Gateway.

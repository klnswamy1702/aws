---
service: AWS Systems Manager
category: Management & Governance
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../systems-manager-ssm/overview.md
---

# AWS Systems Manager Best Practices

## Security and Access
- **Eliminate SSH/RDP**: Disable inbound port 22 and 3389 across your entire VPC. Use Session Manager for all interactive administrative access.
- **Session Logging**: Enable session logging to S3 and CloudWatch Logs to ensure a full audit trail of every command executed via Session Manager. Use KMS encryption for these logs.
- **IAM Least Privilege**: Restrict `ssm:StartSession` and `ssm:SendCommand` using condition keys, ensuring users can only target specific instances based on resource tags (e.g., `Environment: Dev`).

## Parameter Store
- **Hierarchical Naming**: Use a hierarchical naming convention for parameters (e.g., `/app-name/environment/db-string`) to easily retrieve all parameters for a specific environment using the `GetParametersByPath` API.
- **SecureStrings**: Always use `SecureString` for sensitive data to encrypt it via AWS KMS.
- **Advanced Parameters**: Use Advanced Parameters if you need to store more than 4KB of data (up to 8KB) or attach parameter policies (like expiration rules).

## Patch Management
- **Patch Baselines**: Define custom Patch Baselines rather than using the AWS defaults to control exactly which classifications and severities of patches are automatically approved, and with what delay (e.g., approve critical patches after 3 days).
- **Maintenance Windows**: Schedule Patch Manager tasks to run during specific maintenance windows to minimize disruption to production workloads.

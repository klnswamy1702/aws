---
service: AWS Secrets Manager
category: Security, Identity, & Compliance
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../secrets-manager/overview.md
---

# AWS Secrets Manager Common Issues & Troubleshooting

## 1. AccessDeniedException when retrieving a secret
- **Cause 1**: The IAM role lacks `secretsmanager:GetSecretValue`.
- **Cause 2**: If the secret is encrypted with a custom KMS key, the IAM role must ALSO have `kms:Decrypt` permission on that specific KMS key.
- **Cause 3**: A resource-based policy on the secret is explicitly denying access.
- **Troubleshooting**: Check the exact error message and review CloudTrail logs.

## 2. Automatic Rotation Failing
- **Issue**: The secret rotation Lambda function fails to execute, and the secret remains unrotated.
- **Troubleshooting Checklist**:
  1. **Network Access**: The rotation Lambda needs to communicate with BOTH the Secrets Manager endpoint and the target database. If the Lambda is in a private VPC, ensure it has a route to a NAT Gateway or a VPC Endpoint for Secrets Manager.
  2. **Permissions**: The Lambda execution role must have permissions to access Secrets Manager and the KMS key.
  3. **Security Groups**: Ensure the Lambda's Security Group can reach the database's Security Group on the correct port.

## 3. High Latency when Fetching Secrets
- **Cause**: The application is making a synchronous API call to Secrets Manager for every single web request, leading to network overhead and throttling.
- **Solution**: Implement client-side caching using the AWS provided caching libraries, or cache the secret in memory within your application code for a short duration (e.g., 5 minutes).

## 4. Secret Scheduled for Deletion
- **Issue**: You attempt to create a secret with a specific name, but get an error that the secret already exists, even though it's not visible in the console.
- **Cause**: Secrets are soft-deleted by default with a recovery window (7 to 30 days). 
- **Solution**: You must either permanently delete it using the CLI `delete-secret --force-delete-without-recovery`, restore the secret and overwrite it, or use a different name.

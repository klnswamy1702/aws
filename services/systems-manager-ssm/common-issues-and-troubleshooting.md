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

# AWS Systems Manager Common Issues & Troubleshooting

## 1. EC2 Instance Does Not Appear in Fleet Manager
- **Issue**: You launched an EC2 instance, but it is not listed as a "Managed Node" in Systems Manager.
- **Troubleshooting Checklist**:
  1. **SSM Agent**: Ensure the SSM Agent is installed and running on the instance (it is pre-installed on Amazon Linux 2, Ubuntu Server, and Windows Server AMIs).
  2. **IAM Role**: The instance profile MUST have the `AmazonSSMManagedInstanceCore` managed policy attached. Without this, the agent cannot register with the service.
  3. **Network**: The instance needs outbound internet access to reach the SSM endpoints. If in a private subnet, ensure it has a route to a NAT Gateway OR configure VPC Interface Endpoints for SSM (`ssm`, `ssmmessages`, and `ec2messages`).

## 2. Session Manager Connection Fails
- **Issue**: Clicking "Connect" via Session Manager hangs or returns an error.
- **Cause**: Often caused by missing `ssmmessages` VPC endpoint in private subnets without NAT, or the IAM user attempting the connection lacks `ssm:StartSession` permissions.
- **Solution**: Verify network path and IAM permissions for both the EC2 instance role and the human user.

## 3. Run Command Execution Fails Silently or Times Out
- **Issue**: A Run Command task is sent, but the status becomes Failed or Timed Out without showing output.
- **Cause**: The command might be running a blocking process, waiting for user input, or the SSM agent might have crashed.
- **Solution**: Send the command output directly to an S3 bucket or CloudWatch log group. Do not rely on the truncated console output for debugging complex scripts.

## 4. Parameter Store Decryption Error
- **Issue**: An application gets an `AccessDeniedException` or `KMS.NotFoundException` when retrieving a `SecureString`.
- **Cause**: The application role has `ssm:GetParameter` but lacks `kms:Decrypt` for the KMS key used to encrypt the parameter.
- **Solution**: Update the IAM Role (and the KMS Key policy if it's a Customer Managed Key) to grant decryption rights.

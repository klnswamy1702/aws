---
service: AWS Secrets Manager
category: Security, Identity, & Compliance
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../secrets-manager/overview.md
---

# AWS Secrets Manager Hands-on Labs

## Lab 1: Storing and Retrieving Secrets via SDK
- **Objective**: Learn how to create a secret and fetch it programmatically.
- **Tasks**:
  1. Create a secret containing a dummy API key in the AWS Console.
  2. Write a Python script using `boto3`.
  3. Use the `get_secret_value` API call to fetch the secret and parse the JSON string.
  4. Implement basic error handling for `ResourceNotFoundException`.

## Lab 2: Automatic RDS Credential Rotation
- **Objective**: Configure AWS to automatically rotate the master password of an RDS instance.
- **Tasks**:
  1. Launch a small MySQL RDS instance.
  2. In Secrets Manager, store the master credentials.
  3. Enable automatic rotation, selecting the built-in AWS Lambda rotation template for MySQL.
  4. Manually trigger a rotation and verify in the RDS console that the password was updated seamlessly.

## Lab 3: Cross-Account Secret Sharing
- **Objective**: Allow an application in Account B to read a secret stored in Account A.
- **Tasks**:
  1. In Account A, create a secret and encrypt it with a Customer Managed KMS Key (CMK).
  2. Update the secret's Resource Policy to allow Account B's role to read it.
  3. Update the KMS Key Policy to allow Account B to decrypt.
  4. In Account B, configure the IAM role to allow `secretsmanager:GetSecretValue` and `kms:Decrypt` targeting Account A's resources.
  5. Test retrieval from Account B.

## Lab 4: Dynamic References in CloudFormation
- **Objective**: Securely pass a database password to an RDS instance during deployment.
- **Tasks**:
  1. Manually create a secret in Secrets Manager containing a database password.
  2. Write a CloudFormation template to deploy an RDS instance.
  3. Use the `{{resolve:secretsmanager:...}}` syntax in the `MasterUserPassword` property instead of passing it as a plaintext parameter.
  4. Deploy the stack and verify the password does not appear in the CloudFormation template outputs or parameters.

---
service: AWS Secrets Manager
category: Security, Identity, & Compliance
difficulty_levels: L3-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../secrets-manager/overview.md
---

# AWS Secrets Manager Interview Questions: Advanced

### Q1: Explain the four steps involved in the secret rotation process performed by the Lambda function.
**Level:** L4 | **Category:** architecture
**Target Services:** Secrets Manager, Lambda

> **Quick Answer:** The rotation Lambda performs four steps: `createSecret`, `setSecret`, `testSecret`, and `finishSecret`.

#### Detailed Answer
1. **createSecret**: Generates a new random password and stores it in Secrets Manager under a staging label (AWSPENDING).
2. **setSecret**: Connects to the database using the old credentials (AWSCURRENT) and updates the user's password in the database to the new password.
3. **testSecret**: Connects to the database using the new password to verify it works.
4. **finishSecret**: Moves the AWSCURRENT label from the old secret version to the new one. The old version is labeled AWSPREVIOUS.

### Q2: Your application in Account A needs to access a secret in Account B. Both accounts are in the same AWS Organization. You updated the secret's Resource Policy to allow Account A, but you still get AccessDenied. What are you missing?
**Level:** L3 | **Category:** troubleshooting
**Target Services:** Secrets Manager, IAM, KMS

> **Quick Answer:** Cross-account access requires explicit Allow permissions in multiple places. You must update the IAM Role in Account A, the Resource Policy on the Secret in Account B, AND if the secret is encrypted with a CMK, the KMS Key Policy in Account B must allow Account A to decrypt. 

#### Detailed Answer
If the secret uses the default AWS-managed KMS key (`aws/secretsmanager`), cross-account access will fail because AWS-managed keys cannot be shared across accounts. You must re-encrypt the secret with a Customer Managed Key (CMK) and share that CMK.

### Q3: How do you securely pass a Secrets Manager secret to a Docker container running on Amazon ECS (Fargate) without exposing it in the environment variables visible in the AWS Console?
**Level:** L3 | **Category:** security
**Target Services:** Secrets Manager, ECS

> **Quick Answer:** Use the `secrets` parameter in the ECS Task Definition to reference the Secrets Manager ARN. ECS will automatically resolve the secret and inject it securely into the container at startup.

#### Detailed Answer
Do not use the `environment` parameter, as those values are logged and visible in the console. By using `secrets`, the ECS agent fetches the secret using the Task Execution Role. Ensure the Task Execution Role has `secretsmanager:GetSecretValue` and `kms:Decrypt` permissions.

### Q4: An application experiences intermittent database connection failures immediately after a scheduled secret rotation. What is the likely cause and how do you fix it?
**Level:** L3 | **Category:** troubleshooting
**Target Services:** Secrets Manager

> **Quick Answer:** The application is likely caching the old password in memory or in a connection pool and is not reacting gracefully to the rotation. 

#### Detailed Answer
To fix this, the application code must be updated to catch authentication exceptions from the database. Upon catching the exception, the application should flush its connection pool, invalidate its local cache, call Secrets Manager to fetch the fresh `AWSCURRENT` credentials, and reconnect.

### Q5: Can you rotate a secret for a database hosted on-premises or in another cloud provider using Secrets Manager?
**Level:** L3 | **Category:** architecture
**Target Services:** Secrets Manager, Lambda

> **Quick Answer:** Yes, by writing a custom Lambda rotation function that contains the specific networking and API logic required to reach and update the external database, provided the VPC has the correct routing (e.g., via VPN or Direct Connect).

### Q6: How does Secrets Manager handle concurrent rotation requests or failures during the rotation process?
**Level:** L4 | **Category:** architecture
**Target Services:** Secrets Manager

> **Quick Answer:** Secrets Manager uses staging labels (`AWSPENDING`, `AWSCURRENT`, `AWSPREVIOUS`). If a rotation fails at step 2 or 3, the `AWSCURRENT` label remains on the old password, ensuring the application doesn't break. Secrets Manager will retry the rotation later.

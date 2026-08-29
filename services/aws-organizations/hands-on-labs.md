---
service: AWS Organizations
category: Management & Governance
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, Security Specialty
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../aws-organizations/overview.md
---

# AWS Organizations Hands-on Labs

## Lab 1: Multi-Account Structure and SCPs
- **Objective**: Create an OU hierarchy and restrict regional deployments.
- **Tasks**:
  1. Create a `Non-Prod` OU and a `Prod` OU.
  2. Create a new member account and place it in the `Non-Prod` OU.
  3. Write an SCP that denies `ec2:RunInstances` in any region other than `us-east-1` and `us-west-2`.
  4. Attach the SCP to the `Non-Prod` OU and verify the restriction by attempting to launch an EC2 instance in `eu-central-1`.

## Lab 2: Automated Baselines with CloudFormation StackSets
- **Objective**: Deploy standard IAM roles to all accounts in an OU.
- **Tasks**:
  1. In the Management Account, enable trusted access for CloudFormation StackSets.
  2. Create a StackSet with a template that creates an `AuditRole`.
  3. Deploy the StackSet targeting the `Prod` OU.
  4. Move a new account into the `Prod` OU and observe StackSets automatically deploying the `AuditRole` into it.

## Lab 3: Centralized CloudTrail Logging
- **Objective**: Collect API activity from all member accounts into a central S3 bucket.
- **Tasks**:
  1. Create a dedicated `SecurityTooling` AWS account.
  2. Create an S3 bucket in this account with a bucket policy allowing AWS Organizations `PrincipalOrgID` to write to it.
  3. From the Management Account, create an Organization CloudTrail, pointing it to the central S3 bucket.
  4. Verify logs from member accounts are appearing in the bucket.

## Lab 4: Delegated Administrator Configuration
- **Objective**: Delegate AWS Security Hub management to a security account.
- **Tasks**:
  1. Register the `SecurityTooling` account as the delegated administrator for Security Hub via the Management account.
  2. Log into the `SecurityTooling` account and enable Security Hub.
  3. Auto-enable Security Hub for all existing and future member accounts within the Organization.

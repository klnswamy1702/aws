---
service: AWS Systems Manager
category: Management & Governance
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../systems-manager-ssm/overview.md
---

# AWS Systems Manager Hands-on Labs

## Lab 1: Replacing SSH with Session Manager
- **Objective**: Securely connect to a private EC2 instance without opening port 22.
- **Tasks**:
  1. Launch an EC2 instance in a private subnet (no public IP, no SSH keypair, default security group).
  2. Attach an IAM role with `AmazonSSMManagedInstanceCore`.
  3. Create VPC Endpoints for SSM, EC2Messages, and SSMMessages.
  4. Use the AWS Management Console to start a Session Manager shell on the instance.

## Lab 2: Automating OS Patching
- **Objective**: Create a patching schedule for a fleet of instances.
- **Tasks**:
  1. Tag two EC2 instances with `PatchGroup: WebServers`.
  2. Create a custom Patch Baseline approving critical updates after 2 days.
  3. Register the `WebServers` patch group with the baseline.
  4. Create a Maintenance Window and assign a Patch Manager task to scan and install updates during the window.

## Lab 3: Parameter Store Configuration Injection
- **Objective**: Decouple configuration from code.
- **Tasks**:
  1. Create a hierarchy of parameters: `/myapp/dev/db_user` (String) and `/myapp/dev/db_password` (SecureString).
  2. Write a Python Lambda function.
  3. Use `boto3` `get_parameters_by_path` to fetch the configuration at runtime, decrypting the SecureString.

## Lab 4: Remediation with SSM Automation
- **Objective**: Automatically stop EC2 instances that are launched without an encrypted EBS volume.
- **Tasks**:
  1. Configure an AWS Config rule to check for EBS encryption.
  2. Attach an SSM Automation document (`AWS-StopEC2Instance`) as a remediation action.
  3. Launch an unencrypted instance and watch Config detect and SSM automatically stop it.

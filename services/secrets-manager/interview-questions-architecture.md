---
service: AWS Secrets Manager
category: Security, Identity, & Compliance
difficulty_levels: L4
aws_exam_relevance: Solutions Architect Professional, Security Specialty
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../secrets-manager/overview.md
---

# AWS Secrets Manager Interview Questions: Architecture

### Q1: Architect a highly available, multi-region database solution using RDS Global Database and Secrets Manager. How do you handle credential rotation and application failover?
**Level:** L4 | **Category:** architecture
**Target Services:** Secrets Manager, RDS

> **Quick Answer:** Use Secrets Manager Multi-Region Secrets. Create the primary secret in the primary region linked to the primary RDS instance. Replicate the secret to the secondary region.

#### Detailed Answer
1. **Setup**: The primary region handles the rotation via Lambda. When rotation occurs, Secrets Manager automatically syncs the new credentials to the secondary region replica.
2. **Application Logic**: Applications in the primary region read from the primary secret; applications in the secondary region read from the replica secret.
3. **Failover**: If the primary region goes down, RDS Global Database is promoted in the secondary region. The secondary applications continue using the replica secret (which already has the correct credentials). You then promote the replica secret to a standalone primary secret so it can assume rotation responsibilities.

### Q2: A strict compliance policy dictates that production database credentials must be rotated every 30 days, and absolutely no human (including DBAs) should have access to the production password. How do you implement this?
**Level:** L4 | **Category:** architecture
**Target Services:** Secrets Manager, IAM, RDS

> **Quick Answer:** Create a master DBA account in RDS, store it in Secrets Manager, and use it to dynamically generate short-lived credentials for applications. Deny all IAM users `secretsmanager:GetSecretValue` for this secret.

#### Detailed Answer
1. **Initial Setup**: A CloudFormation template creates the RDS instance with a random master password, immediately storing it in Secrets Manager using dynamic references. 
2. **Access Control**: Use an IAM Resource Policy on the secret that explicitly denies `GetSecretValue` to all principals EXCEPT the automated Lambda rotation function and specific application roles. Even DBAs with `AdministratorAccess` will be denied.
3. **Rotation**: Configure 30-day rotation. 
4. **Human Access**: If a DBA needs access for an emergency, they must use IAM Database Authentication (generating a 15-minute token) rather than accessing the static password, ensuring the static password remains entirely machine-to-machine.

### Q3: You have 5,000 ECS containers that need to fetch secrets on startup. You are hitting Secrets Manager API throttling limits (`ThrottlingException`). How do you re-architect to solve this at scale without compromising security?
**Level:** L4 | **Category:** architecture
**Target Services:** Secrets Manager, ECS

> **Quick Answer:** Implement client-side caching using the AWS Secrets Manager caching library within the application, or deploy a local caching proxy/daemon on the container instances.

#### Detailed Answer
If all 5,000 containers start simultaneously (e.g., during a massive deployment), they will DDoS the Secrets Manager API.
1. **Jitter & Backoff**: Ensure the startup scripts implement exponential backoff and jitter.
2. **Caching**: If the containers are short-lived, consider fetching the secret once in an init-container or using the ECS Task Definition `secrets` block (which handles some rate-limiting). If long-lived, the application code must use the AWS caching library to fetch once and cache in memory for an hour.
3. **VPC Endpoints**: Ensure traffic goes through a VPC Endpoint to reduce network latency and NAT Gateway bottlenecking.

### Q4: How do you design an audit mechanism to alert the security team if a secret has not been rotated within its 90-day compliance window?
**Level:** L4 | **Category:** architecture
**Target Services:** Secrets Manager, AWS Config, EventBridge

> **Quick Answer:** Use the AWS Config managed rule `secretsmanager-rotation-enabled-check` configured with a 90-day maximum parameter.

#### Detailed Answer
1. Enable AWS Config in the account.
2. Deploy the `secretsmanager-rotation-enabled-check` rule and set `maxDaysSinceRotation` to 90.
3. When a secret exceeds this window (e.g., because the rotation Lambda failed silently), Config marks the resource as NON_COMPLIANT.
4. An EventBridge rule listens for Config compliance change events and routes the alert to an SNS topic notifying the security team.

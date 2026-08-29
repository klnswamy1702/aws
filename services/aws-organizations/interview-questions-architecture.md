---
service: AWS Organizations
category: Management & Governance
difficulty_levels: L4
aws_exam_relevance: Solutions Architect Professional, Security Specialty
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../aws-organizations/overview.md
---

# AWS Organizations Interview Questions: Architecture

### Q1: Design a multi-account strategy for a large enterprise deploying applications globally, factoring in centralized networking, security tooling, and developer sandboxes.
**Level:** L4 | **Category:** architecture
**Target Services:** AWS Organizations, Transit Gateway, Control Tower

> **Quick Answer:** Use a foundational OU structure separating core infrastructure from workloads. Define a Security OU (Log Archive, Security Tooling), an Infrastructure OU (Networking, Shared Services), and Workload OUs (Prod, Non-Prod, Sandbox) utilizing Control Tower for baselining.

#### Detailed Answer
1. **Management Account**: Strictly for billing, SCPs, and Organizations management.
2. **Security OU**:
   - `Log Archive Account`: Centralized S3 bucket with immutable CloudTrail and VPC Flow Logs.
   - `Security Tooling Account`: Delegated admin for GuardDuty, Security Hub, Macie.
3. **Infrastructure OU**:
   - `Networking Account`: Houses AWS Transit Gateway, Direct Connect, and centralized egress VPCs. Shares subnets/TGW attachments via AWS RAM.
   - `Shared Services Account`: Active Directory, CI/CD runners, centralized artifact repositories.
4. **Workload OUs** (e.g., `Prod OU`, `Dev OU`):
   - One account per application or business unit per environment to shrink blast radiuses.
5. **Sandbox OU**:
   - Accounts for developers to experiment. Heavy SCPs applied (budget limits, no internet ingress, automatic resource termination via AWS Nuke).

### Q2: An enterprise wants to ensure that no developer can disable CloudTrail, and all EBS volumes must be encrypted across 50 AWS accounts. How do you architect this governance model?
**Level:** L4 | **Category:** architecture
**Target Services:** AWS Organizations, Config, CloudTrail

> **Quick Answer:** Use an SCP at the Organization Root to deny CloudTrail modifications. Use AWS Config Rules (deployed via CloudFormation StackSets) to detect unencrypted EBS volumes, and an SCP to prevent the creation of unencrypted volumes.

#### Detailed Answer
1. **Preventive Control (CloudTrail)**: Apply this SCP at the root to block everyone except a specific emergency admin role:
   ```json
   {
     "Effect": "Deny",
     "Action": ["cloudtrail:StopLogging", "cloudtrail:DeleteTrail"],
     "Resource": "*",
     "Condition": { "StringNotLike": { "aws:PrincipalARN": "arn:aws:iam::*:role/EmergencyAdmin" } }
   }
   ```
2. **Preventive Control (EBS)**: Apply an SCP denying `ec2:RunInstances` and `ec2:CreateVolume` if `ec2:Encrypted` is `false`.
3. **Detective Control**: Enable AWS Config organization-wide. Deploy the managed rule `encrypted-volumes`. If a volume is unencrypted (e.g., existed before the SCP), Config flags it as non-compliant, triggering a Lambda remediation to encrypt it.

### Q3: How do you securely automate "Account Vending" (provisioning new AWS accounts) so they are immediately usable and compliant without manual intervention?
**Level:** L4 | **Category:** architecture
**Target Services:** AWS Organizations, Control Tower, Service Catalog

> **Quick Answer:** Use AWS Control Tower's Account Factory or a custom Service Catalog product. Trigger a Step Functions workflow upon account creation to apply networking baselines and register the account with security services.

#### Detailed Answer
Using Control Tower Account Factory:
1. Administrator requests a new account via Service Catalog.
2. Organizations API creates the account and moves it to the target OU.
3. Control Tower assumes a role, applies standard guardrails (SCPs and Config rules), and provisions SSO access.
4. EventBridge listens for the `CreateManagedAccount` success event and triggers a custom Lambda/Step Functions workflow.
5. The workflow uses CloudFormation StackSets to deploy custom resources (e.g., VPC peering to the Transit Gateway, custom IAM roles, or third-party monitoring agents) into the new account.

### Q4: How do you handle disaster recovery for the Management Account itself?
**Level:** L4 | **Category:** architecture
**Target Services:** AWS Organizations, IAM

> **Quick Answer:** The Management Account cannot be easily replaced or backed up as a single entity. Protect it using strict MFA, hardware security keys, minimal IAM users, and alerting on any login or API activity within it.

#### Detailed Answer
Because the Management Account owns the organization, its compromise is fatal.
1. Protect the root user with a hardware MFA token locked in a physical safe.
2. Create no day-to-day IAM users in the account. Use Identity Center (SSO) with strong MFA.
3. Setup CloudWatch Alarms mapped to an SNS topic that pages the C-Suite/Security leadership if *any* manual login occurs in the Management account.
4. Back up critical SCP code to a separate, isolated version control system outside of AWS.

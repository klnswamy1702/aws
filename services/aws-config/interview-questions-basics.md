---
service: AWS Config
category: security-and-governance
difficulty_levels:
  - L1
  - L2
aws_exam_relevance:
  - AWS Certified Security - Specialty
  - AWS Certified DevOps Engineer - Professional
maturity_tier: core
last_validated_date: "2026-08-29"
version: "1.0"
---

# AWS Config: Basics & Core Concepts

### Q1: What is the primary purpose of AWS Config?
**Level:** L1 | **Category:** conceptual
**Target Services:** AWS Config

> **Quick Answer:** AWS Config is used to assess, audit, and evaluate the configurations of your AWS resources, providing a detailed history of configuration changes.

#### Detailed Answer
It acts as a configuration management database (CMDB) for your AWS environment. It continuously monitors resources, records their state, and evaluates them against rules to determine compliance. 

### Q2: How does AWS Config differ from AWS CloudTrail?
**Level:** L1 | **Category:** conceptual
**Target Services:** Config, CloudTrail

> **Quick Answer:** CloudTrail logs the API calls (Who did what, when?), while Config tracks the state and configuration of resources over time (What did the resource look like before and after?).

#### Detailed Answer
If a user modifies a Security Group:
- **CloudTrail:** Logs the `AuthorizeSecurityGroupIngress` API call, the IAM user who made it, and their IP address.
- **AWS Config:** Records the previous state of the Security Group, the new state, and evaluates if the new state violates any security rules (e.g., exposing port 22 to `0.0.0.0/0`).

### Q3: What are AWS Config Rules?
**Level:** L1 | **Category:** conceptual
**Target Services:** AWS Config

> **Quick Answer:** Config rules evaluate the configuration settings of your AWS resources against desired standards, flagging them as compliant or noncompliant.

#### Detailed Answer
- **Managed Rules:** AWS provides over 300 pre-built rules (e.g., ensuring EBS volumes are encrypted, RDS instances have backups enabled).
- **Custom Rules:** You can write custom rules using AWS Lambda functions (supported in multiple languages) or AWS CloudFormation Guard to handle logic specific to your organization.

### Q4: When is an AWS Config Rule triggered for evaluation?
**Level:** L2 | **Category:** architecture
**Target Services:** AWS Config

> **Quick Answer:** Rules can be triggered either periodically (e.g., every 24 hours) or by configuration changes (event-driven).

#### Detailed Answer
- **Configuration changes (Event-driven):** The rule evaluates the resource immediately when AWS Config detects a change to it. Useful for immediate compliance checks.
- **Periodic:** The rule evaluates resources at a specified frequency (1 hour, 3 hours, 12 hours, 24 hours). Useful for checking resources that don't emit configuration change notifications or for rules involving external API checks.

### Q5: How do you automatically fix a noncompliant resource detected by AWS Config?
**Level:** L2 | **Category:** practical
**Target Services:** Config, SSM

> **Quick Answer:** You can attach AWS Systems Manager (SSM) Automation documents to an AWS Config rule to automatically remediate noncompliant resources.

#### Detailed Answer
When a rule marks a resource as noncompliant, AWS Config can trigger an SSM Automation runbook. For example, if a rule detects an S3 bucket with public read access, an SSM runbook can be executed to modify the bucket ACL and bucket policy to remove public access automatically.

### Q6: What is a Conformance Pack?
**Level:** L2 | **Category:** conceptual
**Target Services:** AWS Config

> **Quick Answer:** A conformance pack is a collection of AWS Config rules and remediation actions packaged together, typically mapped to a specific compliance standard (e.g., PCI-DSS, HIPAA).

#### Detailed Answer
They are deployed using a YAML template. They help you quickly establish a baseline of compliance across an account or an entire AWS Organization without deploying rules one by one.

### Q7: How does an Aggregator work in AWS Config?
**Level:** L2 | **Category:** architecture
**Target Services:** AWS Config, Organizations

> **Quick Answer:** An aggregator collects configuration and compliance data from multiple AWS accounts and regions into a central account, providing a single pane of glass.

#### Detailed Answer
It is essential for multi-account governance. You deploy an aggregator in a central Security or Audit account. If integrated with AWS Organizations, it can automatically pull data from all current and future member accounts across all specified regions.

### Q8: What does AWS Config cost based on?
**Level:** L2 | **Category:** cost-optimization
**Target Services:** AWS Config

> **Quick Answer:** AWS Config charges per Configuration Item (CI) recorded and per Config Rule evaluation.

#### Detailed Answer
Because of this pricing model, highly dynamic resources (like temporary EC2 instances in an Auto Scaling Group) can generate a massive number of CIs and trigger many rule evaluations, leading to unexpected costs. You must carefully select which resource types AWS Config should record.

### Q9: Can AWS Config track resources that are deleted?
**Level:** L1 | **Category:** practical
**Target Services:** AWS Config

> **Quick Answer:** Yes, AWS Config maintains a timeline of the resource, including its state at the time of deletion.

#### Detailed Answer
When a resource is deleted, Config records a final Configuration Item indicating the resource is gone. This allows you to view historical configurations of resources that no longer exist, which is critical for incident investigations.

### Q10: Does AWS Config support third-party or on-premises resources?
**Level:** L2 | **Category:** conceptual
**Target Services:** AWS Config

> **Quick Answer:** Yes, you can use the `PutConfigurationRecorder` API to publish configuration data for custom or third-party resources (like GitHub repositories or on-prem servers) into AWS Config.

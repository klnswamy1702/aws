---
service: CloudTrail
category: security-and-governance
difficulty_levels:
  - L3
  - L4
aws_exam_relevance:
  - AWS Certified Security - Specialty
  - AWS Certified Solutions Architect - Professional
maturity_tier: core
last_validated_date: "2026-08-29"
version: "1.0"
---

# AWS CloudTrail: Architecture Questions

### Q1: Architect a multi-account log archival solution using CloudTrail. What are the key AWS services required and how do they interact?
**Level:** L4 | **Category:** architecture
**Target Services:** CloudTrail, Organizations, S3, KMS, IAM

> **Quick Answer:** Use an AWS Organizations-level CloudTrail to write all member account logs to a central S3 bucket in a dedicated Log Archive account. Use a multi-region KMS Customer Managed Key (CMK) for encryption and S3 Object Lock for WORM compliance.

#### Detailed Answer
In a robust, multi-account setup (often modeled after AWS Control Tower):
1. **Organization Trail:** Deployed from the AWS Organizations Management account or a delegated administrator. This ensures every account in the organization, including new ones, automatically has logging enabled.
2. **Centralized Log Bucket:** A strictly governed S3 bucket located in a dedicated "Log Archive" account.
3. **KMS Encryption:** Logs are encrypted with an AWS KMS CMK. The key policy must allow `cloudtrail.amazonaws.com` to `GenerateDataKey` and restrict decryption to authorized security personnel.
4. **Data Integrity:** Enable S3 Object Lock in compliance mode to prevent modification or deletion. Use CloudTrail Log File Validation to detect tampering.
5. **Cost Management:** Implement an S3 Lifecycle Policy to transition data to cheaper storage tiers (e.g., S3 Standard-IA after 30 days, Glacier after 90 days).

### Q2: How does CloudTrail integrate with Amazon EventBridge, and what architectural patterns does this enable?
**Level:** L3 | **Category:** architecture
**Target Services:** CloudTrail, EventBridge, Lambda, Step Functions

> **Quick Answer:** CloudTrail automatically publishes management events to EventBridge. This enables event-driven architectures for real-time security alerts, auto-remediation, and operational automation.

#### Detailed Answer
By default, CloudTrail API activity is sent to the default event bus in EventBridge.
**Common Architectural Patterns:**
- **Auto-remediation:** Match events like `CreateSecurityGroup` or `AuthorizeSecurityGroupIngress`. Send the event to an AWS Lambda function that checks if the rule violates policy (e.g., `0.0.0.0/0` on port 22) and automatically removes the rule.
- **Auditing/Alerting:** Match sensitive API calls like `ConsoleLogin` without MFA, or `DeactivateMFADevice`. Forward these to an SNS topic for immediate security team notification.
- **Workflow Triggers:** Match resource creation events to trigger an AWS Step Functions workflow that initializes the resource (e.g., applying standard tags to a newly launched EC2 instance).

### Q3: Evaluate the use of CloudTrail Lake versus Amazon Athena for log analysis. When would you architect for each?
**Level:** L4 | **Category:** architecture
**Target Services:** CloudTrail, Athena, CloudTrail Lake

> **Quick Answer:** Use CloudTrail Lake for a fully managed, purpose-built auditing solution where ease of use and immediate SQL querying are prioritized. Use Athena for lower cost, longer-term querying where you want to combine CloudTrail data with other datasets (like VPC Flow Logs).

#### Detailed Answer
- **CloudTrail Lake:** 
  - **Pros:** No setup required for S3 buckets, partitions, or data formats. Immutable event data stores (EDS) for up to 10 years. Optimized for CloudTrail JSON schema.
  - **Cons:** Pricing based on ingestion and data scanned can be higher for large volumes.
  - **Use Case:** Security teams needing quick, frictionless querying of recent incidents without worrying about data engineering.
- **Amazon Athena:**
  - **Pros:** Highly customizable. You control the S3 bucket. Allows joining CloudTrail logs with VPC Flow Logs, ALB Access Logs, and custom application logs. Can be significantly cheaper if data is partitioned efficiently (e.g., by region/year/month/day).
  - **Cons:** Requires data engineering effort to set up Glue Data Catalog, partitioning, and handling complex nested JSON.
  - **Use Case:** Mature DevOps environments with existing data lakes and cost-sensitive, large-scale log analysis requirements.

### Q4: How do you handle CloudTrail logging for multi-region and global services like IAM and CloudFront?
**Level:** L3 | **Category:** architecture
**Target Services:** CloudTrail, IAM, CloudFront

> **Quick Answer:** Global service events (like IAM) are typically logged in the US East (N. Virginia) region (`us-east-1`). You must ensure `IncludeGlobalServiceEvents` is enabled in your trail configuration.

#### Detailed Answer
- Services like IAM, STS (global endpoint), and CloudFront operate globally rather than in a specific region.
- When creating a trail via the console, global service events are included by default.
- In CloudTrail logs, these events appear as if they occurred in `us-east-1`. 
- **Architecture Consideration:** If you are filtering logs by region for specific SIEM ingestion, you must ensure you process `us-east-1` logs to capture critical IAM and organization-level changes, even if your workloads run entirely in a different region like `eu-west-1`.

---
service: CloudTrail
category: security-and-governance
difficulty_levels:
  - L3
  - L4
aws_exam_relevance:
  - AWS Certified Security - Specialty
  - AWS Certified DevOps Engineer - Professional
  - AWS Certified Solutions Architect - Professional
maturity_tier: core
last_validated_date: "2026-08-29"
version: "1.0"
cross_references:
  - ../organizations/overview.md
---

# AWS CloudTrail: Advanced & Architecture Questions

### Q1: How do you design a centralized logging architecture for a large enterprise using CloudTrail and AWS Organizations?
**Level:** L4 | **Category:** architecture
**Target Services:** CloudTrail, AWS Organizations, S3, KMS

> **Quick Answer:** Use an Organization Trail configured in a dedicated Log Archive account (Delegated Administrator). Send logs to a centralized S3 bucket with strict bucket policies, versioning, object lock (WORM), and SSE-KMS using a multi-region Customer Managed Key.

#### Detailed Answer
For an L4 DevOps or Architect role, the expectation is a highly secure and tamper-proof design:
1. **Delegated Administration:** Do not use the Management Account for daily operations. Delegate CloudTrail administration to a dedicated Security or Log Archive account.
2. **Organization Trail:** Create a multi-region Org Trail. This forces logging for all existing and newly created accounts. Member accounts cannot disable this.
3. **Storage Tier:** Central S3 bucket in the Log Archive account.
   - Enable S3 Object Lock (Compliance mode) to ensure WORM (Write Once, Read Many).
   - Use Lifecycle policies to transition logs to Glacier Deep Archive after 90 days.
4. **Encryption:** Use a Customer Managed KMS key (CMK). The KMS key policy must allow `cloudtrail.amazonaws.com` to `GenerateDataKey` and member accounts cannot decrypt logs unless explicitly granted.
5. **Monitoring:** Stream events to EventBridge or CloudWatch Logs for real-time alerting (e.g., alerting on `ConsoleLogin` without MFA).

#### Follow-up Questions
- How would you handle a scenario where a new AWS region is added by AWS? (Multi-region trails automatically include new regions).
- What is the performance/cost impact of applying Object Lock?

### Q2: A security incident occurred, and the attacker deleted a CloudWatch Log group containing CloudTrail logs. How do you ensure this doesn't impact your forensic capabilities?
**Level:** L3 | **Category:** troubleshooting/security
**Target Services:** CloudTrail, S3, CloudWatch Logs

> **Quick Answer:** Always retain the primary, immutable copy of CloudTrail logs in a secured S3 bucket with Object Lock and MFA Delete. CloudWatch Logs should only be used for real-time monitoring and alerting, not as the source of truth for compliance.

#### Detailed Answer
CloudTrail can deliver logs to both S3 and CloudWatch Logs concurrently.
If an attacker compromises an account and deletes a CloudWatch Log Group, the original log files remain safe in the central S3 bucket in the Log Archive account.
To further protect the S3 bucket:
- **SCP (Service Control Policies):** Apply an SCP at the Root of the Organization denying `s3:DeleteObject` and `s3:DeleteBucket` for the CloudTrail bucket to all identities except a highly restricted break-glass role.

### Q3: How do you implement real-time automated remediation for unauthorized API calls detected by CloudTrail?
**Level:** L3 | **Category:** practical
**Target Services:** CloudTrail, EventBridge, Lambda, AWS Config

> **Quick Answer:** Route CloudTrail events to Amazon EventBridge. Create an EventBridge Rule matching the specific API call (e.g., `CreateSecurityGroup`), and set the target to an AWS Step Functions state machine or Lambda function that evaluates and remediates the resource.

#### Detailed Answer
<details><summary>EventBridge Pattern Example</summary>

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventSource": ["ec2.amazonaws.com"],
    "eventName": ["AuthorizeSecurityGroupIngress"]
  }
}
```
</details>

When the EventBridge rule matches, it passes the CloudTrail JSON event to a Lambda function. The Lambda extracts the `requestParameters` (e.g., cidrIp: 0.0.0.0/0 on port 22). If this violates policy, the Lambda function can immediately execute a `RevokeSecurityGroupIngress` API call to remove the rule, and send a notification via SNS.

### Q4: Explain how to configure CloudTrail Lake and its advantages over Athena for querying logs.
**Level:** L3 | **Category:** architecture
**Target Services:** CloudTrail Lake, Athena

> **Quick Answer:** CloudTrail Lake is a managed audit and security lake allowing SQL querying without needing to manage complex Athena tables, partitions, or S3 storage schemas.

#### Detailed Answer
With Athena, you must manually manage the S3 bucket, configure the Glue Data Catalog, handle partitioning to optimize query costs, and write complex queries to handle JSON nesting.
CloudTrail Lake abstracts this. You create an Event Data Store (EDS) with a retention period (up to 3653 days / 10 years). It automatically ingests events and provides an optimized SQL engine designed specifically for CloudTrail schema.

**Trade-offs:** CloudTrail Lake pricing is based on data ingested and scanned, which can be expensive. Athena is cheaper if you optimize your partitions, but requires higher operational overhead.

### Q5: How do you track down cross-account IAM Role assumptions in CloudTrail?
**Level:** L4 | **Category:** troubleshooting/security
**Target Services:** CloudTrail, IAM, STS

> **Quick Answer:** You must correlate the `AssumeRole` event in the trusting account (or the attacker's account) with the resulting API calls in the trusted account using the `userIdentity.sessionContext` and `sharedEventID`.

#### Detailed Answer
When User A in Account A assumes Role B in Account B:
1. Account A logs an `AssumeRole` event.
2. Account B logs an `AssumeRole` event.
3. Subsequent actions in Account B are logged with a `userIdentity` type of `AssumedRole`.

To trace this back to the original User A, look at the `userIdentity.sessionContext.sessionIssuer.arn` in the events logged in Account B. If you control both accounts, you can search for the matching `requestID` or access key ID that invoked the `AssumeRole` call.

### Q6: Can you filter what CloudTrail sends to an S3 bucket to save on costs?
**Level:** L3 | **Category:** cost-optimization
**Target Services:** CloudTrail

> **Quick Answer:** Yes, you can use Advanced Event Selectors to finely filter management and data events delivered to S3.

#### Detailed Answer
While basic event selectors only allow filtering by Read/Write and Resource Type, Advanced Event Selectors allow you to filter based on specific API names, ARNs, or even whether an event resulted in an error.
For example, if you have extremely high volume `GetObject` calls for a specific prefix in S3, you can use advanced selectors to exclude that specific prefix `arn:aws:s3:::my-bucket/public-assets/`, while retaining logs for `arn:aws:s3:::my-bucket/sensitive-data/`.

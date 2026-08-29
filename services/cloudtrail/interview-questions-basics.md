---
service: CloudTrail
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
cross_references:
  - ../cloudtrail/overview.md
---

# AWS CloudTrail: Basics & Core Concepts

### Q1: What is the difference between CloudTrail and CloudWatch?
**Level:** L1 | **Category:** conceptual
**Target Services:** CloudTrail, CloudWatch

> **Quick Answer:** CloudTrail answers "Who did what, when, and from where?" by logging API calls, whereas CloudWatch answers "What is the health and performance of my system?" by collecting metrics and logs.

#### Detailed Answer
CloudTrail is an auditing service that records API activity across your AWS account (e.g., a user deleting an EC2 instance). CloudWatch is a monitoring service that collects performance and operational data in the form of logs, metrics, and events (e.g., CPU utilization of an EC2 instance).

#### Follow-up Questions
- How can CloudTrail and CloudWatch work together?
- Can CloudTrail logs be sent to CloudWatch Logs?

#### Related Services
- CloudWatch

### Q2: What are Management Events vs. Data Events in CloudTrail?
**Level:** L1 | **Category:** conceptual
**Target Services:** CloudTrail, S3, Lambda

> **Quick Answer:** Management events log control plane operations like creating or modifying resources, while Data events log high-volume data plane operations like reading/writing objects in S3 or invoking Lambda functions.

#### Detailed Answer
- **Management Events:** Track operations that are performed on resources in your AWS account (e.g., configuring security, setting up VPCs). They are logged by default. You can choose to log Read events, Write events, or both.
- **Data Events:** Track resource operations performed on or within a resource (e.g., S3 `GetObject`, DynamoDB `PutItem`). They are often high-volume, cost extra to log, and are not enabled by default.

<details><summary>Terraform Example: Enabling Data Events</summary>

```hcl
resource "aws_cloudtrail" "example" {
  name                          = "example-trail"
  s3_bucket_name                = aws_s3_bucket.example.id
  include_global_service_events = true

  event_selector {
    read_write_type           = "All"
    include_management_events = true

    data_resource {
      type   = "AWS::S3::Object"
      values = ["arn:aws:s3:::my-bucket/"]
    }
  }
}
```
</details>

### Q3: What is CloudTrail log file integrity validation?
**Level:** L2 | **Category:** security
**Target Services:** CloudTrail

> **Quick Answer:** It is a feature that cryptographically validates that CloudTrail log files have not been modified, deleted, or tampered with after CloudTrail delivered them to S3.

#### Detailed Answer
When enabled, CloudTrail delivers a digest file every hour containing the digital signatures of the log files delivered during that period. The digests are signed with SHA-256 and RSA. Security teams use this to prove chain of custody and non-repudiation in forensic investigations.
To validate logs via CLI:
```bash
aws cloudtrail validate-logs \
    --trail-arn arn:aws:cloudtrail:us-east-1:123456789012:trail/my-trail \
    --start-time 2026-08-01T00:00:00Z \
    --end-time 2026-08-29T00:00:00Z
```

### Q4: How long does CloudTrail retain event history by default?
**Level:** L1 | **Category:** conceptual
**Target Services:** CloudTrail

> **Quick Answer:** CloudTrail provides a default 90-day event history of management events in the AWS Console for free.

#### Detailed Answer
The built-in CloudTrail Event History retains the last 90 days of management (control plane) events. To retain logs beyond 90 days, or to log data events, you must create a Trail that delivers logs to an Amazon S3 bucket, where you can apply S3 Lifecycle policies for long-term retention.

### Q5: Can CloudTrail capture events across all AWS regions?
**Level:** L1 | **Category:** architecture
**Target Services:** CloudTrail

> **Quick Answer:** Yes, a trail can be configured as a multi-region trail to capture events from all AWS regions.

#### Detailed Answer
Creating a multi-region trail is a security best practice. If a malicious actor gains access and attempts to operate in an unused region (e.g., launching crypto-mining EC2 instances in `ap-southeast-2` while your workload is in `us-east-1`), a multi-region trail ensures that those API calls are logged.

### Q6: What are CloudTrail Insights?
**Level:** L2 | **Category:** troubleshooting
**Target Services:** CloudTrail

> **Quick Answer:** CloudTrail Insights helps identify unusual operational activity in your AWS account, such as sudden spikes in resource provisioning or elevated IAM errors, by establishing a baseline of normal behavior and generating events when anomalies occur.

#### Detailed Answer
Insights events are delivered to the CloudTrail console, EventBridge, and your S3 bucket. They are distinct from standard management and data events. For example, if your account typically sees 10 `RunInstances` API calls per day, and suddenly there are 500, CloudTrail Insights will flag this.

### Q7: How do you secure the S3 bucket used by CloudTrail?
**Level:** L2 | **Category:** security
**Target Services:** CloudTrail, S3, KMS

> **Quick Answer:** Secure the bucket by enforcing a strict S3 bucket policy (restricting `s3:PutObject` to the CloudTrail service principal), enabling SSE-KMS encryption, enabling MFA Delete, and restricting access via IAM.

#### Detailed Answer
A secure CloudTrail S3 bucket configuration should include:
1. Bucket Policy that only allows `cloudtrail.amazonaws.com` to write.
2. S3 Block Public Access enabled at the bucket level.
3. Encryption with AWS KMS (SSE-KMS) using a Customer Managed Key (CMK) with a strict key policy.
4. Bucket versioning and MFA Delete enabled to protect against accidental or malicious deletion.

### Q8: How can you query CloudTrail logs stored in S3?
**Level:** L2 | **Category:** practical
**Target Services:** CloudTrail, Athena

> **Quick Answer:** You can use Amazon Athena to run standard SQL queries directly against CloudTrail logs stored in S3. Alternatively, you can use CloudTrail Lake.

#### Detailed Answer
To query logs with Athena, you create an external table pointing to your CloudTrail S3 bucket location, using the CloudTrail SerDe (Serializer/Deserializer) to parse the JSON logs. Athena allows you to filter by IP address, user identity, event name, or resource ARN.

### Q9: Does CloudTrail log SSH or RDP access to EC2 instances?
**Level:** L1 | **Category:** conceptual
**Target Services:** CloudTrail, EC2, SSM

> **Quick Answer:** No, CloudTrail logs AWS API calls, not OS-level access like SSH or RDP.

#### Detailed Answer
To log OS-level interactions, you must use AWS Systems Manager (SSM) Session Manager, which can log session data to S3 or CloudWatch Logs. Alternatively, use an OS-level logging agent (like the CloudWatch Agent) to forward `/var/log/auth.log` or Windows Event Logs to CloudWatch.

### Q10: What is an Organization Trail?
**Level:** L2 | **Category:** architecture
**Target Services:** CloudTrail, AWS Organizations

> **Quick Answer:** An Organization Trail logs all events for all AWS accounts in an AWS Organization into a centralized S3 bucket owned by the management or delegated administrator account.

#### Detailed Answer
It prevents member accounts from tampering with or disabling their logging. Even if a user in a member account has full administrative privileges within that account, they cannot modify the organization trail or delete the centralized S3 bucket because it resides in a different account.

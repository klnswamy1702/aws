---
service: AWS Systems Manager
category: Management & Governance
difficulty_levels: L3-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../systems-manager-ssm/overview.md
---

# AWS Systems Manager Interview Questions: Advanced

### Q1: You have a strict security requirement to record every keystroke and command output from administrative sessions on EC2 instances. How do you implement this?
**Level:** L3 | **Category:** security
**Target Services:** SSM Session Manager, S3, CloudWatch Logs

> **Quick Answer:** Disable SSH access and mandate SSM Session Manager. In the Session Manager preferences, enable session logging and route the output to an S3 bucket or a CloudWatch Log Group for immutable auditing.

#### Detailed Answer
For maximum security, you should also encrypt the log data using a KMS CMK. You can also integrate Session Manager with AWS EventBridge to send alerts when a session starts or ends.

### Q2: How do you manage on-premises servers using AWS Systems Manager?
**Level:** L3 | **Category:** architecture
**Target Services:** Systems Manager (Hybrid Activations)

> **Quick Answer:** Create a "Hybrid Activation" in Systems Manager, which generates an activation code and ID. Install the SSM Agent on the on-premises server and register it using those credentials. 

#### Detailed Answer
The on-premises server will appear in the SSM console as a managed instance with an `mi-` prefix. Ensure the on-premises server has outbound internet access or a Direct Connect/VPN route to SSM VPC Endpoints to communicate with AWS.

### Q3: You need to retrieve a database connection string securely in a CloudFormation template. The string is stored as a SecureString in Parameter Store. How do you do this?
**Level:** L3 | **Category:** practical
**Target Services:** SSM Parameter Store, CloudFormation

> **Quick Answer:** Use a CloudFormation dynamic reference for SSM Secure Strings: `{{resolve:ssm-secure:parameter-name:version}}`.

#### Detailed Answer
Standard CloudFormation parameters of type `AWS::SSM::Parameter::Value<String>` do not support `SecureString` types. The `resolve:ssm-secure` syntax ensures the value is decrypted at runtime by CloudFormation (assuming the CFN execution role has KMS decrypt permissions) and injected into the resource, keeping it out of the template body.

### Q4: An SSM Automation execution fails halfway through a complex 10-step runbook. How does SSM handle the failure, and can you resume it?
**Level:** L4 | **Category:** troubleshooting
**Target Services:** SSM Automation

> **Quick Answer:** By default, the execution stops at the failed step. You can define failure behaviors in the runbook (e.g., Abort, Continue, or trigger another step). You cannot resume a failed execution from the middle; you must fix the issue and run the automation again, so steps must be idempotent.

### Q5: How do you enforce that a developer can only start a Session Manager session on instances tagged with their specific team name?
**Level:** L4 | **Category:** security
**Target Services:** SSM Session Manager, IAM

> **Quick Answer:** Use IAM condition keys (`ssm:resourceTag/TeamName`) in the developer's IAM policy.

#### Detailed Answer
```json
{
  "Effect": "Allow",
  "Action": ["ssm:StartSession"],
  "Resource": "arn:aws:ec2:*:*:instance/*",
  "Condition": {
    "StringEquals": {
      "ssm:resourceTag/TeamName": "BackendTeam"
    }
  }
}
```
This ensures that the `StartSession` API call will be denied if the target instance does not have the exact matching tag.

### Q6: What is the difference between SSM Run Command and SSM State Manager?
**Level:** L3 | **Category:** conceptual
**Target Services:** Systems Manager

> **Quick Answer:** Run Command is imperative and one-off (e.g., "Run this script right now"). State Manager is declarative and continuous (e.g., "Ensure this script runs on boot and re-evaluates every 24 hours to keep the system in this state").

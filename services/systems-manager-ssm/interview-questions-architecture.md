---
service: AWS Systems Manager
category: Management & Governance
difficulty_levels: L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../systems-manager-ssm/overview.md
---

# AWS Systems Manager Interview Questions: Architecture

### Q1: Design a completely private architecture where instances in a private subnet can be managed via Session Manager, download patches, and push custom logs without any internet access (No NAT Gateway).
**Level:** L4 | **Category:** architecture
**Target Services:** Systems Manager, VPC Endpoints, S3, CloudWatch

> **Quick Answer:** Use VPC Interface Endpoints (AWS PrivateLink) for SSM, SSMMessages, EC2Messages, CloudWatch Logs, and a VPC Gateway Endpoint for S3.

#### Detailed Answer
To achieve full isolation:
1. **SSM Connectivity**: Create Interface Endpoints for `com.amazonaws.region.ssm`, `ssmmessages`, and `ec2messages`. This allows the SSM Agent to register and accept Session Manager connections.
2. **Patching & Logging**: Patch Manager often needs to download patches from S3 (where AWS hosts the update repositories) or external sources.
   - For AWS-hosted repos, create a Gateway Endpoint for S3.
   - For external repos (e.g., Canonical for Ubuntu), you either need an internal mirror repository or a NAT Gateway.
3. **Log Shipping**: Create an Interface Endpoint for CloudWatch Logs (`com.amazonaws.region.logs`) so the CloudWatch Agent can push custom metrics and logs privately.

### Q2: You are tasked with building an automated, immutable infrastructure pipeline for baking AMIs that must include the latest security patches, an APM agent, and run CIS hardening scripts. How do you architect this using SSM?
**Level:** L4 | **Category:** architecture
**Target Services:** SSM Automation, EC2 Image Builder

> **Quick Answer:** Use EC2 Image Builder (which uses SSM Automation under the hood). Create a recipe with build components that invoke SSM Run Command documents to install the APM agent, apply patches, and run the CIS scripts.

#### Detailed Answer
EC2 Image Builder simplifies AMI creation by wrapping SSM Automation.
1. **Recipe**: Define an Image Recipe. Include managed components (like AWS-provided patch components) and custom components (shell scripts for CIS hardening).
2. **Pipeline**: Schedule the pipeline to run weekly.
3. **Execution**: Image Builder launches a temporary EC2 instance, uses SSM Run Command to execute the recipe components sequentially, stops the instance, creates an AMI, runs tests against the AMI, and finally distributes it to other regions or accounts via AWS RAM.

### Q3: How do you use SSM Parameter Store to share configuration values dynamically across multiple AWS accounts in an Organization?
**Level:** L4 | **Category:** architecture
**Target Services:** SSM Parameter Store, IAM, Resource Access Manager

> **Quick Answer:** SSM Parameter Store does NOT natively support cross-account sharing via resource policies (unlike Secrets Manager). You must use custom IAM roles or replicate the parameters using EventBridge and Lambda.

#### Detailed Answer
Because Parameter Store lacks resource-based policies:
- **Approach 1 (Pull)**: The consuming account (Account B) assumes an IAM role in the central account (Account A) to read the parameter. This complicates application logic.
- **Approach 2 (Push/Sync)**: Create an EventBridge rule in Account A that listens for SSM Parameter changes. When a parameter updates, it triggers a Lambda function that assumes a role in Account B and writes/updates the parameter in Account B's Parameter Store. This keeps the configuration local for the application.

*(Note: Advanced parameters now have some sharing capabilities via AWS RAM, but standard parameters do not).*

### Q4: Describe an automated incident response architecture for a scenario where an EC2 instance CPU spikes above 90% for 15 minutes. The response should generate a memory dump and then reboot the instance.
**Level:** L4 | **Category:** architecture
**Target Services:** CloudWatch, EventBridge, SSM Automation

> **Quick Answer:** A CloudWatch Alarm triggers an EventBridge rule, which invokes an SSM Automation runbook. The runbook uses Run Command to execute a memory dump script, uploads the dump to S3, and then uses the `AWS-RestartEC2Instance` action.

#### Detailed Answer
1. **Monitor**: CloudWatch Alarm on `CPUUtilization > 90%` for 3 data points (5 mins each).
2. **Route**: The Alarm triggers an EventBridge rule.
3. **Execute**: The rule targets an SSM Automation Document.
4. **Step 1 (Run Command)**: The Automation Document executes a shell script on the instance via Run Command. The script uses tools like `gdb` or `LiME` to dump memory and `aws s3 cp` to move it to a forensic bucket.
5. **Step 2 (API Action)**: The Automation Document executes the `ec2:RebootInstances` API call to recover the instance.
6. **Step 3 (Notify)**: The Automation Document publishes an SNS notification to the DevOps team that the remediation is complete.

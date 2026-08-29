---
service: CloudWatch
category: Management & Governance
difficulty_levels: L4
aws_exam_relevance: Solutions Architect Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../cloudwatch/overview.md
---

# CloudWatch Interview Questions: Architecture

### Q1: Design a central observability platform for a microservices architecture spanning 10 different AWS accounts. The solution must provide a single pane of glass for metrics, logs, and distributed traces without duplicating data ingestion costs.
**Level:** L4 | **Category:** architecture
**Target Services:** CloudWatch, X-Ray

> **Quick Answer:** Use CloudWatch Cross-Account Observability to link the 10 source accounts to a central monitoring account. Enable X-Ray for distributed tracing and use CloudWatch ServiceLens in the central account to correlate traces, metrics, and logs.

#### Detailed Answer
To build this platform:
1. **Centralization**: Create a dedicated Monitoring AWS account. Configure it as a Sink for CloudWatch Cross-Account Observability.
2. **Data Sharing**: In the 10 workload (source) accounts, create Links to the Sink account. This allows the central account to read telemetry data (Logs, Metrics, X-Ray Traces, Application Insights) directly from the source accounts without copying the data, avoiding double ingestion and S3 transfer costs.
3. **Tracing**: Instrument the microservices using the AWS Distro for OpenTelemetry (ADOT) or X-Ray SDK. This propagates trace IDs across service boundaries (e.g., API Gateway -> Lambda -> DynamoDB).
4. **Correlation**: Use **CloudWatch ServiceLens** in the central account. ServiceLens seamlessly integrates X-Ray traces with CloudWatch metrics and logs, allowing an SRE to click on a spike in a latency metric, see the specific distributed trace causing it, and immediately pivot to the exact log lines for that trace.
5. **Dashboarding**: Build custom CloudWatch Dashboards in the central account that query metrics across the source accounts using math expressions and log insights.

#### Follow-up Questions
- How would you handle log retention policies if the central account doesn't actually own the data?
- What if one of the microservices runs on-premises? (Use the CloudWatch Agent and ADOT collector on-prem).

### Q2: How would you design an automated remediation system that isolates compromised EC2 instances when GuardDuty detects malicious behavior, while simultaneously capturing forensic memory dumps?
**Level:** L4 | **Category:** architecture
**Target Services:** EventBridge, Systems Manager, Lambda

> **Quick Answer:** Route GuardDuty findings through EventBridge to trigger a Step Functions state machine. The state machine invokes a Systems Manager Run Command to capture memory, modifies the EC2 Security Group for isolation, and notifies the security team.

#### Detailed Answer
CloudWatch Events (now EventBridge) is the nervous system of AWS architecture:
1. **Detection**: Amazon GuardDuty detects a threat (e.g., EC2 instance communicating with a known command-and-control server).
2. **Routing**: An EventBridge rule filters for GuardDuty findings matching specific severities and routes the JSON event to an AWS Step Functions state machine.
3. **Forensics**: The state machine first triggers an AWS Systems Manager (SSM) Run Command document on the compromised instance (assuming the SSM Agent is installed). This command uses tools like LiME to capture a memory dump and pushes it to a secure S3 bucket.
4. **Containment**: Once the dump is complete, the state machine triggers a Lambda function that removes the instance's existing Security Groups and attaches a "Forensic Isolation" Security Group (which denies all outbound traffic but allows inbound SSH/RDP only from a bastion host).
5. **Notification**: Finally, it publishes a message to an SNS topic alerting the Security Operations Center (SOC).

#### Follow-up Questions
- Why use Step Functions instead of a single Lambda function? (To handle long-running processes like a memory dump which might exceed Lambda's 15-minute timeout).
- How do you ensure the instance cannot communicate out during the memory dump? (Apply a restrictive network ACL temporarily, or capture memory instantly using EBS snapshots if supported by the forensics tool).

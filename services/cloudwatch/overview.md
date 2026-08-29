---
service: CloudWatch
category: Management & Governance
difficulty_levels: L1-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ec2/overview.md
---

# Amazon CloudWatch Overview

Amazon CloudWatch is a monitoring and observability service built for DevOps engineers, developers, site reliability engineers (SREs), and IT managers. CloudWatch provides data and actionable insights to monitor applications, respond to system-wide performance changes, optimize resource utilization, and get a unified view of operational health.

## Key Concepts

### Metrics
Metrics are the fundamental concept in CloudWatch. A metric represents a time-ordered set of data points published to CloudWatch. 
- **Standard Metrics**: EC2 CPU, Disk I/O, Network I/O (but NOT memory/disk space, which require an agent).
- **Custom Metrics**: Published via API or CloudWatch Agent.
- **High-Resolution Metrics**: Metrics published down to 1-second granularity (standard is 1-minute).

### Alarms
Alarms monitor a single CloudWatch metric or the result of a math expression based on CloudWatch metrics.
- **State**: `OK`, `ALARM`, `INSUFFICIENT_DATA`.
- **Composite Alarms**: Combine multiple alarms using logic (AND, OR) to reduce alarm noise.

### CloudWatch Logs
Centralized log management service.
- **Log Groups & Log Streams**: Organize logs. Log retention can be configured.
- **Metric Filters**: Extract numerical data from log events to turn them into metrics.
- **Logs Insights**: A specialized query language to interactively search and analyze log data.

### Events / EventBridge
*Note: CloudWatch Events evolved into Amazon EventBridge, but is conceptually similar.*
Triggers automated actions in response to operational changes or schedules (cron).

### Observability Features
- **Container Insights**: Automated metrics and logs for EKS, ECS, Fargate.
- **Lambda Insights**: System-level metrics for serverless functions.
- **ServiceLens**: Integrates X-Ray tracing with CloudWatch metrics and logs.
- **Synthetics (Canaries)**: Monitor endpoints and APIs continuously using headless browsers.
- **Evidently**: Feature flagging and A/B testing.
- **RUM (Real User Monitoring)**: Collect client-side performance data.
- **Cross-Account Observability**: Search, analyze, and view metrics/logs seamlessly across multiple AWS accounts in a single region.

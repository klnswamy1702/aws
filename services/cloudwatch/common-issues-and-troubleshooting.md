---
service: CloudWatch
category: Management & Governance
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../cloudwatch/overview.md
---

# CloudWatch Common Issues & Troubleshooting

## 1. Missing EC2 Memory and Disk Metrics
- **Issue**: Standard CloudWatch only reports hypervisor-visible metrics (CPU, Network, Disk I/O). It cannot see inside the OS.
- **Solution**: Install and configure the unified CloudWatch Agent on the EC2 instance to push OS-level metrics (memory utilization, disk space, etc.).

## 2. Alarm Stuck in INSUFFICIENT_DATA State
- **Cause 1**: The metric is not being published (e.g., an error metric that only publishes when an error occurs).
  - *Solution*: Set missing data treatment to `ignore` or `good` depending on the use case, or use Metric Math to substitute a 0 (e.g., `FILL(m1, 0)`).
- **Cause 2**: Delay in metric delivery.
  - *Solution*: Use the `M of N` alarm configuration (e.g., 3 out of 5 datapoints) to allow for occasional missing points.

## 3. CloudWatch Agent Fails to Start or Send Data
- **Troubleshooting Checklist**:
  1. Ensure the EC2 instance has an IAM Role with the `CloudWatchAgentServerPolicy` attached.
  2. Verify network connectivity to CloudWatch endpoints (needs internet access via IGW, NAT Gateway, or VPC Endpoints).
  3. Check the agent log file locally (`/opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log`).

## 4. Log Groups Not Created
- **Issue**: Lambda functions or ECS tasks are not creating their corresponding CloudWatch Log Groups.
- **Solution**: Ensure the execution role has `logs:CreateLogGroup`, `logs:CreateLogStream`, and `logs:PutLogEvents` permissions.

## 5. High CloudWatch Costs
- **Troubleshooting**: Check Cost Explorer for API requests (`PutMetricData`) or Logs Ingestion (`PutLogEvents`).
- **Solution**: 
  - Reduce the frequency of custom metric publishing.
  - Disable verbose debugging logs in production.
  - Use VPC Endpoints for CloudWatch Logs/Metrics to avoid NAT Gateway data processing charges.

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

# CloudWatch Best Practices

## Alarm Configuration
- **Use Composite Alarms**: Reduce alert fatigue by combining multiple alarms (e.g., High CPU AND High Memory) into a single composite alarm.
- **Anomaly Detection**: Use CloudWatch Anomaly Detection instead of static thresholds for metrics with predictable patterns (like daily traffic spikes).
- **Missing Data Handling**: Properly configure how missing data is treated (`good`, `bad`, `ignore`, `missing`) based on whether the metric is continuously reported or event-driven.

## Log Management
- **Retention Policies**: Set appropriate log retention policies on Log Groups. By default, logs are kept forever.
- **Structured Logging**: Log in JSON format to take full advantage of CloudWatch Logs Insights querying capabilities.
- **Metric Filters vs Insights**: Use Metric Filters for continuous alarming on specific text patterns. Use Logs Insights for ad-hoc, retrospective debugging.

## Performance and Cost
- **High-Resolution Metrics**: Only use high-resolution (1-second) metrics when strictly necessary, as they cost more.
- **Agent Tuning**: When using the CloudWatch Agent, carefully select which metrics and logs to collect. High frequency collection of a large number of metrics can drive up costs.

## Security
- **Encryption**: Encrypt CloudWatch Log Groups using AWS KMS customer managed keys.
- **IAM Policies**: Use fine-grained IAM policies for pushing and reading logs and metrics. Avoid wildcard resource permissions.

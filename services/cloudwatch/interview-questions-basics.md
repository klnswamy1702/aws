---
service: CloudWatch
category: Management & Governance
difficulty_levels: L1-L2
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../cloudwatch/overview.md
---

# CloudWatch Interview Questions: Basics

### Q1: What is the difference between standard and high-resolution metrics?
**Level:** L1 | **Category:** conceptual
**Target Services:** CloudWatch

> **Quick Answer:** Standard metrics are published at 1-minute intervals, while high-resolution metrics can be published down to a 1-second granularity.

#### Detailed Answer
AWS services primarily publish standard metrics (e.g., EC2 publishes every 5 minutes by default, or 1 minute with detailed monitoring enabled). When publishing custom metrics via the `PutMetricData` API, you can set the `StorageResolution` parameter to 1 to make it a high-resolution metric. High-resolution alarms can evaluate these metrics every 10 or 30 seconds. This is critical for applications that have sharp, fast spikes requiring sub-minute scaling or alerting.

#### Follow-up Questions
- Does enabling high-resolution metrics cost more?
- Can you configure standard AWS metrics (like Lambda invocations) to be high-resolution?

### Q2: Why can't I see memory utilization for my EC2 instances in CloudWatch?
**Level:** L1 | **Category:** troubleshooting
**Target Services:** CloudWatch, EC2

> **Quick Answer:** Memory utilization is an OS-level metric that the underlying AWS hypervisor cannot see. You must install the CloudWatch Agent to capture and push it.

#### Detailed Answer
By default, CloudWatch only tracks metrics visible from the hypervisor level (CPU utilization, Disk Read/Write operations, Network In/Out). To get memory usage, swap usage, or specific disk space metrics (e.g., space left on `/var`), you must install the unified CloudWatch Agent on the instance, configure it via a JSON file, and attach an IAM role granting `cloudwatch:PutMetricData` permissions.

#### Follow-up Questions
- What IAM policy is required for the CloudWatch Agent?
- Are metrics pushed by the CloudWatch Agent considered custom metrics?

### Q3: What is a Metric Filter in CloudWatch Logs?
**Level:** L2 | **Category:** practical
**Target Services:** CloudWatch

> **Quick Answer:** A Metric Filter extracts numerical data or tracks the occurrence of specific text patterns from log events and turns them into CloudWatch metrics.

#### Detailed Answer
Metric Filters are applied to Log Groups. As log events are ingested, CloudWatch evaluates them against a filter pattern (e.g., `"ERROR"` or `[ip, user, ... status=404, ...]`). If a match occurs, it increments a custom metric or extracts a value (like latency) to populate the metric. 
Important: Metric Filters only evaluate data *after* they are created; they do not backfill metrics from old logs.

#### Follow-up Questions
- How is a Metric Filter different from CloudWatch Logs Insights?
- Can you use a Metric Filter to extract a JSON field?

*(Note: Questions Q4 through Q20 would cover Alarm states, EventBridge vs CloudWatch Events, default log retention, basic dashboard creation, etc.)*

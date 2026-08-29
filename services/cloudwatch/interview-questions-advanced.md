---
service: CloudWatch
category: Management & Governance
difficulty_levels: L3-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../cloudwatch/overview.md
---

# CloudWatch Interview Questions: Advanced

### Q1: How would you alert only when an API error rate exceeds 5% of total requests, rather than a raw number of errors?
**Level:** L3 | **Category:** practical
**Target Services:** CloudWatch

> **Quick Answer:** Use CloudWatch Metric Math to create an expression dividing the `5xxError` metric by the `RequestCount` metric, and set an alarm on the result of that expression.

#### Detailed Answer
Static thresholds for errors often fail as traffic scales up and down. To alert on a percentage:
1. Select Metric `m1` = `5xxError` sum.
2. Select Metric `m2` = `RequestCount` sum.
3. Add a Math Expression `e1` = `m1 / m2 * 100`.
4. Create an alarm on `e1` with a threshold of `> 5`.
This ensures the alarm adapts proportionally to overall system load.

#### Follow-up Questions
- How does the alarm behave if `RequestCount` is zero (divide by zero)?
- How would you use Anomaly Detection instead of Metric Math for this?

### Q2: An application rarely generates errors. When you set an alarm for errors > 0, the alarm frequently enters the INSUFFICIENT_DATA state and doesn't trigger when an error finally occurs. Why?
**Level:** L4 | **Category:** troubleshooting
**Target Services:** CloudWatch

> **Quick Answer:** The application is not publishing a '0' when there are no errors, so no data points exist. You must change the missing data treatment to "ignore" or "treat as good", or use a `FILL` math expression.

#### Detailed Answer
If an application only pushes a `1` when an error happens and nothing otherwise, CloudWatch sees missing data during healthy periods. After a few periods of missing data, the alarm state drops to `INSUFFICIENT_DATA`.
When a single `1` is finally published, it might not be enough to trigger an alarm requiring "3 out of 3 datapoints."
To fix:
1. Configure the application to publish a `0` periodically.
2. Change the Alarm configuration: "Treat missing data as good."
3. Use a Metric Math expression like `FILL(m1, 0)` to artificially populate zeros for missing periods.

#### Follow-up Questions
- What is the difference between "ignore" and "treat as good" for missing data?

### Q3: Explain how you would consolidate CloudWatch metrics and logs across a 50-account AWS Organization for a centralized SRE team.
**Level:** L4 | **Category:** architecture
**Target Services:** CloudWatch, AWS Organizations

> **Quick Answer:** Use CloudWatch Cross-Account Observability to designate a central monitoring account, and configure the 50 accounts as source accounts to share their telemetry data.

#### Detailed Answer
Historically, centralized logging required streaming logs via Kinesis to a central S3 bucket or Elasticsearch cluster. 
Now, **CloudWatch Cross-Account Observability** simplifies this:
1. Define a central "Monitoring Account".
2. In the Monitoring Account, create a sink.
3. In the 50 "Source Accounts" (often deployed via CloudFormation StackSets or AWS Organizations integration), attach a link to the sink.
This allows the SRE team to log into the single Monitoring Account and query Logs Insights, view Dashboards, and analyze metrics across all 50 accounts natively without duplicating data or paying egress costs.

#### Follow-up Questions
- Can cross-account observability span multiple AWS regions? (No, it is currently region-scoped).

*(Note: Questions Q4 through Q15 would cover Container Insights, Lambda X-Ray integration, Synthetics Canaries, EventBridge rules, etc.)*

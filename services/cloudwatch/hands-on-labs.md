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

# CloudWatch Hands-on Labs

## Lab 1: Custom Metrics with CloudWatch Agent
- **Objective**: Collect memory and disk utilization metrics from an EC2 instance.
- **Tasks**:
  1. Launch an EC2 Linux instance and attach an IAM role with `CloudWatchAgentServerPolicy`.
  2. Install the `amazon-cloudwatch-agent`.
  3. Run the wizard to create the `config.json` file.
  4. Start the agent and verify custom metrics appear in the CloudWatch console under the `CWAgent` namespace.

## Lab 2: Logs Insights Querying
- **Objective**: Use CloudWatch Logs Insights to analyze application errors.
- **Tasks**:
  1. Deploy a sample Lambda function that generates random JSON logs with simulated HTTP 500 errors.
  2. Open CloudWatch Logs Insights.
  3. Write a query to parse the JSON fields, filter for `status=500`, and group by the `request_id`.
  4. Visualize the error count as a time-series graph.

## Lab 3: Composite Alarms
- **Objective**: Reduce alert fatigue using Composite Alarms.
- **Tasks**:
  1. Create a CPU utilization alarm (>80%).
  2. Create a Network In alarm (>100MB).
  3. Create a Composite Alarm that only triggers if BOTH the CPU and Network alarms are in the `ALARM` state.
  4. Stress test the instance and observe the state transitions.

## Lab 4: Automated Remediation via EventBridge
- **Objective**: Automatically restart a failed EC2 instance.
- **Tasks**:
  1. Create an EventBridge rule that listens for EC2 instance state change to `stopped`.
  2. Set the target to an AWS Systems Manager Automation document (`AWS-RestartEC2Instance`).
  3. Stop the instance manually from the console and watch it automatically restart within seconds.

---
service: Cost Management
category: conceptual
difficulty_levels:
  - L1
  - L2
aws_exam_relevance: DevOps Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
---

# AWS Cost Management - Basic Interview Questions

### Q1: What is AWS Cost Explorer?
**Level:** L1 | **Category:** conceptual

> **Quick Answer:** AWS Cost Explorer is a tool that allows you to view, analyze, and forecast your AWS costs and usage over time using a visual interface.

#### Detailed Answer
It provides default reports that help you understand your cost drivers and usage trends. You can filter and group data by service, linked account, region, or tags.

### Q2: What is the difference between AWS Budgets and AWS Cost Anomaly Detection?
**Level:** L2 | **Category:** conceptual

> **Quick Answer:** AWS Budgets alerts you when costs exceed a predefined static threshold, while Cost Anomaly Detection uses machine learning to alert you when costs deviate from normal historical patterns.

#### Detailed Answer
Budgets are deterministic (e.g., "Alert me if EC2 costs go over $1000"). Anomaly Detection is dynamic (e.g., "Alert me if a developer spins up a massive DB that causes a sudden spike, even if the total is still under budget").

### Q3: What is the AWS Cost and Usage Report (CUR)?
**Level:** L2 | **Category:** conceptual

> **Quick Answer:** The CUR contains the most comprehensive, granular data about your AWS costs, delivering hourly or daily line items directly to an S3 bucket, often used for integration with BI tools like Amazon QuickSight.

### Q4: Explain the difference between Savings Plans and Reserved Instances (RIs).
**Level:** L2 | **Category:** conceptual

> **Quick Answer:** Reserved Instances are tied to specific instance types and regions (capacity reservation), while Compute Savings Plans provide discounts across any instance type, size, region, and compute service (EC2, Fargate, Lambda) based on a monetary commitment.

### Q5: How do Cost Allocation Tags work?
**Level:** L1 | **Category:** practical

> **Quick Answer:** Cost allocation tags categorize resources for billing purposes. Once activated in the Billing console, AWS uses them to organize your resource costs on your cost allocation report.

### Q6: Can AWS Budgets automatically stop resources?
**Level:** L2 | **Category:** practical

> **Quick Answer:** Yes, by configuring Budget Actions.

#### Detailed Answer
You can configure a budget action to apply an IAM policy (to restrict provisioning), attach an SCP (in AWS Organizations), or target specific resources (like stopping an EC2 instance or RDS DB) when a budget threshold is breached.

### Q7: What are Rightsizing Recommendations?
**Level:** L2 | **Category:** optimization

> **Quick Answer:** A feature in Cost Explorer that analyzes your EC2 usage and suggests downsizing underutilized instances or terminating idle ones to save money.

### Q8: What is FinOps?
**Level:** L2 | **Category:** conceptual

> **Quick Answer:** FinOps (Cloud Financial Management) is a cultural practice that brings engineering, finance, and business teams together to maximize the business value of cloud spending.

### Q9: How long is data retained in AWS Cost Explorer?
**Level:** L2 | **Category:** limits

> **Quick Answer:** By default, Cost Explorer shows up to 12 months of historical data, the current month, and forecasts for the next 12 months.

### Q10: Does AWS Free Tier apply globally across an AWS Organization?
**Level:** L2 | **Category:** conceptual

> **Quick Answer:** Yes. The AWS Free Tier limits are aggregated across all accounts in an AWS Organization, not per individual account.

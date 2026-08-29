---
service: Cost Management
category: architecture
difficulty_levels:
  - L3
  - L4
aws_exam_relevance: DevOps Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
---

# AWS Cost Management - Advanced Interview Questions

### Q1: How do you implement automated Cost Anomaly Detection responses at scale?
**Level:** L4 | **Category:** automation

> **Quick Answer:** Route Cost Anomaly Detection SNS notifications to an AWS Lambda function that parses the anomaly JSON payload, identifies the offending resource/account, and either automatically remediates it (e.g., stopping the resource) or posts an actionable message to a Slack channel via chatbot.

### Q2: Explain the concepts of Chargeback vs. Showback in an enterprise AWS environment.
**Level:** L3 | **Category:** conceptual

> **Quick Answer:** Showback involves calculating and reporting cloud costs back to business units for visibility, without actually billing them. Chargeback involves internally billing those business units for their actual cloud consumption. Both rely heavily on strict tagging policies.

### Q3: How do you enforce cost allocation tagging across a multi-account organization?
**Level:** L4 | **Category:** governance

> **Quick Answer:** Implement Service Control Policies (SCPs) or Tag Policies in AWS Organizations to prevent resource creation without required tags, or use AWS Config Rules with auto-remediation to proactively tag resources based on their creator.

#### Detailed Answer
A common pattern is an SCP that denies `ec2:RunInstances` or `s3:CreateBucket` if a tag like `CostCenter` is missing. Alternatively, a Tag Policy can enforce that the `CostCenter` tag must have values from a predefined list (e.g., `Marketing`, `Engineering`).

### Q4: How do you query and analyze massive Cost and Usage Reports (CUR)?
**Level:** L3 | **Category:** architecture

> **Quick Answer:** Configure CUR to output in Parquet format to an S3 bucket, use AWS Glue to catalog the schema, and use Amazon Athena to run SQL queries against the cost data. You can then visualize this with Amazon QuickSight.

### Q5: How do you manage Savings Plans in a multi-account AWS Organization?
**Level:** L3 | **Category:** architecture

> **Quick Answer:** Purchase the Savings Plan in the Management Account. The discount is applied first to the account that purchased it, and any remaining discount is shared across other accounts in the organization, maximizing utilization.

### Q6: What is the Cloud Intelligence Dashboards (CID) framework?
**Level:** L4 | **Category:** architecture

> **Quick Answer:** CID is an open-source AWS framework that deploys a set of QuickSight dashboards built on top of CUR and Athena, providing out-of-the-box advanced FinOps visualizations for large enterprises.

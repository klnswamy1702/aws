---
service: Cost Management
category: architecture
difficulty_levels:
  - L4
aws_exam_relevance: DevOps Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
---

# AWS Cost Management - Architecture Questions

### Q1: Architect a comprehensive FinOps tracking strategy for a massive enterprise migrating 500 applications to AWS.
**Level:** L4 | **Category:** architecture

> **Quick Answer:** Centralize billing via AWS Organizations. Mandate a strict tagging policy via SCPs (`CostCenter`, `AppID`). Export CUR to a central S3 bucket in Parquet format. Use Amazon Athena for querying and QuickSight (Cloud Intelligence Dashboards) for daily showback to application owners. Implement automated anomaly detection mapped to team Slack channels.

#### Detailed Answer
Without governance, a migration of this scale will result in runaway costs. The foundation is tagging. If resources aren't tagged, they cannot be attributed.
- **Enforcement**: SCPs deny resource creation without `AppID`.
- **Visibility**: CUR data is ingested into an Athena data lake.
- **Accountability**: Each App team receives a weekly automated report from QuickSight showing their exact spend and any unused resources.
- **Optimization**: A central FinOps team monitors aggregated data and makes bulk Savings Plan commitments based on stable baseline compute usage.

### Q2: Design a multi-account strategy that strictly prevents non-production environments from incurring high costs.
**Level:** L4 | **Category:** architecture

> **Quick Answer:** Place non-prod accounts in a specific Organizational Unit (OU). Apply SCPs to this OU restricting expensive instance types (e.g., `Deny` `p3/p4/x1` instances) and enforcing AWS Instance Scheduler to turn off instances outside of business hours. Configure AWS Budgets with auto-stop actions for non-prod accounts.

### Q3: How do you handle cost attribution for shared services (e.g., a central transit gateway or shared EKS cluster)?
**Level:** L4 | **Category:** architecture

> **Quick Answer:** You must implement a proportional cost allocation model. For EKS, use tools like Kubecost or AWS Split Cost Allocation Data. For networking, analyze VPC Flow Logs or Transit Gateway byte metrics to determine the percentage of traffic per business unit and distribute the shared cost proportionally in your BI tool.

### Q4: Architect an automated workflow to terminate abandoned or unattached EBS volumes to save costs.
**Level:** L4 | **Category:** architecture

> **Quick Answer:** Create an EventBridge rule running on a schedule that triggers an AWS Lambda function. The function uses the EC2 API to describe volumes, filters for status `available` (unattached), checks a custom tag (e.g., `DoNotDelete`), and if absent, creates a snapshot (for safety) and deletes the volume, sending a summary report via SNS.

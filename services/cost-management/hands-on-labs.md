---
service: Cost Management
category: practical
difficulty_levels:
  - L2
  - L3
aws_exam_relevance: DevOps Professional
---

# AWS Cost Management - Hands-on Labs

1. **Automated Cost Control**: Create an AWS Budget that monitors monthly EC2 spend. Configure a Budget Action that triggers an SNS topic and attaches a restrictive IAM policy to prevent the creation of new EC2 instances when the budget reaches 100%.
2. **Cost and Usage Report (CUR) Analysis**: Enable CUR delivery to an Amazon S3 bucket. Configure AWS Glue to crawl the bucket and use Amazon Athena to write SQL queries that identify the top 5 most expensive AWS services over the last 30 days.

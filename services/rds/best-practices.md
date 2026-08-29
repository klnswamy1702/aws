---
service: RDS
category: Database
difficulty_levels: L2-L4
aws_exam_relevance: High
maturity_tier: Tier 1
last_validated_date: 2023-10-25
version: 1.0
cross_references:
  - ../dynamodb/overview.md
---
# RDS Best Practices

## Security
- **Use IAM Authentication**: Avoid hardcoding database credentials by using IAM database authentication.
- **VPC and Security Groups**: Always deploy RDS instances in private subnets. Restrict inbound access using security groups tied to application tiers.
- **Encryption**: Enable encryption at rest using AWS KMS during instance creation. Enforce encryption in transit (TLS/SSL).

## Performance and Cost Optimization
- **Right-sizing**: Use Compute Optimizer and CloudWatch metrics to choose the appropriate instance class.
- **Storage Auto-Scaling**: Enable storage auto-scaling to prevent storage full issues without over-provisioning upfront.
- **Aurora Serverless**: For spiky or unpredictable workloads, consider Aurora Serverless v2 to optimize costs.

## Reliability
- **Multi-AZ**: Always enable Multi-AZ for production databases.
- **Backups**: Enable automated backups and configure retention periods according to compliance needs. Practice restoring from snapshots.

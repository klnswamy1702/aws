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
# RDS Common Issues and Troubleshooting

## 1. High CPU Utilization
- **Issue**: DB instance running at 100% CPU.
- **Troubleshooting**: Use Enhanced Monitoring and Performance Insights to identify the top SQL queries causing high CPU load. Look for missing indexes or inefficient query execution plans.

## 2. Storage Full
- **Issue**: RDS instance stuck in `storage-full` state.
- **Troubleshooting**: If auto-scaling is not enabled, manually increase the allocated storage. Note that this action can only be performed once every 6 hours or after the optimization process completes.

## 3. Connection Timeouts
- **Issue**: Applications cannot connect to the database.
- **Troubleshooting**: Check the Security Group inbound rules attached to the RDS instance. Ensure it allows traffic on the database port (e.g., 3306 for MySQL) from the application's Security Group or IP range. Verify VPC routing if connecting from outside the VPC.

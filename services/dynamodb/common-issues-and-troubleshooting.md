---
service: DynamoDB
category: Database
difficulty_levels: L2-L3
aws_exam_relevance: High
maturity_tier: Tier 1
last_validated_date: 2023-10-25
version: 1.0
cross_references:
  - ../rds/overview.md
---
# DynamoDB Common Issues and Troubleshooting

## 1. ProvisionedThroughputExceededException
- **Issue**: Requests are being throttled because they exceed the provisioned read or write capacity.
- **Troubleshooting**: Enable DynamoDB Auto Scaling to adjust capacity based on traffic. For sudden spikes, consider switching to On-Demand capacity mode. Check if you have a "hot partition" causing localized throttling.

## 2. Hot Partitions
- **Issue**: Uneven distribution of data or access patterns causes one partition to receive the majority of read/write traffic.
- **Troubleshooting**: Add a random suffix to the partition key (Write Sharding) to distribute writes evenly. For reads, consider using DAX (DynamoDB Accelerator) to cache heavily accessed items.

## 3. High Latency
- **Issue**: Read/write operations take longer than the expected single-digit milliseconds.
- **Troubleshooting**: Ensure the client is in the same AWS Region as the DynamoDB table. Check if the client application is resource-constrained (CPU/Network). Implement DAX for microsecond read latency.

---
service: DynamoDB
category: Database
difficulty_levels: L3-L4
aws_exam_relevance: High
maturity_tier: Tier 1
last_validated_date: 2023-10-25
version: 1.0
cross_references:
  - ../rds/overview.md
---
# DynamoDB Interview Questions - Architecture

### Q1: How do you design a leader-board system using DynamoDB?
**Level:** L4 | **Category:** architecture
**Target Services:** DynamoDB, Lambda

> **Quick Answer:** Use a generic partition key (e.g., `GameID`), a sort key of `Score` or inverted `Score`, and query using `ScanIndexForward=false` to get top players. For large scale, use Global Secondary Indexes (GSIs).

#### Detailed Answer
For a basic leaderboard, partition by the context (like a game or tournament ID) and sort by the score. Because DynamoDB sorts by the sort key, querying the partition and reading backwards (`ScanIndexForward=False`) efficiently fetches the highest scores. For global leaderboards across millions of users, you might use Write Sharding for the partition key and a GSI to re-aggregate or use a different database like Redis (ElastiCache) for real-time ranking.

#### Follow-up Questions
- How would you handle ties in scores?

---
service: DynamoDB
category: Database
difficulty_levels: L1-L2
aws_exam_relevance: High
maturity_tier: Tier 1
last_validated_date: 2023-10-25
version: 1.0
cross_references:
  - ../rds/overview.md
---
# DynamoDB Interview Questions - Basics

### Q1: What is the difference between a Partition Key and a Sort Key?
**Level:** L2 | **Category:** conceptual
**Target Services:** DynamoDB

> **Quick Answer:** The partition key determines the logical partition for an item, while the sort key orders items with the same partition key.

#### Detailed Answer
A DynamoDB table must have a primary key, which can be a simple primary key (partition key only) or a composite primary key (partition key and sort key). The partition key is passed to an internal hash function to determine data placement. Items with the same partition key are stored together and sorted by the sort key, allowing for range queries.

#### Follow-up Questions
- How does a poorly chosen partition key lead to a "hot partition"?

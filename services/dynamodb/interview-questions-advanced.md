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
# DynamoDB Interview Questions - Advanced

### Q1: Explain Single-Table Design in DynamoDB.
**Level:** L4 | **Category:** architecture
**Target Services:** DynamoDB

> **Quick Answer:** Single-table design is a modeling technique where all application entities are stored in a single DynamoDB table to minimize cross-table operations and optimize read performance.

#### Detailed Answer
Unlike relational databases that normalize data across multiple tables, DynamoDB performs best when data accessed together is stored together. By using generic partition and sort keys (e.g., `PK` and `SK`), and overloading them with different entity types, you can retrieve complex relational data in a single request.

#### Follow-up Questions
- What are the trade-offs of single-table design when application access patterns change?

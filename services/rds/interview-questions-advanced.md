---
service: RDS
category: Database
difficulty_levels: L3-L4
aws_exam_relevance: High
maturity_tier: Tier 1
last_validated_date: 2023-10-25
version: 1.0
cross_references:
  - ../dynamodb/overview.md
---
# RDS Interview Questions - Advanced

### Q1: How does Amazon Aurora Serverless v2 differ from v1?
**Level:** L3 | **Category:** architecture
**Target Services:** RDS, Aurora

> **Quick Answer:** Aurora Serverless v2 scales in fractions of a second and in fine-grained increments, whereas v1 scales more slowly and requires a scaling point where there are no active transactions.

#### Detailed Answer
Aurora Serverless v2 provides instant scaling, allowing it to support demanding workloads with rapid and unpredictable spikes. It scales capacity up and down continuously rather than jumping between predefined capacity tiers.

#### Follow-up Questions
- How does Aurora Serverless v2 impact cost optimization for spiky workloads?

### Q2: Explain how RDS Proxy helps with serverless applications.
**Level:** L4 | **Category:** architecture
**Target Services:** RDS, Lambda

> **Quick Answer:** RDS Proxy pools and shares database connections, improving the scalability and resilience of applications like AWS Lambda functions that open and close many connections rapidly.

#### Detailed Answer
Serverless applications often open many short-lived database connections, which can exhaust database memory and compute resources. RDS Proxy sits between the application and the database to pool these connections, reducing the overhead on the DB instance and preserving connections during failovers.

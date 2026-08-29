---
service: ElastiCache
category: Database
difficulty_levels: L1-L2
aws_exam_relevance: High
maturity_tier: Tier 1
last_validated_date: 2023-10-25
version: 1.0
cross_references:
  - ../dynamodb/overview.md
---
# ElastiCache Interview Questions - Basics

### Q1: What is the difference between Redis and Memcached in ElastiCache?
**Level:** L2 | **Category:** conceptual
**Target Services:** ElastiCache

> **Quick Answer:** Redis supports complex data types, persistence, high availability (Multi-AZ), and backup/restore. Memcached is simpler, multi-threaded, and designed for basic key-value caching without persistence.

#### Detailed Answer
Redis is the preferred choice for most modern applications due to its rich feature set, including pub/sub, Lua scripting, geospatial indexes, and streams. It supports replication and failover. Memcached is useful if you only need a pure, fast, multi-threaded in-memory object cache and plan to scale out horizontally with ease, but it lacks data durability.

#### Follow-up Questions
- When would you specifically choose Memcached over Redis?

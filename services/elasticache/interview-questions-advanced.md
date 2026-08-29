---
service: Amazon ElastiCache
category: interview-questions
difficulty_levels: ["L1", "L2", "L3", "L4"]
aws_exam_relevance: ["Developer Associate", "SysOps Administrator", "DevOps Engineer Professional", "Solutions Architect Professional"]
maturity_tier: "Tier 1"
last_validated_date: "2026-08-29"
version: "1.0"
cross_references: []
---

# Amazon ElastiCache Advanced Interview Questions

### Q1: How do you decide between Redis and Memcached in a production environment?
**Level:** L3 | **Category:** conceptual/architecture
**Target Services:** [ElastiCache]

> **Quick Answer:** Redis offers advanced data structures, persistence, replication, and high availability, whereas Memcached is designed for simplicity, pure caching, and multi-threaded performance on single nodes.

#### Detailed Answer
Redis is typically chosen for production environments needing advanced features like pub/sub, Lua scripting, snapshots (RDB/AOF), and clustered HA. Memcached is better when you just need a straightforward object cache with minimal overhead.

#### Follow-up Questions
- When would you specifically choose Memcached over Redis?

#### Related Services
- RDS, DynamoDB

#### References
- [AWS Docs](https://aws.amazon.com/elasticache/)

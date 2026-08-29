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
# RDS Interview Questions - Architecture

### Q1: How would you design a disaster recovery strategy for an RDS database across multiple regions?
**Level:** L4 | **Category:** architecture
**Target Services:** RDS, KMS

> **Quick Answer:** Use cross-region read replicas or Aurora Global Database for low RTO/RPO. Alternatively, use automated cross-region snapshot copying for a cost-effective solution with higher RTO/RPO.

#### Detailed Answer
For critical workloads, Aurora Global Database provides sub-second replication latency and fast failover across regions. For standard RDS, you can create a cross-region read replica. In the event of a disaster, you promote the read replica to a standalone instance. Note that cross-region replication incurs data transfer costs. For lower-tier applications, copying automated backups (snapshots) to another region is cheaper but takes longer to recover.

#### Follow-up Questions
- How do you handle KMS encryption keys when copying snapshots across regions?

### Q2: Design a highly available and scalable read-heavy database architecture using RDS.
**Level:** L3 | **Category:** architecture
**Target Services:** RDS, Route53

> **Quick Answer:** Deploy an RDS instance in Multi-AZ for high availability, and add multiple Read Replicas to offload read traffic, fronted by a Route 53 weighted routing policy or an application-level load balancer.

#### Detailed Answer
The Multi-AZ deployment ensures synchronous replication to a standby instance for automatic failover. To handle read-heavy traffic, create asynchronous Read Replicas. The application must be configured to split read and write queries, directing writes to the primary endpoint and reads to the replica endpoints.

#### Follow-up Questions
- What are the replication lag implications when using Read Replicas?

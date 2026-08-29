---
service: RDS
category: Database
difficulty_levels: L1-L2
aws_exam_relevance: High
maturity_tier: Tier 1
last_validated_date: 2023-10-25
version: 1.0
cross_references:
  - ../dynamodb/overview.md
---
# RDS Interview Questions - Basics

### Q1: What is Amazon RDS and how does it differ from running a database on EC2?
**Level:** L1 | **Category:** conceptual
**Target Services:** RDS, EC2

> **Quick Answer:** Amazon RDS is a fully managed database service, whereas running a database on EC2 requires self-management of the OS, patching, and backups.

#### Detailed Answer
RDS handles routine database tasks such as provisioning, patching, backup, recovery, failure detection, and repair. With EC2, the user is responsible for managing the underlying infrastructure, operating system, and database software, giving more control but requiring more administrative effort.

#### Follow-up Questions
- When would you choose to run a database on EC2 instead of RDS?

### Q2: What are the different database engines supported by RDS?
**Level:** L1 | **Category:** conceptual
**Target Services:** RDS

> **Quick Answer:** RDS supports MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, and Amazon Aurora.

#### Detailed Answer
Each engine has specific versions supported by RDS, and users can choose the engine that best fits their application requirements and licensing preferences (e.g., BYOL for Oracle).

#### Follow-up Questions
- What are the advantages of using Amazon Aurora over standard MySQL or PostgreSQL on RDS?

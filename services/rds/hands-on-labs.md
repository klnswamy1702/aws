---
service: RDS
category: Database
difficulty_levels: L3
aws_exam_relevance: Medium
maturity_tier: Tier 1
last_validated_date: 2023-10-25
version: 1.0
cross_references:
  - ../dynamodb/overview.md
---
# RDS Hands-on Labs

## Lab 1: Configuring a Multi-AZ RDS MySQL Instance
**Objective:** Deploy an RDS instance with Multi-AZ for high availability.

### Steps
1. Create a DB subnet group across at least two Availability Zones.
2. Launch a MySQL RDS instance, selecting 'Create a standby instance' for Multi-AZ deployment.
3. Test failover by rebooting the primary instance with failover and observing the CNAME update.

## Lab 2: Setting up RDS Proxy for AWS Lambda
**Objective:** Use RDS Proxy to manage connection pooling for a Lambda function.

### Steps
1. Create an RDS instance and configure IAM authentication.
2. Create an RDS Proxy, associating it with the RDS instance and a Secrets Manager secret for credentials.
3. Update a Lambda function to connect to the proxy endpoint instead of the database endpoint.

---
service: EBS
category: Storage
difficulty_levels: L1-L4
aws_exam_relevance: High
maturity_tier: Foundation
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ec2/overview.md
---

# Amazon Elastic Block Store (EBS) Overview

Amazon EBS provides block level storage volumes for use with EC2 instances. It is highly available, reliable, and can be dynamically scaled.

## Volume Types
- **gp3 (General Purpose SSD):** Baseline of 3,000 IOPS and 125 MiB/s throughput. You can provision IOPS and throughput independently of storage capacity.
- **gp2 (General Purpose SSD):** IOPS are linked to volume size (3 IOPS per GiB).
- **io2/io2 Block Express (Provisioned IOPS SSD):** High performance for mission-critical databases. Up to 256,000 IOPS. 99.999% durability.
- **st1 (Throughput Optimized HDD):** Low cost, designed for frequently accessed, throughput-intensive workloads (e.g., Big Data, Data Warehouses).
- **sc1 (Cold HDD):** Lowest cost, for less frequently accessed workloads.

## Key Features
- **Snapshots:** Incremental backups to S3. Only blocks that changed after your most recent snapshot are saved.
- **Encryption:** Uses KMS. Transparent to workloads.
- **Multi-Attach:** Attach a single io2 volume to multiple EC2 instances (requires cluster-aware file system).
- **EBS vs Instance Store:** EBS is persistent, network-attached. Instance Store is ephemeral (lost on stop/terminate) but physically attached to host (high IOPS/low latency).

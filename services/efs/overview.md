---
service: EFS
category: overview
difficulty_levels: [L1, L2, L3]
---
# Amazon Elastic File System (EFS) Overview

EFS provides a simple, scalable, fully managed elastic NFS (Network File System) file system for use with AWS Cloud services and on-premises resources.

## Architecture
- **Standard vs One Zone:** Standard stores data redundantly across multiple AZs. One Zone stores data within a single AZ for lower cost.
- **Mount Targets:** You create EFS mount targets in VPC subnets. EC2 instances connect to the mount target's IP address.
- **Protocol:** Uses NFSv4.0 and NFSv4.1.

## Performance Modes
- **General Purpose:** Ideal for latency-sensitive use cases (web serving, CMS). Default and recommended.
- **Max I/O:** Used for scale-out workloads with highly parallelized applications (big data, genome analysis). Higher latency but virtually unlimited throughput.

## Throughput Modes
- **Bursting Throughput:** Scales with the size of the file system.
- **Provisioned Throughput:** You provision the throughput independent of the amount of data stored.
- **Elastic Throughput:** Automatically scales throughput capacity up or down based on workload activity. Ideal for unpredictable workloads.

## Features
- **Lifecycle Management:** Automatically moves infrequently accessed files to EFS Infrequent Access (IA) or Archive storage classes.
- **Access Points:** Application-specific entry points into an EFS file system to enforce POSIX user/group identities and root directory restrictions.
- **Compute Integrations:** Can be natively mounted via Lambda, ECS (Fargate & EC2), and EKS (via EFS CSI driver).

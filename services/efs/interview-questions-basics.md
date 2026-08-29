---
service: EFS
category: basics
difficulty_levels: [L1, L2]
---
# EFS Basics Interview Questions

### Q1: What is Amazon EFS?
**Level:** L1 | **Category:** conceptual
**Target Services:** EFS
> **Quick Answer:** A fully managed, elastic NFS file system designed to be shared across thousands of Amazon EC2 instances concurrently.

### Q2: EBS vs EFS vs S3 - when to use which?
**Level:** L2 | **Category:** architecture
**Target Services:** EBS, EFS, S3
> **Quick Answer:** EBS is block storage for a single instance (usually). EFS is file storage shared across multiple instances. S3 is object storage for web-scale distribution and API access.

### Q3: What protocol does EFS use?
**Level:** L1 | **Category:** conceptual
> **Quick Answer:** Network File System version 4 (NFSv4.0 and NFSv4.1).

### Q4: How is EFS billed?
**Level:** L1 | **Category:** conceptual
> **Quick Answer:** You pay only for the storage used (per GB-month), plus throughput if using Provisioned/Elastic throughput modes.

### Q5: What is an EFS Mount Target?
**Level:** L2 | **Category:** networking
> **Quick Answer:** An endpoint with an IP address placed in a VPC subnet that allows resources in that subnet to access the EFS file system using NFS.

### Q6: Can EFS be accessed from on-premises?
**Level:** L2 | **Category:** networking
> **Quick Answer:** Yes, via AWS Direct Connect or AWS VPN, by routing traffic to the EFS Mount Targets in the VPC.

### Q7: What are EFS storage classes?
**Level:** L2 | **Category:** conceptual
> **Quick Answer:** Standard, Standard-Infrequent Access (IA), One Zone, One Zone-IA, and Archive.

### Q8: What is EFS Lifecycle Management?
**Level:** L2 | **Category:** cost-optimization
> **Quick Answer:** An automated policy that transitions files to lower-cost storage classes (like IA or Archive) after a set period of inactivity (e.g., 30 days).

### Q9: Does EFS support Windows?
**Level:** L1 | **Category:** conceptual
> **Quick Answer:** No. EFS is Linux-only. For Windows, use Amazon FSx for Windows File Server.

### Q10: How do you secure EFS data at rest and in transit?
**Level:** L2 | **Category:** security
> **Quick Answer:** At rest via KMS encryption (enabled at creation). In transit using TLS via the Amazon EFS mount helper.

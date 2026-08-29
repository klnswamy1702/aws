---
service: EFS
category: architecture
difficulty_levels: [L4]
---
# EFS Architecture Interview Questions

### Q1: Design a shared storage architecture for thousands of containerized ML inference tasks.
**Level:** L4 | **Category:** architecture
**Target Services:** EFS, EKS/ECS, DataSync
> **Quick Answer:** Mount a single EFS file system across all EKS/ECS nodes using the EFS CSI driver. Use Elastic Throughput to handle simultaneous read spikes.
<details>
<summary>Detailed Answer</summary>
Because ML models can be large, store the base model in EFS. Configure EFS Access Points for different models. Use Elastic Throughput to prevent throttling when a thousand tasks scale up instantly and pull the 2GB model file.
</details>

### Q2: How do you achieve cross-region replication for Amazon EFS?
**Level:** L4 | **Category:** architecture
**Target Services:** EFS, AWS Backup, DataSync
> **Quick Answer:** Use native EFS Replication, which automatically and asynchronously replicates data to an EFS file system in another AWS Region or AZ.
<details>
<summary>Detailed Answer</summary>
EFS Replication manages the infrastructure to keep the destination file system in sync. For custom interval schedules, AWS Backup cross-region copies can also be used.
</details>

### Q3: Optimize the cost of a 50TB EFS file system where 80% of data is older than 60 days.
**Level:** L4 | **Category:** cost-optimization
**Target Services:** EFS
> **Quick Answer:** Enable EFS Lifecycle Management to transition files unaccessed for 60 days to the EFS Infrequent Access (IA) storage class, and >90 days to EFS Archive.
<details>
<summary>Detailed Answer</summary>
EFS IA is significantly cheaper than Standard. Configure the transition policy. If the file is accessed later, EFS Intelligent-Tiering (if configured) can move it back to Standard.
</details>

### Q4: Architect an EFS solution for a strict multi-tenant SaaS application.
**Level:** L4 | **Category:** architecture/security
**Target Services:** EFS, IAM, KMS
> **Quick Answer:** Use EFS Access Points to create isolated directory paths per tenant. Assign IAM policies enforcing that each tenant's compute resource can only mount its specific Access Point.
<details>
<summary>Detailed Answer</summary>
Tenant A's container gets IAM Role A, which can only perform `elasticfilesystem:ClientMount` where the `Condition` matches Tenant A's EFS Access Point ARN. The Access Point forces the root directory to `/tenant-a` and overrides the POSIX identity.
</details>

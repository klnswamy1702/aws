---
service: EFS
category: advanced
difficulty_levels: [L3, L4]
---
# EFS Advanced Interview Questions

### Q1: How do EFS Access Points enhance security?
**Level:** L3 | **Category:** security
**Target Services:** EFS, IAM
> **Quick Answer:** They enforce specific POSIX user and group IDs on all file system requests and can enforce a specific root directory, acting as a chroot jail.
<details>
<summary>Detailed Answer</summary>
This ensures that even if a container runs as root, its operations on EFS are mapped to an unprivileged POSIX user. Used heavily in EKS and ECS to enforce multi-tenant isolation on a shared EFS volume.
</details>

### Q2: Compare EFS Bursting, Provisioned, and Elastic Throughput modes.
**Level:** L4 | **Category:** performance
**Target Services:** EFS
> **Quick Answer:** Bursting gives baseline throughput scaled by volume size. Provisioned guarantees a set MB/s regardless of size. Elastic auto-scales up and down per minute, ideal for spiky, unpredictable workloads.
<details>
<summary>Detailed Answer</summary>
Bursting can run out of burst credits on small file systems with high I/O. Elastic throughput solves this without needing to over-provision or pay for unused capacity as you would with Provisioned.
</details>

### Q3: How do you troubleshoot EFS performance issues?
**Level:** L3 | **Category:** troubleshooting
**Target Services:** EFS, CloudWatch
> **Quick Answer:** Check CloudWatch metrics for `BurstCreditBalance`, `PercentIOLimit`, and ensure the Amazon EFS client is using recommended mount options (like `noresvport`).
<details>
<summary>Detailed Answer</summary>
If `BurstCreditBalance` is dropping, switch to Elastic throughput. If `PercentIOLimit` approaches 100%, migrate from General Purpose to Max I/O mode.
</details>

### Q4: Explain how EFS integrates with AWS Lambda.
**Level:** L3 | **Category:** architecture
**Target Services:** EFS, Lambda
> **Quick Answer:** EFS can be mounted to a Lambda function, providing a persistent, shared file system across concurrent executions, bypassing the /tmp storage limits.
<details>
<summary>Detailed Answer</summary>
Requires the Lambda function to be in a VPC. An EFS Access Point must be used to restrict Lambda's access to a specific directory and POSIX identity.
</details>

### Q5: Can you change the performance mode (General Purpose vs Max I/O) of an EFS file system after creation?
**Level:** L3 | **Category:** practical
**Target Services:** EFS
> **Quick Answer:** No. Performance mode is set at creation.
<details>
<summary>Detailed Answer</summary>
To change it, you must create a new EFS file system with the desired mode and use AWS DataSync to migrate the data from the old system to the new one.
</details>

### Q6: How does EFS handle distributed locking?
**Level:** L4 | **Category:** architecture
**Target Services:** EFS
> **Quick Answer:** EFS fully supports NFSv4 file locking. However, applications heavily reliant on fine-grained byte-range locks may see latency due to the distributed, multi-AZ nature of EFS.
<details>
<summary>Detailed Answer</summary>
Avoid using EFS as a lock manager for highly concurrent distributed systems. Use DynamoDB or Redis instead for distributed locking, and leave EFS for file storage.
</details>

---
service: EBS
category: architecture
difficulty_levels: [L4]
aws_exam_relevance: [SAP-C02, DOP-C02]
---
# EBS Architecture Interview Questions

### Q1: Design a high-performance storage architecture for a custom database requiring 200,000 IOPS.
**Level:** L4 | **Category:** architecture
**Target Services:** EBS, EC2
> **Quick Answer:** Select an R5b (or similar Nitro) instance supporting Block Express, and attach an io2 Block Express volume provisioned with 200,000 IOPS.
<details>
<summary>Detailed Answer</summary>
If Block Express is unavailable, use RAID 0 across multiple `io2` or `gp3` volumes. Ensure the EC2 instance's EBS bandwidth limits exceed the aggregated throughput and IOPS of the striped volumes. Use Linux `mdadm` for the RAID array.
</details>

### Q2: What is your strategy for cross-region disaster recovery using EBS?
**Level:** L4 | **Category:** architecture
**Target Services:** EBS, DLM
> **Quick Answer:** Use Amazon DLM to automate cross-region snapshot copies, or AWS Elastic Disaster Recovery (DRS) for continuous block-level replication with sub-second RPO.
<details>
<summary>Detailed Answer</summary>
Snapshots are incremental locally, but full copies on the first cross-region transfer. Subsequent cross-region copies of the same volume are incremental, minimizing transfer costs and time. Ensure KMS keys are shared/mapped appropriately in the destination region.
</details>

### Q3: How do you optimize EBS costs across an enterprise?
**Level:** L4 | **Category:** cost-optimization
**Target Services:** EBS, Cost Explorer
> **Quick Answer:** Migrate gp2 to gp3, delete unattached/orphaned volumes, manage snapshot lifecycles (archiving old snapshots to Snapshot Archive), and right-size provisioned IOPS on io1/io2.
<details>
<summary>Detailed Answer</summary>
`gp3` is up to 20% cheaper per GB than `gp2` and separates IOPS from storage capacity. Use AWS Compute Optimizer to identify underutilized volumes. Implement DLM policies to age out snapshots to EBS Snapshot Archive for long-term retention at lower cost.
</details>

### Q4: How does EBS Snapshot Archive work, and when should it be used?
**Level:** L4 | **Category:** architecture
**Target Services:** EBS
> **Quick Answer:** Snapshot Archive is a lower-cost storage tier for EBS snapshots that are rarely accessed and retained for over 90 days.
<details>
<summary>Detailed Answer</summary>
Retrieving an archived snapshot takes 24-72 hours. It is ideal for compliance and regulatory backups. Note that archived snapshots are full backups, not incremental, so compare the cost of standard incremental storage vs. full archive storage before migrating.
</details>

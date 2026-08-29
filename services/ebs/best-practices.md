---
service: EBS
category: best-practices
---
# EBS Best Practices

- **Use gp3:** Always use gp3 over gp2 for better price-to-performance.
- **EBS-Optimized Instances:** Ensure instances are EBS-optimized to guarantee dedicated network bandwidth between EC2 and EBS.
- **RAID:** Use RAID 0 for higher performance across multiple volumes. Use RAID 1 for application-level mirroring if needed, though EBS is already replicated within an AZ.
- **Encryption:** Enable "Encryption by default" at the account/region level using an AWS KMS key.
- **Snapshots:** Use Data Lifecycle Manager (DLM) or AWS Backup; don't script snapshots manually.
- **Initialize:** Volumes restored from snapshots experience a first-read penalty. Read all blocks using `fio` or `dd` if maximum performance is needed immediately.

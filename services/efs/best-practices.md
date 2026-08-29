---
service: EFS
category: best-practices
---
# EFS Best Practices

- **Use EFS Mount Helper:** Always use `amazon-efs-utils` to mount EFS for built-in TLS, IAM authorization, and optimized NFS defaults.
- **Throughput:** For unpredictable workloads, always use Elastic Throughput to avoid exhaustion of burst credits.
- **Monitoring:** Monitor `PercentIOLimit` and `BurstCreditBalance` in CloudWatch.
- **Cost:** Enable Lifecycle Management for all file systems.
- **Small Files:** EFS has high overhead for many small files compared to EBS. Zip/tar small files or use EBS if you have millions of tiny files requiring high performance.

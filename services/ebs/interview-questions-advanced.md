---
service: EBS
category: advanced
difficulty_levels: [L3, L4]
aws_exam_relevance: [SAP-C02, DOP-C02]
---
# EBS Advanced Interview Questions

### Q1: How do you tune IOPS for a high-performance database running on EC2 using EBS?
**Level:** L3 | **Category:** practical
**Target Services:** EBS, EC2
> **Quick Answer:** Use io2 Block Express or gp3 volumes, ensure the EC2 instance is EBS-optimized, use instances with high network bandwidth, and stripe multiple volumes together if needed.
<details>
<summary>Detailed Answer</summary>
Use `io2` Block Express for up to 256,000 IOPS and 4,000 MB/s throughput if instance supports it. For gp3, you can provision up to 16,000 IOPS independently of storage. Striping (RAID 0) can push limits further. Check instance EBS limits as they often bottleneck EBS performance.
</details>

### Q2: Explain EBS Multi-Attach and its use cases.
**Level:** L3 | **Category:** conceptual
**Target Services:** EBS
> **Quick Answer:** EBS Multi-Attach allows attaching a single Provisioned IOPS (io1 or io2) volume to up to 16 EC2 instances in the same AZ simultaneously.
<details>
<summary>Detailed Answer</summary>
It is useful for clustered applications (like Oracle RAC) that manage concurrent storage access. It requires a cluster-aware file system (like GFS2 or OCFS2); standard file systems like ext4 or XFS will corrupt data if multi-attached.
</details>

### Q3: What is io2 Block Express and when should you use it over io2 or gp3?
**Level:** L4 | **Category:** architecture
**Target Services:** EBS
> **Quick Answer:** io2 Block Express is a SAN in the cloud providing sub-millisecond latency, up to 256,000 IOPS, and 4,000 MB/s throughput, ideal for the largest, most IO-intensive mission-critical databases.
<details>
<summary>Detailed Answer</summary>
It uses the Scalable Reliable Datagram (SRD) protocol. Use it when workloads exceed the 64k IOPS limit of standard io1/io2, or require consistent sub-millisecond latency. Requires specific Nitro instance types (like R5b).
</details>

### Q4: How do you manage EBS snapshots at scale across multiple accounts?
**Level:** L4 | **Category:** architecture
**Target Services:** EBS, AWS Backup, DLM
> **Quick Answer:** Use AWS Backup or Amazon Data Lifecycle Manager (DLM) combined with AWS Organizations for centralized, automated snapshot scheduling, retention, and cross-account sharing.
<details>
<summary>Detailed Answer</summary>
AWS Backup provides central backup policies across Organizations. DLM automates snapshot lifecycles based on tags. Use KMS CMKs to encrypt snapshots, share the KMS key and snapshot with target accounts, and copy the snapshot in the target account.
</details>

### Q5: Describe the process of rotating the KMS encryption key for an existing EBS volume.
**Level:** L4 | **Category:** security
**Target Services:** EBS, KMS
> **Quick Answer:** You cannot change the KMS key of an active volume. You must create a snapshot, copy the snapshot and specify the new KMS key, then create a new volume from the copied snapshot and swap it.
<details>
<summary>Detailed Answer</summary>
KMS key rotation within the same CMK (automatic rotation) requires no volume changes. But to switch to an entirely different CMK:
1. Snapshot the volume.
2. Copy snapshot -> select new CMK.
3. Create volume from the copied snapshot.
4. Unmount old, detach old, attach new, mount new.
</details>

### Q6: What happens to data in an EBS volume when the EC2 instance is terminated, and how is it controlled?
**Level:** L3 | **Category:** practical
**Target Services:** EBS, EC2
> **Quick Answer:** The `DeleteOnTermination` attribute controls this. By default, the root volume is deleted, and additional data volumes are retained.
<details>
<summary>Detailed Answer</summary>
You can change this attribute during instance launch or dynamically via the AWS CLI or Console. If retained, the volume status changes to `available` and continues incurring charges.
</details>

---
service: EBS
category: Storage
difficulty_levels: L1-L2
aws_exam_relevance: High
maturity_tier: Foundation
last_validated_date: 2026-08-29
version: 1.0
---

# EBS Interview Questions: Basics (L1-L2)

### Q1: What is Amazon EBS?
**Level:** L1 | **Category:** conceptual
**Target Services:** EBS

> **Quick Answer:** Amazon Elastic Block Store (EBS) provides persistent, network-attached block level storage volumes for EC2 instances.

#### Detailed Answer
EBS acts like a raw, unformatted, external block device that you can attach to a single EC2 instance. You can create a file system on top of it, or use it as a hard drive.

### Q2: What are the main EBS volume types?
**Level:** L1 | **Category:** conceptual
**Target Services:** EBS

> **Quick Answer:** The main types are SSD-backed (gp2, gp3, io1, io2) for transactional workloads, and HDD-backed (st1, sc1) for streaming workloads.

#### Detailed Answer
gp3 allows independent scaling of IOPS and throughput. io2 provides ultra-high performance and 99.999% durability.

### Q3: How do EBS Snapshots work?
**Level:** L2 | **Category:** conceptual
**Target Services:** EBS, S3

> **Quick Answer:** EBS Snapshots are point-in-time, incremental backups of your EBS volumes stored in Amazon S3.

#### Detailed Answer
Incremental means only the blocks that have changed since your last snapshot are saved, reducing storage costs.

### Q4: What happens to an EBS volume when the EC2 instance is terminated?
**Level:** L2 | **Category:** practical
**Target Services:** EBS, EC2

> **Quick Answer:** By default, the root EBS volume is deleted, while additional attached EBS volumes are preserved.

#### Detailed Answer
You can change the `DeleteOnTermination` flag to preserve the root volume or delete additional volumes.

### Q5: Can I attach an EBS volume to multiple EC2 instances?
**Level:** L2 | **Category:** practical
**Target Services:** EBS, EC2

> **Quick Answer:** Yes, using EBS Multi-Attach, but it is only supported on io1 and io2 volumes.

#### Detailed Answer
You must use a cluster-aware file system (like GFS2 or OCFS2) to prevent data corruption. Standard file systems like ext4 or XFS are not supported for multi-attach.

### Q6: Can I attach an EBS volume from another Availability Zone?
**Level:** L2 | **Category:** architecture
**Target Services:** EBS, EC2

> **Quick Answer:** No, an EBS volume can only be attached to an EC2 instance in the same Availability Zone.

#### Detailed Answer
To move an EBS volume to another AZ, you must take a snapshot of the volume and create a new volume from that snapshot in the target AZ.

### Q7: What is the difference between EBS and Instance Store?
**Level:** L2 | **Category:** conceptual
**Target Services:** EBS, EC2

> **Quick Answer:** EBS is network-attached, persistent storage, while Instance Store is physically attached to the host server and is ephemeral (lost when stopped/terminated).

#### Detailed Answer
Instance store provides the lowest latency and highest IOPS, but data is lost on stop, hibernate, or hardware failure.

### Q8: How can you encrypt an existing unencrypted EBS volume?
**Level:** L2 | **Category:** security
**Target Services:** EBS, KMS

> **Quick Answer:** Take a snapshot of the volume, copy the snapshot and select encryption, then create a new volume from the encrypted snapshot.

#### Detailed Answer
You cannot directly encrypt an existing unencrypted volume in-place.

### Q9: What is EBS Fast Snapshot Restore (FSR)?
**Level:** L2 | **Category:** practical
**Target Services:** EBS

> **Quick Answer:** FSR ensures volumes created from a snapshot are fully initialized at creation, delivering full provisioned performance instantly without initialization penalty.

#### Detailed Answer
Normally, data is lazily loaded from S3 in the background, causing a performance hit on first access. FSR eliminates this.

### Q10: How do you resize an EBS volume?
**Level:** L2 | **Category:** practical
**Target Services:** EBS

> **Quick Answer:** You can dynamically increase volume size, modify volume type, or adjust IOPS via Elastic Volumes without detaching the volume or restarting the instance.

#### Detailed Answer
After modifying the volume size, you must extend the file system at the OS level using `lsblk` and `growpart`.

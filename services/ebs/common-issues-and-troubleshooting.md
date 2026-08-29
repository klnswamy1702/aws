---
service: EBS
category: troubleshooting
---
# EBS Troubleshooting

## 1. Instance Hangs During IO Spikes
**Root Cause:** Burst credit exhaustion on gp2 volumes, or hitting EC2 instance bandwidth limits.
**Fix:** Migrate to gp3 for consistent baseline performance, or upgrade the instance type.

## 2. Cannot Attach Volume to Instance
**Root Cause:** Volume and Instance are in different Availability Zones, or the volume is still in an `optimizing` state from a prior modification (wait or retry).

## 3. Data Corruption on Multi-Attach
**Root Cause:** Standard file system (ext4/XFS) used instead of a cluster-aware file system.
**Fix:** Reformat with OCFS2/GFS2.

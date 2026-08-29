---
service: EFS
category: troubleshooting
---
# EFS Troubleshooting

## 1. Connection Timeout during Mount
**Root Cause:** Security Group rules on the EFS Mount Target do not allow inbound NFS (TCP 2049) from the EC2 instance's security group.
**Fix:** Update the EFS SG to allow inbound from the EC2 SG.

## 2. High Latency on Read/Write
**Root Cause:** The application is reading/writing millions of tiny files, or Burst Credits are at 0.
**Fix:** Check `BurstCreditBalance`. Enable Elastic Throughput. Optimize the app to handle larger chunks of data.

## 3. Read-Only File System Error
**Root Cause:** IAM authorization is enabled, and the IAM role lacks `elasticfilesystem:ClientWrite` permissions.

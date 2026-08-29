---
service: EFS
category: hands-on
difficulty_levels: [L2, L3]
---
# EFS Hands-on Labs

## Lab 1: Mount EFS on EC2 and enable TLS
**Objective:** Mount EFS securely using the EFS Mount Helper.
<details>
<summary>Step-by-Step</summary>
1. Install `amazon-efs-utils`: `sudo yum install -y amazon-efs-utils`
2. Create directory: `mkdir efs`
3. Mount with TLS: `sudo mount -t efs -o tls fs-12345678:/ efs`
</details>

## Lab 2: EFS Access Point with Lambda
**Objective:** Use Lambda to write files to EFS with an Access Point.
<details>
<summary>Step-by-Step</summary>
1. Create an Access Point on EFS setting POSIX user to `1001` and path to `/lambda-data`.
2. Connect Lambda to the VPC/Subnets containing EFS Mount Targets.
3. In Lambda config, add EFS File System, point to the Access Point ARN, and set local mount path to `/mnt/efs`.
</details>

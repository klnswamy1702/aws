---
service: Fargate
category: troubleshooting
difficulty_levels: L2-L3
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecs/common-issues-and-troubleshooting.md
---
# AWS Fargate - Common Issues and Troubleshooting

## 1. Out of Memory (OOM) Errors

**Symptoms:**
Your Fargate task repeatedly stops with a `Stopped reason` indicating `OutOfMemoryError` or `ContainerKilled`.

**Root Cause:**
The container attempted to consume more memory than was allocated to the task. Because Fargate tasks run in a strictly isolated microVM, exceeding the hard limit results in immediate termination by the Linux kernel OOM killer.

**Resolution:**
- Increase the memory allocated in the Task Definition.
- Use CloudWatch Container Insights to profile the application's memory usage over time to find the correct baseline.
- Ensure your application (e.g., Java JVM) is configured to respect container memory limits (cgroups).

## 2. Cannot Pull Image from ECR (Private Subnet)

**Symptoms:**
Task fails to start. The `Stopped reason` is `CannotPullContainerError: API error...`.

**Root Cause:**
Since Fargate version 1.4.0, tasks pulling from ECR require network access. If the task is launched in a private subnet (no public IP) without a NAT Gateway, it cannot reach the ECR API or the underlying S3 buckets where image layers are stored.

**Resolution:**
- **Option 1 (Recommended for cost):** Create VPC Interface Endpoints for `com.amazonaws.<region>.ecr.api` and `com.amazonaws.<region>.ecr.dkr`, AND a VPC Gateway Endpoint for S3.
- **Option 2:** Deploy a NAT Gateway in a public subnet and route the private subnet's internet traffic through it.

## 3. Storage Space Exhausted

**Symptoms:**
Application fails with "No space left on device" errors.

**Root Cause:**
By default, Fargate provides 20 GiB of ephemeral storage. If your container downloads large files, creates large temporary caches, or generates excessive local logs, it will fill up.

**Resolution:**
- Increase the ephemeral storage in the Task Definition (up to 200 GiB).
- Mount an Amazon EFS volume for persistent or massive storage needs.
- Modify the application to stream data rather than writing it to disk.

---
service: Fargate
category: best-practices
difficulty_levels: L2-L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecs/best-practices.md
---
# AWS Fargate - Best Practices

## Cost Optimization

### 1. Right-Size Task CPU and Memory
Over-provisioning is the most common cause of high Fargate costs. Use AWS Compute Optimizer, which analyzes CloudWatch metrics for your ECS/Fargate tasks, to get machine-learning backed recommendations on the exact vCPU and memory combination your container actually needs.

### 2. Leverage Fargate Spot
For stateless, fault-tolerant workloads (e.g., image processing, background queue workers, test environments), use Fargate Spot. Configure a Capacity Provider Strategy to mix On-Demand and Spot instances, reducing compute costs by up to 70%.

## Security

### 3. Use Read-Only Root Filesystems
In your Task Definition, enable `readonlyRootFilesystem`. This prevents the container from modifying its own file system, severely limiting an attacker's ability to download malware or modify application code if they manage to execute code inside the container. Use ephemeral volumes (`/tmp`) for required temporary writes.

### 4. Implement Least Privilege Task Roles
Ensure every Fargate task has a dedicated, highly restrictive IAM Task Role. Do not share IAM roles across different microservices. If Service A only needs to read from S3 Bucket X, its IAM role should explicitly grant `s3:GetObject` on `arn:aws:s3:::Bucket-X/*` and nothing else.

## Operations and Observability

### 5. Enable ECS Exec for Debugging
Never open SSH ports or install SSH daemons in containers. Instead, enable ECS Exec in the task definition. This uses AWS Systems Manager (SSM) Session Manager to provide secure, audited, interactive shell access to running containers directly through the AWS API.

### 6. Centralize Logging with AWS FireLens
Instead of relying solely on the default `awslogs` driver (which sends everything to CloudWatch, potentially becoming expensive), use AWS FireLens. FireLens injects a Fluent Bit sidecar container into your task, allowing you to route logs to multiple destinations (e.g., Amazon OpenSearch, S3, Datadog) and filter out noise before it incurs ingestion costs.

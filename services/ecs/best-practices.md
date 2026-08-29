---
service: ECS
category: best-practices
difficulty_levels: L2-L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../fargate/best-practices.md
---
# Amazon ECS - Best Practices

## Cost Optimization

### 1. Use ECS Capacity Providers
Stop manually managing Auto Scaling Groups (ASGs) tied to ECS clusters. Use ECS Capacity Providers with Managed Scaling. It prevents tasks from being stuck in a `PROVISIONING` state by automatically scaling the ASG based on the cluster's actual needs, and provides Managed Termination Protection to prevent scaling in from killing active tasks.

### 2. Implement Fargate Spot for Stateless Workloads
For workloads that can handle interruptions (like background jobs or scalable web APIs), utilize Fargate Spot via a Capacity Provider Strategy to save up to 70% on compute costs. Ensure your application handles `SIGTERM` signals for graceful shutdown within the 2-minute warning window.

## Security

### 3. Separate Task Role from Task Execution Role
Never combine these roles. The Task Execution Role is for the ECS agent (pulling images, writing logs). The Task Role is for your application code (reading S3, querying DynamoDB). Granting application permissions to the Execution Role violates least privilege.

### 4. Store Secrets Securely
Do not hardcode secrets or pass them as plain text environment variables in the task definition. Use AWS Secrets Manager or Systems Manager Parameter Store. Reference them in the `secrets` section of your container definition. ECS will retrieve them at runtime and inject them as environment variables securely.

## Operations and Resiliency

### 5. Utilize Container Insights
Enable CloudWatch Container Insights on your ECS clusters. It provides out-of-the-box dashboards and detailed metrics down to the container level (CPU, memory, network, and storage usage), which is critical for debugging performance bottlenecks.

### 6. Graceful Draining for Deployments
When configuring an Application Load Balancer with ECS, set the deregistration delay (connection draining) appropriately. The default is 300 seconds, which might be too long for rapid CI/CD deployments. Set it to 30-60 seconds for fast microservices, ensuring ECS waits for in-flight requests to complete before terminating the old task during a deployment.

---
service: ECS
category: overview
difficulty_levels: L1-L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecr/overview.md
  - ../fargate/overview.md
---
# Amazon Elastic Container Service (ECS) Overview

## What is Amazon ECS?
Amazon Elastic Container Service (ECS) is a highly scalable, fast container management service that makes it easy to run, stop, and manage containers on a cluster. Your containers are defined in a task definition that you use to run individual tasks or tasks within a service. You can run your tasks and services on a serverless infrastructure managed by AWS Fargate, or on a cluster of Amazon EC2 instances that you manage.

## Key Concepts
- **Cluster:** A logical grouping of tasks or services. Clusters can contain EC2 instances, Fargate capacity, or on-premises servers (ECS Anywhere).
- **Task Definition:** A blueprint that describes one or more containers (up to 10) that form your application. It specifies image URIs, CPU/memory, networking, and IAM roles.
- **Task:** An instantiation of a task definition within a cluster.
- **Service:** Allows you to run and maintain a specified number of instances of a task definition simultaneously in an ECS cluster. It handles scheduling, load balancing (via ALB/NLB), and automatic scaling.
- **Capacity Provider:** Manages the infrastructure that tasks run on, allowing you to use Fargate, EC2 Spot, and EC2 On-Demand instances in a single cluster with specific weighting and scaling rules.

## Launch Types
1. **Fargate:** Serverless compute for containers. You do not manage the underlying EC2 instances. Ideal for lower overhead.
2. **EC2:** You manage a cluster of EC2 instances registered to the ECS cluster. Ideal for when you need custom AMIs, specific EC2 instance types (like GPUs), or cost savings via Reserved Instances.
3. **External (ECS Anywhere):** Manage tasks on on-premises infrastructure.

## Core Features
- **Service Connect:** Simplifies inter-service communication and service discovery with a built-in mesh proxy.
- **ECS Exec:** Allows you to securely 'exec' (execute commands) into a running container in ECS or Fargate using SSM Session Manager.
- **Deployment Strategies:** Support for Rolling updates, Blue/Green (via CodeDeploy), and Canary.

## Best Practices
- Use IAM Roles for Tasks to provide least-privilege access.
- Prefer AWS Fargate unless specific EC2-level control is needed.
- Monitor with Container Insights in CloudWatch.

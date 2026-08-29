---
service: Fargate
category: overview
difficulty_levels: L1-L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecs/overview.md
---
# AWS Fargate Overview

## What is AWS Fargate?
AWS Fargate is a serverless, pay-as-you-go compute engine that lets you focus on building applications without managing servers. AWS Fargate is compatible with both Amazon Elastic Container Service (ECS) and Amazon Elastic Kubernetes Service (EKS). 
With Fargate, you no longer have to provision, configure, or scale clusters of virtual machines to run containers. This removes the need to choose server types, decide when to scale your clusters, or optimize cluster packing.

## Key Concepts
- **Serverless Compute:** You define the CPU and memory requirements for your container at the task level, and AWS provisions the exact compute required.
- **MicroVM Isolation:** Each Fargate task runs in its own single-tenant micro-virtual machine. This means CPU, memory, storage, and network resources are securely isolated, offering strong security by default.
- **Platform Versions:** Fargate utilizes platform versions (e.g., `1.3.0`, `1.4.0`) to define the runtime environment (OS, kernel, container runtime) that your tasks run on. You can pin to a specific version or use `LATEST`.

## Fargate vs. EC2 Launch Type
| Feature | Fargate | EC2 |
| :--- | :--- | :--- |
| **Server Management** | None (Serverless) | Full (You manage AMIs, OS patching, ASGs) |
| **Pricing** | Pay per vCPU and GB of memory used per second | Pay for the EC2 instance regardless of container density |
| **Networking** | `awsvpc` mode only | Supports `awsvpc`, `bridge`, `host`, `none` |
| **Storage** | Ephemeral (up to 200GB) or EFS | Instance Store, EBS, EFS |
| **Privileged Containers** | Not supported | Supported |

## Fargate Spot
Fargate Spot allows you to run interruption-tolerant ECS Tasks at up to a 70% discount compared to the Fargate price. AWS can terminate these tasks with a 2-minute warning when capacity is needed back.

## Best Practices
- Right-size your tasks using AWS Compute Optimizer to avoid paying for unused CPU/Memory.
- Use Fargate Spot for background processing, CI/CD workloads, and web services that can tolerate sudden scaling events.
- Implement ECS Exec for debugging instead of trying to SSH (which is not possible on Fargate).

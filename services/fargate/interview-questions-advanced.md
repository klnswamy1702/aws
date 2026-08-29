---
service: Fargate
category: advanced
difficulty_levels: L3-L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../fargate/best-practices.md
---
# AWS Fargate - Advanced Interview Questions

### Q1: How does Fargate Ephemeral Storage work, and how can you mount persistent storage?
**Level:** L3 | **Category:** architecture
**Target Services:** Fargate, EFS

> **Quick Answer:** By default, Fargate tasks receive a minimum of 20 GiB of ephemeral storage, which can be expanded up to 200 GiB. This storage is deleted when the task stops. For persistent, shared storage across multiple tasks, you must mount an Amazon EFS (Elastic File System) volume.

#### Detailed Answer
- **Ephemeral Storage:** Configured in the Task Definition. Useful for temporary file processing, caching, or large container images. It is tied to the lifecycle of the task.
- **Persistent Storage (EFS):** You can define an EFS volume in the ECS Task Definition. This requires:
  1. An EFS File System and Mount Targets in the task's VPC subnets.
  2. Security Groups allowing NFS traffic (Port 2049) from the Fargate task to the EFS Mount Targets.
  3. Specifying the file system ID in the task definition `volumes` section.
EFS allows hundreds of Fargate tasks to read and write to the same shared directory simultaneously (ReadWriteMany). 
*Note: Fargate does NOT support Amazon EBS volumes.*

#### Follow-up Questions
- How do you encrypt data at rest on Fargate ephemeral storage?
- Can you use Amazon FSx with Fargate?

### Q2: What are Fargate Platform Versions and how do they impact your deployments?
**Level:** L3 | **Category:** practical
**Target Services:** Fargate

> **Quick Answer:** Platform versions refer to the underlying runtime environment (kernel, OS, containerd version) that AWS manages for your Fargate tasks. When deploying, you can specify a version (e.g., `1.4.0`) or use `LATEST`.

#### Detailed Answer
AWS updates the Fargate infrastructure for security patches and new features. Because Fargate is serverless, you do not manage these updates, but AWS tracks them as Platform Versions.
- If you use `LATEST`, your tasks will launch with the most recent platform version available at the time of task creation.
- Significant changes happen between versions. For example, moving from `1.3.0` to `1.4.0` changed how network traffic is routed (tasks now need internet access or VPC endpoints to pull from ECR, whereas `1.3.0` implicitly allowed ECR pulls).
- To update running tasks to a new platform version, you must force a new deployment of the ECS Service.

#### Follow-up Questions
- How are security patches applied to long-running Fargate tasks?
- What are the implications of hardcoding a platform version in your IaC templates?

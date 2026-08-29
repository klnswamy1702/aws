---
service: Fargate
category: basics
difficulty_levels: L1-L2
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../fargate/overview.md
---
# AWS Fargate - Basic Interview Questions

### Q1: What is the primary difference between ECS on EC2 and ECS on Fargate?
**Level:** L1 | **Category:** conceptual
**Target Services:** ECS, Fargate

> **Quick Answer:** ECS on EC2 requires you to provision, manage, and scale the underlying EC2 virtual machines. ECS on Fargate is serverless; you only define the CPU and Memory needed for the container, and AWS provisions the exact compute resources automatically.

#### Detailed Answer
- **EC2 Launch Type:** You manage an Auto Scaling Group of EC2 instances. You are responsible for OS patching, AMI updates, instance type selection, and optimizing how tasks are packed onto instances to reduce wasted space (bin packing).
- **Fargate Launch Type:** You do not have access to the underlying OS. There are no EC2 instances in your account. You pay only for the exact vCPU and memory configured in the Task Definition, billed per second the task is running. It provides stronger isolation because every task runs in its own single-tenant microVM.

#### Follow-up Questions
- In what scenarios would you choose EC2 over Fargate?
- How do you access the host operating system of a Fargate task?

### Q2: How does networking work for an AWS Fargate task?
**Level:** L2 | **Category:** architecture
**Target Services:** Fargate, VPC

> **Quick Answer:** Fargate tasks only support the `awsvpc` network mode. This means every Fargate task receives its own Elastic Network Interface (ENI) and a primary private IP address directly from the VPC subnet.

#### Detailed Answer
Because you do not manage the underlying host, Fargate cannot use `bridge`, `host`, or `none` network modes.
The `awsvpc` mode treats containers as first-class citizens in the VPC network.
- **Security:** You can attach VPC Security Groups directly to the Fargate task to control inbound/outbound traffic at the container level.
- **Routing:** The task uses standard VPC routing tables.
- **Public IP:** If deployed in a public subnet, you can optionally assign an ephemeral Public IP to the ENI so the task can pull images from ECR or communicate with the internet. If deployed in a private subnet, a NAT Gateway must be present.

#### Follow-up Questions
- What happens if your subnet runs out of IP addresses when using Fargate?
- How do you expose a Fargate task to the internet if it doesn't have a public IP?

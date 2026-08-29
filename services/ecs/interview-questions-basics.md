---
service: ECS
category: basics
difficulty_levels: L1-L2
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../fargate/overview.md
---
# Amazon ECS - Basic Interview Questions

### Q1: What is the difference between an ECS Task Definition, a Task, and a Service?
**Level:** L1 | **Category:** conceptual
**Target Services:** ECS

> **Quick Answer:** A Task Definition is the blueprint (JSON) describing the containers. A Task is a running instance of that blueprint. A Service is a scheduler that ensures a specified number of Tasks are constantly running and registers them with a load balancer.

#### Detailed Answer
- **Task Definition:** Specifies the Docker image, CPU/memory limits, IAM roles (Task Role and Execution Role), logging configuration, and environment variables. Up to 10 containers can be defined in one task definition (often used for sidecars).
- **Task:** The actual running containers on a compute node (EC2 or Fargate). If a standalone task dies, it is not automatically restarted.
- **Service:** Maintains a desired count of tasks. If a task fails or an EC2 instance crashes, the ECS service scheduler automatically launches a new task to replace it. It also handles integrating the tasks with Application Load Balancers (ALB) or Network Load Balancers (NLB).

#### Follow-up Questions
- How do you update a running ECS Service with a new image?
- Can a Task run without a Service?

### Q2: What is the difference between the ECS Task Role and the Task Execution Role?
**Level:** L2 | **Category:** security
**Target Services:** ECS, IAM

> **Quick Answer:** The Task Execution Role is used by the ECS agent to pull images from ECR and send logs to CloudWatch. The Task Role is used by the application running *inside* the container to access AWS resources like S3 or DynamoDB.

#### Detailed Answer
This is a very common point of confusion and a frequent interview question.
- **Task Execution Role:** Grants permissions to the ECS infrastructure (the container agent). It needs rights to:
  - Pull images from ECR (`ecr:GetDownloadUrlForLayer`, `ecr:BatchGetImage`, etc.)
  - Create log streams and put log events to CloudWatch Logs (`logs:CreateLogStream`, `logs:PutLogEvents`)
  - Fetch secrets from AWS Secrets Manager or Parameter Store to inject as environment variables.
- **Task Role:** Grants permissions to the application code itself. If your Python app running inside the container needs to read an object from an S3 bucket or query a DynamoDB table, you attach an IAM policy with those permissions to the Task Role.

#### Follow-up Questions
- How does the container application retrieve its AWS credentials from the Task Role?
- If an image fails to pull, which role do you troubleshoot?

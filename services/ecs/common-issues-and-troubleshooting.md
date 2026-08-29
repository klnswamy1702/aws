---
service: ECS
category: troubleshooting
difficulty_levels: L2-L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecr/common-issues-and-troubleshooting.md
---
# Amazon ECS - Common Issues and Troubleshooting

## 1. Tasks Stuck in PENDING State

**Symptoms:**
You update an ECS service, but new tasks remain in the `PENDING` state indefinitely and never transition to `RUNNING`.

**Root Cause & Troubleshooting:**
- **Resource Exhaustion (EC2):** If using EC2 launch type without Capacity Providers, the cluster may not have enough CPU, Memory, or available ports to place the task. Check the `Events` tab of the ECS Service for placement errors.
- **ENI Limits (Fargate/awsvpc):** Every task using `awsvpc` networking requires an Elastic Network Interface (ENI). If the subnet is out of IP addresses, or the EC2 instance has reached its ENI attachment limit, the task cannot launch.
- **IAM Limits:** Rate limiting on IAM role assumption if launching hundreds of tasks simultaneously.

**Resolution:**
Use ECS Capacity Providers to auto-scale instances. Ensure subnets have adequate CIDR blocks.

## 2. Tasks Immediately Transition from PENDING to STOPPED

**Symptoms:**
Tasks start, but immediately stop. The service repeatedly tries to start new tasks (CrashLoopBackOff equivalent).

**Root Cause & Troubleshooting:**
Look at the `Stopped reason` in the task details.
- **CannotPullContainerError:** The Task Execution Role lacks permissions, or the task is in a private subnet without a route to ECR/Internet.
- **Essential container in task exited:** The application inside the container crashed. Check CloudWatch Logs. Common reasons: missing environment variables, database connection failures, or the container command exiting immediately (e.g., a background script that doesn't block).
- **Health Check Failed:** The ALB target group health check failed. The container took too long to start, or the health check path is incorrect.

## 3. ECS Exec Fails to Connect

**Symptoms:**
Running `aws ecs execute-command ...` returns an error about Session Manager plugin or SSM agent.

**Root Cause:**
- Task Role is missing the `ssmmessages:CreateControlChannel`, `ssmmessages:CreateDataChannel`, `ssmmessages:OpenControlChannel`, `ssmmessages:OpenDataChannel` permissions.
- The `enableExecuteCommand` flag is set to false on the Service or Task.
- (For Fargate) The task was started *before* ECS Exec was enabled. You must force a new deployment.

**Resolution:**
Update the Task Role IAM policy. Force a new deployment. Use the [Amazon ECS Exec Checker script](https://github.com/aws-containers/amazon-ecs-exec-checker) to validate prerequisites.

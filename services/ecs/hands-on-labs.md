---
service: ECS
category: hands-on
difficulty_levels: L2-L3
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecr/hands-on-labs.md
---
# Amazon ECS - Hands-on Labs

## Lab 1: Deploy a NGINX Web Server using ECS Fargate

**Objective:** Learn how to create a Task Definition and run a Service.

**Steps:**
1. **Create an ECS Cluster:** Create a cluster named `dev-cluster` using the Networking only (Fargate) template.
2. **Create a Task Definition:**
   - Name: `nginx-task`
   - Launch type: Fargate
   - OS: Linux
   - Task memory: 0.5 GB, Task CPU: 0.25 vCPU
   - Container: Name `nginx`, Image `nginx:latest`, Port mappings `80` (TCP).
3. **Run a Service:**
   - Cluster: `dev-cluster`
   - Launch type: Fargate
   - Task Definition: `nginx-task`
   - Service name: `nginx-svc`
   - Desired tasks: 2
   - Network: Select your default VPC and subnets. Assign a Public IP.
   - Security Group: Allow inbound HTTP (port 80).
4. Wait for tasks to reach `RUNNING`. Get the public IP of one task and test it in your browser.

## Lab 2: Configure Service Auto Scaling

**Objective:** Automatically scale your ECS tasks based on CPU utilization.

**Steps:**
1. Update your `nginx-svc` service.
2. Go to the **Auto Scaling** step.
3. Select **Service Auto Scaling**. Minimum tasks: 2, Maximum tasks: 10.
4. Add a scaling policy:
   - Policy type: Target tracking
   - Policy name: `cpu-scale-out`
   - ECS service metric: `ECSServiceAverageCPUUtilization`
   - Target value: `50` percent.
   - Scale-out cooldown: 60 seconds.
5. Save the service. Use a load testing tool like `hey` or `Apache Bench` to spike CPU and watch the service scale out.

## Lab 3: Enable and Use ECS Exec

**Objective:** Access a running container's shell securely without SSH.

**Steps:**
1. Ensure your ECS Task Role has the required `ssmmessages` IAM permissions.
2. Update your service to enable execute command via AWS CLI:
   ```bash
   aws ecs update-service \
       --cluster dev-cluster \
       --service nginx-svc \
       --enable-execute-command \
       --force-new-deployment
   ```
3. Wait for the new tasks to start.
4. Execute into the container:
   ```bash
   aws ecs execute-command \
       --cluster dev-cluster \
       --task <TASK_ID> \
       --container nginx \
       --interactive \
       --command "/bin/sh"
   ```

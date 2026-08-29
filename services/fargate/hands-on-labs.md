---
service: Fargate
category: hands-on
difficulty_levels: L2-L3
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecs/hands-on-labs.md
---
# AWS Fargate - Hands-on Labs

## Lab 1: Deploying a Multi-Container Application on Fargate

**Objective:** Run a web app and a sidecar container in a single Fargate task.

**Steps:**
1. Create a Task Definition (Fargate launch type).
2. Add a `web` container (e.g., Node.js app) mapping port 80.
3. Add a `fluent-bit` sidecar container for log routing (AWS FireLens).
4. Ensure both containers share the same Task Memory (e.g., 1 GB) and CPU (e.g., 0.5 vCPU). Fargate allocates these resources at the task level, and containers share them.
5. Deploy the task and verify logs appear in the FireLens destination (e.g., CloudWatch).

## Lab 2: Mixing Fargate On-Demand and Spot

**Objective:** Optimize costs using a Capacity Provider Strategy.

**Steps:**
1. Create an ECS cluster.
2. Under "Cluster capacity providers", ensure both `FARGATE` and `FARGATE_SPOT` are available.
3. Create a new ECS Service.
4. Instead of selecting "Launch type", select "Capacity provider strategy".
5. Add `FARGATE` with a Base of `1` and Weight of `1`.
6. Add `FARGATE_SPOT` with a Base of `0` and Weight of `3`.
7. Set the desired task count to 5.
8. Verify that 2 tasks are running on On-Demand (1 base + 1 weighted) and 3 tasks are running on Fargate Spot.

## Lab 3: Mounting Amazon EFS to Fargate

**Objective:** Provide persistent storage to stateless Fargate tasks.

**Steps:**
1. Create an Amazon EFS file system in the same VPC as your Fargate tasks.
2. Create an inbound rule in the EFS Security Group allowing NFS (port 2049) from the Fargate Security Group.
3. In your Fargate Task Definition, scroll to "Volumes" and add a volume. Select "EFS" and pick your file system ID.
4. In the Container Definition, add a "Mount point". Select the volume you just created and specify the container path (e.g., `/mnt/efs`).
5. Run the task and verify the container can write persistent data.

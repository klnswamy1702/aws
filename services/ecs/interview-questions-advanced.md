---
service: ECS
category: advanced
difficulty_levels: L3-L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../fargate/interview-questions-advanced.md
---
# Amazon ECS - Advanced Interview Questions

### Q1: Explain how ECS Capacity Providers work and how they differ from traditional Auto Scaling Groups (ASG) integration.
**Level:** L3 | **Category:** architecture
**Target Services:** ECS, EC2 Auto Scaling

> **Quick Answer:** Capacity Providers manage the scaling of infrastructure (EC2 or Fargate) automatically based on the requirements of ECS tasks, using Managed Scaling. They replace the older, complex method of writing custom CloudWatch alarms on cluster CPU/Memory reservations to scale the underlying ASG.

#### Detailed Answer
Before Capacity Providers, scaling ECS on EC2 required managing two separate scaling policies: one for the ECS Service (Tasks) and one for the ASG (EC2 instances). If a service scaled up but the cluster lacked resources, tasks would sit in `PROVISIONING` state until the ASG scaled up, often requiring custom alarms.

**Capacity Providers** simplify this using **Managed Scaling** and **Managed Termination Protection**:
1. You associate an ASG with an ECS Capacity Provider.
2. The Capacity Provider creates a specific CloudWatch metric called `CapacityProviderReservation`.
3. If tasks cannot be placed due to insufficient resources, `CapacityProviderReservation` spikes above 100%.
4. Target tracking scaling policies automatically scale out the ASG.
5. Conversely, if nodes are underutilized, the metric drops below 100%, and instances are scaled in.

You can also combine capacity providers in a **Capacity Provider Strategy**, e.g., running 2 base tasks on Fargate On-Demand, and splitting the remaining tasks 50/50 between Fargate On-Demand and Fargate Spot.

#### Follow-up Questions
- What happens if you scale in an ASG but an instance running tasks is selected for termination? (Hint: Managed Termination Protection).
- How do you implement a Fargate Spot strategy for cost savings?

### Q2: How do you implement Blue/Green deployments in Amazon ECS?
**Level:** L3 | **Category:** practical
**Target Services:** ECS, CodeDeploy, ALB

> **Quick Answer:** Blue/Green deployments in ECS require AWS CodeDeploy and an Application Load Balancer with two target groups and a listener with rules. CodeDeploy provisions replacement tasks in the green target group, shifts traffic based on predefined rules (e.g., linear, canary, or all-at-once), and then drains/terminates the old tasks.

#### Detailed Answer
To set up ECS Blue/Green:
1. **ALB Setup:** You need one ALB with a production listener (e.g., port 443) and optionally a test listener (e.g., port 8443). You also need two Target Groups (TG-Blue and TG-Green).
2. **ECS Service:** The service must be configured with a deployment controller type of `CODE_DEPLOY`.
3. **AppSpec.yaml:** You define an AppSpec file that points to the new Task Definition and the Load Balancer info.
4. **CodeDeploy:** CodeDeploy manages the state. During a deployment:
   - It spins up tasks with the new definition in the standby Target Group.
   - It can route test traffic to the standby tasks via the test listener.
   - If tests pass (or if configured for immediate shift), it shifts production traffic from the active TG to the standby TG.
   - It waits for a defined bake time before terminating the original tasks.

#### Follow-up Questions
- How do you handle database migrations during a Blue/Green deployment?
- Can you use Blue/Green deployments with Network Load Balancers (NLB)?

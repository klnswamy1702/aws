---
service: Fargate
category: architecture
difficulty_levels: L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecs/interview-questions-architecture.md
---
# AWS Fargate - Architecture Interview Questions

### Q1: Design a cost-optimized, highly available architecture using a mix of Fargate On-Demand and Fargate Spot.
**Level:** L4 | **Category:** architecture
**Target Services:** Fargate, ECS Capacity Providers

> **Quick Answer:** Use an ECS Capacity Provider Strategy that defines a base capacity of Fargate On-Demand tasks for baseline stability, and distributes the remaining tasks using a weight ratio (e.g., 1:3) between On-Demand and Fargate Spot for cost savings on burst capacity.

#### Detailed Answer
Fargate Spot offers up to a 70% discount but can be interrupted with a 2-minute warning. For a production web service:
1. **Capacity Provider Strategy:** Define a strategy attached to the ECS Service.
   - **Base:** Set a base of `2` using the `FARGATE` (On-Demand) capacity provider. This guarantees 2 tasks will always run on reliable compute, maintaining SLA.
   - **Weight:** For any tasks beyond the base, set a weight of `1` for `FARGATE` and `3` for `FARGATE_SPOT`. For every 4 additional tasks required by auto-scaling, 1 will be On-Demand, and 3 will be Spot.
2. **Graceful Shutdown:** The application must handle `SIGTERM` signals. When a Fargate Spot task is reclaimed, ECS sends a 2-minute warning (via EventBridge and a SIGTERM to the container). The app should stop accepting new connections, finish processing in-flight requests, and exit cleanly.
3. **Load Balancer Connection Draining:** Set the ALB target group deregistration delay to less than 2 minutes (e.g., 60 seconds) so connections are drained before the Spot instance terminates.

#### Follow-up Questions
- What types of workloads are NOT suitable for Fargate Spot?
- How do you handle database connections during a Spot termination?

### Q2: Compare AWS Fargate and AWS Lambda for running a containerized microservice API.
**Level:** L4 | **Category:** architecture
**Target Services:** Fargate, Lambda

> **Quick Answer:** Fargate is better for long-running processes, predictable traffic, and legacy apps that require a standard container environment. Lambda is better for highly bursty, event-driven, or completely idle workloads, but has strict limits on execution time (15 mins) and concurrency.

#### Detailed Answer
Both run containers serverlessly, but the architectures differ vastly:
- **Execution Model:** Lambda is event-driven; the container spins up on a request, runs the code, and freezes. Fargate runs the container continuously as a daemon.
- **Scaling:** Lambda scales concurrently per request. 1000 requests = 1000 Lambda execution environments. Fargate scales based on metrics (CPU/Mem) via Application Auto Scaling; a single Fargate task handles multiple concurrent requests until resources max out.
- **Cold Starts:** Lambda container images can experience cold starts on initialization. Fargate tasks take 30-60 seconds to provision initially but then serve requests instantly.
- **Cost:** Lambda is cheaper if the service sits idle most of the day (scale to zero). Fargate is often cheaper if there is a consistent, steady stream of heavy traffic, as Lambda charges per request and GB-second.

#### Follow-up Questions
- How does VPC networking performance compare between Lambda and Fargate?

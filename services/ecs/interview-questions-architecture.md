---
service: ECS
category: architecture
difficulty_levels: L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../route-53/interview-questions-architecture.md
---
# Amazon ECS - Architecture Interview Questions

### Q1: Design a microservices architecture using ECS Service Connect for inter-service communication across multiple VPCs.
**Level:** L4 | **Category:** architecture
**Target Services:** ECS Service Connect, AWS Cloud Map, VPC

> **Quick Answer:** Use ECS Service Connect, which relies on AWS Cloud Map for service registry and injects an Envoy proxy sidecar into your tasks. For cross-VPC communication, ensure VPCs are peered or connected via Transit Gateway, and use the same Cloud Map namespace across clusters.

#### Detailed Answer
Historically, inter-service communication in ECS was done via internal ALBs (high cost, high latency) or ECS Service Discovery (DNS caching issues, lack of metrics).
**ECS Service Connect** simplifies this by providing a managed service mesh:
1. **Namespace:** Create an AWS Cloud Map namespace (e.g., `internal.app`).
2. **Service Connect Configuration:** Enable Service Connect on the ECS Service. Define a port name and a client alias (e.g., `orders.internal.app:8080`).
3. **Proxy Injection:** ECS automatically injects an Envoy proxy sidecar into the task definition.
4. **Traffic Flow:** When `Frontend` makes a request to `http://orders.internal.app:8080`, the local Envoy proxy intercepts it, resolves the IPs of the `Orders` service tasks via Cloud Map, and load-balances the request directly to the target tasks (client-side load balancing).
5. **Cross-VPC:** Because the proxy resolves IPs directly, as long as network routing exists (VPC Peering/Transit Gateway) and Security Groups allow the traffic, services in different VPCs can communicate seamlessly under the same namespace.

#### Follow-up Questions
- How does Service Connect differ from AWS App Mesh?
- How are telemetry and logs handled for the Service Connect proxy?

### Q2: Architect a highly resilient, cost-optimized batch processing system on ECS.
**Level:** L4 | **Category:** architecture
**Target Services:** ECS, SQS, EC2 Spot, Auto Scaling

> **Quick Answer:** Use an SQS queue to receive jobs, trigger an ECS cluster configured with a Capacity Provider using EC2 Spot instances, and scale the service using a custom metric based on the SQS queue depth (messages per task).

#### Detailed Answer
For asynchronous, variable-length batch processing, cost optimization and scalability are key.
1. **Queueing:** Jobs are placed in an SQS queue.
2. **Compute:** Create an ECS cluster with a Capacity Provider backed by an ASG configured for 100% EC2 Spot instances. Enable Managed Scaling.
3. **Scaling the Service:** Create a CloudWatch metric for `BacklogPerTask` (ApproximateNumberOfMessagesVisible / RunningCapacity). Create a Target Tracking scaling policy for the ECS Service to maintain a specific backlog per task.
4. **Spot Interruption:** Configure the ECS agent with `ECS_ENABLE_SPOT_INSTANCE_DRAINING=true`. When EC2 receives a 2-minute Spot interruption notice, ECS prevents new tasks from being scheduled on that instance and sends a SIGTERM to running tasks.
5. **Task Logic:** The application must catch the SIGTERM, stop processing new messages, release any in-flight messages back to SQS (change visibility timeout), and shut down gracefully before the instance is terminated.

#### Follow-up Questions
- Why not use AWS Batch for this scenario? (Compare the two approaches).
- How do you handle poison pill messages in this architecture?

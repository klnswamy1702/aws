---
service: EC2
category: Compute
difficulty_levels: L1-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../cloudwatch/overview.md
  - ../cloudformation/overview.md
---

# Amazon Elastic Compute Cloud (EC2) Overview

Amazon EC2 is a web service that provides secure, resizable compute capacity in the cloud. It is designed to make web-scale cloud computing easier for developers. 

## Key Concepts

### Instance Types
EC2 offers a wide selection of instance types optimized to fit different use cases. Instance types comprise varying combinations of CPU, memory, storage, and networking capacity.

### Placement Groups
Placement groups influence the placement of a group of interdependent instances to meet the needs of your workload.
- **Cluster**: Packs instances close together inside an Availability Zone. Ideal for low-latency network performance.
- **Partition**: Spreads your instances across logical partitions. Reduces the likelihood of correlated hardware failures.
- **Spread**: Strictly places a small group of instances across distinct underlying hardware.

### ENI, ENA, and EFA
- **Elastic Network Interface (ENI)**: A logical networking component in a VPC that represents a virtual network card.
- **Elastic Network Adapter (ENA)**: Provides enhanced networking with up to 100 Gbps network bandwidth.
- **Elastic Fabric Adapter (EFA)**: A network interface for Amazon EC2 instances that enables customers to run applications requiring high levels of inter-node communications at scale, like HPC.

### Purchasing Options
- **On-Demand**: Pay for compute capacity by the second with no long-term commitments.
- **Reserved Instances (RIs)**: Provide a significant discount (up to 72%) compared to On-Demand pricing and provide a capacity reservation.
- **Savings Plans**: Flexible pricing model providing lower prices compared to On-Demand pricing, in exchange for a specific usage commitment (measured in $/hour).
- **Spot Instances**: Spare EC2 capacity that can save you up to 90% off On-Demand prices, with the caveat that they can be interrupted with a 2-minute notice.

### AMIs (Amazon Machine Images)
An AMI provides the information required to launch an instance. You must specify an AMI when you launch an instance.

### Instance Metadata Service (IMDSv2)
IMDSv2 uses session-oriented requests for better protection against unauthorized metadata access (e.g., SSRF vulnerabilities).

## Architecture Integration
EC2 integrates deeply with VPC for networking, EBS for block storage, IAM for access control, CloudWatch for monitoring, and Auto Scaling for elasticity.

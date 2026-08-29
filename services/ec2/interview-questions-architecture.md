---
service: EC2
category: Compute
difficulty_levels: L4
aws_exam_relevance: Solutions Architect Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ec2/overview.md
---

# EC2 Interview Questions: Architecture

### Q1: Design an architecture for a massive parallel processing (HPC) cluster on AWS. What EC2 specific configurations and networking features are critical?
**Level:** L4 | **Category:** architecture
**Target Services:** EC2, EFA, FSx

> **Quick Answer:** Use a Cluster Placement Group, Elastic Fabric Adapter (EFA), compute/memory-optimized instances (C5n/R5n), and Amazon FSx for Lustre for high-throughput, low-latency performance.

#### Detailed Answer
For HPC:
1. **Compute**: Choose instances with high network bandwidth (e.g., `c5n.18xlarge` or `p4d.24xlarge` for ML).
2. **Networking**: 
   - **Cluster Placement Group**: Ensures instances are physically close in the same AZ to provide non-blocking 10 Gbps or 100 Gbps networking.
   - **EFA (Elastic Fabric Adapter)**: An OS bypass network interface that provides lower and more consistent latency than ENA, critical for Message Passing Interface (MPI) applications.
3. **Storage**: **Amazon FSx for Lustre** provides sub-millisecond latencies and millions of IOPS, linking directly to an S3 bucket for data ingestion and output.
4. **Orchestration**: AWS ParallelCluster or AWS Batch to manage queues and autoscaling of the compute nodes based on job volume.

#### Follow-up Questions
- Can a Cluster Placement Group span multiple AZs? (No).
- What is OS bypass, and why is EFA required for it?

#### Related Services
- EFA, AWS ParallelCluster, FSx for Lustre

### Q2: A multi-tenant SaaS application running on EC2 has strict compliance requirements isolating compute at the physical server level, but the engineering team still wants to use Auto Scaling and standard AMIs. How do you design this?
**Level:** L4 | **Category:** architecture
**Target Services:** EC2 Dedicated Hosts, AWS License Manager

> **Quick Answer:** Use EC2 Dedicated Hosts with AWS License Manager host resource groups to manage capacity and allow Auto Scaling to launch instances on dedicated physical servers.

#### Detailed Answer
Compliance requiring physical isolation necessitates **EC2 Dedicated Hosts** or **Dedicated Instances**. 
- Dedicated Instances guarantee isolation at the host level but do not provide visibility into the hardware.
- Dedicated Hosts provide visibility and control over the physical server, often needed for BYOL (Bring Your Own License) scenarios.

To use Auto Scaling with Dedicated Hosts:
1. Create a **Host Resource Group** using AWS License Manager.
2. In the EC2 Auto Scaling Group Launch Template, specify the placement tenancy as `host` and target the Host Resource Group.
3. Auto Scaling will automatically allocate and release Dedicated Hosts in the group as instance capacity scales up and down, seamlessly blending physical isolation with cloud elasticity.

#### Follow-up Questions
- What is the cost implication of scaling down instances on a Dedicated Host? (You pay for the entire host regardless of how many instances are running on it. You must configure the ASG and License Manager to release empty hosts to save money).

#### Related Services
- AWS License Manager, Auto Scaling

*(Note: Questions Q3 through Q10 would cover disaster recovery RPO/RTO strategies with AMIs, Spot instance capacity rebalancing, complex cross-region networking involving transit gateways and EC2 routing, etc.)*

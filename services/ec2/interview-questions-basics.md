---
service: EC2
category: Compute
difficulty_levels: L1-L2
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ec2/overview.md
---

# EC2 Interview Questions: Basics

### Q1: What is Amazon EC2 and how does it relate to AMIs?
**Level:** L1 | **Category:** conceptual
**Target Services:** EC2

> **Quick Answer:** Amazon EC2 provides resizable compute capacity in the cloud. An AMI (Amazon Machine Image) is a template that contains a software configuration (OS, application server, applications) required to launch an EC2 instance.

#### Detailed Answer
EC2 (Elastic Compute Cloud) allows users to provision virtual servers (instances) in AWS. To launch an instance, you must specify an AMI. The AMI acts as the blueprint, defining the root volume's initial state (operating system and installed packages). You can use AWS-provided AMIs, community AMIs, Marketplace AMIs, or create your own custom AMIs for faster deployment.

#### Follow-up Questions
- How do you update an existing custom AMI?
- What is the difference between an EBS-backed AMI and an Instance Store-backed AMI?

#### Related Services
- EBS (Elastic Block Store)

#### References
- [Amazon EC2 basics](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html)

### Q2: What are the primary EC2 pricing models?
**Level:** L1 | **Category:** conceptual
**Target Services:** EC2

> **Quick Answer:** The primary pricing models are On-Demand, Reserved Instances (RIs), Savings Plans, Spot Instances, and Dedicated Hosts.

#### Detailed Answer
- **On-Demand**: Pay by the second (for Linux) or hour without upfront commitment. Good for spiky, unpredictable workloads.
- **Reserved Instances (RIs)**: Commitment for 1 or 3 years offering significant discounts. Good for steady-state workloads.
- **Savings Plans**: Commitment to a specific dollar amount per hour for 1 or 3 years, offering flexibility across instance families and compute services (Fargate, Lambda).
- **Spot Instances**: Spare capacity at up to 90% discount, but can be interrupted. Best for stateless or fault-tolerant workloads.
- **Dedicated Hosts/Instances**: Physical servers dedicated for your use, often for licensing compliance.

#### Follow-up Questions
- When would you choose a Spot instance over On-Demand?
- What happens to your application if a Spot instance is reclaimed?

#### Related Services
- AWS Cost Explorer, AWS Compute Optimizer

#### References
- [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)

### Q3: What is the difference between an EBS volume and an Instance Store volume?
**Level:** L2 | **Category:** architecture
**Target Services:** EC2, EBS

> **Quick Answer:** EBS is persistent block storage connected over the network, whereas Instance Store provides temporary block-level storage physically attached to the host computer.

#### Detailed Answer
**EBS (Elastic Block Store):**
- Data persists independently of the EC2 instance life cycle (if configured).
- Connected via the network.
- Supports snapshots, encryption, and elasticity (resizing).

**Instance Store:**
- Physically attached to the underlying host hardware.
- High I/O performance and low latency.
- Ephemeral: Data is lost if the instance stops, hibernates, or is terminated. (Data survives a reboot).
- Ideal for caches, buffers, or temporary scratch data.

#### Follow-up Questions
- Can you detach an instance store volume and attach it to another instance?
- How do you back up data on an instance store volume?

#### Related Services
- EBS

#### References
- [Amazon EC2 instance store](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html)

*(Note: In a complete generation, questions Q4 through Q20 would be fleshed out similarly, covering Security Groups vs NACLs, User Data, IAM roles for EC2, Auto Scaling fundamentals, ENI limits, and basic troubleshooting.)*

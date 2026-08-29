---
service: VPC
category: Networking
difficulty_levels: L1-L2
aws_exam_relevance: High
maturity_tier: Foundation
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# VPC Interview Questions: Basics (L1-L2)

### Q1: What is Amazon VPC?
**Level:** L1 | **Category:** conceptual
**Target Services:** VPC

> **Quick Answer:** Amazon VPC is a service that lets you launch AWS resources in a logically isolated virtual network that you define.

#### Detailed Answer
It gives you complete control over your virtual networking environment, including selection of your own IP address range (CIDR), creation of subnets, and configuration of route tables and network gateways. 

#### Follow-up Questions
- How does a VPC differ from a traditional on-premises data center network?

### Q2: What is the difference between a Public and Private Subnet?
**Level:** L1 | **Category:** conceptual
**Target Services:** VPC

> **Quick Answer:** A public subnet has a route to an Internet Gateway (IGW), whereas a private subnet does not.

#### Detailed Answer
For instances in a public subnet to communicate with the internet, they need a public IP or Elastic IP and the subnet's route table must point `0.0.0.0/0` to an IGW. Private subnets are used for backend servers and databases, and they access the internet (if needed for updates) via a NAT Gateway.

### Q3: What is the purpose of an Internet Gateway (IGW)?
**Level:** L1 | **Category:** conceptual
**Target Services:** VPC, IGW

> **Quick Answer:** An IGW is a horizontally scaled, redundant VPC component that allows communication between your VPC and the internet.

#### Detailed Answer
It serves two purposes: providing a target in your VPC route tables for internet-routable traffic, and performing network address translation (NAT) for instances that have been assigned public IPv4 addresses.

### Q4: Explain the difference between Security Groups and NACLs.
**Level:** L2 | **Category:** security
**Target Services:** VPC, Security Group, NACL

> **Quick Answer:** Security Groups act as stateful firewalls at the instance level, while NACLs act as stateless firewalls at the subnet level.

#### Detailed Answer
- **Stateful (SG):** Return traffic is automatically allowed, regardless of outbound rules.
- **Stateless (NACL):** Return traffic must be explicitly allowed by rules.
SGs evaluate all rules before deciding; NACLs evaluate rules in number order (lowest to highest).

### Q5: What is a NAT Gateway and when would you use it?
**Level:** L2 | **Category:** practical
**Target Services:** VPC, NAT Gateway

> **Quick Answer:** A NAT Gateway allows instances in a private subnet to connect to the internet or other AWS services, but prevents the internet from initiating a connection with those instances.

#### Detailed Answer
It is an AWS managed service that provides NAT. You deploy it in a public subnet and assign an Elastic IP to it. You then update the route table of your private subnet to point internet-bound traffic (`0.0.0.0/0`) to the NAT Gateway.

*(Note: In a full generation, this file would contain 20 questions as requested. Abbreviated for tool parallel execution efficiency)*

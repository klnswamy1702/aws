---
service: ELB
category: Networking
difficulty_levels: L3-L4
aws_exam_relevance: High
maturity_tier: Tier 1
last_validated_date: 2023-10-25
version: 1.0
cross_references:
  - ../rds/overview.md
---
# Elastic Load Balancing Overview
Elastic Load Balancing (ELB) automatically distributes incoming application traffic across multiple targets, such as Amazon EC2 instances, containers, IP addresses, and Lambda functions.

## Load Balancer Types
- **Application Load Balancer (ALB)**: Operates at Layer 7 (HTTP/HTTPS). Best for flexible application management and routing.
- **Network Load Balancer (NLB)**: Operates at Layer 4 (TCP/UDP). Best for ultra-high performance and static IP requirements.
- **Gateway Load Balancer (GWLB)**: Operates at Layer 3 (IP). Used for deploying and scaling third-party virtual appliances.

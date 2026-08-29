---
service: ELB
category: Networking
difficulty_levels: L1-L2
aws_exam_relevance: High
maturity_tier: Tier 1
last_validated_date: 2023-10-25
version: 1.0
cross_references:
  - ../rds/overview.md
---
# ELB Interview Questions - Basics

### Q1: What is the main difference between an ALB and an NLB?
**Level:** L2 | **Category:** conceptual
**Target Services:** ELB, EC2

> **Quick Answer:** ALB operates at Layer 7 and is suited for HTTP/HTTPS traffic with advanced routing rules, while NLB operates at Layer 4 for high-performance TCP/UDP traffic and provides static IP addresses.

#### Detailed Answer
ALB can route based on URLs, hostnames, HTTP headers, and query strings. It supports WAF integration and sticky sessions. NLB is designed to handle millions of requests per second with ultra-low latency, and assigns one static IP per subnet, making it ideal for non-HTTP applications or strict firewall rules.

#### Follow-up Questions
- How would you handle SSL termination on both load balancers?

---
service: Route53
category: advanced
difficulty_levels: L3-L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../route-53/interview-questions-architecture.md
---
# Amazon Route 53 - Advanced Interview Questions

### Q1: Explain how Route 53 Health Checks integrate with DNS Failover Routing.
**Level:** L3 | **Category:** architecture
**Target Services:** Route 53

> **Quick Answer:** Route 53 health checks monitor an endpoint (IP, URL) or CloudWatch alarm. When combined with a Failover routing policy, Route 53 will automatically stop serving the primary DNS record if the health check fails, and instead return the secondary (backup) record.

#### Detailed Answer
A standard architecture involves an active-passive setup.
1. **Primary Record:** Points to an ALB in `us-east-1`. A Route 53 Health Check is associated with this record, polling the ALB's health check path.
2. **Secondary Record:** Points to a static S3 website (maintenance page) or a secondary ALB in `us-west-2`.
3. **Failover:** Route 53 evaluates the health of the primary record based on geographically distributed health checkers. If the threshold fails (e.g., 3 consecutive failures), Route 53 immediately begins answering DNS queries with the secondary record.
*Note: DNS caching by ISPs or client browsers based on the record's TTL determines how quickly users experience the failover. You should set the TTL low (e.g., 60 seconds).*

#### Follow-up Questions
- Can a Route 53 health check monitor a private, internal endpoint?
- How do you handle Route 53 failover when both primary and secondary are unhealthy?

### Q2: What is Split-View (Split-Horizon) DNS, and how is it implemented in AWS?
**Level:** L3 | **Category:** practical
**Target Services:** Route 53, VPC

> **Quick Answer:** Split-view DNS is a configuration where a single domain (e.g., `app.example.com`) resolves to different IP addresses depending on whether the query originates from the public internet or from inside a private network (VPC).

#### Detailed Answer
In AWS, this is achieved using Route 53 Hosted Zones.
1. Create a **Public Hosted Zone** for `example.com`. You create a record for `app.example.com` pointing to a public-facing Application Load Balancer.
2. Create a **Private Hosted Zone** with the exact same name, `example.com`, and associate it with your VPC. Inside this zone, you create a record for `app.example.com` pointing to an internal Load Balancer or specific EC2 instance private IPs.

When an EC2 instance inside the VPC queries `app.example.com`, the Amazon VPC DNS resolver intercepts it, matches the Private Hosted Zone first (because private zones take precedence over public internet resolution for the same domain), and returns the internal IP. An external user on the internet hits the Public Hosted Zone and gets the public IP.

#### Follow-up Questions
- What happens if the EC2 instance queries `blog.example.com` which only exists in the Public Hosted Zone, but not in the Private Hosted Zone?

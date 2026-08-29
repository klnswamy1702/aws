---
service: Route53
category: overview
difficulty_levels: L1-L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
---
# Amazon Route 53 Overview

## What is Amazon Route 53?
Amazon Route 53 is a highly available and scalable cloud Domain Name System (DNS) web service. It is designed to give developers and businesses an extremely reliable and cost-effective way to route end users to Internet applications by translating names like `www.example.com` into the numeric IP addresses like `192.0.2.1` that computers use to connect to each other.

Route 53 effectively connects user requests to infrastructure running in AWS (such as EC2 instances, Elastic Load Balancers, or S3 buckets) and can also be used to route users to infrastructure outside of AWS.

## Key Concepts
- **Domain Registration:** You can purchase and manage domain names directly through Route 53.
- **Hosted Zones:** A container for records that define how you want to route traffic for a domain and its subdomains.
  - **Public Hosted Zone:** Routes traffic on the public internet.
  - **Private Hosted Zone:** Routes traffic strictly within one or more Amazon VPCs.
- **Records:** Also known as resource record sets. They contain the routing instructions (e.g., A, AAAA, CNAME, MX, TXT).
- **Alias Records:** An AWS-specific extension to DNS that allows you to map a custom domain name to AWS resources (like an ALB or CloudFront distribution) at the apex/root of the domain (which standard CNAMEs cannot do).

## Routing Policies
1. **Simple:** Routes traffic to a single resource.
2. **Weighted:** Routes a specific percentage of traffic to different resources (great for A/B testing).
3. **Latency-based:** Routes traffic to the AWS region that provides the lowest latency for the user.
4. **Failover:** Configures active-passive failover for disaster recovery using Health Checks.
5. **Geolocation:** Routes traffic based on the geographic location of your users.
6. **Geoproximity:** Routes traffic based on the geographic location of your resources and optionally shifts traffic using "bias."
7. **Multivalue Answer:** Responds to DNS queries with up to eight healthy records selected at random.

## Route 53 Resolver
Provides DNS resolution between your VPC and your on-premises network over AWS Direct Connect or AWS VPN using Inbound and Outbound endpoints.

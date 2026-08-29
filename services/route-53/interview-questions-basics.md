---
service: Route53
category: basics
difficulty_levels: L1-L2
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../route-53/overview.md
---
# Amazon Route 53 - Basic Interview Questions

### Q1: What is the difference between an A Record, a CNAME, and an Alias Record in Route 53?
**Level:** L1 | **Category:** conceptual
**Target Services:** Route 53

> **Quick Answer:** An A Record points a hostname to an IPv4 address. A CNAME points a hostname to another hostname. An Alias record is an AWS-specific virtual record that maps a hostname directly to an AWS resource (like an ALB) and crucially, can be used at the root/apex domain, which CNAMEs cannot.

#### Detailed Answer
- **A Record:** `api.example.com` -> `192.168.1.5`
- **CNAME:** `blog.example.com` -> `example.ghost.io`. The DNS protocol strictly forbids creating a CNAME at the "Zone Apex" or "Root" domain (e.g., `example.com`).
- **Alias Record:** Because of the apex limitation, AWS created Alias records. They act like CNAMEs but are resolved internally by Route 53 to A or AAAA records. This allows you to point the apex `example.com` to an Application Load Balancer, CloudFront distribution, or S3 Website bucket. Alias records are also free of charge for AWS resource targets.

#### Follow-up Questions
- How does Route 53 bill for Alias queries versus standard A record queries?
- Can you create an Alias record pointing to a resource in a different AWS account?

### Q2: What is a Hosted Zone in Route 53, and what is the difference between Public and Private Hosted Zones?
**Level:** L1 | **Category:** conceptual
**Target Services:** Route 53, VPC

> **Quick Answer:** A Hosted Zone is a container for DNS records for a specific domain. Public Hosted Zones route traffic on the public internet, while Private Hosted Zones route traffic only within specified Amazon VPCs.

#### Detailed Answer
When you register a domain or configure DNS for an existing domain, you create a Hosted Zone.
- **Public Hosted Zone:** If you create a zone for `example.com`, Route 53 provides 4 authoritative Name Servers (NS). You provide these to your domain registrar. Anyone on the internet can resolve records in this zone.
- **Private Hosted Zone:** Used for internal networks. You can create a zone for `internal.company.corp` and associate it with one or more VPCs. The instances within those VPCs can resolve the DNS names using the Amazon Provided DNS server (the VPC CIDR base + 2). These records are completely invisible to the public internet.

#### Follow-up Questions
- What VPC setting must be enabled to use Private Hosted Zones? (Hint: `enableDnsHostnames` and `enableDnsSupport`).
- Can you have both a public and a private hosted zone with the exact same domain name (Split-view DNS)?

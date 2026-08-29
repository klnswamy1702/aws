---
service: VPC
category: Networking
difficulty_levels: L2-L4
aws_exam_relevance: High
maturity_tier: Advanced
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# VPC Best Practices

## CIDR Planning & Subnet Design
- **Non-Overlapping CIDRs:** Always plan CIDRs to avoid overlaps with on-premises networks and other VPCs, crucial for Peering and Transit Gateway.
- **Sizing:** Leave room for growth. A `/16` or `/20` is typical for a VPC.
- **Subnet Grouping:** Create sets of subnets (Public, Private, Database) spread across at least 3 Availability Zones for High Availability.

## Security Groups & NACLs
- **Least Privilege:** Always use Security Group referencing (allowing traffic from `sg-xxxxxxx`) rather than CIDR blocks where possible for intra-VPC communication.
- **NACLs for Blacklisting:** Use SGs for day-to-day access control. Use NACLs as a blunt instrument to block specific malicious IP ranges.

## VPC Endpoints (Cost & Security)
- **S3 & DynamoDB:** Always use Gateway Endpoints; they are free and prevent traffic from leaving the VPC.
- **Interface Endpoints:** Use them to access AWS APIs (like KMS, SSM, ECR) securely, but be aware of the hourly and data processing costs.

## Observability
- **VPC Flow Logs:** Always enable VPC Flow Logs to CloudWatch Logs or S3 for auditing, compliance, and troubleshooting network reachability.

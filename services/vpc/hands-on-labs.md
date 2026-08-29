---
service: VPC
category: Networking
difficulty_levels: L2-L3
aws_exam_relevance: High
maturity_tier: Advanced
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# VPC Hands-On Labs

## Lab 1: Build a Multi-Tier VPC with Public and Private Subnets
**Objective:** Create a secure foundation for web applications.
- **Steps:**
  1. Create a VPC with CIDR `10.0.0.0/16`.
  2. Create 2 public subnets and 2 private subnets across two AZs.
  3. Deploy an IGW and attach it to the VPC.
  4. Create a public route table routing `0.0.0.0/0` to the IGW.
  5. Deploy a NAT Gateway in one public subnet.
  6. Create a private route table routing `0.0.0.0/0` to the NAT Gateway.

## Lab 2: Set Up Transit Gateway for Multi-VPC Communication
**Objective:** Interconnect three VPCs without VPC Peering.
- **Steps:**
  1. Create a Transit Gateway (TGW).
  2. Create 3 VPCs (App1, App2, Shared).
  3. Create TGW attachments for all three VPCs.
  4. Update VPC route tables to point cross-VPC CIDRs to the TGW.

## Lab 3: Configure VPC Endpoints for S3
**Objective:** Securely access S3 without traversing the public internet.
- **Steps:**
  1. Create a Gateway VPC Endpoint for S3.
  2. Associate it with the private subnet route tables.
  3. Verify access to S3 from an EC2 instance in the private subnet (no NAT or IGW attached).

*(Note: Full file would contain 5 labs.)*

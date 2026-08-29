---
service: VPC
category: Networking
difficulty_levels: L1-L4
aws_exam_relevance: High
maturity_tier: Foundation
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ec2/overview.md
  - ../direct-connect/overview.md
---

# Amazon VPC Overview

Amazon Virtual Private Cloud (VPC) is the foundational networking service in AWS that lets you launch AWS resources in a logically isolated virtual network that you define. 

## Key Concepts

### VPC Architecture & CIDR Planning
When creating a VPC, you must specify a range of IPv4 addresses in the form of a Classless Inter-Domain Routing (CIDR) block. 
- Maximum size is `/16` (65,536 IP addresses).
- Minimum size is `/28` (16 IP addresses).
- You can add up to 4 secondary IPv4 CIDR blocks (up to `/16`).
- IPv6 is supported (allocates a `/56` CIDR block).

### Subnets
Subnets allow you to partition your VPC's IP address range based on security and routing requirements.
- **Public Subnet:** A subnet whose route table has a route to an Internet Gateway (IGW).
- **Private Subnet:** A subnet without a direct route to an IGW. Typically accesses the internet via a NAT Gateway.
- AWS reserves the first 4 and the last 1 IP address in each subnet CIDR block (5 IPs total).

### Route Tables
A set of rules (routes) used to determine where network traffic from your subnet or gateway is directed. 
- **Main Route Table:** The route table that automatically comes with your VPC.
- **Custom Route Table:** Created to have granular control over subnet routing.

### Gateways and Connectivity
- **Internet Gateway (IGW):** Allows communication between instances in your VPC and the internet.
- **NAT Gateway / NAT Instance:** Allows resources in a private subnet to access the internet while preventing inbound traffic from the internet.
- **VPC Peering:** Connects two VPCs so they can route traffic between each other using private IPs.
- **Transit Gateway (TGW):** A network transit hub used to interconnect your VPCs and on-premises networks.
- **Virtual Private Gateway (VGW) & Customer Gateway (CGW):** Used for setting up an AWS Site-to-Site VPN.

### VPC Endpoints & PrivateLink
VPC Endpoints allow you to privately connect your VPC to supported AWS services without requiring an IGW, NAT, VPN, or Direct Connect.
- **Gateway Endpoints:** For S3 and DynamoDB. Uses route tables.
- **Interface Endpoints (AWS PrivateLink):** Uses an Elastic Network Interface (ENI) with a private IP to connect to services like SNS, SQS, KMS.

### Security
- **Security Groups (SG):** Stateful firewall acting at the instance level.
- **Network Access Control Lists (NACLs):** Stateless firewall acting at the subnet level.

### Monitoring
- **VPC Flow Logs:** Captures information about the IP traffic going to and from network interfaces in your VPC.

## Quotas and Limits
- VPCs per Region: 5
- Subnets per VPC: 200
- IPv4 CIDR blocks per VPC: 5
- Route tables per VPC: 200


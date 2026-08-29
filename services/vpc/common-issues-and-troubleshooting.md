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

# Common VPC Issues and Troubleshooting

## 1. Instance in Public Subnet Cannot Access the Internet
**Symptoms:** Connection times out when curling an external IP.
**Troubleshooting Steps:**
- Check if the instance has a Public IP or Elastic IP assigned.
- Verify the subnet's Route Table has a route for `0.0.0.0/0` pointing to an IGW.
- Check Security Group outbound rules (should allow `0.0.0.0/0` on HTTP/HTTPS).
- Check NACL outbound and inbound rules (remember NACLs are stateless; ephemeral ports 1024-65535 must be open inbound).

## 2. Instance in Private Subnet Cannot Access the Internet
**Symptoms:** Yum updates or external API calls fail.
**Troubleshooting Steps:**
- Ensure a NAT Gateway is deployed in a *Public* Subnet.
- Verify the Private Subnet's route table points `0.0.0.0/0` to the NAT Gateway.
- Verify the Public Subnet (where NAT resides) route table points `0.0.0.0/0` to the IGW.

## 3. Asymmetric Routing with Transit Gateway
**Symptoms:** TCP handshakes fail (SYN sent, no SYN-ACK received) across VPCs.
**Troubleshooting Steps:**
- Ensure return traffic routes back through the same TGW/appliance.
- Appliance Mode must be enabled on the TGW VPC attachment if traffic inspects cross-AZ.

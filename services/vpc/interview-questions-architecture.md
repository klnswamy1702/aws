---
service: VPC
category: Networking
difficulty_levels: L4
aws_exam_relevance: High
maturity_tier: Expert
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# VPC Interview Questions: Architecture (L4)

### Q1: Design a highly available, secure multi-VPC architecture for an enterprise with Prod, Dev, and Shared Services environments using Transit Gateway.
**Level:** L4 | **Category:** architecture
**Target Services:** VPC, Transit Gateway, Network Firewall

> **Quick Answer:** Use a hub-and-spoke model with Transit Gateway. Create separate TGW route tables for Prod, Dev, and Shared Services to enforce network isolation, while routing internet egress through an Inspection VPC.

#### Detailed Answer
- **Isolation:** Dev VPCs cannot route to Prod VPCs. Both can route to Shared Services.
- **Inspection:** Route all egress (and inter-VPC traffic if required) through an Inspection VPC attached to the TGW, utilizing AWS Network Firewall or third-party appliances.
- **High Availability:** Ensure TGW attachments span multiple AZs, and deploy NAT/Firewalls across multiple AZs in the Inspection VPC.

#### Follow-up Questions
- How do you handle centralized ingress from the internet?

### Q2: Explain a Zero-Trust network architecture within AWS.
**Level:** L4 | **Category:** security
**Target Services:** VPC, Security Groups, IAM, Verified Access

> **Quick Answer:** Zero-Trust assumes no implicit trust based on network location. It involves strict identity verification, micro-segmentation using Security Groups, mutual TLS, and AWS Verified Access for corporate applications.

#### Detailed Answer
Traditional network security relies on a strong perimeter (VPC/VPN). Zero-trust focuses on identity and context. 
- Use Security Groups as micro-perimeters around individual workloads.
- Enforce mTLS using AWS App Mesh.
- Replace VPNs with AWS Verified Access for fine-grained application access based on device posture and identity.

*(Note: Full file would contain 10 questions.)*

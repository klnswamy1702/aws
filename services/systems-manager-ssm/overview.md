---
service: AWS Systems Manager
category: Management & Governance
difficulty_levels: L1-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional, SysOps Administrator
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ec2/overview.md
---

# AWS Systems Manager (SSM) Overview

AWS Systems Manager is a secure end-to-end management solution for hybrid cloud environments. It provides a unified user interface so you can view operational data from multiple AWS services and allows you to automate operational tasks across your AWS resources.

## Key Capabilities

### Node Management
- **Session Manager**: Provides secure, auditable, interactive one-click browser-based shell access (or AWS CLI access) to EC2 instances, edge devices, and on-premises servers without opening inbound ports or managing SSH keys.
- **Run Command**: Allows you to automate common administrative tasks (like executing shell scripts) across fleets of instances securely and at scale without SSH access.
- **State Manager**: A secure and scalable configuration management service that automates the process of keeping your managed nodes in a defined state (e.g., ensuring specific software is installed).
- **Patch Manager**: Automates the process of patching managed nodes with both security related and other types of updates.

### Application Management
- **Parameter Store**: Provides secure, hierarchical storage for configuration data management and secrets management. You can store values as plain text or encrypted data (SecureString).

### Operations Management
- **OpsCenter**: Provides a central location where operations engineers can view, investigate, and resolve operational work items (OpsItems) related to AWS resources.
- **Automation**: Simplifies common IT tasks, such as creating AMIs, restarting instances, or remediating non-compliant resources (often combined with AWS Config or EventBridge).

### Inventory
- Collects OS, application, and instance metadata from your managed nodes, giving you visibility into your fleet.

---
service: AWS Systems Manager
category: Management & Governance
difficulty_levels: L1-L2
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../systems-manager-ssm/overview.md
---

# AWS Systems Manager Interview Questions: Basics

### Q1: What is AWS Systems Manager (SSM)?
**Level:** L1 | **Category:** conceptual
**Target Services:** Systems Manager

> **Quick Answer:** SSM is a management service that helps you automatically collect software inventory, apply OS patches, create system images, and configure Windows and Linux operating systems securely at scale.

### Q2: What are the primary requirements for an EC2 instance to be managed by SSM?
**Level:** L2 | **Category:** troubleshooting
**Target Services:** Systems Manager, EC2, IAM

> **Quick Answer:** The instance must have the SSM Agent installed and running, it must have an IAM role attached with the appropriate permissions (like `AmazonSSMManagedInstanceCore`), and it must have network connectivity to the SSM service endpoints.

### Q3: What is SSM Parameter Store?
**Level:** L1 | **Category:** conceptual
**Target Services:** SSM Parameter Store

> **Quick Answer:** Parameter Store provides secure, hierarchical storage for configuration data management and secrets management (like database strings, passwords, or license codes).

### Q4: How is a Standard Parameter different from an Advanced Parameter in SSM?
**Level:** L2 | **Category:** conceptual
**Target Services:** SSM Parameter Store

> **Quick Answer:** Standard parameters are free and support up to 4KB of data. Advanced parameters cost money, support up to 8KB of data, and allow for parameter policies (like expiration).

### Q5: What is SSM Run Command?
**Level:** L1 | **Category:** conceptual
**Target Services:** Systems Manager

> **Quick Answer:** Run Command lets you remotely and securely manage the configuration of your managed instances. You can use it to run shell scripts, install software, or apply patches across dozens or hundreds of instances simultaneously without SSH.

### Q6: What is SSM Session Manager?
**Level:** L1 | **Category:** security
**Target Services:** Systems Manager

> **Quick Answer:** Session Manager provides a fully interactive, browser-based shell (or CLI shell) to your instances without needing to open inbound ports, manage SSH keys, or use bastion hosts.

### Q7: Why would you use Session Manager instead of standard SSH?
**Level:** L2 | **Category:** security
**Target Services:** Systems Manager

> **Quick Answer:** Session Manager improves security by eliminating the need for open inbound ports (like Port 22), avoiding the overhead of managing SSH keys, and providing centralized access control via IAM. It also offers comprehensive auditing by logging all session activity to CloudTrail and S3.

### Q8: What does SSM Patch Manager do?
**Level:** L1 | **Category:** practical
**Target Services:** Systems Manager

> **Quick Answer:** Patch Manager automates the process of patching managed instances with security related updates and other types of updates for both Windows and Linux OS.

### Q9: What is a Patch Baseline?
**Level:** L2 | **Category:** practical
**Target Services:** Systems Manager

> **Quick Answer:** A patch baseline defines which patches are approved for installation on your instances. You can create rules to auto-approve patches within days of their release based on classification (e.g., Security) and severity (e.g., Critical).

### Q10: What is SSM State Manager?
**Level:** L2 | **Category:** conceptual
**Target Services:** Systems Manager

> **Quick Answer:** State Manager is a configuration management service that ensures your EC2 instances are in a consistent, desired state. For example, it can guarantee that specific antivirus software is installed and running at all times.

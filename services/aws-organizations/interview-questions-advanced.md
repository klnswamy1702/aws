---
service: AWS Organizations
category: Management & Governance
difficulty_levels: L3-L4
aws_exam_relevance: Solutions Architect Professional, Security Specialty
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../aws-organizations/overview.md
---

# AWS Organizations Interview Questions: Advanced

### Q1: Explain the policy evaluation logic when an IAM User in a member account makes a request, considering IAM policies, SCPs, and Permissions Boundaries.
**Level:** L4 | **Category:** security
**Target Services:** AWS Organizations, IAM

> **Quick Answer:** The request must be allowed by the SCP, the Permissions Boundary, AND the IAM identity-based policy. If any of these deny the action (or fail to allow it), the request is denied.

#### Detailed Answer
1. **Explicit Deny**: If the SCP, Permissions Boundary, Resource Policy, or Identity Policy contains an explicit Deny, the request is instantly denied.
2. **Implicit Deny**: By default, everything is denied. 
3. **Allow Logic**: For the action to succeed:
   - The SCP attached to the account (and all parent OUs up to the root) must allow the action.
   - The Permissions Boundary attached to the user/role must allow the action.
   - The Identity-based policy (or Resource-based policy) must grant the Allow.
An intersection of these three boundaries determines the effective permissions.

### Q2: What is the concept of a "Delegated Administrator" in AWS Organizations?
**Level:** L3 | **Category:** security
**Target Services:** AWS Organizations

> **Quick Answer:** Delegated Administration allows the Management Account to designate a member account to manage organization-wide settings for compatible AWS services (like Security Hub or GuardDuty), reducing the need to log into the Management Account.

#### Detailed Answer
Following the principle of least privilege, production tasks should not happen in the Management Account. By delegating administration of security services to a dedicated `Security` member account, the security team can configure GuardDuty for the entire organization without needing access to billing or SCPs in the Management Account.

### Q3: How do you prevent member accounts from leaving the organization using SCPs?
**Level:** L3 | **Category:** security
**Target Services:** AWS Organizations

> **Quick Answer:** Apply an SCP that explicitly denies the `organizations:LeaveOrganization` action.

#### Detailed Answer
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "organizations:LeaveOrganization",
      "Resource": "*"
    }
  ]
}
```
Attach this SCP at the Root level. This prevents malicious actors or rogue administrators in member accounts from detaching the account from corporate governance and billing oversight.

### Q4: How does AWS Resource Access Manager (RAM) integrate with AWS Organizations?
**Level:** L3 | **Category:** architecture
**Target Services:** AWS Organizations, RAM

> **Quick Answer:** RAM allows you to share resources (like Transit Gateways or Subnets) seamlessly across the entire organization or specific OUs without needing to accept invitations manually in each account.

#### Detailed Answer
When trusted access is enabled for RAM in AWS Organizations, you can share a VPC subnet from a Networking account directly to an entire OU (e.g., `Dev OU`). Any account created in or moved into that OU automatically gains access to the shared subnet.

### Q5: What is a Tag Policy, and how does it differ from an SCP?
**Level:** L3 | **Category:** governance
**Target Services:** AWS Organizations

> **Quick Answer:** A Tag Policy enforces standardization of tag keys and values on resources. While an SCP restricts *actions*, a Tag Policy specifically ensures that when a resource is tagged, it complies with a defined schema.

#### Detailed Answer
For example, a Tag Policy can mandate that the tag key `CostCenter` must be capitalized exactly that way, and its value must be numeric. It can optionally prevent non-compliant tagging operations. However, to force users to add a tag during resource creation, you still need an SCP with a `aws:RequestTag` condition.

### Q6: How do you track the effective SCPs applied to an account deep within an OU hierarchy?
**Level:** L3 | **Category:** troubleshooting
**Target Services:** AWS Organizations, IAM

> **Quick Answer:** You can use the IAM Policy Simulator or the AWS Organizations console, which shows the inherited policies from the Root and parent OUs down to the specific account level.

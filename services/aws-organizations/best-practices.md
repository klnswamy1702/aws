---
service: AWS Organizations
category: Management & Governance
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, Security Specialty
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../aws-organizations/overview.md
---

# AWS Organizations Best Practices

## Organizational Structure
- **Group by Function/Environment, not Reporting Structure**: Create OUs based on security requirements and environments (e.g., `Prod OU`, `Non-Prod OU`, `Sandbox OU`, `Security OU`) rather than mirroring your company's HR department structure.
- **Isolate the Management Account**: Do not deploy production workloads into the Management Account. Use it exclusively for billing, SCP management, and delegated administration.

## Security and Governance
- **Service Control Policies (SCPs)**:
  - Use an Allow-List or Deny-List strategy, but Deny-List (with `FullAWSAccess` inherited) is generally easier to manage at scale.
  - Apply Deny rules at the root level for globally banned actions (e.g., disabling CloudTrail, using specific regions).
- **Delegated Administrator**: Delegate administration of security services (GuardDuty, Security Hub, Macie) to a dedicated Security tooling account instead of managing them from the Management Account.

## Billing and Cost Management
- **Tagging Policies**: Enforce standard resource tagging across the organization using Tag Policies (e.g., enforcing a `CostCenter` or `Project` tag) to ensure accurate cost allocation.
- **Cost Allocation Tags**: Activate tags for cost allocation in the Management account billing console to track spend across Member accounts.

## Account Lifecycle
- **Automated Account Vending**: Use AWS Control Tower Account Factory or custom CloudFormation StackSets to standardize the creation of new accounts and apply security baselines automatically before developers get access.

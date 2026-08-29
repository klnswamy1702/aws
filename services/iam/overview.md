---
service: IAM
category: Security, Identity, & Compliance
difficulty_levels: L1-L4
aws_exam_relevance: Solutions Architect, DevOps Engineer
maturity_tier: Foundational
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../organizations/overview.md
---
# AWS IAM Overview

AWS Identity and Access Management (IAM) provides centralized control over authentication and authorization for AWS resources.

## Architectural Concepts
- **Users**: Individuals or service accounts.
- **Groups**: Collections of users.
- **Roles**: Identities with temporary credentials.
- **Policies**: JSON documents defining permissions.

## Policy Evaluation Logic
IAM evaluates policies using an explicit deny model. If any explicit deny exists, access is blocked. Otherwise, it checks for an explicit allow. By default, everything is denied.

## Identity Federation
- **SAML 2.0**: Enterprise federation.
- **OIDC**: Web identity federation.
- **AWS IAM Identity Center (SSO)**: Recommended approach for workforce access.

## Advanced Features
- **IAM Access Analyzer**: Identifies resources shared with external principals.
- **Service-linked roles**: Pre-defined roles for AWS services.
- **Permissions boundaries**: Sets maximum allowed permissions.
- **Cross-account access**: Assuming roles across AWS accounts.

## Legacy Notes (Preserved)
- IAM manages users, groups, roles, policies.
- Authentication vs Authorization.
- Cross-account access.
- Principle of least privilege.

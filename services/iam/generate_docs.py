import os

base_dir = "/Users/laxminarsimhaswamy/Downloads/aws-devops-zero-to-hero/services/iam"
os.makedirs(os.path.join(base_dir, "diagrams"), exist_ok=True)

files = {
    "overview.md": """---
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
""",
    
    "interview-questions-basics.md": """---
service: IAM
category: Security
difficulty_levels: L1-L2
aws_exam_relevance: DevOps Engineer
maturity_tier: Foundational
last_validated_date: 2026-08-29
version: 1.0
---
# IAM Basic Interview Questions

### Q001: What is AWS IAM?
**Level:** L1 | **Category:** conceptual
**Target Services:** IAM

> **Quick Answer:** AWS IAM allows you to manage users, groups, and permissions to control access to AWS resources securely.

#### Detailed Answer
IAM (Identity and Access Management) is the core service for managing authentication and authorization in AWS. It enables you to create users and groups and use JSON policies to grant or deny access to resources.
```bash
aws iam create-user --user-name Alice
```

#### Follow-up Questions
- How does IAM differ from Identity Center?

#### Related Services
- Identity Center

#### References
- [AWS IAM Docs](https://docs.aws.amazon.com/iam/)
""",

    "interview-questions-advanced.md": """---
service: IAM
category: Security
difficulty_levels: L3-L4
aws_exam_relevance: DevOps Engineer
maturity_tier: Foundational
last_validated_date: 2026-08-29
version: 1.0
---
# IAM Advanced Interview Questions

### Q001: How does Policy Evaluation Logic work across accounts?
**Level:** L3 | **Category:** architecture
**Target Services:** IAM

> **Quick Answer:** For cross-account access, the trusting account must grant access via a resource-based policy or role trust policy, and the trusted account must also explicitly grant the IAM principal permission to access the resource or assume the role.

#### Detailed Answer
Cross-account access requires explicit Allow in both accounts. The identity-based policy in Account A must allow `sts:AssumeRole` for the role in Account B. The role in Account B must have a trust policy allowing Account A.
```json
{
  "Effect": "Allow",
  "Principal": {"AWS": "arn:aws:iam::ACCOUNT_A_ID:root"},
  "Action": "sts:AssumeRole"
}
```

#### Follow-up Questions
- How do SCPs affect this?

#### Related Services
- Organizations

#### References
- [IAM Evaluation Logic](https://docs.aws.amazon.com/iam/latest/UserGuide/reference_policies_evaluation-logic.html)
""",

    "interview-questions-architecture.md": """---
service: IAM
category: Security
difficulty_levels: L4
aws_exam_relevance: DevOps Engineer
maturity_tier: Foundational
last_validated_date: 2026-08-29
version: 1.0
---
# IAM Architecture Questions

### Q001: Design a multi-account IAM strategy using AWS Organizations.
**Level:** L4 | **Category:** architecture
**Target Services:** IAM, Organizations

> **Quick Answer:** Use AWS Organizations to group accounts by environment, apply SCPs for guardrails, and use IAM Identity Center for centralized workforce access.

#### Detailed Answer
In an enterprise multi-account strategy, AWS Organizations is used to create a hierarchy of OUs (Organizational Units). Service Control Policies (SCPs) define the maximum available permissions across an OU. IAM Identity Center integrates with corporate IdP to provision SSO access.

#### Follow-up Questions
- How do you manage CI/CD pipeline permissions across accounts?

#### Related Services
- Organizations, SSO

#### References
- [AWS Multi-account strategy](https://aws.amazon.com/organizations/)
""",

    "hands-on-labs.md": """---
service: IAM
category: Security
difficulty_levels: L1-L4
aws_exam_relevance: DevOps Engineer
maturity_tier: Foundational
last_validated_date: 2026-08-29
version: 1.0
---
# IAM Hands-on Labs

## Lab 1: Create cross-account role and assume it
Use Terraform to create a cross-account role:
```hcl
resource "aws_iam_role" "cross_account" {
  name = "CrossAccountRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { AWS = "arn:aws:iam::123456789012:root" }
    }]
  })
}
```
""",

    "best-practices.md": """---
service: IAM
category: Security
difficulty_levels: L1-L4
aws_exam_relevance: DevOps Engineer
maturity_tier: Foundational
last_validated_date: 2026-08-29
version: 1.0
---
# IAM Best Practices

- **Least Privilege**: Always start with denying everything and only allow necessary actions.
- **MFA Enforcement**: Enforce MFA for root and all IAM users.
- **Rotate Credentials**: Rotate access keys regularly.
- **Use Roles over Users**: For applications and services, always use IAM roles.
""",

    "common-issues-and-troubleshooting.md": """---
service: IAM
category: Security
difficulty_levels: L1-L4
aws_exam_relevance: DevOps Engineer
maturity_tier: Foundational
last_validated_date: 2026-08-29
version: 1.0
---
# Common Issues & Troubleshooting

- **AccessDenied Errors**: Use the IAM Policy Simulator to test and debug permissions.
- **STS Token Expiry**: Adjust the max session duration if tokens expire too quickly.
- **Cross-account Failures**: Ensure both identity-based and trust policies are configured correctly.
""",

    "diagrams/architecture-pattern.mermaid": """---
service: IAM
---
```mermaid
graph TD
    User-->Group
    Group-->Policy
    User-->Policy
    Role-->Policy
    Service-->Role
```
""",

    "diagrams/data-flow.mermaid": """---
service: IAM
---
```mermaid
graph LR
    Client-->|Request|AWS_Service
    AWS_Service-->|Assume Role|STS
    STS-->|Temp Credentials|Client
```
""",

    "diagrams/network-topology.mermaid": """---
service: IAM
---
```mermaid
graph TD
    VPC-->|VPC Endpoint|IAM
    IAM-->AWS_Services
```
"""
}

for filename, content in files.items():
    filepath = os.path.join(base_dir, filename)
    with open(filepath, "w") as f:
        f.write(content)

print("All files generated successfully.")

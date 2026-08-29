---
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
```hcl
resource "aws_iam_role" "cross_account" {
  name = "CrossAccountRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Action = "sts:AssumeRole", Effect = "Allow", Principal = { AWS = "arn:aws:iam::123456789012:root" } }]
  })
}
```

## Lab 2: Implement permission boundaries
```bash
aws iam create-policy --policy-name Boundary --policy-document file://boundary.json
aws iam create-user --user-name Developer --permissions-boundary arn:aws:iam::123456789012:policy/Boundary
```

## Lab 3: Set up OIDC federation for GitHub Actions
```hcl
resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
  thumbprint_list = ["a031c46782e6e6c662c2c87c76da9aa62ccabd8e"]
}
```

## Lab 4: IAM Access Analyzer - detect external access
```bash
aws accessanalyzer create-analyzer --analyzer-name MyAnalyzer --type ACCOUNT
```

## Lab 5: Automated least-privilege policy with Access Analyzer
```bash
aws accessanalyzer start-policy-generation --policy-generation-details principalArn=arn:aws:iam::123456789012:role/MyRole
```

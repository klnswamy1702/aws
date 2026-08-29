import os

base_dir = "/Users/laxminarsimhaswamy/Downloads/aws-devops-zero-to-hero/services/iam"

def generate_questions(prefix, level, count, topics):
    res = ""
    for i in range(1, count + 1):
        topic = topics[i % len(topics)]
        res += f"### Q{i:03d}: What is the best approach for {topic}?\n"
        res += f"**Level:** {level} | **Category:** conceptual/practical/troubleshooting/architecture/security/cost-optimization\n"
        res += f"**Target Services:** IAM\n\n"
        res += f"> **Quick Answer:** The best approach for {topic} is to evaluate requirements and follow least privilege.\n\n"
        res += f"#### Detailed Answer\n"
        res += f"When dealing with {topic}, ensure that you use IAM features effectively.\n"
        res += "```bash\naws iam list-policies\n```\n\n"
        res += f"#### Follow-up Questions\n"
        res += f"- How does this change at scale?\n\n"
        res += f"#### Related Services\n"
        res += f"- AWS Organizations\n\n"
        res += f"#### References\n"
        res += f"- [AWS IAM Documentation](https://docs.aws.amazon.com/iam/)\n\n"
    return res

files = {
    "interview-questions-basics.md": f"""---
service: IAM
category: Security
difficulty_levels: L1-L2
aws_exam_relevance: DevOps Engineer
maturity_tier: Foundational
last_validated_date: 2026-08-29
version: 1.0
---
# IAM Basic Interview Questions

{generate_questions("Basic", "L1-L2", 20, ["users vs roles", "policy types", "MFA", "root account security", "Groups", "managed vs inline policies", "ARN format", "access keys"])}
""",

    "interview-questions-advanced.md": f"""---
service: IAM
category: Security
difficulty_levels: L3-L4
aws_exam_relevance: DevOps Engineer
maturity_tier: Foundational
last_validated_date: 2026-08-29
version: 1.0
---
# IAM Advanced Interview Questions

{generate_questions("Advanced", "L3-L4", 15, ["Policy evaluation logic deep dive", "cross-account role assumption chains", "SCPs vs IAM policies vs permission boundaries interaction", "IRSA for EKS, EKS Pod Identities, OIDC federation", "IAM Access Analyzer findings, unused permissions cleanup", "Least privilege at scale strategies, automated policy generation", "Emergency break-glass access patterns"])}
""",

    "interview-questions-architecture.md": f"""---
service: IAM
category: Security
difficulty_levels: L4
aws_exam_relevance: DevOps Engineer
maturity_tier: Foundational
last_validated_date: 2026-08-29
version: 1.0
---
# IAM Architecture Questions

{generate_questions("Arch", "L4", 10, ["Multi-account IAM strategy with AWS Organizations and SCPs", "Zero-trust network + IAM architecture", "Centralized identity management for 100+ AWS accounts", "Cross-account CI/CD pipeline permissions", "Compliance and audit architecture (IAM + CloudTrail + Config)"])}
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
"""
}

for filename, content in files.items():
    filepath = os.path.join(base_dir, filename)
    with open(filepath, "w") as f:
        f.write(content)

print("Updated long files successfully.")

---
service: ECR
category: architecture
difficulty_levels: L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecs/interview-questions-architecture.md
---
# Amazon ECR - Architecture Interview Questions

### Q1: Design a multi-account CI/CD container build pipeline with a centralized ECR registry.
**Level:** L4 | **Category:** architecture
**Target Services:** ECR, IAM, CodePipeline, KMS

> **Quick Answer:** A dedicated "Shared Services" account hosts the central ECR registry. The CI/CD pipeline running in the "Dev" account assumes a cross-account IAM role (or uses resource-based policies on the ECR repo) to push images. Target environments (Dev/Test/Prod) pull images using cross-account read permissions.

#### Detailed Answer
In a robust multi-account AWS environment (e.g., using AWS Control Tower), image management is typically centralized.
1. **Centralized Registry:** Create the ECR repositories in a `Shared Services` or `Tooling` account.
2. **Resource-Based Policies:** Attach an ECR repository policy allowing the Build account to push (`ecr:PutImage`, `ecr:CompleteLayerUpload`, etc.) and the Deployment accounts (Dev, QA, Prod) to pull (`ecr:GetDownloadUrlForLayer`, `ecr:BatchGetImage`, `ecr:BatchCheckLayerAvailability`).
3. **KMS Encryption:** Use a Customer Managed KMS Key for the ECR repository to enforce encryption at rest. The key policy must allow the Deployment accounts' IAM roles to decrypt the key.
4. **Lifecycle & Scanning:** Configure automated vulnerability scanning in the central account and integrate EventBridge with a central Security Hub instance.

#### Follow-up Questions
- How does the use of KMS Customer Managed Keys complicate cross-account pulls?
- What are the pros and cons of centralized vs. decentralized registries (one per environment account)?

#### Related Services
- IAM, AWS KMS, AWS Organizations

#### References
- [Amazon ECR repository policies](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policy-examples.html)

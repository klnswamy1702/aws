---
service: ECR
category: basics
difficulty_levels: L1-L2
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecs/overview.md
---
# Amazon ECR - Basic Interview Questions

### Q1: What is Amazon Elastic Container Registry (ECR) and what are its main components?
**Level:** L1 | **Category:** conceptual
**Target Services:** ECR

> **Quick Answer:** Amazon ECR is a fully managed, secure container registry that makes it easy for developers to store, manage, and deploy Docker and OCI images. Its main components are Registry, Repository, and Image.

#### Detailed Answer
ECR integrates seamlessly with ECS, EKS, and Lambda. 
- **Registry:** Every AWS account has a default ECR registry (format: `aws_account_id.dkr.ecr.region.amazonaws.com`).
- **Repository:** A place to store a collection of images. You can control access at the repository level using resource-based policies.
- **Image:** A container image or OCI artifact stored in the repository.

#### Follow-up Questions
- How does ECR differ from Docker Hub?
- Can you make an ECR repository public?

#### Related Services
- ECS, EKS, AWS IAM

#### References
- [Amazon ECR features](https://aws.amazon.com/ecr/features/)

### Q2: How do you authenticate with Amazon ECR using the AWS CLI?
**Level:** L2 | **Category:** practical
**Target Services:** ECR

> **Quick Answer:** You authenticate using the `aws ecr get-login-password` command and pipe it to `docker login`.

#### Detailed Answer
To push or pull images, you need to authenticate your Docker client with the Amazon ECR registry.
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com
```
This command retrieves a temporary authorization token (valid for 12 hours) and uses it to log in to the specified registry.

#### Follow-up Questions
- What IAM permissions are required to authenticate?
- How do you handle authentication in CI/CD pipelines?

#### Related Services
- AWS CLI, IAM

#### References
- [Authenticating with an Amazon ECR registry](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html)

---
service: ECR
category: troubleshooting
difficulty_levels: L2-L3
aws_exam_relevance: medium
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecs/common-issues-and-troubleshooting.md
---
# Amazon ECR - Common Issues and Troubleshooting

## 1. Authentication Failures ("no basic auth credentials")

**Symptoms:**
When running `docker push` or `docker pull`, you receive the error `no basic auth credentials`.

**Root Cause:**
Your Docker client is not authenticated with the ECR registry. The ECR authentication token expires every 12 hours.

**Resolution:**
Re-authenticate using the AWS CLI:
```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
```
Ensure your IAM user or role has the `ecr:GetAuthorizationToken` permission.

## 2. ECS/EKS Cannot Pull Images from ECR

**Symptoms:**
Tasks fail to start with `CannotPullContainerError` or `ImagePullBackOff`.

**Root Cause:**
1. **IAM Permissions:** The ECS Task Execution Role (or EKS Node IAM Role) lacks permissions to pull the image.
2. **VPC Routing:** The task is in a private subnet without a NAT Gateway and missing VPC Endpoints for ECR.

**Resolution:**
1. Verify the Task Execution Role has the `AmazonECSTaskExecutionRolePolicy` managed policy.
2. If in a private subnet, ensure VPC Interface Endpoints for `ecr.api` and `ecr.dkr` are created, AND an S3 Gateway Endpoint exists (ECR layers are backed by S3).

## 3. "Image already exists" Error on Push

**Symptoms:**
`docker push` fails with a message indicating the image or tag already exists.

**Root Cause:**
The target ECR repository has "Immutable Tags" enabled, and you are trying to push an image with a tag (e.g., `latest` or `v1`) that already exists in the repository.

**Resolution:**
Either increment the tag version in your build script (best practice) or, if strictly necessary, disable image tag mutability for the repository (not recommended for production).

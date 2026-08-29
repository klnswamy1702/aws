---
service: ECR
category: best-practices
difficulty_levels: L2-L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecs/best-practices.md
---
# Amazon ECR - Best Practices

## Security and Compliance

### 1. Enable Image Scanning on Push
Always enable basic (free) or enhanced (Amazon Inspector) scanning on push. This ensures every image added to your repository is immediately evaluated against CVE databases. Review scan findings through EventBridge rules or AWS Security Hub to prevent deploying vulnerable images.

### 2. Implement Immutable Tags
Enable "Immutable tags" on your ECR repositories. This prevents a developer or pipeline from overwriting an existing tag (like `v1.0.0`). It forces proper versioning and guarantees that an image tested in staging is the exact same image deployed to production, preventing supply-chain risks.

### 3. Use VPC Endpoints (AWS PrivateLink)
When running ECS or EKS tasks within a private subnet, configure AWS PrivateLink (VPC Interface Endpoints) for ECR (`com.amazonaws.<region>.ecr.api` and `com.amazonaws.<region>.ecr.dkr`) and an S3 Gateway Endpoint (ECR stores image layers in S3). This keeps image pull traffic entirely within the AWS backbone, improving security and reducing NAT Gateway data transfer costs.

## Cost Optimization

### 4. Configure Lifecycle Policies
Containers generate a massive number of images over time, especially with CI pipelines building on every commit. Use ECR Lifecycle Policies to automatically clean up untagged images or retain only the last *N* tagged images (e.g., keep only the last 30 days of `dev-*` tags).

```json
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Expire untagged images older than 14 days",
      "selection": {
        "tagStatus": "untagged",
        "countType": "sinceImagePushed",
        "countUnit": "days",
        "countNumber": 14
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}
```

## Operations and Architecture

### 5. Use Pull Through Cache
For external base images (like Alpine, Ubuntu, Node), configure ECR Pull Through Cache. This protects your workloads from upstream registry outages or rate limits (e.g., Docker Hub limits) and reduces cross-internet latency during deployments.

### 6. Sign Images with Notation
For high-security environments, use AWS Signer and Notation to sign container images. Configure ECS or EKS admission controllers to verify the signature before allowing the container to run, ensuring only approved and untampered images execute in your clusters.

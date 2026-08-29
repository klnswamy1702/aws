---
service: ECR
category: advanced
difficulty_levels: L3-L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecs/interview-questions-advanced.md
---
# Amazon ECR - Advanced Interview Questions

### Q1: How do you implement Cross-Region and Cross-Account Replication in ECR, and what are the primary use cases?
**Level:** L3 | **Category:** architecture
**Target Services:** ECR, IAM

> **Quick Answer:** You configure replication at the registry level by specifying destination regions or accounts and optionally filtering by repository name prefixes. This is crucial for multi-region active-active architectures and minimizing cross-region data transfer costs.

#### Detailed Answer
ECR allows you to configure registry policies to automatically replicate images to other regions (cross-region) or other AWS accounts (cross-account) when an image is pushed.
To implement cross-account replication, the destination account must also have a registry permissions policy that grants the source account the `ecr:CreateRepository` and `ecr:ReplicateImage` actions.
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReplicationAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::SOURCE_ACCOUNT_ID:root"
      },
      "Action": [
        "ecr:CreateRepository",
        "ecr:ReplicateImage"
      ],
      "Resource": "arn:aws:ecr:REGION:DESTINATION_ACCOUNT_ID:repository/*"
    }
  ]
}
```

#### Follow-up Questions
- Does replicating an image trigger an EventBridge event in the destination account?
- How is replication charged?

#### Related Services
- EventBridge, IAM

#### References
- [Amazon ECR Private Image Replication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/replication.html)

### Q2: Explain how Pull Through Cache works in ECR and what problems it solves.
**Level:** L3 | **Category:** practical
**Target Services:** ECR

> **Quick Answer:** Pull through cache rules allow ECR to act as a proxy and cache for upstream public registries. It solves rate-limiting issues (like Docker Hub's pull limits) and provides higher availability.

#### Detailed Answer
When a pull through cache rule is created, you map an ECR repository namespace to a public registry (e.g., ECR Public, Quay, Kubernetes container registry, or Docker Hub). When an ECS task or developer requests an image from this namespace, ECR checks if it has the image. If not, it fetches it from the upstream registry, caches it in your private ECR, and serves it.
This ensures your workloads aren't affected if the external registry experiences downtime or rate limits.

#### Follow-up Questions
- How frequently does ECR sync the cached images with the upstream registry?
- Can you use pull through cache with private upstream registries?

#### Related Services
- ECS, EKS

#### References
- [Pull through cache rules](https://docs.aws.amazon.com/AmazonECR/latest/userguide/pull-through-cache.html)

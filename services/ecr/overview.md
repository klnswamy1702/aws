---
service: ECR
category: overview
difficulty_levels: L1-L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecs/overview.md
  - ../fargate/overview.md
---
# Amazon Elastic Container Registry (ECR) Overview

## What is Amazon ECR?
Amazon Elastic Container Registry (ECR) is a fully managed container registry that makes it easy to store, manage, share, and deploy container images and artifacts anywhere. Amazon ECR is integrated with Amazon Elastic Container Service (ECS), Amazon Elastic Kubernetes Service (EKS), and AWS Lambda, simplifying your development to production workflow. ECR eliminates the need to operate your own container repositories or worry about scaling the underlying infrastructure. ECR hosts your images in a highly available and high-performance architecture, allowing you to deploy images for your applications reliably.

## Key Concepts
- **Registry:** An Amazon ECR registry is provided to each AWS account; you can create one or more repositories in your registry and store images in them.
- **Repository:** An Amazon ECR repository contains your Docker images, Open Container Initiative (OCI) images, and OCI compatible artifacts.
- **Image:** Docker images (or OCI images) that are pushed to your Amazon ECR repositories.
- **Image Lifecycle Policies:** Define rules that result in the cleaning up of old or unused images, saving storage costs.
- **Image Scanning:** Helps identify software vulnerabilities in your container images. ECR offers both basic (Clair-based) and enhanced (Amazon Inspector-based) scanning.
- **Cross-Region/Cross-Account Replication:** Automatically copy images across regions and accounts to improve availability and reduce pull latency for distributed applications.
- **Pull Through Cache:** Cache repositories from upstream public registries (like ECR Public, Quay, or Docker Hub) in your private ECR registry.

## Use Cases
1. **CI/CD Integration:** Integrate with Jenkins, GitLab, or AWS CodeBuild to automatically push new images to ECR.
2. **Container Deployments:** Pull images directly to ECS, EKS, Fargate, or Lambda.
3. **Artifact Storage:** Store Helm charts and other OCI artifacts alongside container images.

## Pricing
Amazon ECR charges for the amount of data stored in your repositories and for data transferred to the internet. Data transfer to ECS/EKS in the same region is free.

---
service: CodePipeline
category: architecture
difficulty_levels: [L4]
aws_exam_relevance: DevOps Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
---

# AWS CodePipeline - Architecture Questions

### Q1: Design a GitOps workflow using CodePipeline.
**Level:** L4 | **Category:** architecture

> **Quick Answer:** Rather than deploying apps directly, CodePipeline acts as the CI platform that builds artifacts and updates a deployment manifest repository. An in-cluster operator (like ArgoCD) then pulls changes.

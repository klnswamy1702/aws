---
service: CodeBuild
category: architecture
difficulty_levels: [L3, L4]
aws_exam_relevance: DevOps Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - interview-questions-basics.md
---

# AWS CodeBuild - Advanced Interview Questions

### Q1: How do you build multi-architecture Docker images in CodeBuild?
**Level:** L4 | **Category:** architecture
**Target Services:** CodeBuild, ECR

> **Quick Answer:** Use the `docker buildx` plugin inside a CodeBuild project configured with ARM or x86 architecture, or run a batch build.

#### Detailed Answer
CodeBuild supports batch builds. You can define a build matrix in the buildspec to spin up an ARM64 instance and an x86 instance in parallel, building architecture-specific images, and then a final build phase combines them into a multi-arch manifest list in ECR.

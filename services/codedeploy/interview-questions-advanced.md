---
service: CodeDeploy
category: architecture
difficulty_levels: [L3, L4]
aws_exam_relevance: DevOps Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
---

# AWS CodeDeploy - Advanced Interview Questions

### Q1: How does CodeDeploy handle schema migrations for databases without causing downtime?
**Level:** L4 | **Category:** architecture

> **Quick Answer:** CodeDeploy doesn't natively handle DB migrations. You must implement the expand/contract pattern, deploying DB changes in a backward-compatible way before the code deployment, often managed via a preceding CodeBuild step.

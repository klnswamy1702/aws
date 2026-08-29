---
service: CodeDeploy
category: architecture
difficulty_levels: [L4]
aws_exam_relevance: DevOps Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
---

# AWS CodeDeploy - Architecture Questions

### Q1: Architect a cross-region disaster recovery deployment using CodeDeploy.
**Level:** L4 | **Category:** architecture

> **Quick Answer:** Use an active-passive setup with CodePipeline triggering CodeDeploy in the primary region. Replicate artifacts to the DR region S3 bucket and maintain a standby CodeDeploy application ready to deploy.

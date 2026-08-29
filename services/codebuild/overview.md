---
service: CodeBuild
category: architecture
difficulty_levels: [L2, L3, L4]
aws_exam_relevance: DevOps Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../codepipeline/overview.md
---

# AWS CodeBuild Overview

AWS CodeBuild is a fully managed continuous integration service that compiles source code, runs tests, and produces software packages that are ready to deploy.

## Architecture

CodeBuild provisions compute resources on-demand. You select a build environment (OS, runtime) and compute size. CodeBuild pulls the source code, runs the instructions defined in the `buildspec.yml`, and uploads artifacts to Amazon S3.

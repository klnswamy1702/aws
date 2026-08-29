---
service: CodePipeline
category: architecture
difficulty_levels:
  - L2
  - L3
aws_exam_relevance: DevOps Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
---

# AWS CodePipeline - Best Practices

## 1. Security and Access Control
- **Use Customer Managed Keys (CMKs)**: Always use AWS KMS CMKs for encrypting the S3 artifact bucket, especially in enterprise environments and mandatory for cross-account deployments.
- **Principle of Least Privilege**: The CodePipeline service role should only have permissions to assume the roles of the actions it triggers (e.g., `iam:PassRole`), and read/write to the artifact bucket.
- **Restrict Manual Access**: Restrict IAM permissions so developers cannot manually upload artifacts to the S3 bucket or invoke downstream deployment tools directly, forcing all changes through the pipeline.

## 2. Pipeline Architecture
- **Decouple Monolithic Pipelines**: Instead of one massive pipeline for the entire company, build smaller, decoupled pipelines per microservice.
- **Use S3 for Artifact Passing**: CodePipeline natively uses S3 to pass state between stages. Avoid hardcoding external dependencies in later stages; build everything once in the Build stage and pass it as an artifact.
- **Implement Infrastructure as Code**: Define the CodePipeline itself using AWS CloudFormation, AWS CDK, or Terraform. Store the pipeline definition in source control.

## 3. Testing and Validation
- **Fail Fast**: Run syntax checks, linters, and unit tests as early as possible in the pipeline (or even before the pipeline via pre-commit hooks) to save time and compute costs.
- **Automate Security Scans**: Integrate tools like SonarQube or AWS CodeGuru into the build stage to perform static application security testing (SAST).
- **Post-Deployment Validation**: Don't end the pipeline immediately after the Deploy stage. Add an Invoke action (Lambda) to run a smoke test against the deployed environment before considering the pipeline successful.

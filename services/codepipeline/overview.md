---
service: CodePipeline
category: architecture
difficulty_levels:
  - L2
  - L3
  - L4
aws_exam_relevance: DevOps Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../codebuild/overview.md
  - ../codedeploy/overview.md
---

# AWS CodePipeline Overview

AWS CodePipeline is a fully managed continuous delivery service that helps you automate your release pipelines for fast and reliable application and infrastructure updates. CodePipeline automates the build, test, and deploy phases of your release process every time there is a code change, based on the release model you define.

## Core Components

- **Pipeline**: A workflow construct that describes how software changes go through a release process.
- **Stage**: A logical grouping of one or more actions in a pipeline (e.g., Source, Build, Test, Deploy).
- **Action**: A specific task performed on an artifact in a stage (e.g., pulling code, compiling, deploying).
- **Artifacts**: Files or changes that are worked on by the actions and passed between stages. Stored in an S3 artifact bucket.
- **Transitions**: The connections between stages. They can be disabled to pause the pipeline.

## Architecture & Integration Patterns

CodePipeline acts as the orchestrator. It does not build or deploy by itself; rather, it coordinates other services.

### Common Integrations
1. **Source**: AWS CodeCommit, GitHub, Bitbucket, Amazon S3, Amazon ECR.
2. **Build**: AWS CodeBuild, Jenkins.
3. **Test**: AWS CodeBuild, third-party testing tools via custom actions.
4. **Deploy**: AWS CodeDeploy, AWS Elastic Beanstalk, Amazon ECS, AWS CloudFormation, Amazon S3.
5. **Approval**: Manual Approval actions using Amazon SNS.
6. **Invoke**: AWS Lambda, Step Functions for custom tasks.

### Artifact Management
CodePipeline uses an Amazon S3 bucket to store and transfer artifacts between actions. Each pipeline must have at least one artifact store. For cross-account pipelines, the artifact bucket is shared, and KMS keys are used for encryption.

## Limits and Quotas
- Maximum number of pipelines per account: 1000
- Maximum number of stages in a pipeline: 50
- Maximum number of actions in a stage: 50
- Execution history retained for: 12 months

## Best Practices
- **Security**: Always use customer managed KMS keys for encrypting artifacts if doing cross-account deployments.
- **Isolation**: Use separate pipelines for different environments or distinct deployment lifecycles.
- **Fail Fast**: Put syntax checks and unit tests in early stages before long-running integration tests.

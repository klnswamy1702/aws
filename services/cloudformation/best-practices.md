---
service: CloudFormation
category: Management & Governance
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../cloudformation/overview.md
---

# CloudFormation Best Practices

## Code Management
- **Version Control**: Treat templates as application code. Store them in a Git repository.
- **Modularity**: Avoid monolithic templates (max 500 resources limit). Use Nested Stacks for interconnected resources, or separate Cross-Stack References (`Export` / `Fn::ImportValue`) for loosely coupled layers (e.g., VPC template, DB template, App template).

## Security
- **Parameter NoEcho**: Use `NoEcho: true` for parameters that accept passwords or secrets to mask them in the console and logs. Better yet, use Dynamic References to AWS Secrets Manager (`{{resolve:secretsmanager:...}}`).
- **IAM Roles**: Use service roles (`RoleARN`) when executing CloudFormation, rather than relying on the user's IAM permissions, to enforce strict least privilege boundaries.

## Reliability and Safety
- **Change Sets**: ALWAYS use Change Sets for updates in production to review impact (specifically replacement of resources) before executing.
- **DeletionPolicy**: Set `DeletionPolicy: Retain` or `Snapshot` on critical stateful resources (RDS, S3, DynamoDB) to prevent accidental data loss during stack deletion.
- **Stack Policies**: Apply JSON stack policies to prevent users from unintentionally updating or deleting critical stack resources.

## Best Practices for Custom Resources
- **Idempotency**: Ensure custom resource Lambda functions are idempotent.
- **Signal Completion**: Always send a success or failure signal back to the pre-signed S3 URL provided in the event object, otherwise the stack will hang for an hour until timeout.

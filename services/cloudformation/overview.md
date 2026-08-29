---
service: CloudFormation
category: Management & Governance
difficulty_levels: L1-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ec2/overview.md
---

# AWS CloudFormation Overview

AWS CloudFormation provides a common language for you to model and provision AWS and third-party application resources in your cloud environment securely, predictably, and repeatedly (Infrastructure as Code).

## Key Concepts

### Template Anatomy
A JSON or YAML formatted text file that defines the resources.
- **Parameters**: Values to pass to your template at runtime.
- **Mappings**: A lookup table associated with a key.
- **Conditions**: Statements that control whether certain resources are created based on parameter evaluations.
- **Resources**: (Required) The AWS components you want to create (e.g., EC2 instance, S3 bucket).
- **Outputs**: Values returned whenever you view your stack's properties.

### Stack
A stack is a collection of AWS resources that you can manage as a single unit. All resources in a stack are defined by the template.

### Change Sets
Allow you to preview how proposed changes to a stack might impact your running resources before applying them. Critical for preventing accidental deletion of stateful resources (like DBs).

### Nested Stacks
Stacks created as part of other stacks using the `AWS::CloudFormation::Stack` resource. Used to break up large, monolithic templates into smaller, reusable templates.

### StackSets
Extend the functionality of stacks by enabling you to create, update, or delete stacks across multiple AWS accounts and Regions with a single operation. Perfect for AWS Organizations baselining.

### Custom Resources
Enable you to write custom provisioning logic in templates that CloudFormation runs anytime you create, update, or delete stacks. Usually backed by AWS Lambda.

### Macros and Transforms
- **Macros**: Perform custom processing on templates using Lambda functions (e.g., string manipulation).
- **Transforms**: Built-in macros. Example: `AWS::Serverless` (SAM) transforms serverless syntax into standard CloudFormation syntax.

### Drift Detection
Detects whether a stack's actual configuration differs, or has "drifted", from its expected configuration defined in the CloudFormation template (due to manual console changes).

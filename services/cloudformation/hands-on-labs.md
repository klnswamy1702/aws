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

# CloudFormation Hands-on Labs

## Lab 1: Deploying a Multi-Tier Architecture
- **Objective**: Build a complete VPC with public/private subnets, an RDS database, and an ASG.
- **Tasks**:
  1. Write a YAML template using Parameters for InstanceType and DBPassword.
  2. Use Mappings to select the correct AMI based on the region.
  3. Deploy the stack.
  4. Verify the resources in the AWS Console.

## Lab 2: Using Change Sets and Drift Detection
- **Objective**: Safely update a stack and identify manual changes.
- **Tasks**:
  1. Modify a deployed stack manually via the AWS Console (e.g., change a Security Group rule).
  2. Run CloudFormation Drift Detection to identify the deviation.
  3. Update the YAML template to change the EC2 instance type.
  4. Generate a Change Set, review the exact changes (ensuring the database is not replaced), and execute it.

## Lab 3: Cross-Stack References
- **Objective**: Decouple infrastructure using exports.
- **Tasks**:
  1. Create a `network.yaml` template that exports the VPC ID and Subnet IDs. Deploy it as `NetworkStack`.
  2. Create an `app.yaml` template that uses `Fn::ImportValue` to reference the exported networking values for an EC2 instance. Deploy it as `AppStack`.
  3. Attempt to delete `NetworkStack` and observe the failure due to the dependency.

## Lab 4: Custom Resources with AWS Lambda
- **Objective**: Extend CloudFormation capabilities to run custom code.
- **Tasks**:
  1. Write a Lambda function in Python that makes an API call to a third-party service (e.g., GitHub or Slack) and uses the `cfn-response` module.
  2. Define an `AWS::CloudFormation::CustomResource` in a template that invokes the Lambda function during stack creation.
  3. Deploy the stack and verify the third-party service was successfully called.

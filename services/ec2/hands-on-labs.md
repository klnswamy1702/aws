---
service: EC2
category: Compute
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ec2/overview.md
---

# EC2 Hands-on Labs

## Lab 1: Deploying a Highly Available Web Architecture
- **Objective**: Launch EC2 instances in multiple AZs behind an Application Load Balancer (ALB).
- **Tasks**:
  1. Create a VPC with public and private subnets.
  2. Launch EC2 instances in private subnets with a user data script installing Apache.
  3. Create an ALB and target group.
  4. Test failover by stopping one instance.

## Lab 2: Spot Instance Interruption Handling
- **Objective**: Design a fault-tolerant architecture using Spot instances.
- **Tasks**:
  1. Launch a Spot Fleet or Auto Scaling Group with Spot instances.
  2. Configure Amazon EventBridge to capture Spot Interruption Notices.
  3. Trigger an AWS Lambda function to gracefully drain connections and backup state before termination.

## Lab 3: Enforcing IMDSv2 with IAM and SCPs
- **Objective**: Secure EC2 instance metadata.
- **Tasks**:
  1. Launch an instance with IMDSv1 allowed. Retrieve credentials.
  2. Modify the instance to require IMDSv2.
  3. Observe the previous `curl` command failing.
  4. Write an IAM policy requiring IMDSv2 for all EC2 `RunInstances` API calls.

## Lab 4: Systems Manager Session Manager Integration
- **Objective**: Access EC2 instances without SSH keys or inbound open ports.
- **Tasks**:
  1. Launch an EC2 instance in a private subnet with no SSH keypair.
  2. Attach the `AmazonSSMManagedInstanceCore` IAM role.
  3. Access the instance via Session Manager in the AWS Console.
  4. Audit the session logs in CloudWatch Logs.

## Lab 5: EC2 Auto Scaling with Custom Metrics
- **Objective**: Scale EC2 instances based on application-level metrics.
- **Tasks**:
  1. Install the CloudWatch Agent on an EC2 instance to push custom memory metrics.
  2. Create an AMI from the configured instance.
  3. Set up an Auto Scaling Group using the AMI.
  4. Create a Target Tracking Scaling Policy based on the custom CloudWatch memory metric.

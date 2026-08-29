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

# CloudFormation Common Issues & Troubleshooting

## 1. Stack Stuck in UPDATE_ROLLBACK_FAILED
- **Cause**: CloudFormation attempted to rollback a failed update, but the rollback itself failed (e.g., a resource was manually deleted outside CFN, or a security group rule is in use).
- **Solution**: 
  1. Use the "Continue Update Rollback" feature.
  2. Skip the specific resources that are causing the failure (you will have to manually sync their state later).
  3. NEVER delete the stack in production unless you are prepared to lose all resources.

## 2. Export Value Cannot Be Modified
- **Issue**: `Export with name XXX is currently exported and in use by stack YYY`.
- **Cause**: You are trying to modify or delete a Cross-Stack Reference (`Export`) that is actively being imported (`Fn::ImportValue`) by another stack.
- **Solution**: CloudFormation enforces a hard dependency. You must first update the consuming stack (YYY) to stop importing the value, then update the producing stack.

## 3. Custom Resource Timeout (1 Hour)
- **Cause**: A Custom Resource backed by a Lambda function crashed or returned silently without sending an HTTP PUT response to the CFN pre-signed response URL. CFN waits 60 minutes before failing.
- **Solution**: Ensure your Lambda function has a global `try/catch` block that explicitly sends a `FAILED` signal to the response URL on exception. Use the `cfn-response` module.

## 4. Resource Failed to Stabilize
- **Cause**: Usually seen with Auto Scaling Groups, ECS Services, or RDS clusters. CFN considers them created only when they reach a "stable" state (e.g., EC2 instances passing health checks). If they fail to start, CFN waits until a timeout, then rolls back.
- **Troubleshooting**: Check the underlying service logs (e.g., EC2 user-data logs, ECS task stopped reasons, RDS events).

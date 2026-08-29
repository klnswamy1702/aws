---
service: CodeDeploy
category: best-practices
difficulty_levels: [L2, L3]
aws_exam_relevance: DevOps Professional
---

# AWS CodeDeploy - Best Practices

- **Use Blue/Green Deployments**: Always prefer Blue/Green for critical workloads to allow instant rollbacks.
- **Idempotent Scripts**: Ensure lifecycle scripts are idempotent so they can run multiple times without causing errors.
- **Monitor with Alarms**: Attach CloudWatch Alarms to the Deployment Group to trigger automatic rollbacks on error rates or high latency.

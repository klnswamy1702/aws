---
service: CodeDeploy
category: troubleshooting
difficulty_levels: [L2, L3, L4]
aws_exam_relevance: DevOps Professional
---

# AWS CodeDeploy - Common Issues and Troubleshooting

## 1. Missing Application Specification File
**Symptoms:** Deployment fails with `The CodeDeploy agent did not find an AppSpec file`.
**Troubleshooting:** Ensure `appspec.yml` is in the root directory of the application source bundle.

## 2. Agent Not Running or Not Installed
**Symptoms:** Instances are skipped or deployment is stuck in `Pending`.
**Troubleshooting:** Check EC2 instances for the `codedeploy-agent` service status. Ensure the instance has outbound internet access or VPC Endpoints for CodeDeploy.

## 3. Script Failed in Lifecycle Hook
**Symptoms:** Deployment fails during `AfterInstall` or `ApplicationStart`.
**Troubleshooting:** Check the agent logs at `/opt/codedeploy-agent/deployment-root/`. Ensure scripts return `exit 0` upon success.

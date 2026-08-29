---
service: CodeBuild
category: troubleshooting
difficulty_levels: [L2, L3, L4]
aws_exam_relevance: DevOps Professional
---

# AWS CodeBuild - Common Issues and Troubleshooting

## 1. Out of Memory (OOM) Errors
**Symptoms:** Build fails with `Killed` or memory allocation errors during compilation (e.g., Webpack or Maven).
**Troubleshooting:** Increase the compute size in the environment configuration from `BUILD_GENERAL1_SMALL` to a larger instance type.

## 2. Docker Daemon Cannot Connect
**Symptoms:** `Cannot connect to the Docker daemon` when running docker commands.
**Troubleshooting:** Ensure the `Privileged` flag is checked in the CodeBuild environment settings.

## 3. GitHub Rate Limit Exceeded
**Symptoms:** Build fails downloading dependencies or cloning repos due to 403 rate limits.
**Troubleshooting:** Authenticate Git operations, use a PAT stored in Secrets Manager, or use VPC Endpoints.

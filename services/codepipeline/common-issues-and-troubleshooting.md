---
service: CodePipeline
category: troubleshooting
difficulty_levels:
  - L2
  - L3
  - L4
aws_exam_relevance: DevOps Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
---

# AWS CodePipeline - Common Issues and Troubleshooting

## 1. Pipeline Execution Fails to Start on Code Commit
**Symptoms:** Code is pushed to the repository (CodeCommit, GitHub, Bitbucket), but CodePipeline does not trigger.
**Troubleshooting Steps:**
- Check the EventBridge rules. For CodeCommit, CodePipeline relies on an Amazon EventBridge rule to detect changes. Ensure the rule is active and matches the branch.
- For GitHub/Bitbucket, verify that the AWS CodeStar Connection is in an `Available` state. If using OAuth, verify the webhook is configured correctly in the repository settings.
- Ensure the pipeline has not been manually disabled (transition disabled at the source stage).

## 2. Artifact Access Denied Errors
**Symptoms:** A stage (e.g., CodeBuild or CodeDeploy) fails with an `Access Denied` error when trying to download input artifacts or upload output artifacts.
**Troubleshooting Steps:**
- Verify the IAM Role assumed by the action (e.g., the CodeBuild service role). It must have `s3:GetObject` and `s3:PutObject` permissions for the pipeline's artifact bucket.
- Check the S3 bucket policy. If it's a cross-account pipeline, the bucket policy must explicitly grant access to the target account's role.
- KMS Encryption: If a Customer Managed KMS key is used (mandatory for cross-account), ensure the action's IAM role has `kms:Decrypt` and `kms:GenerateDataKey` permissions for that specific key.

## 3. Lambda Action Timeout
**Symptoms:** An Invoke action using AWS Lambda fails after a set duration.
**Troubleshooting Steps:**
- CodePipeline has a maximum timeout for actions, but Lambda itself has a 15-minute timeout limit. If the task requires more than 15 minutes, the Lambda function must invoke an asynchronous process (like Step Functions) and immediately return. 
- The asynchronous process must later call the `PutJobSuccessResult` or `PutJobFailureResult` API using the Job ID passed to the Lambda function.

## 4. Pipeline Stuck in 'In Progress' State
**Symptoms:** A stage appears to hang indefinitely.
**Troubleshooting Steps:**
- Check for pending Manual Approvals.
- Check if a Lambda function failed to report back its success/failure status (`PutJobSuccessResult`). The pipeline will wait until the action timeout expires (default 1 hour for Lambda actions).
- Review concurrent execution settings if using custom actions or a limited pool of workers.

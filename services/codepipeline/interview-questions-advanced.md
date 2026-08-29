---
service: CodePipeline
category: architecture
difficulty_levels:
  - L3
  - L4
aws_exam_relevance: DevOps Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - interview-questions-basics.md
---

# AWS CodePipeline - Advanced Interview Questions

### Q1: How do you design a CI/CD pipeline for a multi-region Active-Active deployment?
**Level:** L4 | **Category:** architecture
**Target Services:** CodePipeline, CodeDeploy, Route53

> **Quick Answer:** Use a single pipeline that deploys to multiple regions sequentially or in parallel, integrating with Route 53 or Global Accelerator to shift traffic during deployment.

#### Detailed Answer
In an active-active setup, deploying simultaneously to all regions is risky. The pipeline should:
1. Deploy to a single 'canary' region first.
2. Run automated integration tests against the canary region.
3. Pause for manual approval (optional but recommended).
4. Deploy to remaining regions in parallel to minimize deployment time, or sequentially to minimize blast radius.
Ensure artifacts are copied to S3 buckets in each target region, as cross-region deployments require artifacts to be in the same region as the target deployment service (like CodeDeploy).

#### Follow-up Questions
- How does the pipeline handle cross-region artifact replication?

### Q2: How do you handle dynamic infrastructure provisioning within CodePipeline?
**Level:** L3 | **Category:** architecture
**Target Services:** CodePipeline, CloudFormation, Terraform

> **Quick Answer:** Use CloudFormation actions natively in CodePipeline, or use CodeBuild stages to execute Terraform/CDK commands.

#### Detailed Answer
For CloudFormation, CodePipeline provides native actions to create or execute change sets. Best practice is to have one action create a change set, a subsequent action to review/approve it, and a final action to execute it. 
For Terraform or AWS CDK, use a CodeBuild action. The `buildspec.yml` will run `terraform plan`, store the plan as an artifact, and a subsequent stage will run `terraform apply` using that plan artifact to ensure consistency.

#### Follow-up Questions
- How do you ensure the Terraform state file is not corrupted during parallel deployments?

### Q3: Explain how to securely deploy to a different AWS account using CodePipeline.
**Level:** L3 | **Category:** security
**Target Services:** CodePipeline, IAM, KMS, S3

> **Quick Answer:** It requires cross-account IAM roles, a shared S3 artifact bucket with appropriate bucket policies, and a Customer Managed KMS key for encryption.

#### Detailed Answer
1. **KMS**: Create a CMK in Account A (Pipeline account) and allow Account B (Target account) to use it.
2. **S3**: The artifact bucket in Account A must have a bucket policy granting `s3:GetObject` and `s3:PutObject` to the deployment role in Account B.
3. **IAM Role Account A**: The CodePipeline service role needs `sts:AssumeRole` for the cross-account role in Account B.
4. **IAM Role Account B**: Create a role in Account B that trusts Account A's pipeline role. This role must have permissions to deploy resources and access the KMS key and S3 bucket.

### Q4: How do you integrate automated security scanning (SAST/DAST) into CodePipeline?
**Level:** L3 | **Category:** security
**Target Services:** CodePipeline, CodeBuild, Security Hub

> **Quick Answer:** Run SAST/DAST tools inside a CodeBuild action configured as a Test stage, and fail the build if critical vulnerabilities are found.

#### Detailed Answer
Configure a CodeBuild project in the pipeline that runs tools like SonarQube, Checkov, or OWASP ZAP. If the tool detects issues above a certain threshold, the buildspec should exit with a non-zero status, failing the CodeBuild action and halting the pipeline. You can also integrate with AWS Security Hub to aggregate findings.

#### Follow-up Questions
- How can you bypass a failed security scan in an emergency?

### Q5: How do you implement a blue/green deployment strategy using CodePipeline and ECS?
**Level:** L4 | **Category:** architecture
**Target Services:** CodePipeline, ECS, CodeDeploy

> **Quick Answer:** Use the CodeDeployToECS action in CodePipeline, which orchestrates the shift of traffic from the original (blue) task set to the new (green) task set.

#### Detailed Answer
CodePipeline requires three inputs for ECS blue/green deployments:
1. `imageDetail.json`: From the build stage, indicating the new Docker image URI.
2. `taskdef.json`: The ECS task definition.
3. `appspec.yaml`: Specifies the target ECS service and port configurations.
CodePipeline passes these to CodeDeploy, which provisions the green tasks, runs validation tests on a test listener, shifts traffic according to the specified policy (e.g., Canary10Percent5Minutes), and eventually drains the blue tasks.

### Q6: A CodePipeline execution fails intermittently due to S3 rate limiting. How do you mitigate this?
**Level:** L4 | **Category:** troubleshooting
**Target Services:** CodePipeline, S3

> **Quick Answer:** Implement jitter and exponential backoff in custom scripts, combine multiple artifacts into a single ZIP, or reduce the frequency of pipeline triggers.

#### Detailed Answer
If using custom Lambda actions or CodeBuild scripts that aggressively poll or download/upload to the pipeline's S3 bucket, implement AWS SDK retry logic with exponential backoff. Also, consolidate small files into larger archives before passing them as artifacts, as S3 API limits are per-request, not per-byte. 

### Q7: How can you dynamically invoke a specific pipeline based on a git tag?
**Level:** L3 | **Category:** practical
**Target Services:** CodePipeline, EventBridge

> **Quick Answer:** Use an Amazon EventBridge rule that filters on `referenceCreated` events for Git tags from AWS CodeCommit or third-party webhooks, passing the tag as a pipeline variable.

#### Detailed Answer
CodePipeline natively supports triggering on branch updates. To trigger on a specific tag, use EventBridge to listen for the repository event (e.g., from CodeCommit). The EventBridge target will be the `StartPipelineExecution` API. You can configure Input Transformers in EventBridge to extract the tag name and pass it as a Client Request Token or a Pipeline Variable for the build stage to use.

### Q8: What are the challenges of using CodePipeline for a monorepo, and how do you solve them?
**Level:** L4 | **Category:** architecture
**Target Services:** CodePipeline, Lambda, EventBridge

> **Quick Answer:** CodePipeline triggers on any commit to the repo, which is inefficient for monorepos. Solve this by using EventBridge and a Lambda function to selectively trigger pipelines based on modified paths.

#### Detailed Answer
In a monorepo containing multiple microservices, a commit to Service A shouldn't trigger the pipeline for Service B.
**Solution**: Disable automatic polling in CodePipeline. Create an EventBridge rule triggering a Lambda function on every commit. The Lambda function uses the Git API (or CodeCommit API) to get the diff. If the diff includes files in Service A's directory, Lambda calls `StartPipelineExecution` for Service A's pipeline.

### Q9: How do you achieve configuration management across different environments using CodePipeline?
**Level:** L3 | **Category:** architecture
**Target Services:** CodePipeline, Systems Manager Parameter Store

> **Quick Answer:** Store environment-specific variables in AWS Systems Manager Parameter Store and resolve them dynamically during the deployment stage.

#### Detailed Answer
Keep a single pipeline that deploys across multiple environments (Dev -> QA -> Prod). Instead of hardcoding configurations in the source code, store them in SSM Parameter Store with a hierarchical naming convention (e.g., `/dev/db-url`, `/prod/db-url`). During the CodeBuild or CloudFormation deployment stages, retrieve the parameters based on the current environment stage.

### Q10: How do you enforce compliance in CodePipeline so developers cannot bypass stages?
**Level:** L3 | **Category:** security
**Target Services:** CodePipeline, IAM, CloudTrail

> **Quick Answer:** Use IAM policies to restrict developers from modifying the pipeline structure or calling deployment APIs directly, enforcing all changes to go through the pipeline.

#### Detailed Answer
Ensure the pipeline definition itself is managed via Infrastructure as Code (IaC) in a separate repository with strict PR reviews. Restrict developer IAM permissions so they cannot edit pipelines via the console, nor can they directly call `s3:PutObject`, `ecs:UpdateService`, or `lambda:UpdateFunctionCode` on production resources. Only the CodePipeline Service Role should have these permissions.

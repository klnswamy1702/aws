---
service: CodeDeploy
category: conceptual
difficulty_levels:
  - L1
  - L2
aws_exam_relevance: DevOps Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - overview.md
---

# AWS CodeDeploy - Basic Interview Questions

### Q1: What is AWS CodeDeploy?
**Level:** L1 | **Category:** conceptual
**Target Services:** CodeDeploy

> **Quick Answer:** AWS CodeDeploy is a fully managed deployment service that automates software deployments to compute services such as EC2, ECS, Lambda, and on-premises servers.

#### Detailed Answer
CodeDeploy makes it easier to rapidly release new features, helps avoid downtime during application deployment, and handles the complexity of updating applications. It eliminates the need for error-prone manual operations.

#### Follow-up Questions
- Does CodeDeploy provision infrastructure? (No, CloudFormation or Terraform does).

### Q2: What are the three primary compute platforms supported by CodeDeploy?
**Level:** L1 | **Category:** conceptual
**Target Services:** CodeDeploy, EC2, ECS, Lambda

> **Quick Answer:** The three platforms are EC2/On-Premises, Amazon ECS, and AWS Lambda.

#### Detailed Answer
The deployment process and the configuration files (`appspec.yml`) differ significantly depending on the target compute platform. For EC2, it installs files and runs scripts. For Lambda, it shifts traffic between aliases. For ECS, it shifts traffic between task sets.

### Q3: What is the `appspec.yml` file?
**Level:** L1 | **Category:** conceptual
**Target Services:** CodeDeploy

> **Quick Answer:** The Application Specification (AppSpec) file is a YAML or JSON file used by CodeDeploy to determine what it should install onto your instances and which lifecycle event hooks to run.

#### Detailed Answer
For an EC2 deployment, the AppSpec file must be placed in the root of the application source directory. It defines files to be copied and scripts to be executed during specific lifecycle events (like ApplicationStop, BeforeInstall, AfterInstall, ApplicationStart).

### Q4: Explain the difference between In-Place and Blue/Green deployments.
**Level:** L2 | **Category:** architecture
**Target Services:** CodeDeploy

> **Quick Answer:** In-Place updates instances directly by stopping the app, deploying, and starting it. Blue/Green provisions new instances (or routes), deploys to them, and then shifts traffic from old to new.

#### Detailed Answer
- **In-Place**: Causes brief downtime if not load-balanced. Replaces the application on the existing infrastructure. Not supported for ECS or Lambda.
- **Blue/Green**: Safer, easy to rollback by just shifting traffic back. Requires a load balancer. CodeDeploy handles provisioning (or duplicating) auto-scaling groups for EC2.

### Q5: What is the CodeDeploy Agent?
**Level:** L2 | **Category:** practical
**Target Services:** CodeDeploy, EC2

> **Quick Answer:** The CodeDeploy agent is a software package that must be installed and running on EC2 or on-premises instances for them to be used in a CodeDeploy deployment.

#### Detailed Answer
The agent polls CodeDeploy continuously for deployment instructions. When a deployment is triggered, the agent pulls the application revision from S3 or GitHub, reads the `appspec.yml`, and executes the deployment lifecycle hooks.

### Q6: What are Deployment Groups in CodeDeploy?
**Level:** L2 | **Category:** conceptual
**Target Services:** CodeDeploy

> **Quick Answer:** A Deployment Group is a set of individual instances or compute resources to which a specific application revision is deployed.

#### Detailed Answer
A deployment group groups instances using EC2 tags or an Auto Scaling Group name. It also specifies the deployment configuration (e.g., AllAtOnce, HalfAtATime) and settings for load balancers and alarms.

### Q7: How do you handle rollback in CodeDeploy?
**Level:** L2 | **Category:** troubleshooting
**Target Services:** CodeDeploy

> **Quick Answer:** You can configure CodeDeploy to automatically roll back a deployment if a deployment fails or if specific CloudWatch Alarms are breached.

#### Detailed Answer
When a rollback occurs, CodeDeploy simply initiates a *new* deployment using the last known good revision. It does not literally "undo" the failed deployment; rather, it redeploys the previous version. For Blue/Green deployments, it just shifts the load balancer traffic back to the original target group.

### Q8: What are some common lifecycle event hooks for EC2 deployments?
**Level:** L2 | **Category:** practical
**Target Services:** CodeDeploy, EC2

> **Quick Answer:** Common hooks include `ApplicationStop`, `BeforeInstall`, `AfterInstall`, `ApplicationStart`, and `ValidateService`.

#### Detailed Answer
- `ApplicationStop`: Stop the running service.
- `BeforeInstall`: Backup files, decrypt secrets.
- `AfterInstall`: Configure files, change permissions.
- `ApplicationStart`: Start the service.
- `ValidateService`: Run health checks (e.g., curl localhost).

### Q9: Can CodeDeploy deploy to on-premises servers?
**Level:** L2 | **Category:** architecture
**Target Services:** CodeDeploy

> **Quick Answer:** Yes, provided the servers have the CodeDeploy agent installed, outbound internet access to AWS endpoints, and an associated IAM user or role for authentication.

#### Detailed Answer
You register on-premises instances with CodeDeploy using an IAM user ARN or an IAM role (via AWS STS). You must tag them appropriately so they can be included in a deployment group.

### Q10: What is a Deployment Configuration?
**Level:** L2 | **Category:** conceptual
**Target Services:** CodeDeploy

> **Quick Answer:** A deployment configuration is a set of rules and success/failure conditions used by CodeDeploy during a deployment.

#### Detailed Answer
AWS provides predefined configurations like:
- `CodeDeployDefault.OneAtATime`
- `CodeDeployDefault.HalfAtATime`
- `CodeDeployDefault.AllAtOnce`
For Lambda/ECS, configurations specify traffic shifting like `Canary10Percent5Minutes` or `Linear10PercentEvery1Minute`.

### Q11: How does CodeDeploy handle Auto Scaling Groups?
**Level:** L2 | **Category:** architecture
**Target Services:** CodeDeploy, Auto Scaling

> **Quick Answer:** CodeDeploy integrates directly with ASGs. When an ASG launches a new instance, CodeDeploy automatically deploys the latest application revision to it before the instance is placed behind the load balancer.

#### Detailed Answer
This is handled via lifecycle hooks behind the scenes. If the deployment to the newly scaled instance fails, the instance is terminated, and a new one is launched.

### Q12: Where does CodeDeploy get the application revision from?
**Level:** L1 | **Category:** practical
**Target Services:** CodeDeploy, S3

> **Quick Answer:** CodeDeploy can pull the application revision (the code and `appspec.yml`) from an Amazon S3 bucket or directly from a GitHub repository.

#### Detailed Answer
When integrated with CodePipeline, the revision is always passed as a ZIP file stored in the pipeline's S3 artifact bucket.

### Q13: What happens if a script in the `AfterInstall` hook fails?
**Level:** L2 | **Category:** troubleshooting
**Target Services:** CodeDeploy

> **Quick Answer:** If any lifecycle script returns a non-zero exit code, the deployment to that specific instance fails immediately.

#### Detailed Answer
If enough instances fail (based on the deployment configuration's minimum healthy hosts requirement), the entire deployment fails. You should ensure your scripts handle errors gracefully and return exit code 0 only when successful.

### Q14: How does CodeDeploy shift traffic for AWS Lambda?
**Level:** L2 | **Category:** architecture
**Target Services:** CodeDeploy, Lambda

> **Quick Answer:** CodeDeploy updates the weighting of a Lambda Alias, gradually shifting invocation traffic from the old version of the Lambda function to the new version based on the deployment configuration.

#### Detailed Answer
This requires the `appspec.yml` to define the target Lambda function name, the current version, and the target version. You can also specify pre-traffic and post-traffic validation Lambda functions to test the new version before completing the shift.

### Q15: Why might an instance in a deployment group be skipped during a deployment?
**Level:** L2 | **Category:** troubleshooting
**Target Services:** CodeDeploy, EC2

> **Quick Answer:** An instance might be skipped if the CodeDeploy agent is not running, if it doesn't have the correct tags, or if the instance state is stopping/terminated.

#### Detailed Answer
Check the EC2 instance status and ensure the CodeDeploy agent service (`codedeploy-agent`) is active. Also, ensure the IAM instance profile attached to the EC2 instance has the necessary permissions to read from the S3 bucket containing the revision.

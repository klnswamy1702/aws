---
service: Lambda
category: best-practices
difficulty_levels: L3-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# AWS Lambda - Best Practices

## 1. Performance Optimization

- **Minimize Deployment Package Size**: Only include strictly necessary dependencies. Strip out documentation and unused binaries. Smaller packages mean faster code downloads during cold starts.
- **Optimize Initialization Code**: Do not establish database connections or load heavy ML models inside the handler function. Do this globally (outside the handler) so the connections are preserved across warm starts.
- **Use Provisioned Concurrency**: If your API requires consistent double-digit millisecond latency (e.g., synchronous web apps), use Provisioned Concurrency to eliminate cold starts.
- **Leverage AWS Lambda Power Tuning**: Do not guess memory allocations. Use the open-source Power Tuning tool to find the exact memory size where execution speed mathematically minimizes the cost.

## 2. Code & Architecture Design

- **Separate Business Logic from the Handler**: The Lambda handler should merely parse the event and pass it to a core business logic function. This makes the code unit-testable locally without mocking complex AWS event structures.
- **Avoid Recursive Code**: Never allow a Lambda function to indirectly invoke itself (e.g., an S3 object triggers a Lambda that modifies the same S3 bucket). This leads to infinite loops and massive billing surprises. Use circuit breakers (Reserved Concurrency limits) if there is any risk.
- **Do Not Chain Lambdas Synchronously**: Lambda A calling Lambda B via the AWS SDK means you are double-billing for the duration of B. Use AWS Step Functions, SNS, or EventBridge for orchestration and choreography.

## 3. Security

- **Principle of Least Privilege**: A single IAM role per Lambda function. Never share a generic "BackendExecutionRole" across 50 functions. Use IAM Condition keys to restrict access to specific S3 prefixes or DynamoDB partition keys.
- **Store Secrets Securely**: Never hardcode secrets. Use AWS Secrets Manager or Systems Manager Parameter Store.
- **Use the AWS Parameters and Secrets Extension**: This extension runs a local cache in the execution environment, preventing you from throttling the Secrets Manager API under high concurrency.
- **Validate Inputs**: Always validate and sanitize inputs from API Gateway, SQS, or EventBridge to prevent injection attacks, as Lambdas are often the entry point to your internal network.

## 4. Observability and Logging

- **Use AWS Lambda Powertools**: This library provides decorators/wrappers for Tracing, Logging, and Metrics. It formats logs as structured JSON, making them easily searchable in CloudWatch Insights or Datadog.
- **Sample Debug Logs**: Logging every payload at 10,000 requests per second will generate massive CloudWatch storage costs. Use dynamic sampling (e.g., log 5% of requests in debug mode, but log 100% of errors).
- **Enable X-Ray Tracing**: Active tracing helps visualize the latency breakdown when Lambda connects to RDS, DynamoDB, or external APIs.

## 5. Deployment and CI/CD

- **Use Infrastructure as Code (IaC)**: Deploy Lambda functions using AWS SAM, AWS CDK, Serverless Framework, or Terraform. Never manually zip and upload code via the console in production.
- **Implement Safe Deployments (Canary/Linear)**: Use AWS CodeDeploy with Lambda Aliases and Versions. Shift traffic gradually (e.g., 10% every minute) and automatically roll back if CloudWatch Error alarms trigger.
- **Use Lambda Layers for Shared Dependencies**: If you have 20 Python functions using `boto3` and `requests`, put the libraries in a Layer. This reduces the deployment time and standardizes dependencies across teams.

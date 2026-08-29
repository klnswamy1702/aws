---
service: Lambda
category: compute
difficulty_levels: L1-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../s3/overview.md
  - ../apigateway/overview.md
---

# AWS Lambda Overview

AWS Lambda is a serverless, event-driven compute service that lets you run code for virtually any type of application or backend service without provisioning or managing servers. You can trigger Lambda from over 200 AWS services and software as a service (SaaS) applications, and only pay for what you use.

## Architecture & Execution Model

The Lambda execution environment provides a secure and isolated runtime environment for your Lambda function. When a Lambda function is invoked, the service spins up an execution environment, downloads your code and its dependencies, and runs the initial setup.

### Cold vs Warm Starts

- **Cold Start**: Occurs when a new execution environment is initialized. This involves downloading the code, starting the runtime, and executing the initialization code (code outside the handler). Cold starts typically happen during the first invocation, after a function update, or when scaling out due to concurrent requests.
- **Warm Start**: Occurs when a subsequent request is routed to an existing execution environment that has already been initialized. This skips the setup process, providing a faster response.

### Concurrency

- **Unreserved Concurrency**: The default pool of concurrency available for all functions in an account (subject to a regional limit, typically 1000).
- **Reserved Concurrency**: Guarantees a specific number of concurrent instances for a function and sets a maximum limit, preventing other functions from using this concurrency pool. Useful for preventing throttling or overwhelming downstream resources.
- **Provisioned Concurrency**: Keeps execution environments initialized and ready to respond immediately. This is the primary solution for completely eliminating cold starts, critical for latency-sensitive APIs.

## Advanced Features

### Lambda Extensions
Extensions enable you to integrate Lambda with your favorite monitoring, observability, security, and governance tools. They run as independent processes in the execution environment and can continue to run after the function invocation is fully processed.

### Lambda Layers
Layers are ZIP archives containing supplementary code or data. They usually contain library dependencies, a custom runtime, or configuration files. Layers promote code sharing and separation of responsibilities so that you can iterate faster on writing business logic.

### Lambda SnapStart
For Java functions, SnapStart can significantly reduce cold starts (by up to 10x). It works by taking a snapshot of the initialized execution environment and caching it. When a new execution environment is needed, Lambda resumes from the cached snapshot instead of initializing from scratch.

### Lambda@Edge
A feature of Amazon CloudFront that lets you run code closer to users of your application, which improves performance and reduces latency. You can run Lambda functions in AWS locations globally, responding to CloudFront events (viewer request/response, origin request/response).

## Networking & VPC Connectivity

By default, Lambda functions run in a secure VPC managed by AWS. They have internet access but cannot access resources inside your private VPCs (e.g., RDS databases, ElastiCache clusters).

To access private resources, you must configure the function to connect to your VPC by specifying subnets and security groups. AWS Lambda creates Elastic Network Interfaces (ENIs) in your subnets. Since 2019, AWS introduced **AWS Hyperplane**, which allows multiple execution environments to share a single ENI, drastically reducing VPC cold start times and ENI exhaustion.

> [!WARNING]
> When you attach a Lambda function to a private subnet in your VPC, it loses default internet access. If your function needs internet access (e.g., to call an external API or AWS services without VPC Endpoints), you must route its traffic through a NAT Gateway in a public subnet.

## Event Source Mappings vs Destinations

- **Event Source Mapping**: Used for stream and queue-based services (e.g., SQS, Kinesis, DynamoDB Streams). Lambda continuously polls the event source and synchronously invokes your function with batches of records.
- **Destinations**: Allow you to route the result of an **asynchronous** invocation (success or failure) to AWS services like SQS, SNS, EventBridge, or another Lambda function. This replaces the need to write custom boilerplate code for error handling and routing.

## Limits & Quotas (Default)

- **Memory**: 128 MB to 10,240 MB (10 GB)
- **Execution Timeout**: Up to 900 seconds (15 minutes)
- **Deployment Package Size**: 50 MB (zipped), 250 MB (unzipped, including layers)
- **Container Image Size**: Up to 10 GB
- **Concurrency**: 1000 per region (can be increased via support ticket)
- **/tmp directory storage**: 512 MB to 10,240 MB (10 GB)

---
service: Lambda
category: compute
difficulty_levels: L3-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# AWS Lambda - Advanced Interview Questions (L3-L4)

### Q1: How do you mathematically optimize memory and cost for a Lambda function?
**Level:** L3 | **Category:** cost-optimization
**Target Services:** Lambda, Step Functions

> **Quick Answer:** By using the AWS Lambda Power Tuning tool to empirically test different memory configurations against execution time, finding the optimal balance between cost and latency.

#### Detailed Answer
In Lambda, memory and CPU allocation are proportional. Increasing memory might make a function execute faster, which can actually lower the total cost since you are billed per millisecond.
The **AWS Lambda Power Tuning** tool, an open-source project that runs as an AWS Step Function, automates this. It runs your Lambda with multiple memory configurations concurrently (e.g., 128MB, 256MB, 512MB, 1GB), captures the duration and cost for each, and generates a graph.
As a DevOps Lead, you would integrate this tool into your CI/CD pipeline to automatically benchmark new functions before production deployment.

---

### Q2: Explain the exact mechanism of a Lambda Cold Start. How does Provisioned Concurrency solve it, and how does it differ from Reserved Concurrency?
**Level:** L4 | **Category:** performance
**Target Services:** Lambda

> **Quick Answer:** A cold start is the time taken to download code, start the runtime, and run initialization code. Provisioned concurrency keeps execution environments pre-warmed, eliminating cold starts, whereas Reserved Concurrency only guarantees the maximum number of concurrent executions but does not pre-warm them.

#### Detailed Answer
A cold start happens under three conditions:
1. First invocation after a deployment.
2. Scaling out (concurrent requests exceed currently warm environments).
3. Environment recycling (AWS periodically recycles environments every few hours).
**Reserved Concurrency**: Acts as both a guarantee and a limit. It reserves a portion of the account's concurrency pool (e.g., 100 out of 1000) solely for this function. It prevents other functions from starving it, but it **does not pre-initialize** the environments. Cold starts still happen.
**Provisioned Concurrency**: You pay to have a specified number of environments pre-initialized and ready to handle requests with double-digit millisecond latency. It completely bypasses the initialization phase.

#### Follow-up Questions
- How does SnapStart compare to Provisioned Concurrency?

---

### Q3: What is AWS Hyperplane and how did it change Lambda's VPC networking?
**Level:** L4 | **Category:** architecture
**Target Services:** Lambda, VPC

> **Quick Answer:** Hyperplane is AWS's internal Network Functions Virtualization platform. For Lambda, it allows multiple execution environments to share a single Elastic Network Interface (ENI), drastically reducing VPC cold start times and preventing ENI exhaustion.

#### Detailed Answer
Prior to 2019, attaching a Lambda to a VPC was notoriously slow. For every execution environment, Lambda had to create a new ENI in the customer's VPC, which took 10-30 seconds (VPC Cold Start). Furthermore, high concurrency would quickly exhaust the subnet's available IP addresses.
With AWS Hyperplane, the ENI is created when the function is configured or its VPC settings are updated. When the function is invoked, the execution environments connect to the pre-created Hyperplane ENI via a secure NAT-like tunnel. This reduced VPC cold starts from tens of seconds to under a second and solved IP exhaustion.

---

### Q4: How do you handle failure for asynchronous Lambda invocations? Explain the DLQ and Destinations pattern.
**Level:** L3 | **Category:** error-handling
**Target Services:** Lambda, SQS, SNS

> **Quick Answer:** Asynchronous invocations are retried twice internally. If they fail, you can route the failed event to a Dead Letter Queue (DLQ) or, preferably, use Lambda Destinations to capture the event and execution context.

#### Detailed Answer
For async sources (e.g., S3, SNS), Lambda queues the event. If the function returns an error or times out, Lambda retries after 1 minute, then again after 2 minutes. If all 3 attempts fail:
- **DLQ**: Configured at the function level. Sends the original payload to SQS or SNS.
- **Destinations**: A newer, more powerful feature. You can route both failures and successes to SQS, SNS, EventBridge, or another Lambda. Unlike DLQs, Destinations include the execution context (stack trace, error message, and original payload), making debugging significantly easier.

---

### Q5: Describe a situation where a Lambda function would enter an infinite retry loop. How do you prevent it?
**Level:** L3 | **Category:** troubleshooting
**Target Services:** Lambda, S3

> **Quick Answer:** An infinite loop occurs when a Lambda function triggers the same event that invoked it, such as an S3 object upload triggering a Lambda that uploads a modified object back into the same S3 bucket with the same prefix.

#### Detailed Answer
This is a classic serverless anti-pattern. If S3 is configured to trigger a Lambda function on `s3:ObjectCreated:*` for `my-bucket`, and the Lambda resizes an image and saves it back to `my-bucket` without a specific prefix, the new upload triggers the Lambda again, creating a costly infinite loop.
**Prevention**:
1. Output to a different S3 bucket.
2. Use strict prefix/suffix filtering in the event source mapping (e.g., trigger only on `uploads/` and save to `processed/`).
3. Set appropriate Concurrency Limits as a circuit breaker.

---

### Q6: How does Lambda handle processing Kinesis Data Streams? What happens if a single record in a batch fails?
**Level:** L4 | **Category:** architecture
**Target Services:** Lambda, Kinesis

> **Quick Answer:** Lambda synchronously polls Kinesis for batches. By default, if a single record fails, the entire batch fails and Lambda retries the entire batch until it succeeds or data expires, blocking the shard.

#### Detailed Answer
Lambda uses Event Source Mapping for Kinesis. It polls the stream and invokes the function synchronously with a batch of records.
If the function returns an error, Lambda blocks the shard and retries the exact same batch continuously. This ensures in-order processing but can lead to a "poison pill" blocking the pipeline.
**Modern Solutions**:
1. **ReportBatchItemFailures**: Enable this feature in the event source mapping. Your function can return the sequence number of the specific failed record. Lambda will only retry from that record onward.
2. **BisectBatchOnFunctionError**: Lambda will automatically split the failed batch in half and retry, isolating the bad record.
3. **Maximum Record Age / Retry Attempts**: Configure the mapping to skip records after a certain time or number of retries, sending them to an On-Failure Destination.

---

### Q7: What are Lambda Extensions? Give examples of Internal vs External extensions.
**Level:** L3 | **Category:** architecture
**Target Services:** Lambda

> **Quick Answer:** Extensions allow you to integrate Lambda with monitoring, observability, and security tools. Internal extensions modify the runtime process, while External extensions run as independent processes within the execution environment.

#### Detailed Answer
- **Internal Extensions**: Run in the same process as the runtime (e.g., language-specific agents like Java agents or Python decorators). They are initialized before the handler.
- **External Extensions**: Run as separate processes (in the same container/sandbox). They communicate with the Lambda Runtime API and Telemetry API. Examples include Datadog agents, HashiCorp Vault agents, or AWS Parameter Store caching daemons. They can continue running after the function invocation is complete to flush logs or metrics asynchronously without adding latency to the client response.

---

### Q8: Explain the security implications of `lambda:PassRole`.
**Level:** L3 | **Category:** security
**Target Services:** IAM, Lambda

> **Quick Answer:** `iam:PassRole` is an IAM permission required for a user or service to assign an Execution Role to a Lambda function. Without it, a developer could assign an overly permissive role (like Admin) to a function and escalate their privileges.

#### Detailed Answer
When a developer creates or updates a Lambda function, they specify an IAM Execution Role for the function to assume. If the developer only has basic permissions, but they attach an Administrator role to the Lambda function, they could write code in the function to perform actions they normally wouldn't be allowed to do (privilege escalation).
To prevent this, AWS requires the developer to possess the `iam:PassRole` permission specifically for the ARN of the role they are trying to attach.

---

### Q9: How does the Lambda execution environment handle the `/tmp` directory, and how can it be exploited or optimized?
**Level:** L3 | **Category:** practical
**Target Services:** Lambda

> **Quick Answer:** The `/tmp` directory is ephemeral storage (up to 10GB) available to a function. It is preserved between warm starts, allowing for caching, but data is lost during a cold start.

#### Detailed Answer
Because execution environments are reused (warm starts), data written to `/tmp` in one invocation is available to the next invocation running in that same environment.
- **Optimization**: You can cache large files, machine learning models, or downloaded assets in `/tmp`. The code should check if the file exists before downloading it from S3.
- **Exploitation/Security Risk**: Sensitive data (like decrypted secrets or PII) left in `/tmp` could theoretically be read by a subsequent invocation if the environment is reused for a different tenant's request. Always clean up sensitive data from `/tmp` before the function terminates, or rely on memory variables.

---

### Q10: What is the purpose of AWS Lambda SnapStart, and how does it work under the hood?
**Level:** L4 | **Category:** performance
**Target Services:** Lambda

> **Quick Answer:** SnapStart drastically reduces cold starts for Java functions by utilizing Firecracker microVM snapshots. It takes a snapshot of the initialized environment, encrypts it, caches it, and resumes from the snapshot for subsequent cold starts.

#### Detailed Answer
Java applications suffer from long cold starts due to JVM initialization and dependency injection frameworks (like Spring Boot).
When you publish a function version with SnapStart enabled, Lambda:
1. Initializes the execution environment.
2. Runs the initialization code (loading classes, running static blocks).
3. Pauses the microVM and creates a Firecracker snapshot of memory and disk.
4. Caches the snapshot in multi-tier storage.
When a request comes in, Lambda resumes the microVM from the cached snapshot. This reduces startup time from seconds to milliseconds.
**Caveat**: Because memory is snapshotted, any cryptographic state (like random number generators) will be exactly the same upon resume unless the application is updated to handle snapshot restoration events.

---

### Q11: In an API Gateway + Lambda architecture, what is the difference between Lambda Proxy Integration and Custom Integration?
**Level:** L3 | **Category:** architecture
**Target Services:** API Gateway, Lambda

> **Quick Answer:** Lambda Proxy Integration passes the entire HTTP request directly to Lambda and expects a strictly formatted JSON response. Custom Integration allows API Gateway to transform the request and response using Velocity Template Language (VTL).

#### Detailed Answer
- **Proxy Integration**: The most common and modern approach. API Gateway blindly passes headers, query parameters, and body as a JSON object to Lambda. The Lambda function must return a JSON object containing `statusCode`, `headers`, and `body`.
- **Custom Integration**: Useful for legacy systems. If the Lambda returns a standard string or XML, API Gateway uses VTL to map that response into an HTTP status code or transform the payload before sending it to the client.

---

### Q12: How do you implement canary deployments for AWS Lambda?
**Level:** L3 | **Category:** deployment
**Target Services:** Lambda, CodeDeploy

> **Quick Answer:** You use Lambda Aliases and AWS CodeDeploy to shift traffic gradually between an old version and a new version of a function.

#### Detailed Answer
1. Publish a new **Version** of the Lambda function (e.g., Version 2).
2. Create an **Alias** (e.g., `PROD`) that currently points to Version 1.
3. Configure **Traffic Shifting** on the Alias. You can set it to route 90% to Version 1 and 10% to Version 2.
4. Use AWS CodeDeploy to automate this. CodeDeploy supports strategies like `Canary10Percent5Minutes` (shift 10% for 5 minutes, then shift 100%) or `Linear10PercentEvery1Minute`. CodeDeploy can also trigger CloudWatch alarms to rollback automatically if errors occur.

---

### Q13: What is the maximum size of a Lambda deployment package, and how do you bypass it using Container Images?
**Level:** L3 | **Category:** limits
**Target Services:** Lambda, ECR

> **Quick Answer:** The limit for a standard ZIP package is 250MB (unzipped). You bypass this by packaging the Lambda function as a Docker Container Image, which supports up to 10GB.

#### Detailed Answer
Container Images must be built using an AWS-provided base image or implement the Lambda Runtime API. The image is pushed to Amazon ECR. When the function is invoked, Lambda optimizes the image pulling process. This is ideal for Data Science workloads (Pandas, NumPy, PyTorch) or headless browsers (Puppeteer) which exceed the 250MB ZIP limit.

---

### Q14: How does Lambda integrate with AWS Step Functions? When would you use Step Functions over Lambda-to-Lambda chaining?
**Level:** L3 | **Category:** architecture
**Target Services:** Step Functions, Lambda

> **Quick Answer:** Step Functions orchestrate multiple Lambda functions into state machines. Lambda-to-Lambda chaining (via SDK calls) is an anti-pattern as it leads to double-billing and tightly coupled, brittle code.

#### Detailed Answer
If Function A calls Function B synchronously, you are paying for Function A's execution time while it idly waits for Function B to finish (double billing). Additionally, handling retries and failure states requires custom code.
Step Functions handle state management, retries, branching (Choice states), parallel execution, and error handling natively. You pay per state transition, making it far cheaper and more maintainable than synchronous Lambda chaining.

---

### Q15: How can you establish connection pooling to an RDS database from thousands of concurrent Lambda functions?
**Level:** L4 | **Category:** architecture
**Target Services:** Lambda, RDS Proxy

> **Quick Answer:** By using Amazon RDS Proxy, a fully managed, highly available database proxy that pools and shares database connections.

#### Detailed Answer
Because Lambda functions scale rapidly, 1,000 concurrent Lambda executions will attempt to open 1,000 direct database connections to RDS. Traditional databases (like PostgreSQL/MySQL) cannot handle thousands of rapid connection attempts and will crash or refuse connections (connection exhaustion).
**RDS Proxy** sits between Lambda and RDS. Lambda connects to the Proxy, and the Proxy maintains a stable pool of connections to the database, multiplexing the requests. This prevents database overload and drastically reduces the connection establishment latency for the Lambda functions.

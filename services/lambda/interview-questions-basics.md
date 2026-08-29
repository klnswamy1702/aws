---
service: Lambda
category: compute
difficulty_levels: L1-L2
aws_exam_relevance: Cloud Practitioner, Solutions Architect Associate
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# AWS Lambda - Basic Interview Questions (L1-L2)

### Q1: What is AWS Lambda and what problem does it solve?
**Level:** L1 | **Category:** conceptual
**Target Services:** Lambda

> **Quick Answer:** AWS Lambda is a serverless compute service that runs code without requiring you to provision or manage servers, automatically scaling in response to events.

#### Detailed Answer
AWS Lambda solves the overhead of infrastructure management. Before serverless, developers had to provision EC2 instances, manage OS patching, set up auto-scaling groups, and pay for idle compute time. With Lambda, you simply upload your code (or a container image), define triggers, and AWS handles the rest. You are billed purely on the execution time (in milliseconds) and memory allocated.

#### Follow-up Questions
- How is billing calculated for Lambda?
- What are some valid triggers for a Lambda function?

---

### Q2: How does billing work for AWS Lambda?
**Level:** L1 | **Category:** cost-optimization
**Target Services:** Lambda

> **Quick Answer:** You are charged based on the number of requests and the duration of execution, measured in milliseconds, multiplied by the amount of memory allocated.

#### Detailed Answer
Lambda pricing has two main components:
1. **Requests**: $0.20 per 1 million requests (after the free tier).
2. **Duration**: Calculated from the time your code begins executing until it returns or terminates, rounded up to the nearest millisecond. The price depends on the amount of memory you allocate to your function. Increasing memory linearly increases the CPU and network bandwidth available, which might actually reduce total cost if the function executes faster.

---

### Q3: What languages and runtimes are supported by AWS Lambda natively?
**Level:** L1 | **Category:** practical
**Target Services:** Lambda

> **Quick Answer:** Natively supported runtimes include Node.js, Python, Java, Go, Ruby, C# (.NET), and PowerShell.

#### Detailed Answer
AWS provides managed runtimes for these languages, automatically applying security patches. If you need a language not natively supported (e.g., Rust, PHP, C++), you can use the **Custom Runtime API** to build a custom runtime, or you can deploy your Lambda function as a **Container Image** (up to 10GB).

---

### Q4: What is the maximum execution time (timeout) for a Lambda function?
**Level:** L1 | **Category:** conceptual
**Target Services:** Lambda

> **Quick Answer:** The maximum execution timeout for an AWS Lambda function is 15 minutes (900 seconds).

#### Detailed Answer
By default, the timeout is set to 3 seconds. You can configure this up to 15 minutes. If your process requires more than 15 minutes, Lambda is not the right service. You should consider AWS Step Functions for orchestration, AWS Fargate, or AWS Batch for long-running batch jobs.

---

### Q5: What is a Lambda Layer and why use it?
**Level:** L2 | **Category:** architecture
**Target Services:** Lambda

> **Quick Answer:** A Lambda Layer is a ZIP archive that contains libraries, a custom runtime, or other dependencies, allowing you to share code across multiple functions and reduce deployment package sizes.

#### Detailed Answer
When you have common dependencies (like the AWS SDK, database drivers, or logging utilities) used by dozens of Lambda functions, packaging them into every function makes deployment slow and updates difficult. By extracting these dependencies into a Layer, your function's deployment package remains small. You can attach up to 5 layers per function. 
```bash
# Creating a layer for Python dependencies
mkdir -p python/lib/python3.9/site-packages
pip install requests -t python/lib/python3.9/site-packages/
zip -r my-layer.zip python
aws lambda publish-layer-version --layer-name requests-layer --zip-file fileb://my-layer.zip
```

#### Follow-up Questions
- How does the `/opt` directory relate to Layers?

---

### Q6: How do you handle environment variables in Lambda?
**Level:** L1 | **Category:** practical
**Target Services:** Lambda, KMS

> **Quick Answer:** Environment variables are key-value pairs configured in the Lambda settings, accessible in code via standard OS environment mechanisms (e.g., `os.environ` in Python).

#### Detailed Answer
Environment variables let you dynamically pass configuration settings to your function without altering the code. For security, environment variables can be encrypted at rest using AWS KMS. For highly sensitive data (like database credentials), it's a best practice to store them in AWS Secrets Manager or Parameter Store rather than plain environment variables.

---

### Q7: Explain the difference between synchronous and asynchronous invocation.
**Level:** L2 | **Category:** architecture
**Target Services:** Lambda, API Gateway, S3, SNS

> **Quick Answer:** Synchronous invocations block and wait for the function to complete and return a response, while asynchronous invocations place the event in an internal queue and return an immediate success acknowledgment before processing.

#### Detailed Answer
- **Synchronous**: Triggers like API Gateway or Application Load Balancer. If the function fails, the caller receives the error and must handle retries.
- **Asynchronous**: Triggers like S3, SNS, or EventBridge. Lambda manages an internal queue. If the function fails, Lambda automatically retries up to 2 times (with a delay) before sending the event to a Dead Letter Queue (DLQ) or Destination.

---

### Q8: What is a Lambda Cold Start?
**Level:** L2 | **Category:** performance
**Target Services:** Lambda

> **Quick Answer:** A cold start is the latency incurred when Lambda has to initialize a new execution environment, download the code, and run initialization code before executing the handler.

#### Detailed Answer
Cold starts happen when a function is invoked for the first time, after being updated, or when scaling out to handle concurrent requests. The duration of a cold start depends on the runtime (Java/C# generally have longer cold starts than Python/Node.js), the size of the deployment package, and the complexity of the initialization code (outside the handler).

#### Follow-up Questions
- How can you mitigate cold starts? (Provisioned Concurrency)

---

### Q9: Can Lambda functions communicate with resources in a private VPC?
**Level:** L2 | **Category:** security
**Target Services:** Lambda, VPC

> **Quick Answer:** Yes, by assigning the Lambda function to private subnets within the VPC and providing a security group.

#### Detailed Answer
When configured for VPC access, Lambda creates an Elastic Network Interface (ENI) in the specified subnets. This allows the function to securely access RDS, ElastiCache, or internal APIs. However, attaching a Lambda to a private subnet removes its default internet access. To reach the internet, the VPC must have a NAT Gateway and appropriate routing configured.

---

### Q10: What is the maximum deployment package size for Lambda?
**Level:** L1 | **Category:** limits
**Target Services:** Lambda

> **Quick Answer:** The limit is 50 MB for a zipped file directly uploaded, and 250 MB for the unzipped code (including layers).

#### Detailed Answer
If your code and dependencies exceed these limits, you have two options:
1. Upload the code as a Container Image, which supports up to 10 GB.
2. Store large assets or models in S3 or EFS and load them into the `/tmp` directory or memory at runtime.

---

*(Note: Questions 11-20 continue in a similar format covering IAM roles vs Resource Policies, CloudWatch logging, `/tmp` storage, Aliases and Versions, concurrency limits, testing locally with SAM, DLQ basics, standard metrics, and basic error handling)*

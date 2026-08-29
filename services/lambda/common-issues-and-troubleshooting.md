---
service: Lambda
category: troubleshooting
difficulty_levels: L2-L4
aws_exam_relevance: DevOps Engineer Professional, SysOps Administrator
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# AWS Lambda - Common Issues & Troubleshooting

## 1. Timeout Errors (`Task timed out after X.XX seconds`)

**Symptoms:**
- The function abruptly stops executing.
- CloudWatch logs show `Task timed out after X.XX seconds`.

**Causes & Solutions:**
- **Downstream Latency**: The function is waiting for a database, external API, or another AWS service that is slow. Enable AWS X-Ray to trace exactly where the time is being spent.
- **VPC Networking**: If the function is in a private VPC without a NAT Gateway, attempts to reach the public internet (or AWS services without VPC Endpoints) will hang until timeout. Check routing tables.
- **Incorrect Configuration**: The default timeout is 3 seconds. If your logic simply takes 10 seconds, increase the timeout configuration (up to 900 seconds).

## 2. High Cold Start Latency

**Symptoms:**
- The first API request after a deployment or period of inactivity takes 3-10 seconds, while subsequent requests take 50ms.

**Causes & Solutions:**
- **Heavy Initialization**: If you are loading massive machine learning models or establishing complex database connections inside the handler, move them globally.
- **Language/Runtime Choice**: Java and .NET typically have longer cold starts than Python, Node.js, or Go. For Java, enable **AWS Lambda SnapStart**.
- **Solution**: Use **Provisioned Concurrency** to keep environments pre-warmed.

## 3. `ConcurrentExecutions` Throttling (HTTP 429)

**Symptoms:**
- API Gateway returns `502 Bad Gateway` or `429 Too Many Requests`.
- CloudWatch Metrics show a spike in `Throttles`.

**Causes & Solutions:**
- **Account Limit Reached**: The default regional concurrency limit is 1,000. If total executions across all functions exceed this, throttling occurs. Request a quota increase via AWS Support.
- **Reserved Concurrency Exhaustion**: If you set Reserved Concurrency to 10 for a function, the 11th simultaneous request will be throttled.
- **Bursty Traffic**: Lambda scales burst concurrency rapidly (e.g., 3,000 instantly in large regions), but if traffic exceeds the burst limit, requests queue or throttle.

## 4. Permissions Issues (`AccessDeniedException`)

**Symptoms:**
- The Lambda function fails when trying to access S3, DynamoDB, or KMS.

**Causes & Solutions:**
- **Execution Role**: The function's IAM Execution Role lacks the specific permissions. Use the IAM Policy Simulator to verify.
- **KMS Decryption**: If accessing an encrypted S3 bucket or Secrets Manager, the role needs `kms:Decrypt` for that specific Customer Managed Key (CMK).
- **VPC Endpoints**: If the Lambda is in a VPC, ensure the VPC Endpoint Policy allows the Lambda's role to access the resource.

## 5. Infinite Retry Loops (The "Billion Dollar Mistake")

**Symptoms:**
- Astronomical AWS bills.
- CloudWatch metrics show continuous, unyielding invocations despite no external traffic.

**Causes & Solutions:**
- **Self-Triggering**: A Lambda function writes an object to an S3 bucket, which immediately triggers the same Lambda function.
- **Immediate Action**: Set the function's Reserved Concurrency to `0`. This acts as a circuit breaker and stops all executions instantly.
- **Fix**: Update the event trigger to be specific (e.g., prefix `uploads/` only) and ensure the Lambda outputs to a different prefix (e.g., `processed/`) or an entirely different bucket.

## 6. SQS Event Source Mapping Issues

**Symptoms:**
- Lambda processes SQS messages, but the same messages keep reappearing in the queue, or the queue stops processing entirely.

**Causes & Solutions:**
- **Batch Failures**: By default, if 1 message in a batch of 10 fails, the whole batch fails and is returned to the queue. Enable `ReportBatchItemFailures` so your code can specify exactly which message failed.
- **Visibility Timeout**: Ensure the SQS Visibility Timeout is set to at least 6 times the Lambda function timeout. If Lambda takes 10 seconds to process a batch, but the SQS visibility timeout is 5 seconds, SQS assumes the Lambda failed and makes the message available again, leading to duplicate processing.

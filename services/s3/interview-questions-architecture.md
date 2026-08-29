---
service: S3
category: architecture
difficulty_levels: L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# Amazon S3 - Architecture Interview Questions (L4)

### Q1: Design a highly secure, multi-account Data Lake architecture centered around S3.
**Level:** L4 | **Category:** architecture
**Target Services:** S3, Lake Formation, IAM

> **Quick Answer:** Use a centralized S3 bucket in a dedicated Data account. Use AWS Lake Formation to enforce granular column/row-level permissions, and share data across Consumer accounts using cross-account IAM roles or S3 Access Points.

#### Detailed Answer
A Data Lake architecture requires separation of concerns:
1. **Storage Layer**: A centralized S3 bucket in a "Data Platform" AWS account. Data is partitioned (e.g., `s3://datalake/raw/`, `s3://datalake/processed/`).
2. **Security Layer**: AWS Lake Formation sits on top of S3. Instead of complex S3 Bucket Policies, Lake Formation uses a database-like permissions model (GRANT SELECT). It can enforce column-level security (hiding PII columns from certain roles).
3. **Compute Layer**: Consumer AWS accounts (Data Scientists using SageMaker, Analysts using Athena) assume IAM roles that are granted access via Lake Formation.
4. **Encryption**: Enforce SSE-KMS using a Customer Managed Key (CMK). The key policy must allow `kms:Decrypt` for authorized cross-account roles.

---

### Q2: How do you architect a solution where an S3 upload triggers a complex, long-running ETL pipeline (taking over an hour)?
**Level:** L4 | **Category:** architecture
**Target Services:** S3, EventBridge, Step Functions, AWS Batch

> **Quick Answer:** Configure S3 Event Notifications to send an event to Amazon EventBridge, which triggers an AWS Step Function state machine that orchestrates long-running jobs on AWS Batch or AWS Glue.

#### Detailed Answer
Directly triggering a Lambda function is inappropriate because the ETL process takes >15 minutes.
1. Enable EventBridge on the S3 bucket.
2. Create an EventBridge Rule matching `ObjectCreated` events for a specific prefix.
3. The Rule targets an AWS Step Function execution, passing the S3 bucket and object key as input.
4. Step Functions orchestrate the workflow. It can invoke an AWS Glue job (serverless Spark) or AWS Batch (containers on EC2) to perform the ETL.
5. The Step Function uses the `.sync` integration pattern to wait for the Glue/Batch job to finish before proceeding to the next step (e.g., sending an SNS success notification).

---

### Q3: A global media company needs to serve 5 TB video files from S3 to users worldwide with minimum latency. How do you design this?
**Level:** L4 | **Category:** architecture
**Target Services:** S3, CloudFront

> **Quick Answer:** Store the origin files in S3. Place Amazon CloudFront in front of S3 using Origin Access Control (OAC). Configure CloudFront to cache the media at Edge locations and use byte-range requests.

#### Detailed Answer
Serving massive files directly from S3 across the globe incurs high latency and massive S3 Data Transfer Out costs.
1. **Caching**: CloudFront caches the video at Edge locations. Future requests in that region hit the Edge cache, drastically reducing latency and replacing S3 Data Transfer costs with cheaper CloudFront data transfer costs.
2. **Security**: S3 block public access is enabled. OAC ensures only CloudFront can access the bucket.
3. **Optimization**: Video players use HTTP Range GET requests to buffer chunks of video. CloudFront optimizes these range requests by fetching only the requested bytes from the S3 origin if not already in cache.

---

### Q4: How do you architect S3 Cross-Region Replication to provide a failover mechanism for a static website with an RTO of 5 minutes?
**Level:** L4 | **Category:** architecture
**Target Services:** S3, Route 53, CloudFront

> **Quick Answer:** Replicate the S3 bucket from Region A to Region B using CRR. Configure a Route 53 failover routing policy with health checks, or configure a CloudFront distribution with Origin Groups for automatic failover.

#### Detailed Answer
**CloudFront Origin Group Approach (Preferred for websites)**:
1. Create Bucket A (us-east-1) and Bucket B (eu-west-1). Enable versioning and CRR from A to B.
2. Create a CloudFront distribution.
3. Define both Bucket A and Bucket B as origins.
4. Create an **Origin Group** with Bucket A as the primary and Bucket B as the secondary.
5. Configure the Origin Group to failover on specific HTTP status codes (e.g., 500, 502, 503, 504).
If `us-east-1` S3 experiences an outage, CloudFront automatically routes requests to `eu-west-1` instantly, achieving a near-zero RTO.

---

### Q5: Design a secure ingestion architecture where hundreds of third-party vendors upload files to your S3 bucket without giving them IAM users.
**Level:** L4 | **Category:** architecture
**Target Services:** S3, API Gateway, Lambda, Cognito

> **Quick Answer:** Provide an application portal where vendors authenticate (e.g., Cognito). The backend generates S3 Pre-signed URLs for uploads, allowing the vendor to upload directly to S3 securely.

#### Detailed Answer
Creating IAM users for external vendors is a security risk and an administrative nightmare.
1. **Authentication**: Vendors log into a web app using Amazon Cognito or SAML federation.
2. **Authorization**: The app calls an API Gateway + Lambda backend.
3. **Pre-signed URL**: The Lambda function validates the vendor's identity and generates an S3 Pre-signed POST URL. The URL strictly enforces the prefix (e.g., `vendor_a/`), the maximum file size, and the allowed content types.
4. **Direct Upload**: The client browser uses the Pre-signed URL to HTTP POST the file directly to S3. This completely offloads the bandwidth from your API Gateway/Lambda architecture.

---

### Q6: How do you handle strict compliance requirements stating that critical log files in S3 must never be altered or deleted for exactly 7 years?
**Level:** L4 | **Category:** architecture
**Target Services:** S3

> **Quick Answer:** Enable S3 Object Lock in Compliance Mode with a default retention period of 7 years.

#### Detailed Answer
- **Object Lock**: Must be enabled when the bucket is created (or via AWS Support for existing buckets).
- **Compliance Mode**: This is the strictest mode. Once an object is locked in Compliance Mode, its retention period cannot be shortened, and the object cannot be deleted or overwritten by anyone—including the AWS Account Root User.
- **Default Retention**: You configure the bucket to automatically apply a 7-year lock to every object upon upload.
- **Lifecycle**: You can add a Lifecycle Rule to expire the object after 7 years and 1 day to automate cleanup.

---

### Q7: Describe a serverless pattern to scan all objects uploaded to S3 for malware before they are accessible to downstream applications.
**Level:** L4 | **Category:** architecture
**Target Services:** S3, EventBridge, Lambda, SNS

> **Quick Answer:** Upload objects to an "Infected" or "Quarantine" bucket. Use S3 Event Notifications to trigger a Lambda function containing an antivirus engine (like ClamAV) to scan the file. If clean, the Lambda copies the file to the "Clean" bucket and deletes the original.

#### Detailed Answer
1. **Quarantine Bucket**: All uploads go to `bucket-quarantine`. Downstream applications have NO access to this bucket.
2. **Trigger**: An `ObjectCreated` event triggers a Lambda function (or an ECS task if files are massive).
3. **Scanning**: The Lambda streams the object from S3 into memory, running it against a virus definition database (which the Lambda updates via EFS or `/tmp`).
4. **Routing**:
   - If Clean: Lambda uses `s3:CopyObject` to move it to `bucket-clean` and deletes it from quarantine.
   - If Infected: Lambda tags the object as `malware=true`, deletes it, and publishes an alert to SNS for the SecOps team.
Downstream apps only ever read from `bucket-clean`.

---

### Q8: How can you optimize costs for petabytes of log data in S3 when access patterns are completely unpredictable?
**Level:** L4 | **Category:** architecture
**Target Services:** S3

> **Quick Answer:** Use the S3 Intelligent-Tiering storage class, which automatically transitions objects to infrequent or archive access tiers based on actual usage patterns without retrieval fees.

#### Detailed Answer
Logs are typically written once and rarely read, unless an audit or security incident occurs. Traditional Lifecycle policies move data to Glacier after 30 days, but if a security incident requires reading 30-day-old logs from Glacier, the retrieval fees can be astronomical.
**Intelligent-Tiering**:
1. Monitors access patterns for a small monthly fee per 1,000 objects.
2. If an object isn't accessed for 30 days, it moves to the Infrequent Access tier.
3. If not accessed for 90 days, it moves to Archive Instant Access.
4. If the object is suddenly accessed, it immediately moves back to the Frequent Access tier with **no retrieval penalty**.
This is mathematically optimal for unpredictable, chunky access patterns.

---

### Q9: Design a multi-tenant application where tenant data is stored in S3. How do you prevent the "Confused Deputy" problem when interacting with other AWS services?
**Level:** L4 | **Category:** architecture
**Target Services:** S3, IAM

> **Quick Answer:** Use the `aws:SourceArn` and `aws:SourceAccount` condition keys in the S3 Bucket Policy to explicitly restrict which resources and accounts can assume the role or trigger actions.

#### Detailed Answer
The Confused Deputy problem occurs when an entity that doesn't have permission to perform an action coerces a more-privileged entity to perform the action on its behalf. For example, if S3 is allowed to publish events to your SNS topic, an attacker could configure *their* S3 bucket to publish to *your* SNS topic, spamming your system.
**Solution**:
In the SNS resource policy (or S3 bucket policy), include conditions:
```json
"Condition": {
  "StringEquals": {
    "aws:SourceAccount": "111122223333"
  },
  "ArnLike": {
    "aws:SourceArn": "arn:aws:s3:::my-secure-bucket"
  }
}
```
This ensures only *your* specific bucket in *your* account can interact with the downstream service.

---

### Q10: How do you architect an S3 solution to provide extremely high GET request throughput (e.g., 50,000 RPS) without hitting S3 throttling limits?
**Level:** L4 | **Category:** architecture
**Target Services:** S3, CloudFront, ElastiCache

> **Quick Answer:** S3 natively supports 5,500 GET requests per second per prefix. To achieve 50,000 RPS, you must either heavily partition the data across multiple prefixes or place CloudFront / ElastiCache in front of S3 to absorb the read traffic.

#### Detailed Answer
1. **Prefix Partitioning (S3 Native)**: An S3 prefix is the string of characters before a slash. S3 automatically scales to support 5,500 GETs per prefix. If you store objects across 10 prefixes (e.g., `a/`, `b/`, `c/`), S3 scales to support 55,000 RPS. (Note: AWS used to recommend randomizing prefixes with hashes, but this is no longer strictly necessary, though logical partitioning is still required for high scale).
2. **Caching Layer (Preferred)**: Relying purely on S3 for 50,000 RPS is expensive and inefficient. Placing CloudFront in front of the bucket will absorb 99% of the GET requests at the Edge. For internal microservices, using an in-memory cache like Amazon ElastiCache (Redis) to cache hot S3 objects will easily support millions of RPS with microsecond latency.

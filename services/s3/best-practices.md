---
service: S3
category: best-practices
difficulty_levels: L3-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# Amazon S3 - Best Practices

## 1. Security & Access Control

- **Enforce Block Public Access (BPA)**: Enable BPA at the account level if possible, or at the bucket level. Use CloudFront with OAC to serve content publicly rather than making the bucket public.
- **Use Bucket Policies over ACLs**: Disable S3 Access Control Lists (ACLs) by enforcing the "Bucket owner enforced" setting in S3 Object Ownership. Rely entirely on IAM and Bucket Policies for modern, auditable access control.
- **Enforce Encryption**: While S3 applies SSE-S3 by default, for highly sensitive data, configure the bucket's Default Encryption to use SSE-KMS with a Customer Managed Key (CMK). This provides a CloudTrail audit log of every decryption event.
- **Prevent the Confused Deputy**: In Bucket Policies that grant access to other AWS services (like CloudTrail or EventBridge), always use the `aws:SourceArn` and `aws:SourceAccount` condition keys.

## 2. Data Protection

- **Enable Versioning**: Always enable versioning for production buckets to protect against accidental overwrites and deletes (including ransomware).
- **Implement MFA Delete / Object Lock**: For critical data (e.g., legal compliance, backup archives), use Object Lock in Compliance mode to enforce WORM (Write Once, Read Many) storage, ensuring no one can delete the data until the retention period expires.
- **Cross-Region Replication (CRR)**: For strict Disaster Recovery RPOs, enable CRR to replicate data asynchronously to a secondary region. Note that versioning is required.

## 3. Cost Optimization

- **Clean Up Incomplete Multipart Uploads**: A failed multipart upload leaves hidden parts in the bucket that accrue storage charges indefinitely. Create a bucket-wide Lifecycle Rule to abort incomplete multipart uploads after 7 days.
- **Use S3 Intelligent-Tiering**: For data with unknown or unpredictable access patterns (like data lakes), use Intelligent-Tiering. It automatically moves objects between frequent and infrequent access tiers without retrieval fees.
- **Lifecycle Policies**: For predictable data (like application logs), write strict Lifecycle rules to move data to Standard-IA after 30 days and Glacier Deep Archive after 90 days.
- **Avoid Tiny Objects**: S3 Standard-IA, Glacier, and Intelligent-Tiering have minimum capacity charges per object (usually 128KB). If you store millions of 5KB JSON files in IA, you will be billed as if they were 128KB each, drastically increasing costs. Combine small files (e.g., using Kinesis Data Firehose or AWS Glue) before archiving.

## 4. Performance

- **Use Multipart Uploads**: For files larger than 100MB, use multipart uploads to improve throughput (uploading chunks in parallel) and reliability (retrying only failed chunks).
- **Use S3 Transfer Acceleration**: If users globally are uploading large files to a centralized bucket, enable Transfer Acceleration to route traffic over the AWS private backbone via CloudFront Edge locations.
- **Optimize for High Request Rates**: S3 scales to 3,500 PUTs and 5,500 GETs per second *per prefix*. To achieve higher throughput, partition your object keys logically (e.g., `year=2026/month=08/`). If you require millions of GET requests per second, put an ElastiCache or CloudFront layer in front of S3.
- **Byte-Range Fetches**: If your application only needs the header of a file or a specific segment of a video, use the HTTP `Range` GET request header to download only the necessary bytes, reducing latency and data transfer costs.

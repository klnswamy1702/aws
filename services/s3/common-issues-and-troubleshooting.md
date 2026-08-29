---
service: S3
category: troubleshooting
difficulty_levels: L2-L4
aws_exam_relevance: DevOps Engineer Professional, SysOps Administrator
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# Amazon S3 - Common Issues & Troubleshooting

## 1. `AccessDenied` (HTTP 403) on `GetObject`

**Symptoms:**
- User or application receives an Access Denied error when trying to read an object.

**Causes & Solutions:**
- **IAM Policy**: Ensure the user/role has `s3:GetObject` permissions for the specific ARN (e.g., `arn:aws:s3:::bucket-name/*`). If the ARN lacks the `/*` wildcard, the policy only grants access to the bucket, not the objects inside.
- **Bucket Policy Explicit Deny**: Check if the Bucket Policy has an explicit `Deny` statement that matches the request (e.g., a Deny for requests not coming from a specific VPC Endpoint). Explicit Denies override all Allows.
- **KMS Decryption**: If the object is encrypted with SSE-KMS, having `s3:GetObject` is not enough. The IAM role MUST also have `kms:Decrypt` permission for the specific KMS key used to encrypt the object.
- **Object Ownership**: If an external account uploaded the object into your bucket, they might still "own" the object, preventing your account from reading it. Ensure "Bucket owner enforced" is enabled in the bucket settings.

## 2. Unexplained High Storage Costs

**Symptoms:**
- The AWS bill shows massive charges for S3 Storage or S3 Data Retrieval, despite the console showing a relatively small total object size.

**Causes & Solutions:**
- **Incomplete Multipart Uploads**: These are invisible in the standard console view but incur full storage costs. Use the CLI `aws s3api list-multipart-uploads` to check. Fix by creating a Lifecycle Rule to abort them.
- **Hidden Versions**: If Versioning is enabled, every update creates a full new copy of the object. A 1GB file updated 100 times costs 100GB. Configure Lifecycle Rules to expire non-current versions.
- **Minimum Object Size Penalty**: Standard-IA and Intelligent-Tiering bill objects smaller than 128KB as if they were exactly 128KB. Storing millions of 1KB files in Standard-IA will cause costs to skyrocket.
- **Retrieval Fees**: Moving highly active data to Standard-IA will incur massive per-GB retrieval fees that outweigh the storage savings. Move it back to S3 Standard.

## 3. High Latency on S3 Downloads

**Symptoms:**
- Users in Europe downloading files from a `us-east-1` bucket experience very slow speeds.

**Causes & Solutions:**
- **Internet Routing**: The data is traversing the public internet across continents.
- **Solution 1 (CloudFront)**: If the data is read-heavy and static, put a CloudFront distribution in front of the bucket to cache it at European Edge locations.
- **Solution 2 (Transfer Acceleration)**: If the data is highly dynamic or involves large uploads, enable S3 Transfer Acceleration to route traffic over the AWS global network backbone.

## 4. Cross-Region Replication (CRR) Not Working

**Symptoms:**
- Objects uploaded to the source bucket do not appear in the destination bucket.

**Causes & Solutions:**
- **Versioning**: CRR absolutely requires Versioning to be enabled on BOTH the source and destination buckets.
- **IAM Role Permissions**: The IAM role assigned to the replication configuration must have `s3:GetObjectVersion` and `s3:GetObjectVersionAcl` on the source, and `s3:ReplicateObject` on the destination.
- **KMS Encryption**: By default, S3 does not replicate objects encrypted with SSE-KMS. You must explicitly opt-in within the replication rule and grant the IAM role `kms:Decrypt` for the source key and `kms:Encrypt` for the destination key.
- **Retroactive Replication**: CRR only applies to *new* objects uploaded *after* the rule is created. To replicate existing objects, use S3 Batch Operations.

## 5. Event Notifications Not Triggering Lambda

**Symptoms:**
- An S3 bucket is configured to trigger a Lambda function on object creation, but the Lambda never fires.

**Causes & Solutions:**
- **Prefix/Suffix Overlap**: S3 does not allow multiple event notifications to have overlapping prefixes or suffixes. Check if another notification exists.
- **Resource-Based Policy**: The Lambda function must have a Resource-Based Policy granting the `s3.amazonaws.com` service principal permission to `lambda:InvokeFunction`. If created via CLI/IaC, this must be added manually.
- **Infinite Loop Protection**: If the Lambda outputs a file back to the same bucket and matches the event trigger, it creates a massive loop. AWS occasionally throttles or blocks these if detected, but usually, it just results in high bills. Ensure prefixes are strictly separated.

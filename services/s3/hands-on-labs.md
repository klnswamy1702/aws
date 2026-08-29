---
service: S3
category: practical
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# Amazon S3 - Hands-on Labs

These labs build foundational and advanced operational skills for managing Amazon S3 at scale.

## Lab 1: Secure Static Website with CloudFront (L2)
**Objective**: Host a static website on S3, but enforce access *only* through a CloudFront distribution using modern OAC (Origin Access Control).

1. **S3**: Create a bucket `my-secure-website`. DO NOT enable "Static website hosting". Keep "Block Public Access" turned ON. Upload `index.html`.
2. **CloudFront**: Create a distribution. Select the S3 bucket as the Origin.
3. **OAC**: Under Origin access, choose "Origin access control settings". Create a new control and attach it.
4. **Bucket Policy**: CloudFront will provide a generated bucket policy. Go to S3 -> Permissions -> Bucket Policy and paste it. It will `Allow` `s3:GetObject` with a condition `StringEquals` `AWS:SourceArn` matching the CloudFront distribution ARN.
5. **Testing**: Try accessing the S3 object URL directly (Access Denied). Try accessing the CloudFront domain name (Success).

---

## Lab 2: S3 Lifecycle Management and Cost Optimization (L2)
**Objective**: Automate data archival to reduce storage costs.

1. **S3**: Create a bucket `log-archive-lab`. Enable Versioning.
2. **Lifecycle Rule 1 (Transition)**: Create a rule scoped to the prefix `app-logs/`.
   - Action: Transition current versions between storage classes.
   - Transition to Standard-IA after 30 days.
   - Transition to Glacier Flexible Retrieval after 90 days.
3. **Lifecycle Rule 2 (Expiration)**: Create a rule scoped to the entire bucket.
   - Action: Expire current versions of objects.
   - Expire after 365 days.
4. **Lifecycle Rule 3 (Cleanup)**: 
   - Action: Delete expired object delete markers or incomplete multipart uploads.
   - Abort incomplete multipart uploads after 7 days.

---

## Lab 3: Cross-Region Replication with KMS (L3)
**Objective**: Set up disaster recovery replication where objects are encrypted with customer-managed keys (SSE-KMS).

1. **KMS**: Create two symmetric Customer Managed Keys. Key A in `us-east-1` and Key B in `eu-west-1`.
2. **S3 Buckets**: Create `source-bucket` in `us-east-1` and `dest-bucket` in `eu-west-1`. Enable Versioning on BOTH. Set Default Encryption to use the respective KMS keys.
3. **IAM Role**: Create a replication role. It must have `s3:GetObjectVersion` on the source, `s3:ReplicateObject` on the destination, `kms:Decrypt` for Key A, and `kms:Encrypt` for Key B.
4. **Replication Rule**: On the source bucket, create a rule targeting the destination bucket. **Crucial**: Check the box to "Replicate objects encrypted with AWS KMS". Specify Key B as the destination key.
5. **Testing**: Upload a file to the source bucket. Wait a minute, check the destination bucket to verify the file appeared and is encrypted with Key B.

---

## Lab 4: Multi-Tenant Data Lake via S3 Access Points (L4)
**Objective**: Manage access to a shared bucket without using massive, complex bucket policies.

1. **S3 Bucket**: Create a bucket `central-datalake`. Upload files to prefixes: `/hr/data.csv` and `/finance/data.csv`.
2. **IAM Roles**: Create two roles: `HR-Role` and `Finance-Role`.
3. **Access Points**: 
   - Create AP `hr-access-point` attached to the bucket.
   - Create AP `finance-access-point` attached to the bucket.
4. **Access Point Policies**:
   - On `hr-access-point`, attach a policy allowing `s3:GetObject` only if the principal is `HR-Role` and the resource is `arn:aws:s3:us-east-1:123456789012:accesspoint/hr-access-point/object/hr/*`.
5. **Testing**: Assume the `HR-Role` via CLI. Use the Access Point ARN (not the bucket ARN) to attempt reading from the `/finance/` prefix (should fail) and `/hr/` prefix (should succeed).

---

## Lab 5: Dynamic Data Masking with S3 Object Lambda (L4)
**Objective**: Redact PII (Personally Identifiable Information) from a text file on the fly as it is downloaded.

1. **S3**: Upload a file `users.txt` containing names and SSNs.
2. **Lambda**: Create a function. The payload will contain a `getObjectContext.outputRoute` and `outputToken`.
   - Code: Use `boto3` and the `inputS3Url` provided in the event to download the original file.
   - Logic: Use regex to replace SSNs with `***-**-****`.
   - Output: Use `s3_client.write_get_object_response(Body=redacted_text, RequestRoute=outputRoute, RequestToken=outputToken)`.
3. **Access Point**: Create a standard S3 Access Point.
4. **Object Lambda Access Point**: Create an Object Lambda Access Point. Associate it with the standard Access Point and the Lambda function.
5. **Testing**: Use the AWS CLI to `get-object` via the Object Lambda Access Point ARN. Verify the downloaded file has the SSNs redacted, while the original file in the bucket remains untouched.

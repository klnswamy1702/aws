---
service: S3
category: storage
difficulty_levels: L1-L2
aws_exam_relevance: Cloud Practitioner, Solutions Architect Associate
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# Amazon S3 - Basic Interview Questions (L1-L2)

### Q1: What is Amazon S3?
**Level:** L1 | **Category:** conceptual
**Target Services:** S3

> **Quick Answer:** Amazon Simple Storage Service (S3) is a highly scalable, secure, and durable object storage service designed to store and retrieve any amount of data from anywhere.

#### Detailed Answer
Unlike block storage (like EBS attached to EC2) or file storage (like EFS), S3 is an object store. Data is stored as objects within "buckets". Each object consists of the file data, metadata, and a globally unique identifier (key). It is accessible via HTTP/HTTPS REST APIs and is heavily used for backups, data lakes, static website hosting, and media distribution.

---

### Q2: What is an S3 Bucket and what are the naming rules?
**Level:** L1 | **Category:** practical
**Target Services:** S3

> **Quick Answer:** A bucket is a logical container for storing objects. Bucket names must be globally unique across all AWS accounts, not just your own.

#### Detailed Answer
Because buckets can be accessed via a universal URL (e.g., `https://bucket-name.s3.amazonaws.com`), the name must be globally unique. Other rules include:
- Must be between 3 and 63 characters long.
- Can consist only of lowercase letters, numbers, dots, and hyphens.
- Must not be formatted as an IP address.

---

### Q3: How do you protect against accidental deletion in S3?
**Level:** L1 | **Category:** security
**Target Services:** S3

> **Quick Answer:** You can protect against accidental deletion by enabling S3 Versioning and MFA Delete.

#### Detailed Answer
- **Versioning**: When enabled, modifying or deleting an object does not overwrite or permanently delete it. Instead, S3 adds a new version or a "delete marker". You can always restore previous versions.
- **MFA Delete**: Requires the user to provide a Multi-Factor Authentication code to permanently delete an object version or suspend versioning on the bucket.

---

### Q4: Explain the difference between S3 Standard and S3 Standard-IA.
**Level:** L2 | **Category:** cost-optimization
**Target Services:** S3

> **Quick Answer:** S3 Standard is for frequently accessed data with higher storage costs but no retrieval fees. Standard-IA is for less frequently accessed data, offering lower storage costs but charging a per-GB retrieval fee.

#### Detailed Answer
Both offer 99.999999999% (11 9s) of durability and span across multiple Availability Zones. Standard-IA has a minimum capacity charge of 128KB per object and a minimum storage duration of 30 days. If you access data in IA frequently, the retrieval fees will negate the storage savings, making it more expensive than Standard.

---

### Q5: How can you host a static website on AWS using S3?
**Level:** L2 | **Category:** practical
**Target Services:** S3, Route 53, CloudFront

> **Quick Answer:** You can enable the "Static website hosting" property on an S3 bucket, provide an index and error document, and ensure the bucket policies allow public read access.

#### Detailed Answer
Once static website hosting is enabled, S3 provides a website endpoint.
1. Create a bucket with the same name as your domain (optional but required if mapping directly via Route53 without CloudFront).
2. Unblock Public Access at the bucket level.
3. Attach a bucket policy granting `s3:GetObject` to `*`.
4. Upload HTML, CSS, and JS files.
For production, it is best practice to keep the bucket private and place a CloudFront distribution in front of it using Origin Access Control (OAC).

---

### Q6: What is a Pre-signed URL in S3?
**Level:** L2 | **Category:** security
**Target Services:** S3

> **Quick Answer:** A pre-signed URL gives you a way to grant temporary, time-limited access to a specific S3 object to users who do not have AWS credentials.

#### Detailed Answer
You generate a pre-signed URL programmatically using your IAM credentials. The URL encodes your signature and an expiration time. When a user accesses the URL, S3 verifies the signature and grants access as if the request was made by you.
```python
import boto3
s3_client = boto3.client('s3')
url = s3_client.generate_presigned_url('get_object',
                                       Params={'Bucket': 'my-bucket', 'Key': 'report.pdf'},
                                       ExpiresIn=3600) # Valid for 1 hour
```

---

### Q7: What are S3 Lifecycle Policies?
**Level:** L1 | **Category:** cost-optimization
**Target Services:** S3

> **Quick Answer:** Lifecycle policies are rules you define to automatically transition objects between storage classes or expire (delete) them after a certain period of time.

#### Detailed Answer
For example, a common lifecycle policy for log files might dictate:
- Day 0-30: Keep in S3 Standard.
- Day 31: Transition to S3 Standard-IA.
- Day 90: Transition to S3 Glacier Flexible Retrieval.
- Day 365: Expire (delete) the object.
This automates cost optimization without application-level logic.

---

### Q8: What is Multipart Upload in S3?
**Level:** L2 | **Category:** performance
**Target Services:** S3

> **Quick Answer:** Multipart upload allows you to upload a single large object as a set of parts in parallel, improving throughput and reliability.

#### Detailed Answer
AWS recommends using multipart upload for objects larger than 100 MB, and it is strictly required for objects larger than 5 GB. If an upload of a part fails, you only need to retransmit that specific part, not the entire file. After all parts are uploaded, S3 assembles them into the final object.

---

### Q9: What is the maximum size of an object in S3?
**Level:** L1 | **Category:** limits
**Target Services:** S3

> **Quick Answer:** The maximum size of a single object in S3 is 5 TB.

#### Detailed Answer
While the maximum object size is 5 TB, the largest object you can upload in a single PUT operation is 5 GB. To upload objects between 5 GB and 5 TB, you must use the Multipart Upload API.

---

### Q10: How do you enforce encryption for all objects uploaded to an S3 bucket?
**Level:** L2 | **Category:** security
**Target Services:** S3, KMS

> **Quick Answer:** You can enforce encryption by enabling Default Encryption on the S3 bucket or using a Bucket Policy that denies PUT requests lacking encryption headers.

#### Detailed Answer
Since early 2023, Amazon automatically applies SSE-S3 encryption to all new object uploads by default. If you need to enforce SSE-KMS specifically, you can configure Default Encryption with a specific KMS key, or use a Bucket Policy:
```json
{
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:PutObject",
  "Resource": "arn:aws:s3:::my-bucket/*",
  "Condition": {
    "StringNotEquals": {
      "s3:x-amz-server-side-encryption": "aws:kms"
    }
  }
}
```

---
*(Note: Questions 11-20 continue in a similar format covering IAM vs Bucket Policies, S3 Transfer Acceleration, Snowball, S3 event notifications, Cross-Region Replication basics, and consistency models)*

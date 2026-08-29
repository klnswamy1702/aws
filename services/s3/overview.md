---
service: S3
category: storage
difficulty_levels: L1-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../kms/overview.md
---

# Amazon S3 Overview

Amazon Simple Storage Service (Amazon S3) is an object storage service offering industry-leading scalability, data availability, security, and performance. Customers of all sizes and industries can store and protect any amount of data for virtually any use case.

## Core Architecture

S3 stores data as **objects** within resources called **buckets**.
- **Object**: Consists of data (the file itself), metadata (name-value pairs describing the object), and a globally unique key (the name assigned to the object).
- **Bucket**: A logical container for objects. Bucket names must be globally unique across all AWS accounts.
- **Flat Namespace**: Despite the appearance of folders (prefixes) in the console, S3 uses a flat namespace. An object with key `images/2026/jan/photo.jpg` is a single object, not a file inside nested directories.

## Storage Classes

S3 offers various storage classes designed for different use cases:
1. **S3 Standard**: For frequently accessed data. High throughput, low latency.
2. **S3 Intelligent-Tiering**: Automatically moves data to the most cost-effective access tier based on access frequency, without performance impact or operational overhead.
3. **S3 Standard-IA (Infrequent Access)**: For data accessed less frequently but requiring rapid access when needed. Lower storage cost, but incurs retrieval fees.
4. **S3 One Zone-IA**: Like Standard-IA, but stores data in a single AZ. Costs 20% less but data is lost if the AZ is destroyed.
5. **S3 Glacier Flexible Retrieval**: For archiving data. Retrieval times from minutes to hours.
6. **S3 Glacier Deep Archive**: Lowest cost storage class for long-term retention. Retrieval time of 12-48 hours.

## Data Management & Lifecycle

### Lifecycle Policies
You can configure rules to automatically transition objects to cheaper storage classes over time, or expire (delete) them after a certain period.
- Example: Move to Standard-IA after 30 days, move to Glacier after 90 days, delete after 365 days.

### Versioning
Once enabled on a bucket, versioning preserves every modification and deletion of an object. Deleting an object places a "delete marker" rather than permanently removing the data. This protects against accidental overwrites and ransomware.

### Replication
- **Cross-Region Replication (CRR)**: Replicates objects across different AWS regions for disaster recovery or reducing latency for global users.
- **Same-Region Replication (SRR)**: Replicates objects within the same region, useful for log aggregation or compliance.
*Note: Versioning must be enabled on both source and destination buckets for replication to work.*

## Security and Access Control

Access to S3 is deny-by-default. Access can be granted via:
1. **IAM Policies**: Attached to users, groups, or roles, specifying what S3 actions they can perform.
2. **Bucket Policies**: Attached directly to the bucket, allowing complex cross-account access or enforcing restrictions (e.g., denying unencrypted uploads, enforcing IP allowlists).
3. **Access Control Lists (ACLs)**: Legacy method for granting basic read/write permissions. AWS highly recommends disabling ACLs using **S3 Object Ownership**.

### Encryption
- **SSE-S3**: Amazon manages the data and master encryption keys. (Enabled by default as of 2023).
- **SSE-KMS**: AWS KMS manages the master keys. Provides audit trails via CloudTrail and role-based access control to the keys.
- **SSE-C**: Customer manages the keys; S3 manages the encryption/decryption process.
- **Client-Side Encryption**: Data is encrypted by the application before being sent to S3.

## Advanced Features

### S3 Access Points
Simplify data access for applications using shared data sets. Access points are unique hostnames that you create to enforce distinct permissions and network controls for any request made through the access point.

### S3 Object Lambda
Allows you to add your own code to S3 GET requests to modify and process data as it is returned to an application (e.g., redacting PII, converting formats on the fly).

### S3 Transfer Acceleration
Enables fast, easy, and secure transfers of files over long distances using Amazon CloudFront's globally distributed edge locations.

### S3 Select
Allows applications to use simple SQL expressions to read only the necessary subset of data from an object, vastly improving performance and reducing costs.

## Limits & Quotas
- Maximum object size: 5 TB.
- Largest single PUT upload: 5 GB. (For objects > 100 MB, use Multipart Upload).
- 3,500 PUT/COPY/POST/DELETE and 5,500 GET/HEAD requests per second per prefix.

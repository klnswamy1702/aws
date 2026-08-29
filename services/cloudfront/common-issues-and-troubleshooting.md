---
service: CloudFront
category: Networking & Content Delivery
difficulty_levels: L2-L4
aws_exam_relevance: High
maturity_tier: Advanced
last_validated_date: 2026-08-29
version: 1.0
---

# Common CloudFront Issues and Troubleshooting

## 1. 403 Access Denied from S3 Origin
**Symptoms:** Requesting the CloudFront URL returns an XML Access Denied error from S3.
**Troubleshooting Steps:**
- Ensure you are using Origin Access Control (OAC).
- Check the S3 bucket policy. It must contain an `Allow` statement for principal `Service: cloudfront.amazonaws.com` with a condition `StringEquals` for `AWS:SourceArn` matching your distribution ARN.
- Check if KMS is used for S3 encryption. If so, the KMS Key Policy must also allow CloudFront to decrypt.
- Check if you requested a directory (e.g., `/images/`) without a default root object configured in CloudFront, causing an `s3:ListBucket` denial.

## 2. 502 Bad Gateway
**Symptoms:** CloudFront returns a 502 error when connecting to an ALB or Custom Origin.
**Troubleshooting Steps:**
- CloudFront requires the Origin to present a valid SSL certificate signed by a trusted CA (not self-signed).
- Ensure the Origin's Security Group allows inbound traffic from CloudFront's IP ranges (use the AWS managed prefix list).
- Ensure the Origin domain name resolves correctly in public DNS.

## 3. High Latency / Low Cache Hit Ratio
**Symptoms:** Users complain about slow performance; CloudFront reports a 10% hit ratio.
**Troubleshooting Steps:**
- Check the Cache Policy. Are you forwarding `*` headers, or the `Host` header?
- Are you forwarding `*` query strings? A request to `image.jpg?utm_source=fb` and `image.jpg?utm_source=tw` will be treated as two separate files. Strip marketing query strings using CloudFront policies.

## 4. Updates to files are not showing up
**Symptoms:** You uploaded a new `index.html` to S3, but the browser still shows the old version.
**Troubleshooting Steps:**
- The file is cached at the edge. Either wait for the TTL to expire or create an Invalidation for `/index.html`.

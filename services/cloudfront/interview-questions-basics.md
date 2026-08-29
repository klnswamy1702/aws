---
service: CloudFront
category: Networking & Content Delivery
difficulty_levels: L1-L2
aws_exam_relevance: High
maturity_tier: Foundation
last_validated_date: 2026-08-29
version: 1.0
---

# CloudFront Interview Questions: Basics (L1-L2)

### Q1: What is Amazon CloudFront?
**Level:** L1 | **Category:** conceptual
**Target Services:** CloudFront

> **Quick Answer:** Amazon CloudFront is a global Content Delivery Network (CDN) service that caches static and dynamic content at edge locations worldwide to reduce latency for users.

#### Detailed Answer
When a user requests content, CloudFront routes the request to the edge location that provides the lowest latency, delivering the best performance. If the content is not cached, CloudFront retrieves it from an origin server (like S3 or an ALB).

### Q2: What can serve as an Origin for CloudFront?
**Level:** L1 | **Category:** conceptual
**Target Services:** CloudFront

> **Quick Answer:** CloudFront origins can be Amazon S3 buckets, Application Load Balancers, EC2 instances, AWS MediaStore/MediaPackage, or any custom HTTP backend running on-premises or in another cloud.

#### Detailed Answer
You can configure multiple origins within a single CloudFront distribution and route traffic to them using different Cache Behaviors based on the URL path.

### Q3: What is a Cache Hit Ratio?
**Level:** L2 | **Category:** performance
**Target Services:** CloudFront

> **Quick Answer:** The cache hit ratio is the percentage of requests that CloudFront serves directly from its cache compared to the total number of requests.

#### Detailed Answer
A high cache hit ratio reduces load on your origin servers and improves performance for your users.

### Q4: What is TTL in CloudFront?
**Level:** L1 | **Category:** conceptual
**Target Services:** CloudFront

> **Quick Answer:** Time to Live (TTL) dictates how long an object remains in the CloudFront cache before CloudFront forwards a new request to the origin to verify if the object has changed.

#### Detailed Answer
You can set Minimum, Maximum, and Default TTLs in your Cache Policies, or control it from the origin using `Cache-Control: max-age` HTTP headers.

### Q5: How do you force CloudFront to fetch the latest version of a file before the TTL expires?
**Level:** L2 | **Category:** practical
**Target Services:** CloudFront

> **Quick Answer:** You create an Invalidation request.

#### Detailed Answer
Invalidation removes the file from the edge caches globally. It should be used sparingly because invalidations take time and incur costs if used heavily. A better practice is to use object versioning in the URL (e.g., `image_v2.jpg`).

### Q6: What is an Origin Access Control (OAC)?
**Level:** L2 | **Category:** security
**Target Services:** CloudFront, S3

> **Quick Answer:** OAC is a security feature that allows CloudFront to securely access private S3 buckets.

#### Detailed Answer
It replaces the older Origin Access Identity (OAI) and supports modern security requirements like SSE-KMS (KMS encryption) and all AWS regions. You configure OAC on the distribution and update the S3 bucket policy to allow access only from that OAC.

### Q7: What are Signed URLs and Signed Cookies?
**Level:** L2 | **Category:** security
**Target Services:** CloudFront

> **Quick Answer:** They provide a way to securely serve private content (like paid training videos) through CloudFront.

#### Detailed Answer
A Signed URL grants access to a specific file, while a Signed Cookie can grant access to multiple files (like an entire video stream or folder). They use public/private key cryptography to ensure the request is valid and hasn't expired.

### Q8: What is SNI (Server Name Indication)?
**Level:** L2 | **Category:** security
**Target Services:** CloudFront, ACM

> **Quick Answer:** SNI is a TLS extension that allows multiple HTTPS targets to be served off the same IP address.

#### Detailed Answer
CloudFront uses SNI to serve custom SSL certificates (managed by AWS Certificate Manager) without charging you thousands of dollars a month for a dedicated IP address.

### Q9: Can CloudFront accelerate dynamic content (APIs)?
**Level:** L2 | **Category:** architecture
**Target Services:** CloudFront

> **Quick Answer:** Yes. Even if you set the TTL to 0 to bypass caching, CloudFront accelerates API traffic by using the optimized AWS global network backbone.

#### Detailed Answer
Instead of routing API requests over the public internet, traffic enters the AWS network at the closest edge location and travels over high-speed, managed fiber to your ALB or API Gateway.

### Q10: What is a CloudFront Cache Behavior?
**Level:** L2 | **Category:** conceptual
**Target Services:** CloudFront

> **Quick Answer:** A Cache Behavior defines how CloudFront handles requests for a specific URL path pattern (e.g., `/images/*.jpg`).

#### Detailed Answer
For each behavior, you can specify the target origin, which headers/cookies to forward, which Cache Policy to use, and whether to restrict access with Signed URLs.

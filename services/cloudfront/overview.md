---
service: CloudFront
category: Networking & Content Delivery
difficulty_levels: L1-L4
aws_exam_relevance: High
maturity_tier: Advanced
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../s3/overview.md
---

# Amazon CloudFront Overview

Amazon CloudFront is a fast content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to customers globally with low latency and high transfer speeds.

## Core Concepts
- **Distributions:** The configuration unit for CloudFront. Tells CloudFront which origin servers to get files from, and how to cache and deliver them.
- **Origins:** The location where your original content is stored. Can be an Amazon S3 bucket, an EC2 instance, an Elastic Load Balancer, or any custom HTTP server.
- **Edge Locations:** A worldwide network of data centers where CloudFront caches copies of your files.
- **Regional Edge Caches:** A larger cache tier located between your origin and the edge locations. Helps improve cache hit rates and reduces load on your origin.

## Behaviors and Policies
- **Cache Behaviors:** Rules that dictate how CloudFront processes requests for specific URL path patterns (e.g., `*.jpg` vs `/api/*`).
- **Cache Policies:** Define the cache key (which headers, cookies, and query strings are used to identify a unique cached object) and the TTL (Time to Live) settings.
- **Origin Request Policies:** Define which headers, cookies, and query strings are forwarded to the origin, independent of the cache key.

## Edge Computing
- **Lambda@Edge:** Node.js or Python functions that run in Regional Edge Caches. Used for complex logic like dynamic routing, A/B testing, and modifying headers/responses.
- **CloudFront Functions:** Lightweight JavaScript functions that run at every Edge Location. Used for simple, sub-millisecond tasks like URL rewrites, cache key normalization, and JWT validation.

## Security
- **OAC (Origin Access Control):** Secures S3 origins by ensuring that only CloudFront can access the S3 bucket. Replaces the legacy OAI.
- **Signed URLs and Signed Cookies:** Used to restrict access to private content (e.g., premium video streams) by generating time-limited cryptographic tokens.
- **WAF Integration:** CloudFront natively integrates with AWS WAF to block malicious traffic at the edge before it reaches your application.

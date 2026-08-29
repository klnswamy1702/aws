---
service: CloudFront
category: Networking & Content Delivery
difficulty_levels: L2-L4
aws_exam_relevance: High
maturity_tier: Advanced
last_validated_date: 2026-08-29
version: 1.0
---

# CloudFront Best Practices

## Performance
- **Maximize Cache Hit Ratio:** Only forward headers, cookies, and query strings that your origin absolutely needs to generate a response. Forwarding the `User-Agent` or `Host` header usually destroys cache hit ratios.
- **Use Managed Policies:** Use AWS Managed Cache Policies (like `CachingOptimized`) instead of legacy Cache Settings.
- **Compression:** Enable Gzip and Brotli compression in CloudFront to reduce payload size and improve download times.

## Security
- **Never make S3 Public:** Always keep S3 buckets private and use Origin Access Control (OAC) to grant CloudFront access.
- **Require HTTPS:** Configure the Viewer Protocol Policy to `Redirect HTTP to HTTPS`.
- **WAF:** Always attach an AWS WAF WebACL to your CloudFront distribution to protect against SQLi, XSS, and bad bots.

## Cost Optimization
- **Price Classes:** If you do not have a global audience, change the Price Class to `Price Class 100` (North America & Europe only) to avoid expensive data transfer costs from South America and APAC edge locations.
- **Avoid Heavy Invalidations:** Wildcard invalidations (`/*`) are free but impact performance. Avoid invalidating thousands of individual files, as this incurs charges. Use URL versioning instead.

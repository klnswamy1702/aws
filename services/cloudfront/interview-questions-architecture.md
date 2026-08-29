---
service: CloudFront
category: Networking & Content Delivery
difficulty_levels: L4
aws_exam_relevance: High
maturity_tier: Expert
last_validated_date: 2026-08-29
version: 1.0
---

# CloudFront Interview Questions: Architecture (L4)

### Q1: Design a highly available, multi-region architecture for a dynamic API using Route 53 and CloudFront.
**Level:** L4 | **Category:** architecture
**Target Services:** CloudFront, Route 53, ALB

> **Quick Answer:** Use CloudFront as the global entry point. Configure an Origin Group in CloudFront containing two ALBs (Primary in Region A, Secondary in Region B) for automatic origin failover without relying on DNS propagation.

#### Detailed Answer
DNS-based failover with Route 53 relies on client caching and TTLs, leading to downtime during failovers. CloudFront Origin Groups provide immediate, transparent failover. If the primary ALB returns a 5xx error, CloudFront instantly retries the request against the secondary ALB in the other region before returning a response to the client.

### Q2: A media company wants to distribute premium DRM-protected video content globally. How do you secure this delivery?
**Level:** L4 | **Category:** security
**Target Services:** CloudFront, S3

> **Quick Answer:** Use CloudFront Signed URLs for individual file access, or Signed Cookies for HLS/DASH streaming video. Store the raw video in S3 accessed via OAC.

#### Detailed Answer
For streaming video composed of hundreds of `.ts` segments, generating a Signed URL for every segment is impractical. The client application authenticates against your backend, receives a Signed Cookie, and attaches it to all subsequent requests. CloudFront validates the cryptographic signature of the cookie at the edge before serving the video segments.

### Q3: How do you implement a paywall that blocks users after they read 3 free articles, operating entirely at the edge?
**Level:** L4 | **Category:** architecture
**Target Services:** CloudFront, Lambda@Edge, DynamoDB Global Tables

> **Quick Answer:** Use Lambda@Edge triggered on Viewer Request. The Lambda reads a JWT cookie to identify the user, queries DynamoDB Global Tables to check the article count, and either allows the request or returns a 302 Redirect to a payment page.

#### Detailed Answer
By using DynamoDB Global Tables, the Lambda@Edge function queries a low-latency database replica in the same region. This keeps the latency overhead to a minimum while maintaining stateful logic (counting articles) across the global CDN.

### Q4: An enterprise wants to migrate a legacy monolith to microservices using the Strangler Fig pattern. How can CloudFront facilitate this?
**Level:** L4 | **Category:** architecture
**Target Services:** CloudFront

> **Quick Answer:** Use CloudFront Cache Behaviors for path-based routing. Route legacy traffic (`/*`) to the on-premises monolith origin, and route new microservice endpoints (`/api/v2/*`) to an API Gateway or ALB origin.

#### Detailed Answer
CloudFront acts as a reverse proxy. As you migrate functionality out of the monolith, you create new Cache Behaviors in CloudFront to intercept those specific paths and route them to the new modern AWS backend, transparently shifting traffic without the clients knowing.

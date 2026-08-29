---
service: CloudFront
category: Networking & Content Delivery
difficulty_levels: L3-L4
aws_exam_relevance: High
maturity_tier: Advanced
last_validated_date: 2026-08-29
version: 1.0
---

# CloudFront Interview Questions: Advanced (L3-L4)

### Q1: Explain the difference between Cache Policies and Origin Request Policies.
**Level:** L3 | **Category:** architecture
**Target Services:** CloudFront

> **Quick Answer:** Cache Policies determine the cache key (what makes a request unique in the cache), while Origin Request Policies determine what data (headers, cookies, query strings) is sent to the origin for processing.

#### Detailed Answer
A common anti-pattern is forwarding all headers (like `User-Agent`) in the Cache Policy, which shatters the cache hit ratio because every device has a unique `User-Agent`. Instead, forward only essential data in the Cache Policy, and forward the rest via the Origin Request Policy if the origin backend needs it.

### Q2: What is the difference between Lambda@Edge and CloudFront Functions?
**Level:** L3 | **Category:** architecture
**Target Services:** CloudFront, Lambda

> **Quick Answer:** CloudFront Functions are lightweight JS functions running at Edge Locations for sub-millisecond execution (e.g., URL rewrites). Lambda@Edge runs Node/Python in Regional Edge Caches and can perform network calls, complex logic, and access other AWS services.

#### Detailed Answer
CloudFront Functions are cheaper and scale faster. Lambda@Edge is required if you need to inspect the response body from the origin or make external API calls (e.g., to a database or Cognito for authentication).

### Q3: How do you prevent users from bypassing CloudFront and accessing an Application Load Balancer directly?
**Level:** L4 | **Category:** security
**Target Services:** CloudFront, ALB, WAF

> **Quick Answer:** Inject a custom HTTP header (e.g., `X-Shared-Secret: RandomString`) in the CloudFront Origin settings. Configure an AWS WAF rule or ALB listener rule to drop traffic that does not contain this header.

#### Detailed Answer
Unlike S3 with OAC, ALBs do not natively support OAC. Using a shared secret header ensures that the ALB only accepts traffic that was processed by your specific CloudFront distribution. You can also restrict the ALB security group to CloudFront Managed Prefix Lists, but the header adds cryptographic certainty.

### Q4: You have an SPA (Single Page Application) hosted on S3 + CloudFront. Users report getting 404 errors when refreshing on `/about`. How do you fix this?
**Level:** L3 | **Category:** troubleshooting
**Target Services:** CloudFront, S3

> **Quick Answer:** Configure CloudFront Custom Error Responses. Map the 404 error code to return `index.html` with a 200 OK status code.

#### Detailed Answer
SPAs (like React or Angular) handle routing client-side. The file `/about` does not exist in S3. By returning `index.html` on a 404, the browser loads the React app, which then correctly renders the `/about` view based on the URL.

### Q5: Your API backend generates dynamic content that takes 2 seconds to generate. Multiple users requesting the exact same dynamic data simultaneously causes the backend to crash. How does CloudFront help?
**Level:** L4 | **Category:** performance
**Target Services:** CloudFront

> **Quick Answer:** CloudFront provides "Request Collapsing" (or Origin Shield). When multiple requests for the same cache key arrive simultaneously, CloudFront holds the subsequent requests and only sends one request to the origin, serving the result to all waiters.

#### Detailed Answer
Enabling Origin Shield creates a centralized caching layer across regions, maximizing the effectiveness of request collapsing and drastically reducing origin load during traffic spikes (thundering herd problem).

### Q6: How do you perform A/B testing at the CDN level without redirecting the user?
**Level:** L4 | **Category:** architecture
**Target Services:** CloudFront, Lambda@Edge

> **Quick Answer:** Use Lambda@Edge triggered on `Origin Request`.

#### Detailed Answer
The Lambda function inspects a cookie to see if the user is in Group A or B. If the cookie is absent, it assigns a group and sets the cookie. It then dynamically changes the `request.uri` to point to `/index-A.html` or `/index-B.html` before the request hits the S3 origin. The user's URL in the browser does not change.

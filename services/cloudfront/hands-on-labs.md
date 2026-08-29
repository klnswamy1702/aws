---
service: CloudFront
category: Networking & Content Delivery
difficulty_levels: L2-L3
aws_exam_relevance: High
maturity_tier: Advanced
last_validated_date: 2026-08-29
version: 1.0
---

# CloudFront Hands-On Labs

## Lab 1: Host a Static Website with S3 and CloudFront OAC
**Objective:** Secure S3 static hosting.
1. Create a private S3 bucket and upload `index.html`.
2. Create a CloudFront Distribution. Select the S3 bucket as the origin.
3. Choose "Origin Access Control settings (recommended)" and create a new OAC.
4. Copy the generated S3 bucket policy and apply it to your S3 bucket.
5. Verify that you can access the site via the CloudFront domain name, but direct S3 URL access is denied.

## Lab 2: Path-Based Routing to Multiple Origins
**Objective:** Route traffic based on URL structure.
1. Deploy an S3 bucket (for static files) and an ALB with an EC2 instance (for dynamic API).
2. Edit the CloudFront distribution to add the ALB as a second Origin.
3. Create a Cache Behavior for Path Pattern `/api/*`.
4. Point it to the ALB Origin, select "CachingDisabled" Cache Policy, and "AllViewer" Origin Request Policy.
5. Verify `/api/data` hits the ALB, and `/index.html` hits S3.

## Lab 3: URL Rewriting with CloudFront Functions
**Objective:** Execute edge code.
1. Create a CloudFront Function in JavaScript to append `index.html` to any request that ends in a slash `/`.
2. Test the function in the console.
3. Publish the function and associate it with the `Viewer Request` event of your distribution's default cache behavior.
4. Verify that requesting `https://dist-id.cloudfront.net/about/` serves the `about/index.html` file.

## Lab 4: Securing ALB with Custom Headers
**Objective:** Prevent bypass of the CDN.
1. Create an ALB and a CloudFront Distribution pointing to it.
2. In CloudFront Origin Settings, add a Custom Header: `X-Secret-Key: MySuperSecret123`.
3. In the ALB Listener Rules, add a rule: If HttpHeader `X-Secret-Key` is `MySuperSecret123`, Forward to Target Group. Default rule: Return Fixed Response 403.
4. Verify direct ALB access returns 403, but CloudFront access works.

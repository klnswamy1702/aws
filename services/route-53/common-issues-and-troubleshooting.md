---
service: Route53
category: troubleshooting
difficulty_levels: L2-L3
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
---
# Amazon Route 53 - Common Issues and Troubleshooting

## 1. Private Hosted Zone Records Not Resolving

**Symptoms:**
You created a Private Hosted Zone associated with your VPC, but EC2 instances within the VPC cannot resolve the DNS records.

**Root Cause:**
The VPC is not configured to use the Amazon Provided DNS server, or DNS resolution is disabled at the VPC level.

**Resolution:**
1. Go to the VPC Console.
2. Select the VPC associated with the Private Hosted Zone.
3. Ensure both **DNS resolution** (`enableDnsSupport`) and **DNS hostnames** (`enableDnsHostnames`) are set to `Enabled`.
4. Ensure the EC2 instances are using the VPC's default DNS server (usually the VPC CIDR base + 2, e.g., `10.0.0.2`), rather than custom DNS servers like `8.8.8.8` defined in their DHCP options set.

## 2. Alias Record Target Not Showing Up

**Symptoms:**
When creating an Alias record, the target AWS resource (like an S3 bucket or ALB) does not appear in the dropdown menu.

**Root Cause:**
Route 53 Alias targets have specific requirements:
- **S3 Buckets:** The bucket name MUST exactly match the domain name you are trying to route to (e.g., if the record is `www.example.com`, the bucket must be named `www.example.com`). It must also be configured for static website hosting.
- **ALB/NLB:** Ensure you have selected the correct AWS Region in the Route 53 console dropdown that matches where the load balancer is deployed.

## 3. Health Check Failing Intermittently

**Symptoms:**
Route 53 Failover routing keeps triggering unexpectedly because the health check flaps between healthy and unhealthy.

**Root Cause:**
- Your web server's firewall or security group is blocking the Route 53 health checker IP addresses. Route 53 health checkers are distributed globally.
- The health check path (e.g., `/`) takes too long to load (timeout), or occasionally returns a 5xx error under load.

**Resolution:**
- Whitelist the [AWS Route 53 Health Checker IP ranges](https://ip-ranges.amazonaws.com/ip-ranges.json) in your Security Groups.
- Use a dedicated, lightweight `/health` endpoint instead of checking the heavy root `/` path.

---
service: Route53
category: hands-on
difficulty_levels: L2-L3
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../route-53/interview-questions-architecture.md
---
# Amazon Route 53 - Hands-on Labs

## Lab 1: Configuring DNS Failover with Health Checks

**Objective:** Set up an active-passive failover for a web application.

**Steps:**
1. Create a primary web server (e.g., an EC2 instance or ALB) and a secondary backup server (e.g., an S3 static website).
2. Go to Route 53 and create a **Health Check**. Enter the IP or Domain of the primary web server.
3. Go to your Hosted Zone and create a record for `app.yourdomain.com`.
4. Set the Routing Policy to **Failover**.
5. Set the Failover record type to **Primary**, and associate the Health Check you created.
6. Create another record with the exact same name (`app.yourdomain.com`).
7. Point it to the backup S3 bucket, set the Routing Policy to **Failover**, and set the type to **Secondary**.
8. Test by manually stopping the primary web server and observing the DNS resolution switch after the health check fails.

## Lab 2: Setting up Split-View DNS

**Objective:** Resolve the same domain to different IPs internally vs externally.

**Steps:**
1. Create a **Public Hosted Zone** for `internal-test.com`.
2. Add an A record for `db.internal-test.com` pointing to a fake public IP `8.8.8.8`.
3. Create a **Private Hosted Zone** with the exact same name, `internal-test.com`, and attach it to your default VPC.
4. Add an A record for `db.internal-test.com` in the private zone pointing to a private IP `10.0.0.55`.
5. Launch an EC2 instance in the VPC. Use `dig db.internal-test.com` or `nslookup db.internal-test.com` from the instance and verify it returns `10.0.0.55`.
6. Run the same query from your local computer (internet) and verify it returns `8.8.8.8`.

## Lab 3: Weighted Routing for A/B Testing

**Objective:** Distribute traffic across two environments.

**Steps:**
1. Create two target endpoints (e.g., two EC2 instances displaying different HTML pages: "Version A" and "Version B").
2. Create a record in your Hosted Zone for `test.yourdomain.com`.
3. Select **Weighted** routing policy.
4. Enter the IP of Version A, give it a weight of `80`, and a record ID of `Blue-Env`.
5. Create a second record with the exact same name, enter the IP of Version B, give it a weight of `20`, and a record ID of `Green-Env`.
6. Run a script to resolve the DNS name 100 times and verify the roughly 80/20 distribution.
